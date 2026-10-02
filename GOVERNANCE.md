# Governance — Informational Fork Protocol (IFP)

**Classification:** RESEARCH  
**Claim level:** 0 (hypothesis / protocol design only)  
**Governing source:** [ADL-Governance](https://github.com/beyond-repair/ADL-Governance)  
**Canonical physics definitions:** [ware-constant-phenomenology](https://github.com/beyond-repair/ware-constant-phenomenology)

## Allowed uses
- Protocol design and documentation of the Informational Fork Protocol (ZDP, DCH, TFM).
- Instrumentation script (`final_verification.py`) for computing Computational Burden Inequality under stated assumptions.
- Companion notes to the Ware Constant framework.

## Forbidden claims
- No claim that non-local informational retrieval has been experimentally demonstrated.
- No claim that T_Red / T_CIS violations have been observed in production systems.
- No claim that the Ware Constant W ≈ 0.08 is empirically measured beyond the derivation in the canonical repository.
- No product, production, or validated physics status.

## CI / Tests
- No GitHub Actions workflow in this repo (token/workflow policy). Verification is local pytest.
- `final_verification.py` runtime is the Python 3.10+ standard library.
- `pip install -e ".[dev]"` then `pytest -q` checks the burden inequality, Landauer bound, screening formula, and CLI. Green tests are not experimental validation.

## Lifecycle
- RESEARCH until experimental validation evidence is supplied and claim level raised under ADL-Governance CLAIM_VALIDATION.md.
- Do not promote to ACTIVE without tests + CI + evidence.

## Sweep lock
- Sweep-128 (2026-09-08): docs lock complete; classification RESEARCH confirmed.
