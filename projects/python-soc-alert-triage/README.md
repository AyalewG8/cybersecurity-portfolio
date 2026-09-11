# Python SOC Alert Triage Lab

A reproducible Python project that generates synthetic authentication and proxy logs, parses the events, and produces severity-ranked SOC findings.

**Interactive companion:** [Network-Traffic Investigation](../../hands-on-labs.html#network-lab)

## What the Lab Detects

1. Password spraying across multiple accounts
2. Successful login after a password spray
3. Account and SSH-key persistence
4. Periodic command-and-control beaconing
5. Large outbound uploads

The lab demonstrates event parsing, time-window analysis, behavioral detection, severity ranking, evidence reporting, and false-positive control.

## Project Structure

```text
python-soc-alert-triage/
├── generate_logs.py
├── data/
│   ├── auth.log
│   └── proxy.log
├── tools/
│   ├── triage.py
│   └── test_triage.py
├── INCIDENT-REPORT.md
└── README.md
```

## Run the Lab

Python 3.10 or newer is recommended. No external packages are required.

```bash
python generate_logs.py
python tools/triage.py
python tools/triage.py --format json
```

The triage command returns exit code `1` when critical findings are present. That result is expected for the bundled incident dataset and allows the script to act as a pipeline gate.

## Run the Tests

```bash
python -m unittest discover -s tools -v
```

The suite contains 28 tests covering parsers, password-spray detection, login-after-spray correlation, persistence, beaconing, upload direction and volume, generated-dataset figures, JSON output, and expected false-positive cases.

## Verified Dataset Results

| Analytic | Verified evidence | Severity |
|---|---|---|
| Password spray | 37 accounts targeted from one documentation address | High |
| Login after spray | Password login followed by planted-key access | Critical |
| Persistence | New account, sudoers modification, and authorized-key write | Medium / High |
| Beaconing | 55 requests; 300-second median gap; 93% timing agreement | High |
| Large upload | 88.8 MiB outbound in three requests | Critical |

See [INCIDENT-REPORT.md](INCIDENT-REPORT.md) for the investigation narrative and response recommendations.

## Safety and Integrity

- The organization, identities, hosts, and activity are fictional.
- Public IP addresses use RFC 5737 documentation ranges.
- The suspicious destination uses the reserved `.example` namespace.
- The generator is seeded and self-checking, producing repeatable evidence.
- No external systems, APIs, or networks are contacted.

> Educational portfolio project. Use only authorized systems and approved organizational procedures for real security work.
