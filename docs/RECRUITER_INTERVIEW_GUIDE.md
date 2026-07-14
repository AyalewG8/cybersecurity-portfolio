# Recruiter & Interview Guide

This guide turns the six portfolio projects into concise, interview-ready stories. Each project follows a simple structure: **challenge, approach, outcome, and talking points**.

## 1. Northbridge Logistics Risk Assessment

**Challenge:** A fictional 150-employee logistics company faced phishing, unauthorized logins, malware, weak monitoring, and recovery gaps across three offices and hybrid infrastructure.

**Approach:** Identified critical assets and threats, ranked risks by likelihood and impact, and designed a defense-in-depth strategy using MFA, RBAC, EDR, segmentation, SIEM/SOAR, email security, immutable backups, and BCP/DR planning.

**Outcome:** Produced a prioritized risk-treatment plan that connected technical controls to business continuity, operational resilience, and executive decision-making.

**Interview talking points:**
- Why phishing and ransomware received critical priority
- How layered controls reduce single points of failure
- How MFA, EDR, SIEM, segmentation, and backups work together
- How technical risk was translated into business language

## 2. Cryptography & Secure Architecture

**Challenge:** Design a secure architecture that protects confidentiality, integrity, authentication, and trust across data, networks, users, and devices.

**Approach:** Compared AES, RSA, ECC, hashing, HMAC, digital signatures, TLS, PKI, certificate validation, WPA3, and secure key-management practices. Combined asymmetric trust establishment with efficient symmetric encryption.

**Outcome:** Created a layered cryptographic design and documentation package covering encryption choices, trust chains, key lifecycle, secure communications, and legacy-risk reduction.

**Interview talking points:**
- When to use symmetric versus asymmetric encryption
- Why AES-GCM provides confidentiality and integrity
- How PKI establishes trust
- Why key generation, storage, rotation, and revocation matter

## 3. Threat & Vulnerability Management

**Challenge:** Build a repeatable process for finding weaknesses without treating every scanner result as equally urgent.

**Approach:** Defined authorization and scope, discovered assets and services, validated findings, prioritized risk using CVSS and business context, assigned remediation ownership, and planned retesting.

**Outcome:** Developed a discovery-to-closure lifecycle that emphasizes actionable findings, accountable remediation, residual-risk documentation, and ethical testing.

**Interview talking points:**
- Why scanner results require validation
- How asset value changes vulnerability priority
- The difference between severity and business risk
- Why retesting is necessary before closing a finding

## 4. Web Application Security

**Challenge:** Assess common application risks while keeping testing authorized, safe, and aligned with secure-development practices.

**Approach:** Mapped assets, users, data flows, entry points, and trust boundaries. Reviewed authentication, authorization, input handling, session security, dependencies, configuration, TLS, security headers, and logging.

**Outcome:** Produced a risk-based assessment method and remediation checklist aligned with OWASP concepts, secure coding, policy, and verification.

**Interview talking points:**
- How parameterized queries reduce injection risk
- Why authorization must be enforced server-side
- How secure cookies and session rotation reduce session theft
- How secure SDLC practices prevent recurring weaknesses

## 5. Cloud Security Foundations

**Challenge:** Clarify how organizations protect identities, workloads, data, networks, and logs under the cloud shared-responsibility model.

**Approach:** Designed least-privilege IAM, segmented networking, deny-by-default controls, encryption, secrets management, centralized logging, alerting, versioned backups, and restoration testing.

**Outcome:** Created a cloud-control framework that separates provider responsibilities from customer responsibilities and connects configuration security to resilience.

**Interview talking points:**
- What the customer still owns in a managed cloud service
- Why cloud IAM is often the highest-priority control area
- How centralized audit logging supports investigation
- Why backup existence is not enough without restoration testing

## 6. SOC Alert Triage & Incident Response

**Challenge:** Create a consistent process for validating alerts, investigating suspicious activity, containing incidents, and improving defenses.

**Approach:** Centralized identity, endpoint, network, email, cloud, and vulnerability telemetry. Built triage steps and playbooks for phishing, suspicious logins, malware, and anomalous data access.

**Outcome:** Produced a practical SOC workflow covering validation, enrichment, severity, escalation, containment, evidence handling, recovery, lessons learned, and corrective actions.

**Interview talking points:**
- How severity, confidence, asset value, and impact affect triage
- What information is needed before declaring an incident
- Why timelines and evidence documentation matter
- How lessons learned should improve preventive and detective controls

## 30-Second Portfolio Introduction

> I am an Information Technology student building practical cybersecurity experience through six portfolio projects. My work covers enterprise risk assessment, cryptography, vulnerability management, web application security, cloud defense, and SOC incident response. Across these projects, I focus on translating technical findings into prioritized controls, clear documentation, and business-focused recommendations.

## Strong Closing Statement

> These projects demonstrate how I approach cybersecurity work: understand the environment, identify the highest risks, select practical controls, document decisions clearly, and verify that improvements actually reduce risk.
