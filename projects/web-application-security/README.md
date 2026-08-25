# RetailHub OWASP Web Assessment

## Public E-Commerce Application — OWASP Top 10 Review

### Objective
Assess a fictional public e-commerce application against the **OWASP Top 10** and produce a prioritized remediation plan based on exploitability, business impact, and remediation urgency.

### My Role
Performed a structured application-security review, translated findings into business risk, and organized a remediation roadmap for identity, authorization, input handling, encryption, logging, and API protections.

## Key Findings

### Critical
- **Broken access control** — unauthorized actions could be performed
- **Injection and XSS** — risk of data manipulation and account compromise
- **No MFA** — elevated account-takeover risk

### High / Medium
- Weak encryption choices
- Missing or insufficient logging
- Missing API rate limits

## Assessment Flow

```text
Browser / User Input
        |
       WAF
        |
    RetailHub App
   /      |       \
Access  Injection  No MFA
   \      |       /
 Crypto  Logging  API Limits
        |
Prioritized Remediation
```

## Priority Remediation Actions

1. **Enforce MFA and secure sessions**
2. **Correct authorization logic and least privilege**
3. **Validate input and prevent injection/XSS**
4. **Improve encryption, logging, and API controls**

## Recommended Practices
- Secure coding standards
- Server-side authorization checks
- Parameterized queries and input validation
- Context-aware output encoding
- WAF protections
- OAuth 2.0 where appropriate
- SAST / DAST in the SDLC
- Centralized security logging / SIEM concepts
- API rate limiting

## Outcome
Delivered a risk register and remediation roadmap focused on **MFA, authorization, secure coding, encryption, logging, and API controls**.

## Key Learning
The most urgent web-security issues are those that directly affect **unauthorized access, input handling, identity protection, and sensitive data**. Effective application security requires prioritization rather than treating every finding equally.

## Career Relevance
Web applications are a frequent attack surface. Identifying, prioritizing, and communicating these weaknesses supports **blue-team, SOC, vulnerability-management, and application-security analyst** responsibilities.

**Skills:** OWASP Top 10 · Broken Access Control · Injection · XSS · MFA · Secure Sessions · SAST/DAST · WAF · OAuth 2.0 · Logging · API Security · Risk Prioritization

> Educational, sanitized assessment of a fictional application. No public systems were tested.