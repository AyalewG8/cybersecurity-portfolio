# Security Operations Lab

## Project Summary

This project demonstrates how a security operations team collects telemetry, investigates alerts, coordinates incident response, and improves defensive controls. The lab uses sanitized scenarios involving phishing, suspicious logins, and malware indicators.

## Objectives

- Centralize security-relevant logs in a SIEM
- Triage alerts using severity, confidence, asset value, and business impact
- Build repeatable investigation and escalation procedures
- Preserve evidence and maintain an incident timeline
- Contain, eradicate, recover, and document lessons learned
- Use recurring findings to improve preventive and detective controls

## Telemetry Sources

- Identity and authentication logs
- Endpoint detection and response events
- Firewall, DNS, VPN, and network-flow data
- Email security gateway alerts
- Cloud audit and application logs
- Vulnerability and asset inventory data

## Alert Triage Workflow

1. Validate the alert and identify the affected user, host, or service
2. Establish severity, confidence, scope, and potential business impact
3. Enrich the alert with identity, endpoint, network, and threat context
4. Determine whether the activity is benign, suspicious, or confirmed malicious
5. Escalate and contain according to the incident-response plan
6. Document evidence, decisions, actions, and timestamps
7. Close with lessons learned and control-improvement tasks

## Example Playbooks

| Scenario | Initial actions | Containment priorities |
|---|---|---|
| Phishing | Review sender, headers, URLs, attachments, and recipients | Quarantine messages, block indicators, reset compromised credentials |
| Suspicious login | Compare device, location, time, MFA, and user behavior | Revoke sessions, reset credentials, restrict risky access |
| Malware alert | Review process tree, file hash, persistence, and connections | Isolate endpoint, block indicators, collect evidence |
| Data-access anomaly | Confirm identity, asset, volume, and authorization | Suspend access, preserve logs, notify incident leadership |

## Incident Documentation

- Executive incident summary
- Scope and impact assessment
- Evidence and sanitized timeline
- Containment, eradication, and recovery actions
- Root-cause and contributing-factor analysis
- Lessons learned and corrective-action register

## Deliverables

- SOC workflow diagram
- Alert-triage checklist
- Incident-response playbooks
- Sample sanitized incident timeline
- Executive incident summary
- Post-incident improvement plan

## Skills Demonstrated

Security monitoring · SIEM · Incident response · Alert triage · Evidence handling · Executive communication · Continuous improvement

> All scenarios, indicators, identities, and evidence are simulated or sanitized for safe portfolio use.