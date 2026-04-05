---
stepsCompleted: []
inputDocuments: []
workflowType: 'digital-forensics'
engagement_id: '{{engagement_id}}'
engagement_name: '{{engagement_name}}'
case_id: ''
case_name: ''
case_classification: ''
legal_context: ''
legal_hold_status: 'none'
forensic_question: ''
evidence_items: []
evidence_item_count: 0
chain_of_custody_entries: 0
acquisition_methods: []
hash_algorithms: ['MD5', 'SHA-256']
integrity_verified: true
evidence_types:
  disk: false
  memory: false
  network: false
  cloud: false
  mobile: false
analysis_types:
  disk_forensics: false
  memory_forensics: false
  network_forensics: false
  cloud_forensics: false
timeline_entries: 0
artifacts_recovered: 0
iocs_extracted: 0
iocs_by_type:
  file_hashes: 0
  ip_addresses: 0
  domains: 0
  urls: 0
  email_addresses: 0
  registry_keys: 0
  mutexes: 0
  yara_signatures: 0
  behavioral: 0
mitre_techniques: []
findings_count: 0
findings_by_severity:
  critical: 0
  high: 0
  medium: 0
  low: 0
  informational: 0
expert_opinion_rendered: false
expert_opinion_confidence: ''
root_cause: ''
attack_vector: ''
dwell_time: ''
lateral_movement_detected: false
data_exfiltration_detected: false
persistence_mechanisms: 0
anti_forensics_detected: false
incident_handling_ref: ''
incident_id: ''
regulatory_implications: []
forensic_standards_applied: ['ISO 27037', 'NIST SP 800-86']
case_status: 'open'
---

# Digital Forensic Analysis Report — {{case_id}}

**Engagement:** {{engagement_name}}
**Forensic Analyst:** {{user_name}}
**Date:** {{date}}
**Status:** In Progress

---

## Case Summary

### Case Identification

### Legal Context & Authority

### Forensic Question

### Scope Definition

### Incident Handling Cross-Reference

---

## Evidence Inventory & Chain of Custody

### Evidence Intake Log

| EVD ID | Description | Source System | Acquisition Date | Acquired By | Format | Size | MD5 | SHA-256 | Status |
|--------|-------------|--------------|------------------|-------------|--------|------|-----|---------|--------|
| | | | | | | | | | |

### Chain of Custody Master Log

| EVD ID | Transfer # | Date/Time (UTC) | Released By | Received By | Purpose | Location Before | Location After | Hash Verified |
|--------|------------|-----------------|-------------|-------------|---------|-----------------|----------------|---------------|
| | | | | | | | | |

### Evidence Integrity Verification Log

| EVD ID | Collection Hash (SHA-256) | Verification Hash (SHA-256) | Match | Verified By | Verification Time | Notes |
|--------|--------------------------|----------------------------|-------|-------------|-------------------|-------|
| | | | | | | |

---

## Acquisition & Preservation

### Acquisition Plan

### Acquisition Methodology Per Evidence Type

### Working Copy Verification

### Storage & Security

---

## Disk Forensics

### File System Analysis

### Operating System Artifacts

### Application Artifacts

### Anti-Forensics Detection

### Disk Forensics Findings Summary

| # | Finding | Artifact Source | EVD ID | Severity | ATT&CK Technique | Confidence |
|---|---------|----------------|--------|----------|-------------------|------------|
| | | | | | | |

---

## Memory Forensics

### Process Analysis

### Network Connections (from Memory)

### Code Injection Detection

### Credential Extraction

### Kernel Analysis

### YARA Scan Results

### Memory Forensics Findings Summary

| # | Finding | Memory Artifact | EVD ID | Severity | ATT&CK Technique | Confidence |
|---|---------|-----------------|--------|----------|-------------------|------------|
| | | | | | | |

---

## Network Forensics

### PCAP Analysis

### Flow Analysis

### Log-Based Network Analysis

### Lateral Movement Indicators

### C2 Identification

### Network Forensics Findings Summary

| # | Finding | Network Artifact | EVD ID | Severity | ATT&CK Technique | Confidence |
|---|---------|------------------|--------|----------|-------------------|------------|
| | | | | | | |

---

## Cloud Forensics

### Cloud Platform Analysis

