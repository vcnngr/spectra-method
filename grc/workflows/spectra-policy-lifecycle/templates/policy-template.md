---
stepsCompleted: []
inputDocuments: []
workflowType: 'policy-lifecycle'
engagement_id: '{{engagement_id}}'
engagement_name: '{{engagement_name}}'
policy_id: ''
policy_name: ''
policy_type: ''
policy_version: '1.0'
policy_status: 'draft'
effective_date: ''
review_date: ''
next_review_date: ''
owner: ''
author: ''
approver: ''
classification: 'internal'
framework_alignment: []
controls_addressed: []
scope_departments: []
scope_systems: []
target_audience: ''
exceptions_granted: 0
policy_trigger: ''
regulatory_drivers: []
industry_benchmarks: []
related_policies: []
supersedes: ''
research_complete: false
drafting_complete: false
review_cycles_completed: 0
reviewers_signed_off: 0
reviewers_total: 0
approval_status: 'pending'
approval_date: ''
publication_date: ''
awareness_plan_created: false
training_requirements: 0
acknowledgment_tracking: false
enforcement_mechanisms: 0
automated_controls: 0
manual_controls: 0
detective_controls: 0
corrective_controls: 0
compliance_kpis: 0
exception_process_defined: false
violation_framework_defined: false
review_schedule_set: false
maintenance_plan_created: false
lifecycle_report_complete: false
chronicle_recommended: false
change_log:
  - version: '1.0'
    date: '{{date}}'
    author: '{{user_name}}'
    description: 'Initial draft'
review_history: []
---

# {{policy_name}} — {{policy_type}}

**Engagement:** {{engagement_name}}
**Policy Author:** {{user_name}}
**Date:** {{date}}
**Status:** Draft
**Classification:** {{classification}}
**Version:** {{policy_version}}

---

## Document Control

### Document Information

| Field | Value |
|-------|-------|
| **Policy ID** | {{policy_id}} |
| **Policy Name** | {{policy_name}} |
| **Document Type** | {{policy_type}} |
| **Version** | {{policy_version}} |
| **Status** | {{policy_status}} |
| **Classification** | {{classification}} |
| **Effective Date** | {{effective_date}} |
| **Review Date** | {{review_date}} |
| **Next Scheduled Review** | {{next_review_date}} |
| **Owner** | {{owner}} |
| **Author** | {{author}} |
| **Approver** | {{approver}} |
| **Supersedes** | {{supersedes}} |

### Change Log

| Version | Date | Author | Description | Approved By |
|---------|------|--------|-------------|-------------|
| {{policy_version}} | {{date}} | {{user_name}} | Initial draft | Pending |

### Review History

| Review Date | Reviewer | Role | Outcome | Comments |
|-------------|----------|------|---------|----------|
| | | | | |

### Distribution

| Audience | Method | Date | Acknowledgment Required |
|----------|--------|------|------------------------|
| | | | |

---

## 1. Purpose & Scope

### 1.1 Purpose

*Why does this document exist? What organizational need does it address?*

> {{purpose_statement}}

### 1.2 Scope

**Applies To:**

| Category | In Scope | Details |
|----------|----------|---------|
| **Departments** | {{scope_departments}} | |
| **Systems** | {{scope_systems}} | |
| **Personnel** | {{target_audience}} | |
| **Locations** | | |
| **Data Types** | | |
| **Third Parties** | | |

**Does Not Apply To (Explicit Exclusions):**

| Exclusion | Reason |
|-----------|--------|
| | |

### 1.3 Document Hierarchy

*Where this document sits in the policy framework:*

| Level | Document | Relationship |
|-------|----------|-------------|
| **Policy** | {{parent_policy_or_self}} | Sets management intent |
| **Standard** | {{related_standards}} | Specifies mandatory requirements |
| **Procedure** | {{related_procedures}} | Defines step-by-step implementation |
| **Guideline** | {{related_guidelines}} | Recommends best practices |

### 1.4 Framework Alignment

| Framework | Control(s) | Requirement | Coverage |
|-----------|-----------|-------------|----------|
| | | | |

---

## 2. Policy Statements

*High-level mandatory statements of management intent. Each statement uses RFC 2119 language (SHALL, SHALL NOT, SHOULD, MAY, MUST, MUST NOT).*

