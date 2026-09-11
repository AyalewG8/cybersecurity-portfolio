#!/usr/bin/env python3
"""Unit tests for triage.py. Every analytic is tested for what it must catch
and for what it must ignore.

Run from the project folder:
    python -m unittest discover -s tools -v
"""
import io
import json
import sys
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from statistics import mean, pstdev

sys.path.insert(0, str(Path(__file__).resolve().parent))
import triage  # noqa: E402

BASE = datetime(2026, 9, 10, 2, 0, 0, tzinfo=timezone.utc)
DATA = Path(__file__).resolve().parent.parent / "data"


def iso(ts):
    return ts.strftime("%Y-%m-%dT%H:%M:%SZ")


def sshd(seconds, message):
    return f"{iso(BASE + timedelta(seconds=seconds))} bastion-01 sshd[4121]: {message}"


def sudo(seconds, user, command):
    return (f"{iso(BASE + timedelta(seconds=seconds))} bastion-01 sudo: {user} : TTY=pts/0 ; "
            f"PWD=/home/{user} ; USER=root ; COMMAND={command}")


def fail(seconds, user, src="203.0.113.9"):
    return sshd(seconds, f"Failed password for {user} from {src} port 50000 ssh2")


def accept(seconds, user, src="203.0.113.9", method="password"):
    return sshd(seconds, f"Accepted {method} for {user} from {src} port 50001 ssh2")


def proxy(seconds, src="10.0.0.5", host="c2.example", method="GET", bytes_out=400, bytes_in=200):
    return (f"{iso(BASE + timedelta(seconds=seconds))} src={src} method={method} host={host} "
            f"path=/ status=200 bytes_out={bytes_out} bytes_in={bytes_in}")


def auth_events(lines):
    return triage.parse_auth(lines)


def proxy_events(lines):
    return triage.parse_proxy(lines)


def spray_lines(accounts=12, spacing=20, src="203.0.113.9"):
    return [fail(i * spacing, f"user{i:02d}", src) for i in range(accounts)]


class ParsingTests(unittest.TestCase):
    def test_parse_auth_strips_process_tag(self):
        event = auth_events([fail(0, "alice")])[0]
        self.assertEqual(event.process, "sshd")
        self.assertTrue(event.message.startswith("Failed password for alice"))

    def test_parse_auth_handles_tag_without_pid(self):
        event = auth_events([sudo(0, "bob", "/usr/bin/id")])[0]
        self.assertEqual(event.process, "sudo")
        self.assertTrue(event.message.startswith("bob : TTY="))

    def test_parse_proxy_reads_fields(self):
        event = proxy_events([proxy(0, bytes_out=1234, bytes_in=99)])[0]
        self.assertEqual((event.src, event.host, event.method), ("10.0.0.5", "c2.example", "GET"))
        self.assertEqual((event.bytes_out, event.bytes_in), (1234, 99))

    def test_parsers_skip_malformed_lines(self):
        self.assertEqual(auth_events(["", "not a syslog line", "2026-09-10 sshd: missing T"]), [])
        self.assertEqual(proxy_events(["", "2026-09-10T02:00:00Z src=10.0.0.5 method=GET",
                                       "2026-09-10T02:00:00Z src=1 method=GET host=h path=/ "
                                       "status=OK bytes_out=1 bytes_in=1"]), [])


class PasswordSprayTests(unittest.TestCase):
    def test_spray_fires_on_distinct_accounts(self):
        findings = triage.detect_password_spray(auth_events(spray_lines(12)))
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].evidence["accounts_failed"], 12)

    def test_spray_ignores_one_account_brute_force(self):
        lines = [fail(i * 5, "alice") for i in range(40)]
        self.assertEqual(triage.detect_password_spray(auth_events(lines)), [])

    def test_spray_ignores_failures_below_threshold(self):
        self.assertEqual(triage.detect_password_spray(auth_events(spray_lines(9))), [])

    def test_spray_ignores_failures_spread_beyond_window(self):
        lines = spray_lines(12, spacing=20 * 60)  # one account every 20 minutes
        self.assertEqual(triage.detect_password_spray(auth_events(lines)), [])


