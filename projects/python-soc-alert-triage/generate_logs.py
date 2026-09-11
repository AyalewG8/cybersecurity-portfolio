#!/usr/bin/env python3
"""Generate the synthetic Cedarline Systems dataset for the SOC Alert Triage Lab.

The generator is seeded and self-checking: the same seed always writes
byte-identical files, and the script refuses to write a dataset whose key
figures drift from the incident report. Every figure in the report can be
re-derived from this source rather than taken on trust.

All organizations, people, and hosts are fictional. 203.0.113.0/24 is an
RFC 5737 documentation range.

Usage:
    python generate_logs.py            # writes data/auth.log and data/proxy.log
    python generate_logs.py --out DIR  # writes to another directory
"""
import argparse
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path
from statistics import median

SEED = 20260970
DAY = datetime(2026, 9, 10, tzinfo=timezone.utc)

BASTION = "bastion-01"
ATTACKER_IP = "203.0.113.47"
VICTIM_USER = "j.okafor"
PERSIST_USER = "svc-backup2"
WORKSTATION = "10.20.4.116"
C2_HOST = "cdn-metrics-sync.example"
UPLOAD_SIZES = (31_234_112, 30_987_264, 30_892_173)  # 88.8 MiB in total

# 36 accounts fail during the spray; the 37th, j.okafor, accepts the password.
SPRAY_ACCOUNTS = [
    "a.alvarez", "a.mensah", "b.carter", "b.nakamura", "c.duarte", "c.oyelaran",
    "d.kowalski", "d.silva", "e.haddad", "e.lindqvist", "f.moreau", "g.ivanova",
    "h.tanaka", "i.petrov", "j.brennan", "k.adeyemi", "k.larsen", "l.chen",
    "l.fischer", "m.reyes", "m.santos", "n.bauer", "n.okoro", "o.hughes",
    "p.rossi", "p.singh", "q.nguyen", "r.garcia", "r.osei", "s.patel",
    "s.weber", "t.brooks", "t.kim", "u.ahmed", "v.costa", "w.murphy",
]
ADMINS = ["m.reyes", "d.kowalski", "s.patel", "a.mensah"]


def at(hms):
    h, m, s = (int(part) for part in hms.split(":"))
    return DAY.replace(hour=h, minute=m, second=s)


def iso(ts):
    return ts.strftime("%Y-%m-%dT%H:%M:%SZ")


def build_auth(rng):
    events = []  # (timestamp, line)
    pid = iter(range(4100, 9000, 7))

    def sshd(ts, message):
        events.append((ts, f"{iso(ts)} {BASTION} sshd[{next(pid)}]: {message}"))

    def sudo(ts, user, command):
        events.append((ts, f"{iso(ts)} {BASTION} sudo: {user} : TTY=pts/0 ; "
                           f"PWD=/home/{user} ; USER=root ; COMMAND={command}"))

    # Routine activity: admin key logins, two single-typo failures, one routine sudo.
    for hms in ("00:12:41", "01:37:09", "02:05:55", "04:18:30", "05:52:14", "07:26:48", "08:03:17"):
        user = rng.choice(ADMINS)
        sshd(at(hms), f"Accepted publickey for {user} from 10.20.1.{rng.randint(20, 60)} "
                      f"port {rng.randint(40000, 65000)} ssh2")
    for hms, user in (("01:58:22", "t.brooks"), ("05:11:03", "l.chen")):
        sshd(at(hms), f"Failed password for {user} from 10.20.2.{rng.randint(10, 90)} "
                      f"port {rng.randint(40000, 65000)} ssh2")
    events.append((at("04:18:52"), f"{iso(at('04:18:52'))} {BASTION} sudo: m.reyes : TTY=pts/1 ; "
                                   "PWD=/home/m.reyes ; USER=root ; COMMAND=/usr/bin/systemctl restart nginx"))

    # Password spray: one attempt per account, roughly every 19 seconds from 02:35:00.
    ts = at("02:35:00")
    order = SPRAY_ACCOUNTS[:]
    rng.shuffle(order)
    for user in order:
        sshd(ts, f"Failed password for {user} from {ATTACKER_IP} port {rng.randint(40000, 65000)} ssh2")
        ts += timedelta(seconds=rng.randint(17, 21))
    sshd(at("02:47:03"), f"Accepted password for {VICTIM_USER} from {ATTACKER_IP} port 50122 ssh2")

    # Persistence through the compromised account.
    sudo(at("02:51:39"), VICTIM_USER, f"/usr/sbin/useradd -m -s /bin/bash {PERSIST_USER}")
    events.append((at("02:51:42"), f"{iso(at('02:51:42'))} {BASTION} useradd[5120]: new user: "
                                   f"name={PERSIST_USER}, UID=1007, GID=1007, home=/home/{PERSIST_USER}, shell=/bin/bash"))
    sudo(at("02:52:18"), VICTIM_USER, f"/usr/bin/tee /etc/sudoers.d/{PERSIST_USER}")
    sudo(at("02:53:05"), VICTIM_USER, f"/usr/bin/tee -a /home/{PERSIST_USER}/.ssh/authorized_keys")

    # Re-entry with the planted key.
    sshd(at("03:04:55"), f"Accepted publickey for {PERSIST_USER} from {ATTACKER_IP} port 50988 ssh2")

    events.sort(key=lambda item: item[0])
    return [line for _, line in events]


