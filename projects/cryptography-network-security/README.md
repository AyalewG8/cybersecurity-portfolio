# SecureHealth Cryptography & Network Security

## Protected Health Information Architecture

### Objective
Protect **protected health information (PHI)** across internal EHR servers, cloud services, and partner hospital connections against eavesdropping, man-in-the-middle attacks, ransomware, insider threats, and denial-of-service while aligning the design to **HIPAA/HITECH** requirements.

### My Role
Mapped threats to controls and selected cryptographic protocols, access controls, network zones, and key-management protections appropriate for a healthcare environment.

## Security Objectives
- Confidentiality
- Integrity
- Authenticity
- Non-repudiation
- Secure key management
- Protection of PHI in transit and at rest

## Cryptographic Controls

| Need | Control |
|---|---|
| PHI in transit | TLS 1.3 / AES-256-GCM |
| Digital signatures | ECDSA P-256 |
| Ephemeral session keys | ECDH with Perfect Forward Secrecy |
| Hashing / integrity | SHA-256 / SHA-3-256 |
| Message authentication | HMAC-SHA-256 |
| Legacy compatibility concept | RSA-2048 |

## Key Management
- Three-tier PKI
- Offline Root CA
- Online Intermediate CA
- X.509 certificate validation
- FIPS 140-3 HSM for protected private-key storage
- Key generation, storage, rotation, revocation, and archival
- CRL and OCSP certificate-status support

## Network Security Zones

### DMZ
Patient portal protected by a WAF and TLS 1.3.

### Internal
EHR services protected with network segmentation, encryption, and mutual TLS concepts.

### Cloud
Client-side encryption before sensitive data is uploaded.

### Partners
IPsec VPN and mutual TLS for trusted healthcare-system connections such as HL7/FHIR exchanges.

## Trust Flow

```text
Patient Portal
     |
   TLS 1.3
     |
  DMZ / WAF
     |
     EHR
   /     \
PKI     AES-256 / HSM
 |            |
Partner     Cloud
IPsec VPN   Encrypted data
     \
      Audit / signed logs
```

## Compliance Alignment
- Encryption for PHI in transit
- Encryption for PHI at rest
- Audit controls through logging and digital-signature concepts
- Integrity controls for protected records
- Key lifecycle and certificate validation supporting trusted communications

## Key Insight
Strong cryptography depends on more than selecting secure algorithms. **Key generation, storage, rotation, revocation, certificate validation, and lifecycle management** are what make cryptographic protection operationally effective.

## Career Relevance
This project demonstrates the ability to connect technical security controls with **business, compliance, and architecture requirements** — useful in SOC, healthcare security, enterprise security, and regulated environments.

**Skills:** TLS 1.3 · AES-256-GCM · ECDSA · ECDH · PKI · X.509 · HSM · SHA-256 · HMAC · IPsec · Network Segmentation · HIPAA/HITECH

> Educational architecture. No real patient information, production credentials, or sensitive cryptographic keys are used.