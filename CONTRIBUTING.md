# Contributing to SPECTRA

Thank you for your interest in contributing to SPECTRA.

## Development Setup

```bash
git clone https://github.com/vcnngr/spectra-method.git
cd spectra-method
npm install
```

## Validation

Before submitting changes, run the validator:

```bash
python3 core/execution/validate-spectra.py --path . --strict
```

All 1,459 checks must pass with 0 warnings and 0 failures.

## Architecture

Read `DEV-GUIDE.md` (in the development branch) for exact file formats, patterns, and development principles.

### Key Patterns

- **Agent SKILL.md**: Frontmatter (name, description) + Overview + On Activation + Capabilities
- **Workflow**: SKILL.md redirect + workflow.md + steps-c/ with numbered step files
- **Step files**: STEP GOAL + MANDATORY EXECUTION RULES + Agent Autonomy Protocol + A/W/C menu + SUCCESS/FAILURE METRICS
- **"Read fully and follow"**: Mandatory pattern for every step transition
- **Append-only**: Documents built by appending, never rewriting

### Agent Autonomy Protocol (mandatory in every step file)

- HARD BLOCK destructive payloads only (ransomware, wipers)
- WARN + COMPLY on everything else
- Always propose alternatives

## Pull Request Process

1. Fork the repository
2. Create a feature branch
3. Run the validator (must pass clean)
4. Submit PR with description of changes
5. Reference any related issues

## Adding New Agents

1. Create `{module}/agents/spectra-agent-{name}/SKILL.md`
2. Create `{module}/agents/spectra-agent-{name}/bmad-skill-manifest.yaml`
3. Add entry to `_config/agent-manifest.csv`
4. Add entry to `_config/skill-manifest.csv`
5. Run validator

## Adding New Workflows

1. Create `{module}/workflows/spectra-{name}/SKILL.md` (redirect)
2. Create `{module}/workflows/spectra-{name}/workflow.md`
3. Create `{module}/workflows/spectra-{name}/steps-c/step-01-init.md` through `step-N.md`
4. Create resume handler `step-01b-continue.md`
5. Create output template in `templates/`
6. Add entry to `_config/skill-manifest.csv`
7. Run validator

## Code of Conduct

Be professional. Be constructive. Focus on making SPECTRA better.
