---
stepsCompleted: []
inputDocuments: []
workflowType: 'compliance-audit'
engagement_id: '{{engagement_id}}'
engagement_name: '{{engagement_name}}'
audit_id: ''
audit_name: ''
audit_type: ''
audit_status: 'open'
audit_trigger: ''
primary_framework: ''
secondary_frameworks: []
frameworks_assessed: []
scope_systems: []
scope_processes: []
scope_locations: []
scope_exclusions: []
total_controls_assessed: 0
controls_compliant: 0
controls_partially_compliant: 0
controls_non_compliant: 0
controls_not_applicable: 0
controls_not_assessed: 0
findings_critical: 0
findings_high: 0
findings_medium: 0
findings_low: 0
findings_informational: 0
total_findings: 0
evidence_items_collected: 0
evidence_items_validated: 0
evidence_gaps: 0
remediation_items: 0
remediation_immediate: 0
remediation_short_term: 0
remediation_medium_term: 0
remediation_long_term: 0
compensating_controls: 0
cross_framework_mappings: 0
evidence_reuse_percentage: 0
overall_compliance_percentage: 0
certification_readiness: ''
certification_blockers: 0
statement_of_applicability_complete: false
control_mapping_complete: false
evidence_collection_complete: false
gap_analysis_complete: false
remediation_plan_complete: false
crossmap_complete: false
executive_summary_complete: false
report_finalized: false
chronicle_recommended: false
initialization_timestamp: ''
---

# Compliance Audit Report — {{engagement_id}}

**Engagement:** {{engagement_name}}
**Compliance Auditor:** {{user_name}}
**Date:** {{date}}
**Status:** In Progress
**Audit ID:** {{audit_id}}

---

## 1. Audit Scope & Methodology

### 1.1 Engagement Authorization

*Verified authorization for compliance audit operations under the active engagement.*

**Authorization Checks:**

| Check | Requirement | Status |
|-------|------------|--------|
| File exists | engagement.yaml present | |
| Status active | `status: active` | |
| Dates valid | `start_date <= today <= end_date` | |
| Compliance audit authorized | Engagement permits compliance-audit, grc, blue-team, or purple-team | |
| Policy/procedure access | RoE permits access to policies, procedures, standards | |
| System configuration access | RoE permits access to configs, ACLs, technical controls | |
| Interview authorization | RoE permits structured interviews with control/process owners | |
| Scope defined | At least one target system, process, or org unit in scope | |

**Data Access Restrictions (if any):**

| Restriction | Source (RoE Clause) | Impact on Audit |
|-------------|---------------------|-----------------|
| | | |

### 1.2 Audit Trigger & Context

**Audit Type:** {{audit_type — certification/regulatory/internal/M&A/incident-driven/client-request}}
**Audit Trigger:** {{audit_trigger_description}}
**Timeline:** {{expected_timeline}}
**Prior Audit Reference:** {{prior_audit_id or 'Baseline — no prior audit'}}

### 1.3 Framework Selection

**Primary Framework:**

| Attribute | Value |
|-----------|-------|
| Framework | {{primary_framework}} |
| Version | {{version}} |
| Effective Date | {{effective_date}} |
| Total Controls | {{total_controls}} |
| Audit Standard | {{audit_standard_reference}} |

**Secondary Frameworks (Cross-Mapping):**

| Framework | Version | Purpose | Mapping Basis |
|-----------|---------|---------|---------------|
| | | | |

### 1.4 Scope Definition

**Systems in Scope:**

| System | Type | Owner | Environment | Classification |
|--------|------|-------|-------------|---------------|
| | | | | |

**Business Processes in Scope:**

| Process | Owner | Department | Regulatory Driver |
|---------|-------|------------|-------------------|
| | | | |

**Locations in Scope:**

| Location | Type | Jurisdiction | Applicable Regulations |
|----------|------|-------------|----------------------|
| | | | |

**Explicit Exclusions:**

| Exclusion | Reason | Risk of Exclusion |
|-----------|--------|-------------------|
| | | |

### 1.5 Methodology

**Audit Approach:** {{full/focused/gap/readiness}}
**Evidence Types:** {{documentary/technical/interview/observation}}
**Sampling Method:** {{sampling_approach}}
**Independence Statement:** {{independence_declaration}}