### 2.1 General Statements

> **PS-01:** {{policy_statement_01}}

> **PS-02:** {{policy_statement_02}}

> **PS-03:** {{policy_statement_03}}

### 2.2 Specific Requirements

*Measurable, enforceable requirements that implement the policy statements above.*

| Req ID | Requirement | Implements | Measurement Criteria | Enforcement Method |
|--------|-------------|-----------|---------------------|-------------------|
| REQ-01 | | PS-## | | |
| REQ-02 | | PS-## | | |
| REQ-03 | | PS-## | | |

---

## 3. Standards & Requirements

*Specific technical or operational standards that support the policy statements. Each standard must be measurable and verifiable.*

### 3.1 Technical Standards

| Standard ID | Requirement | Threshold/Metric | Verification Method | Framework Reference |
|-------------|-------------|-------------------|--------------------|--------------------|
| STD-01 | | | | |
| STD-02 | | | | |

### 3.2 Operational Standards

| Standard ID | Requirement | Frequency | Responsible Role | Evidence Required |
|-------------|-------------|-----------|-----------------|-------------------|
| STD-01 | | | | |
| STD-02 | | | | |

### 3.3 Data Handling Standards

| Data Classification | Handling Requirement | Storage | Transmission | Disposal |
|--------------------|---------------------|---------|-------------|----------|
| | | | | |

---

## 4. Procedures

*Step-by-step operational instructions for implementing the standards above. Each procedure is linked to a specific standard.*

### 4.1 {{Procedure Name}}

**Implements:** STD-##
**Performed By:** {{role}}
**Frequency:** {{frequency}}
**Estimated Duration:** {{duration}}

**Prerequisites:**
- {{prerequisite_1}}

**Steps:**

| Step | Action | Details | Decision Point | Escalation |
|------|--------|---------|---------------|-----------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |

**Rollback / Recovery:**
- {{rollback_instructions}}

---

## 5. Roles & Responsibilities

### 5.1 RACI Matrix

| Activity | {{Role_1}} | {{Role_2}} | {{Role_3}} | {{Role_4}} |
|----------|-----------|-----------|-----------|-----------|
| Policy approval | | | | |
| Policy implementation | | | | |
| Compliance monitoring | | | | |
| Exception approval | | | | |
| Violation response | | | | |
| Policy review | | | | |

**Legend:** R = Responsible, A = Accountable, C = Consulted, I = Informed

### 5.2 Role Definitions

| Role | Responsibilities | Authority | Escalation Path |
|------|-----------------|-----------|----------------|
| **Policy Owner** | | | |
| **Policy Author** | | | |
| **Compliance Monitor** | | | |
| **Exception Approver** | | | |

---

## 6. Compliance & Enforcement

### 6.1 Compliance Monitoring

| Mechanism | Type | Frequency | Responsible | KPI |
|-----------|------|-----------|-------------|-----|
| | Automated/Manual/Detective | | | |

### 6.2 Non-Compliance Handling

| Violation Severity | Description | Response | Escalation | Timeline |
|-------------------|-------------|----------|-----------|----------|
| **Minor** (Inadvertent) | | | | |
| **Moderate** (Negligent) | | | | |
| **Major** (Willful) | | | | |
| **Critical** (Malicious) | | | | |

### 6.3 Enforcement Metrics

| KPI | Target | Measurement Method | Reporting Frequency |
|-----|--------|-------------------|-------------------|
| Compliance rate | | | |
| Exception rate | | | |
| Violation rate | | | |
| Training completion | | | |
| Acknowledgment rate | | | |

---

## 7. Exceptions Process

### 7.1 Exception Request

To request an exception to this {{policy_type}}:

