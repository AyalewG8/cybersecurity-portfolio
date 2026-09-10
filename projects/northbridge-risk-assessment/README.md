# Northbridge Logistics Risk Assessment

## Cybersecurity Risk Assessment & Defense Strategy

### Objective
Identify business risks and build a practical security roadmap for a fictional logistics company with **150 employees, three offices, 180 endpoints, and 20 servers**.

### My Role
Assessed assets, threats, vulnerabilities, and business impact using **NIST SP 800-30 concepts** and **CVSS prioritization**. Mapped key threats to **MITRE ATT&CK awareness** and produced a **90-day phased control roadmap** with clear sequencing and ownership.

## Risk Scoring Method

Every score below is arithmetic, not judgement dressed up as a number. A
reviewer should be able to recompute any cell.

**Inherent risk = Likelihood × Impact**, each rated 1–5 against the definitions
below, giving a 1–25 scale.

| Rating | Likelihood | Impact |
|---:|---|---|
| 5 | Expected within 12 months; already occurring in the sector | Business stopped; regulatory or contractual breach |
| 4 | Likely within 12 months | Major disruption to a core process; significant data loss |
| 3 | Possible within 12 months | Localized disruption; recoverable data loss |
| 2 | Unlikely but credible | Limited disruption; minor data exposure |
| 1 | Rare; requires an improbable chain | Negligible operational effect |

| Band | Score |
|---|---:|
| Critical | 20–25 |
| High | 12–19 |
| Medium | 6–11 |
| Low | 1–5 |

**Residual risk** is the same calculation re-applied *after* the proposed
treatment, which is what makes the roadmap arguable: each control has to move a
specific number, or it does not earn its place.

## Risk Register

| ID | Asset | Threat | Existing control | L | I | Inherent | Treatment | L′ | I′ | Residual | Owner | Target |
|---|---|---|---|---:|---:|---:|---|---:|---:|---:|---|---|
| R-01 | Email · all 150 staff | Phishing → credential theft | Spam filter only; no MFA | 5 | 4 | **20 Critical** | MFA, secure email gateway, quarterly awareness training | 2 | 4 | **8 Medium** | IT Manager | 0–30 d |
| R-02 | File servers · endpoints | Ransomware | Signature AV; weekly backup, never restore-tested | 4 | 5 | **20 Critical** | EDR, immutable offsite backups, quarterly restore test | 2 | 4 | **8 Medium** | Infrastructure | 30–60 d |
| R-03 | Customer tracking portal (public) | Credential stuffing / brute force | Password policy only | 4 | 4 | **16 High** | WAF, rate limiting, MFA on portal accounts | 2 | 3 | **6 Medium** | Application owner | 60–90 d |
| R-04 | 20 servers | Exploitation of known vulnerabilities | Manual, ad-hoc patching | 4 | 4 | **16 High** | Automated patch management on a monthly cycle with exception tracking | 2 | 3 | **6 Medium** | Infrastructure | 30–60 d |
| R-05 | Privileged accounts | Insider misuse / excessive access | Shared administrator credentials | 3 | 5 | **15 High** | PAM, individually attributable admin accounts, quarterly access review | 2 | 4 | **8 Medium** | IT Manager | 0–30 d |
| R-06 | Branch Wi-Fi · 3 offices | MITM / rogue access point | WPA2-PSK, one shared key | 3 | 4 | **12 High** | WPA3-Enterprise with 802.1X, VLAN segmentation | 1 | 3 | **3 Low** | Network | 30–60 d |

**Reading the register:** R-05 scores lower than R-01 on likelihood but higher
on impact, because shared administrator credentials are less likely to be
abused than a phishing email is to be clicked — and far more damaging when they
are. That difference is why it is treated in the same 30-day window as R-01
despite a lower inherent score.

## Results

| Measure | Before | After treatment | Change |
|---|---:|---:|---:|
| Aggregate inherent risk (sum of scores) | 99 | 39 | **−61%** |
| Findings rated Critical | 2 | 0 | −2 |
| Findings rated High | 4 | 0 | −4 |
| Findings rated Medium | 0 | 5 | +5 |
| Findings rated Low | 0 | 1 | +1 |
| Highest single residual score | 20 | 8 | −60% |

The two treatments scheduled in the first 30 days — MFA (R-01) and privileged
access management (R-05) — account for 19 of the 60 points of reduction. They
are sequenced first not because they reduce the most in absolute terms (EDR and
tested backups under R-02 reduce as much as R-01 on their own) but because both
are configuration changes to systems already owned, with no procurement cycle in
front of them. The roadmap is sequenced by **risk reduction available per unit
of elapsed time**, which is why a 12-point treatment requiring a purchase order
sits behind a 7-point treatment that does not.

**What the register does not claim:** these are projected residual scores for a
proposed control set, not measured outcomes. Nothing here was implemented or
tested. A real programme would re-score after implementation and expect the
residuals to land higher than projected.

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
Six risks scored, treated, and re-scored: **aggregate risk down 61%**, with both
Critical findings and all four High findings moved to Medium or Low. Delivered
as a register leadership can fund against and a 90-day sequence operations can
execute.

## What I Would Do Differently
- **I scored likelihood without incident data.** The ratings rest on sector
  reporting and reasoning, not on Northbridge's own history, because a fictional
  company has none. In a real assessment I would anchor likelihood to the
  organization's ticket and incident records first, and say so where I could not.
- **I did not cost the treatments.** A register that shows risk reduction
  without showing spend is only half of a funding argument, and leadership will
  ask the other half immediately.
- **R-03's residual assumes the WAF is tuned.** An untuned WAF in blocking mode
  breaks the portal and gets switched to monitoring, at which point the residual
  is wrong. The register should carry that dependency as an explicit assumption
  rather than burying it in the treatment description.

## Key Learning
Security is not a single product. Effective protection requires continuous improvement across **technology, processes, and people**. Social engineering can bypass technical controls when user awareness is weak.

## Career Relevance
This project demonstrates the ability to translate a risk assessment into an action plan that leadership can understand and operations can execute — directly relevant to entry-level **SOC Analyst, Cybersecurity Analyst, Blue Team, and risk-support roles**.

**Skills:** Risk Assessment · NIST · CVSS · MITRE ATT&CK · MFA · EDR · Network Segmentation · SIEM/SOAR · Incident Response · BCP/DR

> Educational project using a fictional organization. No real credentials, private data, or production systems were used.