### 1.6 Stakeholders

| # | Stakeholder Name/Role | Category | Interest in Audit | Influence (H/M/L) | Communication Need |
|---|----------------------|----------|-------------------|-------------------|--------------------|
| | | | | | |

### 1.7 Audit Limitations

| Limitation | Source | Impact on Audit | Mitigation |
|------------|--------|-----------------|------------|
| | | | |

---

## 2. Framework Control Mapping & Statement of Applicability

### 2.1 Control Enumeration

*Complete control set for the primary framework with applicability determination.*

**Primary Framework: {{primary_framework}}**

| Control ID | Control Title | Domain/Theme | Applicable? | Justification (if N/A) | Control Owner |
|-----------|--------------|-------------|-------------|----------------------|---------------|
| | | | | | |

### 2.2 Statement of Applicability Summary

| Category | Count |
|----------|-------|
| Total Controls | |
| Applicable | |
| Not Applicable (with justification) | |
| Excluded (with risk acceptance) | |

### 2.3 Cross-Framework Mapping

| Primary Control ID | Primary Control Title | Secondary Framework | Secondary Control ID | Mapping Type |
|-------------------|----------------------|--------------------|--------------------|-------------|
| | | | | |

### 2.4 Responsibility Matrix

| Control ID | Control Owner | Implementer | Assessor | Shared Responsibility Notes |
|-----------|--------------|-------------|---------|---------------------------|
| | | | | |

---

## 3. Evidence Collection & Validation

### 3.1 Evidence Catalog

| Evidence ID | Description | Type | Source | Date Collected | Controls Mapped | Quality Rating |
|------------|-------------|------|--------|---------------|----------------|---------------|
| | | | | | | |

### 3.2 Evidence Quality Assessment

| Evidence ID | Currency | Completeness | Accuracy | Relevance | Sufficiency | Overall Quality |
|------------|---------|-------------|---------|-----------|-------------|----------------|
| | | | | | | |

### 3.3 Evidence Gaps & Follow-Up Requests

| Gap ID | Control(s) Affected | Evidence Missing | Requested From | Request Date | Status |
|--------|-------------------|-----------------|---------------|-------------|--------|
| | | | | | |

### 3.4 Technical Validation Summary

| Validation Type | Tool/Method | Systems Assessed | Findings Summary |
|----------------|------------|-----------------|-----------------|
| | | | |

---

## 4. Gap Analysis & Findings

### 4.1 Per-Control Assessment

| Control ID | Control Title | Status | Evidence Reference | Justification |
|-----------|--------------|--------|-------------------|---------------|
| | | | | |

**Status Legend:** Compliant / Partially Compliant / Non-Compliant / Not Applicable / Not Assessed

### 4.2 Compliance Scoring

| Domain/Theme | Total Controls | Compliant | Partial | Non-Compliant | N/A | Compliance % |
|-------------|---------------|-----------|---------|---------------|-----|-------------|
| | | | | | | |

**Overall Compliance Percentage:** {{overall_compliance_percentage}}%

### 4.3 Finding Details

#### FIND-001: {{Finding Title}}

| Attribute | Value |
|-----------|-------|
| Finding ID | FIND-001 |
| Severity | {{Critical/High/Medium/Low/Informational}} |
| Affected Control(s) | {{control_ids}} |
| Framework Requirement(s) | {{specific_requirement_numbers}} |
| Description | |
| Evidence | {{evidence_ids}} |
| Business Risk | |
| Root Cause | |
| Recommendation | |
| Remediation Deadline | |
| Finding Owner | |

---

## 5. Remediation Roadmap

### 5.1 Prioritized Remediation Plan

| Priority | Finding ID | Finding Title | Severity | Remediation Action | Timeline | Resources | Owner | Status |
|----------|-----------|--------------|----------|-------------------|----------|-----------|-------|--------|
| | | | | | | | | |

### 5.2 Phased Roadmap

**Phase 1 — Critical & High Findings (0-90 days):**

| # | Action | Finding(s) | Dependencies | Acceptance Criteria | Owner | Milestone |
|---|--------|-----------|-------------|--------------------|---------|---------| 
| | | | | | | |

**Phase 2 — Medium Findings (90-180 days):**

