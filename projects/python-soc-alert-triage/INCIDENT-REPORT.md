# SOC Incident Report — Cedarline Systems

## Executive Summary

Synthetic authentication and proxy logs support a high-confidence finding of account compromise followed by persistence, command-and-control beaconing, and outbound data transfer. The evidence should be treated as a critical incident requiring immediate containment and escalation.

## Evidence Timeline

| Time (UTC) | Evidence | Assessment |
|---|---|---|
| 02:35–02:46 | One documentation address targeted 37 accounts; 36 attempts failed | Password spray |
| 02:47:03 | Password login succeeded for `j.okafor` from the spray source | Account compromise |
| 02:51–02:53 | New `svc-backup2` account, sudoers entry, and SSH authorized key created | Persistence |
| 03:04:55 | `svc-backup2` authenticated with the planted public key | Persistence validated |
| 02:58–07:10 | 55 requests to `cdn-metrics-sync.example`; median gap 300 seconds; 93% timing agreement | Suspected command-and-control beaconing |
| 06:41–06:42 | Three outbound POST requests transferred 88.8 MiB | Suspected data exfiltration |

## Severity-Ranked Findings

- **Critical:** successful login from the password-spray source.
- **Critical:** 88.8 MiB outbound upload to the suspicious destination.
- **High:** password spray across 37 accounts.
- **High:** sudoers and SSH authorized-key persistence.
- **High:** regular beaconing from `10.20.4.116`.
- **Medium:** new local account creation.

## Recommended Response

1. Isolate the affected workstation while keeping it powered on for evidence collection.
2. Disable the compromised and persistence accounts; revoke active sessions and keys.
3. Block confirmed indicators at approved DNS, proxy, and network controls.
4. Preserve authentication, proxy, endpoint, and volatile-memory evidence.
5. Scope for the attacker address, affected identities, destination, and persistence artifacts across the environment.
6. Escalate through the incident-response process and notify required stakeholders.
7. Eradicate validated artifacts, recover from a trusted state, and monitor for recurrence.

## Confidence and Limitations

Confidence is high because identity, privilege, network-timing, and upload evidence form a consistent sequence. The dataset is synthetic and demonstrates analytic reasoning; it is not evidence from a production environment.
