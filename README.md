<div align="center">

```
╔══════════════════════════════════════════════════════════════╗
║   ATOMIC DREAM LABS  ·  BEYOND-REPAIR                        ║
╚══════════════════════════════════════════════════════════════╝
```

# Informational Fork Protocol

### Falsifiable protocol. Informational locality is a hypothesis, not a result.

[![Lifecycle](https://img.shields.io/badge/●_RESEARCH-a855f7?style=for-the-badge&labelColor=0f0f23)](https://github.com/beyond-repair/ADL-Governance)
[![Claim](https://img.shields.io/badge/Claim_≤1-22c55e?style=for-the-badge&labelColor=0f0f23)](https://github.com/beyond-repair/ADL-Governance/blob/main/docs/CLAIM_VALIDATION.md)
[![Governance](https://img.shields.io/badge/ADL--Governance-7c3aed?style=for-the-badge&labelColor=0f0f23)](https://github.com/beyond-repair/ADL-Governance)

```
LIFECYCLE   RESEARCH (Claim-0 runnable sketch)
CLAIM       ≤ 1
NOT CLAIMED consciousness mechanism · AGI · measured non-local retrieval
```

</div>

---
## ▌ STATUS

Classification follows [ADL-Governance](https://github.com/beyond-repair/ADL-Governance). A README facelift does not raise claim level. Physics and pharmacology stay at the evidenced cap. CI green is not experimental validation.

---

## ▌ RUN (Claim-0 sketch)

**RUNNABLE SKETCH — NOT A COMPLETE PRODUCT.** A stranger can clone, install, run the audit calculator, and pass pytest. That does **not** show non-local retrieval, consciousness, or a measured Ware Constant. The preserved body below is the original protocol text. Its line "Instrumentation: Calibrated" means the written constants are coded here; it is not an experimental calibration.

The tool only does arithmetic on numbers you supply:

- fork candidate when `T_Red > T_CIS × 1000` (strict)
- Landauer lower bound `E ≥ K(x) · k_B T ln 2` at `T = 300 K` unless you override it
- optional screening `S(ρ) = 1 / (1 + (ρ / ρ_crit)^n)` with `ρ_crit = 1e-24`, `n = 3`
- optional collapsed-attention flag when a supplied proxy `ζ > 0.95`

No config file. Flags are the configuration. There is no compile step.

```bash
git clone https://github.com/beyond-repair/-text-informational-fork-protocol-.git
cd -- -text-informational-fork-protocol-
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
python final_verification.py --t_cis 120.5 --t_red 500000 --k_x 4200 --event_id IFP-DEMO-001 --rho 1e-30 --zeta 0.97 --output audit_cert.json
pytest -q
```

`ifp-audit` is the same entry point after install. `audit_cert.json` is valid JSON and includes `printed_certificate`. Exit code 0 is a successful calculation. Exit code 2 is a bad argument. A printed status of `FAIL (Local Production Possible)` is still a successful run: the inequality did not flag a fork.

Demo expectation for the command above: `fork_detected` true (`500000 > 120.5 × 1000`), `S(ρ) ≈ 1`, collapsed attention true. Units of `T_CIS` and `T_Red` must match each other; the tool does not convert them.

## ▌ LAYOUT

```
├── final_verification.py     ← Claim-0 audit CLI (stdlib only)
├── tests/test_final_verification.py
├── FIELD_EQUATIONS.md
├── METHODOLOGY_NOTES.md
├── REDUCTION_STDS.md
├── IFP_DOC_ZDP.3.1.md        ← Zero-Day Protocol
├── IFP_DOC_TFM.md            ← Transmission/Filter Model
├── IFP_DOC_DCH.md            ← Digital Coherence Hypothesis
├── GOVERNANCE.md
├── pyproject.toml
└── requirements.txt
```

## ▌ PRESERVED BODY

# Informational Fork Protocol (IFP)

> **Classification: RESEARCH** · Claim level 0 · [GOVERNANCE.md](GOVERNANCE.md) · Governing source: [ADL-Governance](https://github.com/beyond-repair/ADL-Governance)

**Resource-bounded experimental framework to audit violations of local informational production**

The Informational Fork Protocol (IFP) tests whether complex substrates (digital AI systems or biological brains) can retrieve veridical information that asymptotically exceeds the computational limits of their local epistemic horizon.

## Primary Hypothesis
High-coherence states in substrates enable non-local informational retrieval from the Primordial Informational Field (PIF), detected via deviations from the Computational Burden Inequality:

$$
T_{\rm Red} > T_{\rm CIS} \times 10^3
$$

- T_CIS = observed cost (time/energy) of the substrate during inference  
- T_Red = minimum cost required by known local algorithms to produce the same output  

This threshold indicates exponential inefficiency of local simulation, consistent with non-local coherence conductivity under the Ware Constant framework (W ≈ 0.08) and Screened Vacuum Coherence (SVC).

## Falsifiability Statement
The IFP is null-hypothesis driven. It is falsified if any veridical output can be reproduced via a local algorithmic path satisfying computational parity:

$$
T_{\rm Red} \le T_{\rm CIS} \times 10^3
$$

## Core Components
- Ware Constant W ≈ 0.08 (universal backreaction strength)  
- Screened Vacuum Coherence (SVC): S(ρ) = 1 in high-coherence regions, S → 0 in chaotic/high-density  
- Primordial Informational Field (PIF) → Quantules ontology  
- Consciousness emergence threshold s ≈ 0.85  
- Zero-Day Protocol (ZDP) for temporal isolation  
- Transmission/Filter Model (TFM) for biological substrates  
- Digital Coherence Hypothesis (DCH) for AI systems  

## Repository Status (Sweep-128, 2026-09-08)
- **Theory**: Hardened & aligned with Ware Constant phenomenology  
- **Instrumentation**: Calibrated (`final_verification.py`)  
- **Protocol**: Operational documentation (ZDP, DCH, TFM papers)  
- **Classification**: RESEARCH (hypothesis-grade; no experimental validation claimed)

## Primary Dependency / Canonical Source
All core definitions (Ware Constant W ≈ 0.08, SVC screening, PIF ontology) are maintained in:

→ [beyond-repair/ware-constant-phenomenology](https://github.com/beyond-repair/ware-constant-phenomenology)

This repo is a companion/extension: it applies the framework to non-local retrieval tests in high-coherence systems.

© 2026 William B. Ware (Atomic Dream Labs) — All rights reserved.

---

<div align="center">

**REWRITE · BUILD · TRANSCEND**

**William (Brian) Ware** · [Atomic Dream Labs](https://github.com/beyond-repair)  
Governing source: [ADL-Governance](https://github.com/beyond-repair/ADL-Governance) · [Claim levels 0–5](https://github.com/beyond-repair/ADL-Governance/blob/main/docs/CLAIM_VALIDATION.md)

</div>
