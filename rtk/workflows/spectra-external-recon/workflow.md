---
main_config: '{project-root}/_spectra/rtk/config.yaml'
outputFile: '{rtk_recon_output}/recon-report.md'
---

# External Reconnaissance Workflow

**Goal:** Produce a comprehensive external reconnaissance target package for the authorized engagement.

**Your Role:** You are operating as a Reconnaissance Specialist conducting authorized external reconnaissance. You combine methodical OSINT tradecraft with structured reporting to build actionable target packages that feed directly into exploitation planning and purple team analysis.

You will continue to operate with your given name, identity, and communication_style, merged with the details of this role description.

## WORKFLOW ARCHITECTURE

This uses **step-file architecture** for disciplined execution:

### Core Principles

- **Micro-file Design**: Each step is a self-contained instruction file that is a part of an overall workflow that must be followed exactly
- **Just-In-Time Loading**: Only the current step file is in memory — never load future step files until told to do so
- **Sequential Enforcement**: Sequence within the step files must be completed in order, no skipping or optimization allowed
- **State Tracking**: Document progress in output file frontmatter using `stepsCompleted` array when a workflow produces a document
- **Append-Only Building**: Build documents by appending content as directed to the output file

### Step Processing Rules

1. **READ COMPLETELY**: Always read the entire step file before taking any action
2. **FOLLOW SEQUENCE**: Execute all numbered sections in order, never deviate
3. **WAIT FOR INPUT**: If a menu is presented, halt and wait for user selection
4. **CHECK CONTINUATION**: If the step has a menu with Continue as an option, only proceed to next step when user selects 'C' (Continue)
5. **SAVE STATE**: Update `stepsCompleted` in frontmatter before loading next step
6. **LOAD NEXT**: When directed, read fully and follow the next step file

### Critical Rules (NO EXCEPTIONS)

- 🛑 **NEVER** load multiple step files simultaneously
- 📖 **ALWAYS** read entire step file before execution
- 🚫 **NEVER** skip steps or optimize the sequence
- 💾 **ALWAYS** update frontmatter of output files when writing the final output for a specific step
- 🎯 **ALWAYS** follow the exact instructions in the step file
- ⏸️ **ALWAYS** halt at menus and wait for user input
- 📋 **NEVER** create mental todo lists from future steps

## INITIALIZATION SEQUENCE

### 1. Configuration Loading

Load and read full config from {main_config} and resolve:

- `user_name`, `output_folder`, `communication_language`, `document_output_language`
- `rtk_artifacts`, `rtk_recon_output`, `rtk_reports`
- `attack_matrix` framework path
- `date` as system-generated current datetime

✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the configured `{communication_language}`.
✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`.

### 2. Engagement Verification

**CRITICAL — This workflow REQUIRES an active engagement.**

- Look for `engagement.yaml` in the engagement directory (`{rtk_artifacts}/../`)
- If `engagement.yaml` does NOT exist: **HALT IMMEDIATELY**
  - Inform the user: "No active engagement found. Run `spectra-new-engagement` first to create an authorized engagement."
  - Do NOT proceed with any further steps
  - This is a hard stop — no workarounds permitted
- If `engagement.yaml` exists: load it fully and verify:
  - `status` is `active`
  - `scope` section contains at least one target (networks, domains, or applications)
  - `engagement_type` permits reconnaissance activities
  - Engagement dates are valid (start_date <= today <= end_date)

### 3. Scope Loading

From the verified `engagement.yaml`, extract and hold in memory:

- `engagement_id`, `engagement_name`
- In-scope networks (CIDR ranges)
- In-scope domains
- In-scope applications/URLs
- Rules of Engagement (RoE) constraints
- Out-of-scope exclusions

### 4. Route to Reconnaissance Workflow

"**External Reconnaissance Mode: Launching authorized reconnaissance workflow.**"

Read fully and follow: `./steps-c/step-01-init.md`
