# Cryptography and Network Security

## Project Summary

This project explains how modern cryptography protects confidentiality, integrity, authentication, and nonrepudiation across networks. It combines encryption, hashing, message authentication, public-key infrastructure, wireless security, and secure architecture into a defense-in-depth design.

## Security Objectives

- Protect sensitive data at rest and in transit
- Detect unauthorized data modification
- Verify users, devices, servers, and messages
- Establish and maintain trusted cryptographic keys
- Reduce exposure to interception, replay, spoofing, and on-path attacks

## Technologies and Concepts

### Symmetric Encryption

- AES for efficient data protection
- CBC, CTR, GCM, and XTS modes for different use cases
- DES and 3DES as legacy algorithms requiring replacement
- Secure initialization vectors, nonces, padding, and key handling

### Public-Key Cryptography

- RSA encryption and digital signatures
- Diffie–Hellman key exchange
- ElGamal concepts
- Elliptic-curve cryptography for efficient security
- Hybrid encryption combining asymmetric key exchange with symmetric data encryption

### Integrity and Authentication

- SHA-256, SHA-512, and SHA-3
- HMAC and CMAC
- Authenticated encryption with AES-GCM
- Digital signatures and certificate validation

### Public-Key Infrastructure

- Certificate authorities and registration authorities
- Certificate signing requests
- Certificate chains and trust stores
- Certificate status through CRLs and OCSP
- Key generation, storage, rotation, recovery, and revocation

## Secure Architecture

The proposed architecture uses TLS for communications, AES-GCM for protected data, centralized certificate management, multifactor authentication, segmented networks, WPA3 wireless security, secure email controls, continuous logging, and monitored key-lifecycle processes.

## Threats Addressed

- Eavesdropping
- Replay attacks
- Man-in-the-middle attacks
- Weak or reused keys
- Certificate spoofing
- Unauthorized decryption
- Data tampering
- Rogue wireless access

## Deliverables

- Cryptography comparison matrix
- AES and RSA process diagrams
- PKI trust-chain diagram
- Key-management lifecycle
- Secure network architecture
- Threat and mitigation analysis
- Technical report and executive presentation

## Skills Demonstrated

Cryptography · Key management · PKI · TLS · Network security · Wireless security · Architecture design · Technical communication

> Examples use educational, nonproduction values and do not expose real credentials or sensitive keys.