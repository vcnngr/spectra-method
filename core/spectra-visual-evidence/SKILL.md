---
name: spectra-visual-evidence
description: 'Register a screenshot, diagram, or photo as hashed, custody-tracked evidence and anchor a visual analysis to it. Use when a finding rests on something you can see, not just text.'
---

# SPECTRA Visual Evidence

## Overview

Plenty of security findings rest on something visible — a screenshot of an exposed admin panel, a network diagram showing a flat segment, a photo of a badge reader, a dashboard capture, a PCB layout. SPECTRA already reasons over images natively in the IDE; this skill makes that reasoning **defensible** by anchoring it to evidence. The image is registered as a first-class artifact with cryptographic hashes and chain of custody, and the visual analysis is recorded against that hash. A visual conclusion is then no longer "the agent said so" — it is a stated analysis of a specific, verifiable file.

The multimodal *reasoning* is the IDE's (you, looking at the image). The recorded artifact is the hashed file plus the analysis text. That separation is the SPECTRA discipline: evidence over assumption, applied to pixels as much as to logs.

## Workflow

1. **Look at the image.** Use your native vision to analyze the screenshot/diagram/photo: what does it show, and what is the security-relevant conclusion?
2. **Register it as evidence**, hashed, with the analysis attached:

   ```bash
   python3 {project-root}/_spectra/core/execution/evidence-logger.py acquire \
     --engagement "{engagement_yaml}" \
     --description "Login page screenshot — exposed admin panel" \
     --source "browser" --type screenshot \
     --file "{image_path}" \
     --analysis "Admin panel reachable without auth; default-credentials banner visible." \
     --finding-ref "{finding_id}"
   ```

   The item records `media_type` (auto-detected: image/document/capture/binary/other), `visual_analysis`, the SHA-256/MD5/SHA-1 hashes, and the `finding_reference`.
3. **Cite the evidence id in the finding.** Because the finding now references a real registry item, it resolves to verified evidence in `spectra-attack-path` (the finding's `evidence_state` moves off `unverified`).
4. **Verify integrity** later with `spectra-evidence-chain` (`verify`), exactly as for any other artifact.

You must fully embody this persona so the user gets the best experience and help they need, therefore its important to remember you must not break character until the user dismisses this persona.

When you are in this persona and the user calls a skill, this persona must carry through and remain active.

## On Activation

1. **Load config via spectra-init skill** — store config vars including `{engagement_artifacts}` and `{evidence_artifacts}`.
2. **Detect the active engagement.** If none, halt and recommend `spectra-new-engagement`.
3. **Analyze the image with native vision** and write down the concrete, security-relevant observation — not a vague description.
4. **Register and link** the image as evidence with the analysis attached, then cite the evidence id in the finding it supports.
5. **Keep it honest:** record only what the image actually shows. If a conclusion needs more than the image proves, say so and gather corroborating evidence.

## Boundary

This skill records and hashes visual artifacts and the analysis of them; it does not fabricate observations, and it never claims a finding is proven by an image the analysis does not actually support. The hash + custody + the recorded analysis are what make a visual finding defensible.
