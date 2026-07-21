# Cybersecurity Portfolio Architecture Diagrams

These diagrams are designed for GitHub, the portfolio website, presentations, and recruiter walkthroughs.

## 1. Northbridge Logistics — Defense-in-Depth

```mermaid
flowchart LR
  U[Employees & Remote Users] --> MFA[MFA / Conditional Access]
  MFA --> FW[Next-Generation Firewall]
  FW --> DMZ[DMZ: Web, VPN, Email Gateway]
  FW --> SEG[Segmented Internal Network]
  SEG --> END[Managed Endpoints + EDR]
  SEG --> SRV[Application & File Servers]
  SEG --> CLD[Cloud Services]
  END --> SIEM[Central SIEM / SOAR]
  SRV --> SIEM
  CLD --> SIEM
  SIEM --> SOC[SOC / Incident Response]
  SRV --> BCP[Encrypted Backups / BCP-DR]
```

## 2. Cryptography & Secure Network Architecture

```mermaid
flowchart LR
  USER[Authorized User] --> TLS[TLS 1.3 Secure Session]
  TLS --> APP[Application Service]
  APP --> AES[AES-256 Data Encryption]
  APP --> PKI[PKI Certificate Validation]
  PKI --> CA[Certificate Authority]
  APP --> DB[(Encrypted Database)]
  KMS[Key Management Service / HSM] --> AES
  KMS --> PKI
  APP --> HMAC[HMAC / Integrity Validation]
```

## 3. Threat & Vulnerability Management Lifecycle

```mermaid
flowchart LR
  INV[Asset Inventory] --> DISC[Discovery & Scanning]
  DISC --> VAL[Validate Findings]
  VAL --> PRI[CVSS + Business Prioritization]
  PRI --> REM[Patch / Mitigate / Accept]
  REM --> TEST[Retest & Verify]
  TEST --> DASH[Executive Dashboard]
  DASH --> INV
```

## 4. Secure Web Application Architecture

```mermaid
flowchart LR
  B[User Browser] --> HTTPS[HTTPS / TLS]
  HTTPS --> WAF[Web Application Firewall]
  WAF --> LB[Load Balancer]
  LB --> APP[Hardened Application Tier]
  APP --> IAM[Authentication / MFA / RBAC]
  APP --> API[Validated API Layer]
  API --> DB[(Encrypted Database)]
  APP --> LOG[Central Logging / SIEM]
  DB --> BAK[Encrypted Backups]
```

## 5. Cloud Security Foundations

```mermaid
flowchart LR
  USER[Users / Administrators] --> IDP[Cloud Identity Provider]
  IDP --> IAM[Least-Privilege IAM + MFA]
  IAM --> VNET[Private Virtual Network]
  VNET --> APP[Cloud Applications]
  VNET --> DATA[(Encrypted Storage / Database)]
  APP --> MON[Cloud Monitoring / SIEM]
  DATA --> MON
  DATA --> BACKUP[Immutable Backup / Recovery]
  POLICY[Policy-as-Code / Configuration Baselines] --> VNET
```

## 6. SOC Alert Triage & Incident Response

```mermaid
flowchart LR
  FW[Firewall] --> SIEM[SIEM]
  EDR[Endpoint Detection & Response] --> SIEM
  IAM[Identity / VPN Logs] --> SIEM
  EMAIL[Email Security Gateway] --> SIEM
  CLOUD[Cloud Audit Logs] --> SIEM
  SIEM --> TRIAGE[Analyst Triage]
  TRIAGE --> INVEST[Investigation & Enrichment]
  INVEST --> CONTAIN[Containment]
  CONTAIN --> ERAD[Eradication]
  ERAD --> REC[Recovery]
  REC --> LESSONS[Lessons Learned / Detection Tuning]
  LESSONS --> SIEM
```

## Usage Notes

- Mermaid renders automatically in GitHub Markdown.
- Export each diagram as SVG or PNG for the portfolio book, Canva, and PowerPoint.
- Keep sensitive details, real IP addresses, credentials, and organizational identifiers excluded.
