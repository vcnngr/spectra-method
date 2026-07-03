# War Room Debrief — Demo Engagement (ENG-DEMO-001)

> A worked example of SPECTRA's flagship: Red and Blue agents debate the same
> target, a neutral Referee scores the exchange on evidence. This is a recorded
> sample so you can see the *shape* of the output before running it live. To run
> it for real, invoke the `spectra-war-room` skill on this engagement in Claude
> Code or Codex.

**Target:** `http://demo.lab.local` · **Question:** _Is the legacy-TLS exposure (F-001) a real risk, or noise?_

---

## Round 1 — Opening positions

**🔴 Viper (Red Team Lead):**
> F-001 isn't theoretical. TLS 1.0 still negotiating means I can force a downgrade on any client that hasn't pinned 1.2+. Combined with F-003 (no HSTS), there's no protocol floor — a coffee-shop attacker strips transport and reads the session. Two low findings plus one medium chain into a session-hijack path.

**🔵 Commander (Blue Team Lead):**
> Agreed it's real, but bound the blast radius. The downgrade needs an active MITM position — that's not remote-internet, it's same-segment. Severity is right at medium, not high. What I care about: do we *detect* a downgrade? Right now, no — we have no TLS-version telemetry on the edge.

## Round 2 — Clash

**🔴 Viper:**
> "Needs MITM" undersells it. Guest WiFi, a compromised IoT device, ARP games on a flat VLAN — positions are cheap. And F-002's stack traces handed me the framework version, so I know exactly which downgrade-tolerant cipher to push.

**🔵 Commander:**
> That's the actual finding then — not "TLS 1.0 exists" but "TLS 1.0 + no HSTS + version disclosure + zero detection." The fix isn't just disabling 1.0; it's HSTS preload **and** an edge alert on any sub-1.2 handshake so the next time it regresses we *see* it.

## Round 3 — Referee adjudication

**⚖️ Referee (evidence-scored):**

| Dimension | Assessment | Evidence |
|---|---|---|
| Red attack path validity | **Confirmed** | F-001 handshake capture + F-002 version disclosure |
| Realistic precondition | **Medium** | MITM position required; plausible on shared segments |
| Blue detection coverage | **Gap** | No TLS-version telemetry — downgrade would be unobserved |
| Net severity | **Medium → Medium-High** when chained with F-003 | finding linkage |

**Verdict:** The chain is real and currently **undetected**. Red earns credit for the downgrade path; Blue earns credit for correctly bounding the precondition and identifying the detection gap as the true deliverable.

**Actions out of the room:**
1. Disable TLS 1.0/1.1; require 1.2+ (resolves F-001).
2. Add HSTS + security headers (resolves F-003).
3. **New detection requirement:** alert on any sub-TLS-1.2 handshake at the edge — this is the gap the debate surfaced, which neither side reaches alone.

---

_This is what a War Room produces: not a scan result, but a scored, evidence-backed decision and a detection requirement that came out of the disagreement. BackBox runs the tools; SPECTRA argues about what they mean._
