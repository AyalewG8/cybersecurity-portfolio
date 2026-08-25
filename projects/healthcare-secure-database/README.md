# Project 03 — Healthcare Clinic Secure Database

## HIS Secure Data Model — Confidentiality, Integrity, Availability

### Objective
Design a secure, normalized healthcare database that preserves the confidentiality, integrity, and availability of protected health information (PHI).

### My Role
Designed the entity relationship model and access model, applied HIPAA-aware security controls across core entities, and documented how administrative and technical safeguards work together.

## Core Data Model

### Patients
- Patient demographics
- Identifiers
- Contact details
- Protected health information fields

### Visits
- Encounter data
- Diagnoses
- Treatments
- Provider associations

### Users
- Clinicians and staff
- Login identities
- Roles and permissions

## Security Controls

### Access & Identity
- Role-Based Access Control (RBAC)
- Least privilege
- MFA concept for privileged access
- Separation of duties

### Data Protection
- Encryption at rest
- TLS for application connections in transit
- Audit logging and timestamps
- Validation rules and referential constraints

### Availability
- Backups
- Recovery planning
- Reliable system design

## Secure Architecture Flow

```text
Clinicians
   |
MFA Login
   |
Application / API
   |
TLS + Validation
   |
RBAC / Least Privilege
   |
+-------------------------------+
| Patients | Visits | Users     |
+-------------------------------+
   |                    |
Audit Log           Backup / DR
```

## Implementation Highlights
- Develop normalized PostgreSQL tables
- Assign primary and foreign keys
- Define user roles
- Apply access controls
- Align controls to HIPAA expectations for confidentiality and accountability

## Deliverables
- Entity Relationship Diagram (ERD)
- Security-aware access model
- Controls rationale
- Technical documentation

## Key Learning
A secure database is not only about schema design. Real protection depends on identity, access, encryption, logging, integrity controls, and recovery planning working together.

## Career Relevance
This project strengthened my understanding of how backend data structures and security controls support application security, investigations, accountability, and regulatory compliance.

---

**Presentation alignment:** Project 03 in my 2026 IT / Cybersecurity Portfolio presentation.