| # | Action | Finding(s) | Dependencies | Acceptance Criteria | Owner | Milestone |
|---|--------|-----------|-------------|--------------------|---------|---------| 
| | | | | | | |

**Phase 3 — Low & Improvement (180+ days):**

| # | Action | Finding(s) | Dependencies | Acceptance Criteria | Owner | Milestone |
|---|--------|-----------|-------------|--------------------|---------|---------| 
| | | | | | | |

### 5.3 Compensating Controls

| Finding ID | Compensating Control | Effectiveness | Type (Temp/Perm) | Review Date |
|-----------|---------------------|--------------|-----------------|------------|
| | | | | |

### 5.4 Continuous Compliance Recommendations

| # | Recommendation | Category | Tools/Methods | Frequency | Owner |
|---|---------------|----------|--------------|-----------|-------|
| | | | | | |

---

## 6. Cross-Framework Analysis

### 6.1 Unified Control Matrix

| Unified Control | {{Primary Framework}} | {{Secondary 1}} | {{Secondary 2}} | Evidence Reuse |
|----------------|----------------------|-----------------|-----------------|---------------|
| | | | | |

### 6.2 Efficiency Analysis

| Metric | Value |
|--------|-------|
| Total controls across all frameworks | |
| Unique controls (after deduplication) | |
| Overlap percentage | |
| Evidence items collected | |
| Evidence items reusable across frameworks | |
| Evidence reuse percentage | |
| Estimated effort reduction | |

### 6.3 Multi-Framework Compliance Dashboard

| Framework | Total Controls | Compliant | Partial | Non-Compliant | N/A | Compliance % |
|-----------|---------------|-----------|---------|---------------|-----|-------------|
| | | | | | | |

### 6.4 Framework-Unique Controls

| Framework | Unique Control ID | Control Title | Status | Notes |
|-----------|------------------|--------------|--------|-------|
| | | | | |

---

## 7. Executive Summary

### 7.1 Audit Overview

*High-level summary of audit scope, methodology, and key outcomes.*

### 7.2 Key Findings

*Top findings by severity with business impact and recommended action.*

### 7.3 Compliance Posture

*Overall compliance percentage, certification readiness, and risk assessment.*

### 7.4 Top Recommendations

| # | Recommendation | Addresses Finding(s) | Priority | Timeline | Estimated Investment |
|---|---------------|---------------------|----------|----------|---------------------|
| | | | | | |

### 7.5 Certification Readiness Assessment

| Criterion | Status | Notes |
|-----------|--------|-------|
| All critical findings remediated | | |
| All high findings remediated or compensated | | |
| Statement of Applicability complete | | |
| Evidence package complete | | |
| Management commitment documented | | |

### 7.6 Audit Metrics

| Metric | Value |
|--------|-------|
| Controls Assessed | |
| Controls Compliant | |
| Controls Partially Compliant | |
| Controls Non-Compliant | |
| Controls Not Applicable | |
| Total Findings | |
| — Critical | |
| — High | |
| — Medium | |
| — Low | |
| — Informational | |
| Evidence Items Collected | |
| Cross-Framework Mappings | |
| Remediation Items | |
| Estimated Total Investment | |
| Overall Compliance Percentage | |
| Certification Readiness | |

---

## 8. Appendices

### Appendix A — Framework Reference

*Complete framework control listing with version and effective date.*

### Appendix B — Evidence Index

*Complete evidence catalog with chain of custody and quality ratings.*

### Appendix C — Interview Log

| # | Interviewee | Role | Date | Controls Covered | Key Findings |
|---|-------------|------|------|-----------------|-------------|
| | | | | | |

### Appendix D — Technical Validation Details

*Detailed technical assessment results: CIS benchmarks, vulnerability scans, access reviews, log analysis.*

### Appendix E — Cross-Framework Mapping Detail

*Complete mapping table between all assessed frameworks.*

### Appendix F — Management Response

*Placeholder for management responses to audit findings.*

| Finding ID | Management Response | Responsible Party | Target Date | Accepted? |
|-----------|--------------------|--------------------|-------------|----------|
| | | | | |

### Appendix G — Glossary & Acronyms

| Term | Definition |
|------|-----------|
| | |
