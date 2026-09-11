#!/usr/bin/env python3
"""Triage sshd authentication logs and web proxy logs into severity-ranked findings.

Five analytics run in sequence:
  1. password_spray      one source failing against many accounts in a short window
  2. login_after_spray   any successful login from a source that sprayed
  3. persistence         new accounts and sudo writes to sudoers or authorized_keys
  4. beacon              regular request timing from one host to one destination
  5. large_upload        outbound volume to one destination above a threshold

Usage:
    python tools/triage.py                          # text report on the bundled dataset
    python tools/triage.py --format json            # machine-readable findings
    python tools/triage.py --auth A.log --proxy P.log

Exit codes: 0 when no critical finding is present, 1 when at least one is
(so the tool can gate a pipeline), 2 for usage errors.
"""
import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from statistics import median

SEVERITY_RANK = {"critical": 0, "high": 1, "medium": 2, "low": 3}
MIB = 2 ** 20
DATA_DIR = Path(__file__).resolve().parent.parent / "data"


# ---------------------------------------------------------------- parsing

@dataclass
class AuthEvent:
    ts: datetime
    host: str
    process: str
    message: str


@dataclass
class ProxyEvent:
    ts: datetime
    src: str
    method: str
    host: str
    path: str
    status: int
    bytes_out: int
    bytes_in: int


@dataclass
class Finding:
    severity: str
    analytic: str
    title: str
    ts: datetime
    evidence: dict = field(default_factory=dict)

    def to_dict(self):
        return {"severity": self.severity, "analytic": self.analytic, "title": self.title,
                "ts": iso(self.ts), "evidence": self.evidence}


AUTH_LINE = re.compile(
    r"^(?P<ts>\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ) (?P<host>\S+) "
    r"(?P<process>[\w.-]+)(?:\[\d+\])?: (?P<message>.*)$"
)
PROXY_FIELD = re.compile(r"(\w+)=(\S+)")


