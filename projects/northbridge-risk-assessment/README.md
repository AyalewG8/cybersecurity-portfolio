# Northbridge Logistics Risk Assessment

## Cybersecurity Risk Assessment & Defense Strategy

### Objective
Identify business risks and build a practical security roadmap for a fictional logistics company with **150 employees, three offices, 180 endpoints, and 20 servers**.

### My Role
Assessed assets, threats, vulnerabilities, and business impact using **NIST SP 800-30 concepts** and **CVSS prioritization**. Mapped key threats to **MITRE ATT&CK awareness** and produced a **90-day phased control roadmap** with clear sequencing and ownership.

## Priority Risks

| Risk | Priority | Why It Matters |
|---|---|---|
| Phishing / spear phishing | Critical | Credential theft, malware delivery, account compromise |
| Ransomware | High | Operational disruption and recovery impact |
| Insider threat | High | Misuse of broad employee or privileged access |
| MITM / Wi-Fi exposure | High | Interception of traffic and session compromise |
| Credential stuffing / brute force | High | Risk to external portal and VPN access |

## Business & CIA Impact
- **Confidentiality:** exposure of customer and employee data
- **Integrity:** unauthorized modification of systems or records
- **Availability:** ransomware or outages disrupting logistics operations

## Defense-in-Depth Strategy

### Technical Controls
- Next-generation firewall (NGFW)
- Endpoint detection and response (EDR)
- Multi-factor authentication (MFA)
- Automated patch management
- Secure email gateway
- WPA3 and VLAN segmentation
- WAF for the public-facing portal
- SIEM / SOAR concepts
- Backup and disaster recovery controls

### Administrative Controls
- Security awareness training
- Acceptable use policy
- Password policy
- Data classification
- Incident response plan

### Physical Controls
- Badge / key-card access
- CCTV with 90-day retention

## Recommended Architecture

```text
Internet
   |
 NGFW
   |
+-------------------------------+
| DMZ / WAF | Internal | VPN    |
+-------------------------------+
      |          |        |
   Users      Servers    Admin
 MFA + EDR   Patch+EDR  PAM+MFA
      \          |        /
       \---------+-------/
             SIEM / SOAR
                 |
           Backups / DR
```

## 90-Day Implementation Roadmap

| Timeframe | Priority Action |
|---|---|
| 0–30 days | Enforce MFA |
| 30–60 days | Deploy EDR |
| 30–60 days | Improve patch management |
| 60–90 days | Add WAF and penetration testing |
| 60–90 days | Expand security awareness training |

## Outcome
Converted business risk into a practical defense-in-depth roadmap that strengthens **prevention, detection, response, and recovery**.

## Key Learning
Security is not a single product. Effective protection requires continuous improvement across **technology, processes, and people**. Social engineering can bypass technical controls when user awareness is weak.

## Career Relevance
This project demonstrates the ability to translate a risk assessment into an action plan that leadership can understand and operations can execute — directly relevant to entry-level **SOC Analyst, Cybersecurity Analyst, Blue Team, and risk-support roles**.

**Skills:** Risk Assessment · NIST · CVSS · MITRE ATT&CK · MFA · EDR · Network Segmentation · SIEM/SOAR · Incident Response · BCP/DR

> Educational project using a fictional organization. No real credentials, private data, or production systems were used.