class LoginAfterSprayTests(unittest.TestCase):
    def run_detector(self, extra):
        events = auth_events(spray_lines(12) + extra)
        return triage.detect_login_after_spray(events, triage.detect_password_spray(events))

    def test_login_after_spray_flags_password_login(self):
        findings = self.run_detector([accept(300, "victim")])
        self.assertEqual([(f.severity, f.evidence["user"]) for f in findings], [("critical", "victim")])

    def test_login_after_spray_flags_key_login(self):
        findings = self.run_detector([accept(3600, "backdoor", method="publickey")])
        self.assertEqual(findings[0].evidence["method"], "publickey")

    def test_login_from_other_source_not_flagged(self):
        self.assertEqual(self.run_detector([accept(300, "admin", src="10.20.1.30", method="publickey")]), [])

    def test_login_before_spray_not_flagged(self):
        self.assertEqual(self.run_detector([accept(-600, "early")]), [])


class PersistenceTests(unittest.TestCase):
    def test_useradd_flagged(self):
        line = f"{iso(BASE)} bastion-01 useradd[5120]: new user: name=svc-x, UID=1007, GID=1007"
        findings = triage.detect_persistence(auth_events([line]))
        self.assertEqual([(f.severity, f.evidence["account"]) for f in findings], [("medium", "svc-x")])

    def test_sudoers_write_flagged(self):
        findings = triage.detect_persistence(auth_events([sudo(0, "eve", "/usr/bin/tee /etc/sudoers.d/svc-x")]))
        self.assertEqual(len(findings), 1)
        self.assertIn("sudoers", findings[0].title)

    def test_authorized_keys_write_flagged(self):
        line = sudo(0, "eve", "/usr/bin/tee -a /home/svc-x/.ssh/authorized_keys")
        findings = triage.detect_persistence(auth_events([line]))
        self.assertIn("authorized_keys", findings[0].title)

    def test_routine_sudo_not_flagged(self):
        lines = [sudo(0, "ops", "/usr/bin/systemctl restart nginx"), sudo(5, "ops", "/usr/bin/apt-get update")]
        self.assertEqual(triage.detect_persistence(auth_events(lines)), [])

    def test_sudo_rule_matches_parsed_line(self):
        # Regression: the rule once anchored on the "sudo:" tag, which parse_auth()
        # strips first. It loaded and ran but produced zero alerts. Always test a
        # detection through the parser, never against a hand-trimmed message.
        raw = sudo(0, "eve", "/usr/bin/tee /etc/sudoers.d/svc-x")
        self.assertIn("sudo:", raw)
        self.assertEqual(len(triage.detect_persistence(auth_events([raw]))), 1)


class BeaconTests(unittest.TestCase):
    def test_beacon_fires_on_regular_interval(self):
        findings = triage.detect_beacons(proxy_events([proxy(i * 300) for i in range(20)]))
        self.assertEqual(findings[0].evidence["median_gap_s"], 300)

    def test_beacon_tolerates_jitter(self):
        jitter = [0, 12, -9, 14, -13, 7, -4, 11, -14, 3, 9, -8, 13, -11]
        times, t = [], 0
        for j in jitter:
            t += 300 + j
            times.append(t)
        self.assertEqual(len(triage.detect_beacons(proxy_events([proxy(s) for s in times]))), 1)

    def test_still_fires_when_other_traffic_interleaves(self):
        beacons = [i * 300 for i in range(20)]
        uploads = [3005, 3045, 3090]  # operator traffic inside one beacon interval
        times = sorted(beacons + uploads)
        gaps = [b - a for a, b in zip(times, times[1:])]
        # A coefficient-of-variation test would miss this beacon: the three short
        # gaps push stdev/mean far past any usable threshold.
        self.assertGreater(pstdev(gaps) / mean(gaps), 0.25)
        findings = triage.detect_beacons(proxy_events([proxy(s) for s in times]))
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].evidence["requests"], 23)

    def test_random_traffic_not_flagged(self):
        irregular = [0, 40, 400, 460, 1300, 1320, 2900, 3100, 5000, 5020, 7700, 7800, 9900]
        self.assertEqual(triage.detect_beacons(proxy_events([proxy(s) for s in irregular])), [])

    def test_rapid_page_load_burst_not_flagged(self):
        burst = [proxy(i, host="cdn.example") for i in range(30)]  # 30 requests, 1 s apart
        self.assertEqual(triage.detect_beacons(proxy_events(burst)), [])

    def test_too_few_requests_not_flagged(self):
        self.assertEqual(triage.detect_beacons(proxy_events([proxy(i * 300) for i in range(9)])), [])