def parse_ts(text):
    return datetime.strptime(text, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def iso(ts):
    return ts.strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_auth(lines):
    """Split each syslog line into timestamp, host, process, and message.

    The process tag ("sshd[4121]:", "sudo:") is removed from the message, so
    analytics must match message bodies only.
    """
    events = []
    for line in lines:
        match = AUTH_LINE.match(line.rstrip("\n"))
        if match:
            events.append(AuthEvent(parse_ts(match["ts"]), match["host"],
                                    match["process"], match["message"]))
    return events


def parse_proxy(lines):
    events = []
    for line in lines:
        parts = line.strip().split(" ", 1)
        if len(parts) != 2:
            continue
        fields = dict(PROXY_FIELD.findall(parts[1]))
        try:
            events.append(ProxyEvent(parse_ts(parts[0]), fields["src"], fields["method"],
                                     fields["host"], fields["path"], int(fields["status"]),
                                     int(fields["bytes_out"]), int(fields["bytes_in"])))
        except (KeyError, ValueError):
            continue
    return events


# ---------------------------------------------------------------- analytics

FAILED_LOGIN = re.compile(r"^Failed password for (?:invalid user )?(?P<user>\S+) from (?P<src>\S+) port \d+")
ACCEPTED_LOGIN = re.compile(r"^Accepted (?P<method>password|publickey) for (?P<user>\S+) from (?P<src>\S+) port \d+")
NEW_USER = re.compile(r"^new user: name=(?P<user>[^,\s]+)")
# Match the message body only. parse_auth() strips the "sudo:" process tag, so a
# pattern anchored on "sudo:" loads, runs, and never matches anything.
SUDO_COMMAND = re.compile(r"^(?P<user>\S+) : .*?USER=(?P<runas>\S+) ; COMMAND=(?P<command>.+)$")


def detect_password_spray(events, min_accounts=10, window=timedelta(minutes=15)):
    """Flag a source whose failures reach min_accounts distinct users inside one window."""
    failures = defaultdict(list)
    for event in events:
        if event.process == "sshd":
            match = FAILED_LOGIN.match(event.message)
            if match:
                failures[match["src"]].append((event.ts, match["user"]))

    findings = []
    for src, attempts in failures.items():
        attempts.sort()
        users_in_window, left, best = Counter(), 0, (0, None, None)
        for ts, user in attempts:
            users_in_window[user] += 1
            while ts - attempts[left][0] > window:
                old_user = attempts[left][1]
                users_in_window[old_user] -= 1
                if not users_in_window[old_user]:
                    del users_in_window[old_user]
                left += 1
            if len(users_in_window) > best[0]:
                best = (len(users_in_window), attempts[left][0], ts)
        if best[0] < min_accounts:
            continue
        _, start, end = best
        failed = {user for ts, user in attempts if start <= ts <= end}
        succeeded = set()
        for event in events:
            if event.process == "sshd" and start <= event.ts <= end + window:
                match = ACCEPTED_LOGIN.match(event.message)
                if match and match["src"] == src and match["method"] == "password":
                    succeeded.add(match["user"])
        targeted = len(failed | succeeded)
        findings.append(Finding(
            "high", "password_spray",
            f"Password spray from {src} against {targeted} accounts",
            start,
            {"source": src, "accounts_targeted": targeted, "accounts_failed": len(failed),
             "succeeded": sorted(succeeded), "first": iso(start), "last_failure": iso(end)},
        ))
    return findings


def detect_login_after_spray(events, spray_findings):
    """Any accepted login, by password or key, from a spraying source after the spray began."""
    spray_start = {f.evidence["source"]: f.ts for f in spray_findings}
    findings = []
    for event in events:
        if event.process != "sshd":
            continue
        match = ACCEPTED_LOGIN.match(event.message)
        if match and match["src"] in spray_start and event.ts >= spray_start[match["src"]]:
            kind = "Password" if match["method"] == "password" else "Key-based"
            findings.append(Finding(
                "critical", "login_after_spray",
                f"{kind} login for {match['user']} from spray source {match['src']}",
                event.ts,
                {"user": match["user"], "source": match["src"], "method": match["method"]},
            ))
    return findings


def detect_persistence(events):
    """New local accounts, and sudo commands that write sudoers or SSH authorized_keys."""
    findings = []
    for event in events:
        if event.process == "useradd":
            match = NEW_USER.match(event.message)
            if match:
                findings.append(Finding("medium", "persistence",
                                        f"New local account created: {match['user']}",
                                        event.ts, {"account": match["user"], "host": event.host}))
        elif event.process == "sudo":
            match = SUDO_COMMAND.match(event.message)
            if not match:
                continue
            command = match["command"]
            if "/etc/sudoers" in command:
                title = f"sudo write to sudoers by {match['user']}"
            elif "authorized_keys" in command:
                title = f"sudo write to SSH authorized_keys by {match['user']}"
            else:
                continue
            findings.append(Finding("high", "persistence", title, event.ts,
                                    {"user": match["user"], "run_as": match["runas"],
                                     "command": command, "host": event.host}))
    return findings


def detect_beacons(events, min_requests=10, tolerance=0.10, min_agreement=0.80, min_median_gap=30):
    """Flag host-to-destination traffic whose gaps mostly agree with the median gap.

    Consensus, not spread: when an operator sends other traffic to the same
    destination (uploads, tasking), a few short gaps inflate the standard
    deviation enough to hide a real beacon from a coefficient-of-variation test.
    Counting the share of gaps within +/-tolerance of the median ignores them.
    """
    series = defaultdict(list)
    for event in events:
        series[(event.src, event.host)].append(event.ts)

    findings = []
    for (src, host), times in series.items():
        if len(times) < min_requests:
            continue
        times.sort()
        gaps = [(b - a).total_seconds() for a, b in zip(times, times[1:])]
        mid = median(gaps)
        if mid < min_median_gap:  # page loads and bursts are regular but are not beacons
            continue
        agreeing = sum(abs(gap - mid) <= tolerance * mid for gap in gaps)
        share = agreeing / len(gaps)
        if share >= min_agreement:
            findings.append(Finding(
                "high", "beacon",
                f"Beaconing from {src} to {host} every {mid:.0f}s",
                times[0],
                {"source": src, "destination": host, "requests": len(times),
                 "median_gap_s": round(mid), "agreement_pct": round(share * 100),
                 "agreeing_gaps": agreeing, "total_gaps": len(gaps),
                 "first": iso(times[0]), "last": iso(times[-1])},
            ))
    return findings


def detect_large_uploads(events, threshold_bytes=50 * MIB, window=timedelta(hours=1)):
    """Flag outbound bytes from one host to one destination above threshold within a window."""
    series = defaultdict(list)
    for event in events:
        if event.bytes_out:
            series[(event.src, event.host)].append((event.ts, event.bytes_out))

    findings = []
    for (src, host), sends in series.items():
        sends.sort()
        left, total, best = 0, 0, (0, 0, 0)
        for right, (ts, size) in enumerate(sends):
            total += size
            while ts - sends[left][0] > window:
                total -= sends[left][1]
                left += 1
            if total > best[0]:
                best = (total, left, right)
        total, left, right = best
        if total >= threshold_bytes:
            # Report only the sends large enough to matter, not the beacons around them.
            window_sends = [s for s in sends[left:right + 1] if s[1] >= MIB]
            first, last = window_sends[0][0], window_sends[-1][0]
            findings.append(Finding(
                "critical", "large_upload",
                f"{total / MIB:.1f} MiB uploaded from {src} to {host}",
                first,
                {"source": src, "destination": host, "bytes_out": total,
                 "mib": round(total / MIB, 1), "large_requests": len(window_sends),
                 "first": iso(first), "last": iso(last)},
            ))
    return findings


# ---------------------------------------------------------------- pipeline

def triage(auth_events, proxy_events):
    sprays = detect_password_spray(auth_events)
    findings = (sprays
                + detect_login_after_spray(auth_events, sprays)
                + detect_persistence(auth_events)
                + detect_beacons(proxy_events)
                + detect_large_uploads(proxy_events))
    return sorted(findings, key=lambda f: (SEVERITY_RANK[f.severity], f.ts))


def render_text(findings):
    counts = Counter(f.severity for f in findings)
    summary = ", ".join(f"{counts[s]} {s}" for s in SEVERITY_RANK if counts[s])
    lines = [f"SOC alert triage: {len(findings)} findings ({summary or 'none'})", ""]
    for f in findings:
        lines.append(f"[{f.severity.upper():<8}] {iso(f.ts)}  {f.analytic:<17} {f.title}")
        for key, value in f.evidence.items():
            lines.append(f"{'':12}{key}: {value}")
        lines.append("")
    return "\n".join(lines)


def main(argv=None, stdout=None):
    stdout = stdout or sys.stdout
    parser = argparse.ArgumentParser(description="Severity-ranked triage of sshd and proxy logs.")
    parser.add_argument("--auth", type=Path, default=DATA_DIR / "auth.log")
    parser.add_argument("--proxy", type=Path, default=DATA_DIR / "proxy.log")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args(argv)
    for path in (args.auth, args.proxy):
        if not path.is_file():
            parser.error(f"log file not found: {path}")

    with args.auth.open(encoding="utf-8") as auth, args.proxy.open(encoding="utf-8") as proxy:
        findings = triage(parse_auth(auth), parse_proxy(proxy))

    if args.format == "json":
        json.dump([f.to_dict() for f in findings], stdout, indent=2)
        stdout.write("\n")
    else:
        stdout.write(render_text(findings) + "\n")
    return 1 if any(f.severity == "critical" for f in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
