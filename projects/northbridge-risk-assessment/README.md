# Northbridge Logistics — Cybersecurity Risk Assessment

## Project Overview

Northbridge Logistics is a fictional logistics company with approximately 150 employees across three offices. Its environment includes on-premises systems, cloud services, remote users, email, endpoints, and business-critical operational data. The project evaluates indicators of compromise involving phishing, unauthorized logins, and malware, then proposes a practical defense strategy.

## Business Problem

The organization needs to reduce cyber risk without interrupting daily logistics operations. Weak access controls, inconsistent monitoring, limited endpoint visibility, and gaps in recovery readiness could allow a routine phishing event to become a major business disruption.

## Objectives

- Identify critical assets, threats, vulnerabilities, and business impacts.
- Prioritize risk using likelihood and impact.
- Recommend administrative, technical, and physical controls.
- Design a defense-in-depth security architecture.
- Improve detection, response, continuity, and recovery.
- Communicate technical findings to leadership in clear business language.

## Scope

### In Scope

- User identities and privileged accounts
- Email and collaboration systems
- Employee endpoints
- Local and wide-area networks
- Cloud applications and storage
- Security monitoring and logging
- Backup, continuity, and disaster recovery

### Out of Scope

- Offensive exploitation of production systems
- Collection of real employee credentials
- Destructive testing
- Vendor contract negotiation

## Risk Assessment Method

1. **Asset identification** — Determine systems, data, services, and processes that support the business.
2. **Threat identification** — Review phishing, credential theft, malware, insider misuse, cloud misconfiguration, and service interruption.
3. **Vulnerability analysis** — Identify weaknesses in authentication, patching, monitoring, segmentation, user awareness, and recovery.
4. **Risk evaluation** — Rate likelihood and impact using a qualitative scale.
5. **Risk treatment** — Select mitigation, transfer, avoidance, or acceptance based on business needs.
6. **Continuous monitoring** — Reassess risk as systems, threats, and controls change.

## Priority Risks

| Risk | Likelihood | Impact | Priority | Recommended Treatment |
|---|---:|---:|---:|---|
| Phishing leads to account compromise | High | High | Critical | MFA, secure email gateway, awareness training, conditional access |
| Malware spreads from an endpoint | Medium-High | High | High | EDR, segmentation, patching, application control, tested backups |
| Privileged account misuse | Medium | High | High | RBAC, PAM, separate admin accounts, logging, access reviews |
| Cloud data exposure | Medium | High | High | Least privilege, encryption, configuration reviews, DLP |
| Business interruption after ransomware | Medium | Critical | Critical | Immutable backups, BCP/DR, incident exercises, recovery testing |

## Recommended Security Controls

### Identity and Access Management

- Enforce multi-factor authentication for employees, administrators, and remote access.
- Apply role-based access control and least privilege.
- Use separate administrative accounts for privileged work.
- Review access when employees change roles or leave the company.
- Add conditional-access rules for risky sign-ins and unmanaged devices.

### Email Security

- Deploy a secure email gateway with attachment and URL analysis.
- Configure SPF, DKIM, and DMARC.
- Provide recurring phishing-awareness exercises.
- Add an easy method for employees to report suspicious messages.

### Endpoint and Network Defense

- Deploy endpoint detection and response across supported systems.
- Establish patching and vulnerability-remediation targets.
- Segment users, servers, management systems, and sensitive services.
- Restrict unnecessary ports, protocols, and administrative pathways.
- Monitor DNS, authentication, endpoint, firewall, and cloud logs.

### Security Operations

- Centralize logs in a SIEM.
- Develop alert rules for impossible travel, repeated login failures, privilege changes, malware detections, and unusual data transfer.
- Use documented response playbooks for phishing, compromised accounts, malware, and ransomware.
- Track lessons learned and control improvements after incidents.

### Resilience

- Maintain offline or immutable backups.
- Define recovery time and recovery point objectives.
- Test restoration procedures regularly.
- Document crisis communications and leadership responsibilities.
- Conduct tabletop exercises involving IT, security, operations, and management.

## Target Architecture

```text
Internet
   |
[DNS / Email Security / Web Filtering]
   |
[Next-Generation Firewall]
   |
+------------------ Segmented Network ------------------+
| Users | Servers | Management | Guest | Security Tools |
+--------------------------------------------------------+
   |          |          |               |
 [EDR]      [Backup]   [Privileged]     [SIEM/SOAR]
   |          |        [Access Mgmt]         |
   +----------+-------------+----------------+
                        |
                  Incident Response
```

## Deliverables

- Executive summary
- Asset and risk register
- Threat and vulnerability analysis
- Risk treatment plan
- Defense-in-depth architecture diagram
- Identity and access strategy
- Incident response recommendations
- Business continuity and disaster recovery recommendations
- Final presentation

## Skills Demonstrated

`Risk Assessment` · `IAM` · `MFA` · `RBAC` · `SIEM` · `EDR` · `Email Security` · `Network Segmentation` · `Incident Response` · `BCP/DR` · `Executive Communication`

## Key Takeaway

Cybersecurity controls are most effective when they work together. Identity protection, endpoint defense, segmentation, monitoring, user awareness, and tested recovery create multiple opportunities to prevent, detect, contain, and recover from an attack.

> This project is educational and uses a fictional organization. No real credentials, private data, or production systems were used.