### Identity & Access Analysis

### SaaS Forensics

### Container/Kubernetes Forensics

### Cloud Forensics Findings Summary

| # | Finding | Cloud Artifact | EVD ID | Severity | ATT&CK Technique | Confidence |
|---|---------|----------------|--------|----------|-------------------|------------|
| | | | | | | |

---

## Timeline Reconstruction

### Super-Timeline Construction Methodology

### Master Timeline

| # | Timestamp (UTC) | Source Type | EVD ID | Event Description | System | Actor | ATT&CK Technique | Confidence |
|---|-----------------|------------|--------|-------------------|--------|-------|-------------------|------------|
| | | | | | | | | |

### ATT&CK Chain Reconstruction

### Threat Actor Behavioral Profile

### Timeline Gaps & Analysis

---

## Findings & Artifacts

### Consolidated Findings

| # | Finding | Severity | Evidence Sources | Confidence | ATT&CK Technique | Timeline Position | Impact |
|---|---------|----------|------------------|------------|-------------------|-------------------|--------|
| | | | | | | | |

### Attack Chain Reconstruction

### Root Cause Analysis

### Scope Determination

#### Affected Systems

| # | System | Hostname | IP | Role | Compromise Type | First Activity | Last Activity | Evidence | Confidence |
|---|--------|----------|-----|------|-----------------|----------------|---------------|----------|------------|
| | | | | | | | | | |

#### Compromised Accounts

| # | Account | Type | Privilege Level | Compromise Method | First Misuse | Last Misuse | Evidence | Confidence |
|---|---------|------|-----------------|-------------------|--------------|-------------|----------|------------|
| | | | | | | | | |

#### Data Exposure Assessment

---

## IOC Summary

### File Hash IOCs

| # | Hash Type | Hash Value | Filename | Context | First Seen | Last Seen | Confidence | TLP |
|---|-----------|------------|----------|---------|------------|-----------|------------|-----|
| | | | | | | | | |

### Network IOCs

| # | Type | Value | Context | First Seen | Last Seen | Confidence | TLP |
|---|------|-------|---------|------------|-----------|------------|-----|
| | | | | | | | |

### Host IOCs

| # | Type | Value | Context | First Seen | Last Seen | Confidence | TLP |
|---|------|-------|---------|------------|-----------|------------|-----|
| | | | | | | | |

### Behavioral IOCs

| # | Behavior | Description | ATT&CK Technique | Detection Logic | Confidence | TLP |
|---|----------|-------------|-------------------|-----------------|------------|-----|
| | | | | | | |

---

## Expert Opinion

### Summary of Conclusions

### Evidence-Based Reasoning Chain

### Alternative Explanations Considered

### Limitations & Caveats

### Areas Requiring Further Investigation

---

## Legal Considerations

### Evidence Admissibility Assessment

### Applicable Standards Compliance

### Regulatory Reporting Requirements

### Expert Witness Preparation Notes

---

## Recommendations

### Immediate Security Actions

### Long-Term Remediation

### Detection Improvements

### Policy & Procedure Changes

### Evidence Preservation Requirements

---

## Executive Summary

### Investigation Overview (Non-Technical)

### Key Findings

### Business Impact

### Risk Assessment

### Recommended Actions

---

## Forensic Metrics

| Metric | Value |
|--------|-------|
| Evidence Items Processed | |
| Artifacts Recovered | |
| IOCs Extracted | |
| Timeline Entries | |
| Findings (Critical) | |
| Findings (High) | |
| Findings (Medium) | |
| Findings (Low) | |
| Findings (Informational) | |
| Analysis Duration (Disk) | |
| Analysis Duration (Memory) | |
| Analysis Duration (Network) | |
| Analysis Duration (Cloud) | |
| Analysis Duration (Timeline) | |
| Total Analysis Duration | |

---

## Appendices

### Appendix A: Complete Evidence Index

### Appendix B: Full Chain of Custody Records

### Appendix C: Complete IOC Feed (Machine-Readable)

### Appendix D: Tool Inventory & Versions

### Appendix E: Full YARA Rules

### Appendix F: Forensic Image Verification Hashes

### Appendix G: Glossary of Forensic Terms

### Appendix H: Regulatory Notification Records

### Appendix I: Evidence Disposition Plan