def build_beacon_times(rng):
    """52 beacons at a 300 s median with jitter; one interval is split by the uploads."""
    gaps = ([rng.randint(284, 299) for _ in range(20)] + [300] * 6 +
            [rng.randint(301, 306) for _ in range(24)])
    rng.shuffle(gaps)
    split_gap = 294
    first = at("02:58:04")
    for k in range(40, 50):  # place the split interval so it opens just before 06:41
        candidate = gaps[:k] + [split_gap] + gaps[k:]
        times = [first]
        for gap in candidate:
            times.append(times[-1] + timedelta(seconds=gap))
        if at("06:37:45") <= times[k] < at("06:41:00"):
            uploads = [at("06:41:05"), at("06:41:48"), at("06:42:35")]
            assert times[k] < uploads[0] and uploads[-1] < times[k + 1]
            return times, uploads
    raise SystemExit("seed does not place the upload window at 06:41; choose another seed")


def build_proxy(rng):
    events = []

    def request(ts, src, method, host, path, status, bytes_out, bytes_in):
        events.append((ts, f"{iso(ts)} src={src} method={method} host={host} path={path} "
                           f"status={status} bytes_out={bytes_out} bytes_in={bytes_in}"))

    beacons, uploads = build_beacon_times(rng)
    for ts in beacons:
        request(ts, WORKSTATION, "GET", C2_HOST, "/v2/metrics/ping", 200,
                rng.randint(380, 460), rng.randint(180, 260))
    for ts, size in zip(uploads, UPLOAD_SIZES):
        request(ts, WORKSTATION, "POST", C2_HOST, "/v2/metrics/upload", 200, size, rng.randint(140, 180))

    # 420 background requests across 41 workstations, including the compromised one.
    sites = [
        ("outlook.office365.com", "/owa/", "GET"), ("teams.microsoft.com", "/api/chats", "POST"),
        ("login.microsoftonline.com", "/common/oauth2/token", "POST"), ("github.com", "/", "GET"),
        ("slack.com", "/api/conversations.history", "GET"), ("zoom.us", "/wc/join", "GET"),
        ("salesforce.com", "/lightning/page/home", "GET"), ("www.google.com", "/search", "GET"),
        ("docs.google.com", "/document/d/", "POST"), ("www.linkedin.com", "/feed/", "GET"),
        ("cdn.jsdelivr.net", "/npm/", "GET"), ("api.weather.gov", "/points", "GET"),
    ]
    hosts = [f"10.20.4.{n}" for n in range(100, 141)]
    start, span = at("02:00:00"), 6 * 3600
    for _ in range(417):
        ts = start + timedelta(seconds=rng.randrange(span))
        site, path, method = rng.choice(sites)
        out = rng.randint(600, 2_000_000) if method == "POST" else rng.randint(300, 1_500)
        request(ts, rng.choice(hosts), method, site, path, 200, out, rng.randint(2_000, 900_000))
    for _ in range(3):  # large downloads: inbound volume must not look like exfiltration
        ts = start + timedelta(seconds=rng.randrange(span))
        request(ts, rng.choice(hosts), "GET", "download.windowsupdate.com", "/c/msdownload/update",
                200, rng.randint(500, 900), rng.randint(180_000_000, 260_000_000))

    events.sort(key=lambda item: item[0])
    return [line for _, line in events], beacons, uploads


def self_check(auth_lines, proxy_lines, beacons, uploads):
    """Refuse to write a dataset whose figures drift from the incident report."""
    assert len(auth_lines) == 52, len(auth_lines)
    assert len(proxy_lines) == 475, len(proxy_lines)
    assert beacons[0].strftime("%H:%M") == "02:58" and beacons[-1] < at("07:12:00")
    times = sorted(beacons + uploads)
    gaps = [(b - a).total_seconds() for a, b in zip(times, times[1:])]
    mid = median(gaps)
    agree = sum(abs(g - mid) <= 0.10 * mid for g in gaps)
    assert (len(times), mid, agree, len(gaps)) == (55, 300, 50, 54), (len(times), mid, agree, len(gaps))
    assert round(sum(UPLOAD_SIZES) / 2**20, 1) == 88.8


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", type=Path, default=Path(__file__).resolve().parent / "data")
    args = parser.parse_args(argv)
    rng = random.Random(SEED)
    auth_lines = build_auth(rng)
    proxy_lines, beacons, uploads = build_proxy(rng)
    self_check(auth_lines, proxy_lines, beacons, uploads)
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "auth.log").write_text("\n".join(auth_lines) + "\n", encoding="utf-8")
    (args.out / "proxy.log").write_text("\n".join(proxy_lines) + "\n", encoding="utf-8")
    print(f"wrote {len(auth_lines)} auth events and {len(proxy_lines)} proxy events to {args.out}")


if __name__ == "__main__":
    main()
