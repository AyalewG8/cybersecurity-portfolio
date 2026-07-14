# Cloud Security Lab

## Project Summary

This lab explores how organizations protect workloads, identities, data, and logs across public, private, community, and hybrid cloud environments. The design centers on the shared-responsibility model, least privilege, secure configuration, visibility, and resilience.

## Objectives

- Explain provider and customer security responsibilities
- Design role-based cloud access with least privilege
- Protect stored and transmitted data with encryption
- Reduce exposure through secure networking and configuration
- Centralize logs for detection and investigation
- Plan backup, recovery, and continuity controls

## Architecture Components

- Identity provider, MFA, and role-based access
- Separate network segments for public, application, and data services
- Security groups and deny-by-default firewall rules
- Managed encryption keys and secrets management
- Centralized audit, network, identity, and workload logs
- Monitoring alerts routed to an incident-response workflow
- Versioned backups with tested restoration procedures

## Shared-Responsibility Review

| Area | Provider responsibility | Customer responsibility |
|---|---|---|
| Physical facilities | Data centers, hardware, foundational infrastructure | Select appropriate services and regions |
| Managed platform | Availability and service-layer maintenance | Secure configuration and application use |
| Identity | Service capability | Users, roles, MFA, credentials, and permissions |
| Data | Storage service operation | Classification, access, encryption, retention, and backup |
| Monitoring | Logging features | Enable, centralize, review, alert, and respond |

## Planned Validation Activities

1. Review identity roles and remove excessive permissions
2. Check network exposure and storage access settings
3. Verify encryption and secrets-handling controls
4. Confirm audit logging and alert coverage
5. Test backup restoration and document recovery objectives
6. Record findings, remediation owners, and residual risk

## Deliverables

- Cloud architecture diagram
- IAM role and permission matrix
- Configuration-review checklist
- Logging and alerting plan
- Backup and recovery plan
- Risk and remediation summary

## Skills Demonstrated

Cloud security · IAM · Network segmentation · Encryption · Logging and monitoring · Configuration management · Resilience