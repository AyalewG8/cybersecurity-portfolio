# Hands-On Cybersecurity Labs

Interactive, browser-based simulations demonstrating practical security-analysis decisions with synthetic data.

**Live lab:** [Open the Hands-On Cybersecurity Labs](https://ayalewg8.github.io/cybersecurity-portfolio/hands-on-labs.html)  
**SOC Analyst case study:** [Review the SOC Analyst case study](https://ayalewg8.github.io/cybersecurity-portfolio/soc-analyst-case-study.html)

## Project Purpose

This project turns five cybersecurity workflows into safe, repeatable practice exercises:

1. SOC alert triage
2. Vulnerability prioritization
3. Risk assessment
4. Log analysis and incident investigation
5. Phishing email analysis and containment

The goal is to show analytical reasoning, not simply display definitions. Each simulation asks the user to review evidence, make a decision, and compare that decision with a documented model.

## Skills Demonstrated

- Security alert triage
- Log filtering and event correlation
- Evidence-based incident investigation
- Indicator identification
- Email-header and authentication analysis
- Phishing triage and containment
- Incident-response decision making
- CVSS interpretation
- Asset-criticality analysis
- Vulnerability remediation prioritization
- Inherent and residual risk calculation
- Control-effectiveness reasoning
- Clear communication for technical and non-technical audiences
- Accessible, responsive front-end development

## Lab 1 — SOC Alert Triage

The analyst reviews synthetic authentication, endpoint, or network evidence and selects:

- an alert severity;
- the most appropriate first response; and
- whether the event should be documented, verified, contained, or escalated; and
- a structured analyst triage note that can be copied or downloaded as a text file.

### Included Scenarios

| Scenario | Key indicators | Recommended decision |
|---|---|---|
| Repeated MFA prompts and impossible travel | MFA fatigue, distant successful logins, recovery-method change | High severity; contain the account and escalate |
| Encoded PowerShell and outbound traffic | Encoded command, unsigned child process, unexpected external connection | Critical severity; isolate the endpoint and escalate |
| Approved internal vulnerability scan | Port sweep, approved scanner identity, authorized change window | Informational; validate, document, and close |

This lab demonstrates that alerts should be evaluated in context. Similar technical activity may be malicious or expected depending on identity, authorization, timing, and business purpose.

## Lab 2 — Vulnerability Prioritization

The tool combines four inputs:

- CVSS base score;
- asset criticality;
- network exposure; and
- known active exploitation.

### Portfolio Formula

```text
Priority score =
(CVSS × 55%)
+ (asset criticality scaled to 10 × 25%)
+ (network exposure scaled to 10 × 12%)
+ (known exploitation × 8%)
```

| Priority score | Rating | Example remediation target |
|---:|---|---|
| 8.0–10.0 | Critical | 24–72 hours |
| 6.0–7.9 | High | 7 days |
| 3.5–5.9 | Medium | 30 days |
| 0.0–3.4 | Low | 90 days |

The service targets and weights are illustrative. A production organization should define them through its approved risk policy, regulatory obligations, asset inventory, and threat intelligence.

## Lab 3 — Risk Assessment

The calculator distinguishes risk before and after proposed controls.

```text
Inherent risk = likelihood × impact
Residual risk = inherent risk × (1 − estimated control effectiveness)
```

| Score | Rating |
|---:|---|
| 16–25 | Critical |
| 11–15 | High |
| 6–10 | Moderate |
| 1–5 | Low |

Residual scores are projections, not proof of actual risk reduction. Control effectiveness should be supported by testing, monitoring, audit evidence, and ownership.

## Lab 4 — Log-Analysis Investigation

The investigator searches and filters a ten-event synthetic timeline, flags suspicious activity, and selects an incident conclusion and containment action.

The evidence chain includes repeated failed sign-ins, a later successful sign-in from the same documentation address, encoded PowerShell, credential-storage access, and internal SMB connection attempts. Benign backup, policy, inventory, and software-update events are included to test false-positive control.

The supported conclusion is **suspected endpoint compromise with lateral-movement activity**. The evidence does not prove data exfiltration, reinforcing the difference between a defensible conclusion and an unsupported assumption.

## Lab 5 — Phishing Email Analysis

The analyst inspects a synthetic payroll-themed message and evaluates:

- SPF, DKIM, and DMARC authentication results;
- sender, Reply-To, and Return-Path alignment;
- urgency and credential-request language;
- the displayed destination; and
- the safest containment and reporting response.

The supported verdict is **credential phishing**. Authentication failures, unrelated sender domains, urgency, and a credential-verification link form a defensible evidence chain. The evidence does not establish that an internal account was compromised, so the simulation does not label the message as confirmed business email compromise.

All domains use the reserved `.example` namespace, and the source uses an RFC 5737 documentation address. The link is displayed as inert text and should not be opened.

## Technology

- Semantic HTML
- Responsive CSS
- Vanilla JavaScript
- Client-side calculations
- Accessible labels, keyboard focus, and live result announcements
- GitHub Pages deployment

No frameworks, external APIs, databases, accounts, or installations are required.

## Security and Privacy Boundaries

- All logs, users, IP addresses, organizations, and events are fictional or synthetic.
- Documentation IP ranges are used where examples require public addresses.
- No real systems are scanned, contacted, or modified.
- No personal data, credentials, or user-entered information is transmitted or stored.
- Downloaded triage notes are created locally in the browser and are not uploaded.
- The simulations reset when the page is reloaded.
- Results are educational decision-support examples, not production security advice.

## How to Review the Project

1. Open the [live lab](https://ayalewg8.github.io/cybersecurity-portfolio/hands-on-labs.html).
2. Complete each simulation with different inputs.
3. Review the explanation produced after each decision.
4. Inspect the source in [hands-on-labs.html](../../hands-on-labs.html).

## Future Improvements

- Add more synthetic SOC scenarios mapped to MITRE ATT&CK techniques.
- Add downloadable investigation summaries for the log-analysis scenario.
- Expand the log investigation with a larger synthetic event set and additional filters.
- Add unit tests for the scoring functions.

> Educational portfolio project. Use only authorized systems and approved organizational procedures for real security work.