class LargeUploadTests(unittest.TestCase):
    def test_large_upload_flagged(self):
        lines = [proxy(i * 60, method="POST", bytes_out=30 * triage.MIB) for i in range(2)]
        findings = triage.detect_large_uploads(proxy_events(lines))
        self.assertEqual((findings[0].severity, findings[0].evidence["mib"]), ("critical", 60.0))

    def test_small_uploads_not_flagged(self):
        lines = [proxy(i * 60, method="POST", bytes_out=2 * triage.MIB) for i in range(20)]
        self.assertEqual(triage.detect_large_uploads(proxy_events(lines)), [])

    def test_large_download_not_flagged(self):
        lines = [proxy(0, bytes_out=700, bytes_in=250 * triage.MIB)]
        self.assertEqual(triage.detect_large_uploads(proxy_events(lines)), [])


class DatasetTests(unittest.TestCase):
    """Figures quoted in INCIDENT-REPORT.md, checked against the generated data."""

    @classmethod
    def setUpClass(cls):
        with (DATA / "auth.log").open() as auth, (DATA / "proxy.log").open() as prox:
            cls.auth = triage.parse_auth(auth)
            cls.proxy = triage.parse_proxy(prox)
        cls.findings = triage.triage(cls.auth, cls.proxy)

    def by(self, analytic):
        return [f for f in self.findings if f.analytic == analytic]

    def test_dataset_findings_match_incident_report(self):
        self.assertEqual((len(self.auth), len(self.proxy)), (52, 475))
        c2 = [e for e in self.proxy if e.host == "cdn-metrics-sync.example"]
        self.assertEqual((sum(e.method == "GET" for e in c2), sum(e.method == "POST" for e in c2)), (52, 3))
        self.assertEqual(len(self.findings), 8)

        spray = self.by("password_spray")[0]
        self.assertEqual((spray.evidence["source"], spray.evidence["accounts_targeted"]), ("203.0.113.47", 37))
        self.assertEqual(iso(spray.ts)[11:16], "02:35")

        logins = {f.evidence["user"]: iso(f.ts)[11:19] for f in self.by("login_after_spray")}
        self.assertEqual(logins, {"j.okafor": "02:47:03", "svc-backup2": "03:04:55"})
        self.assertIn("02:51:42", [iso(f.ts)[11:19] for f in self.by("persistence")])

        beacon = self.by("beacon")[0].evidence
        self.assertEqual((beacon["source"], beacon["requests"], beacon["agreement_pct"], beacon["median_gap_s"]),
                         ("10.20.4.116", 55, 93, 300))
        self.assertEqual(beacon["first"][11:16], "02:58")

        upload = self.by("large_upload")[0].evidence
        self.assertEqual((upload["mib"], upload["large_requests"], upload["first"][11:16]), (88.8, 3, "06:41"))

    def test_cli_exit_code_and_json(self):
        out = io.StringIO()
        code = triage.main(["--format", "json"], stdout=out)
        payload = json.loads(out.getvalue())
        self.assertEqual(code, 1)  # critical findings present
        self.assertEqual(len(payload), 8)
        self.assertEqual(payload[0]["severity"], "critical")


if __name__ == "__main__":
    unittest.main(verbosity=2)