| Field | Description |
|-------|-------------|
| **Requestor** | Name and role of the person requesting the exception |
| **Policy Requirement** | Specific requirement (REQ-##/STD-##) for which exception is sought |
| **Business Justification** | Why the exception is needed — business impact of compliance |
| **Risk Assessment** | What risk does the exception introduce? |
| **Compensating Controls** | What alternative controls will be in place? |
| **Duration** | How long is the exception needed? (Must be time-limited) |
| **Review Date** | When will the exception be reassessed? |

### 7.2 Exception Approval Authority

| Risk Level of Exception | Approval Authority | Maximum Duration |
|------------------------|-------------------|-----------------|
| Low | {{approver_low}} | 12 months |
| Medium | {{approver_medium}} | 6 months |
| High | {{approver_high}} | 3 months |
| Critical | {{approver_critical}} | 1 month (with board notification) |

### 7.3 Exception Register

| Exception ID | Requestor | Requirement | Justification | Risk | Compensating Control | Approved By | Expiry | Status |
|-------------|-----------|-------------|---------------|------|---------------------|-------------|--------|--------|
| | | | | | | | | |

---

## 8. Related Documents

| Document | Type | Relationship | Location |
|----------|------|-------------|----------|
| | Policy/Standard/Procedure/Guideline | Parent/Child/Related/Supersedes | |

---

## 9. Definitions & Glossary

| Term | Definition |
|------|-----------|
| | |

**RFC 2119 Language Reference:**

| Keyword | Meaning |
|---------|---------|
| **SHALL / MUST / REQUIRED** | Absolute requirement — non-compliance is a violation |
| **SHALL NOT / MUST NOT** | Absolute prohibition — doing this is a violation |
| **SHOULD / RECOMMENDED** | Strong recommendation — deviation requires documented justification |
| **SHOULD NOT / NOT RECOMMENDED** | Strong discouragement — doing this requires documented justification |
| **MAY / OPTIONAL** | Truly optional — no justification needed for either choice |

---

## 10. Review & Maintenance

### 10.1 Review Schedule

| Review Type | Frequency | Next Due | Responsible | Trigger Events |
|-------------|-----------|----------|------------|----------------|
| **Scheduled Review** | {{review_frequency}} | {{next_review_date}} | {{owner}} | Calendar |
| **Triggered Review** | As needed | N/A | {{owner}} | See trigger events below |

**Trigger Events for Unscheduled Review:**

- Regulatory change affecting this policy domain
- Security incident revealing a policy gap
- Organizational restructuring affecting scope
- Technology change affecting enforceability
- Audit finding related to this policy
- Framework update (ISO/NIST/PCI DSS version change)
- Material risk assessment finding
- Stakeholder or executive request

### 10.2 Maintenance Classification

| Change Type | Process | Approval | Examples |
|-------------|---------|----------|---------|
| **Minor Update** | Author updates, owner approves | Policy Owner | Clarification, formatting, contact updates, typo fixes |
| **Major Update** | Full review cycle | Original approval authority | New requirements, scope changes, enforcement changes |
| **Emergency Update** | Expedited review (48h) | CISO + Policy Owner | Critical vulnerability, regulatory deadline, active incident |
| **Retirement** | Sunset review | Original approval authority | Policy superseded, domain no longer applicable |

### 10.3 Version Control

- Major versions: X.0 (new requirements, scope changes, enforcement changes — full review required)
- Minor versions: X.Y (clarifications, formatting, non-substantive changes — owner approval only)
- All versions archived with change rationale
- Previous versions accessible for audit trail

---

## 11. Appendices

### Appendix A: Framework Control Mapping

| Policy Requirement | ISO 27001 | NIST 800-53 | CIS Controls v8 | SOC 2 | PCI DSS |
|-------------------|-----------|-------------|-----------------|-------|---------|
| | | | | | |

### Appendix B: Implementation Checklist

| # | Action Item | Responsible | Deadline | Status | Evidence |
|---|------------|------------|----------|--------|----------|
| 1 | | | | | |

### Appendix C: Awareness & Training Plan

| Audience | Training Type | Content | Delivery Method | Frequency | Tracking |
|----------|--------------|---------|----------------|-----------|----------|
| | | | | | |

### Appendix D: Quick Reference Card

*One-page summary of key requirements for day-to-day reference.*

**{{policy_name}} — Quick Reference**

| What You Must Do | What You Must Not Do | Where to Get Help |
|-----------------|---------------------|-------------------|
| | | |

---

*This document was created using the SPECTRA Policy Lifecycle workflow. All requirements are traceable to the frameworks listed in Appendix A. For questions about this {{policy_type}}, contact {{owner}}.*
