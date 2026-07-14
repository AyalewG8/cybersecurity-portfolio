# Web Application Security

## Project Summary

This project examines common web application risks and the secure design, policy, testing, and remediation practices used to reduce them. The work follows an authorized, risk-based assessment approach rather than testing public systems.

## Objectives

- Map application assets, users, data flows, and trust boundaries
- Identify authentication, authorization, input-handling, and configuration risks
- Connect technical findings to business impact
- Recommend secure development and operational controls
- Verify remediation with repeatable testing

## Focus Areas

- Authentication, MFA, password storage, and session security
- Authorization, least privilege, and access-control testing
- Input validation, parameterized queries, and output encoding
- Injection and cross-site scripting prevention
- Secure configuration, secrets handling, and dependency management
- TLS, security headers, logging, monitoring, and incident response
- Enterprise, issue-specific, and system-specific security policies

## Assessment Method

1. Define scope and authorization
2. Create a simple application and data-flow model
3. Identify assets, entry points, trust boundaries, and likely threats
4. Review security requirements, code concepts, and configurations
5. Test controls in an isolated lab
6. Rank findings by likelihood and business impact
7. Recommend fixes and verify remediation

## Defensive Control Examples

| Risk | Primary defensive controls |
|---|---|
| Injection | Parameterized queries, validation, least-privileged database accounts |
| Cross-site scripting | Context-aware output encoding, CSP, safe templating |
| Broken access control | Server-side authorization checks and deny-by-default rules |
| Session theft | Secure, HttpOnly, SameSite cookies and session rotation |
| Vulnerable dependencies | Software inventory, scanning, patching, and upgrade planning |
| Security misconfiguration | Hardened baselines, automated checks, and change control |

## Deliverables

- Application threat model
- Security testing checklist
- Findings and remediation report
- Secure development recommendations
- Supporting security-policy documentation

## Skills Demonstrated

Web security · Threat modeling · Secure coding concepts · Access control · Policy development · Risk communication · Remediation verification

> Testing examples are educational, sanitized, and restricted to authorized lab environments.