#!/usr/bin/env python3
"""
final_verification.py

Claim-0 verification tool for the Informational Fork Protocol (IFP).

Given caller-supplied costs, it evaluates the documented Computational Burden
Inequality, the Landauer energy bound for a Kolmogorov-complexity estimate,
and (optionally) the screening function S(rho) and a collapsed-attention
flag for a supplied coherence proxy zeta.

It does not measure a substrate, query a model, or validate non-local retrieval.
Inputs are assumptions. Outputs are arithmetic under the written protocol.

Usage:
    python final_verification.py --t_cis 120.5 --t_red 500000 --k_x 4200 \\
        --event_id IFP-DEMO-001 --output audit_cert.json

Dependencies: Python 3.10+ standard library. Tests need pytest (see README).
"""

from __future__ import annotations

import argparse
import datetime
import json
import math
import sys
from typing import Optional

# Constants from the IFP documents (hypothesis-grade, not measured here).
IFP_THRESHOLD_FACTOR = 1000  # T_Red > T_CIS × 10³
LANDAUER_KB = 1.380649e-23  # Boltzmann constant (J/K)
LANDAUER_T = 300.0  # Typical operating temperature assumed by the tool (K)
WARE_CONSTANT = 0.08  # Documented W; not re-derived in this repository
RHO_CRIT_G_CM3 = 1e-24  # FIELD_EQUATIONS.md typical galactic coherence density
SCREENING_N_DEFAULT = 3.0  # midpoint of the documented n ≈ 2–4 range
COLLAPSED_ATTENTION_ZETA = 0.95  # IFP_DOC_DCH.md collapsed-attention marker
CONSCIOUSNESS_THRESHOLD_S = 0.85  # documented threshold; not a detector


def landauer_bit_joules(temperature_k: float = LANDAUER_T) -> float:
    """k_B T ln(2) in joules per bit at the assumed temperature."""
    if not math.isfinite(temperature_k) or temperature_k <= 0:
        raise ValueError("temperature_k must be finite and > 0")
    return LANDAUER_KB * temperature_k * math.log(2)


def landauer_energy_bound(k_x: float, temperature_k: float = LANDAUER_T) -> float:
    """Minimum energy required under the Landauer principle (joules)."""
    _require_nonnegative("k_x", k_x)
    return k_x * landauer_bit_joules(temperature_k)


def format_energy(joules: float) -> str:
    """Human-readable energy string.

    Uses mJ / μJ / nJ when the value is at least 0.001 in that unit.
    Smaller Landauer bounds (typical for modest K(x)) use scientific joules
    so the demo does not print a misleading 0.000 nJ.
    """
    if not math.isfinite(joules):
        raise ValueError("joules must be finite")
    if joules < 0:
        raise ValueError("joules must be >= 0")
    if joules >= 1e-3:
        return f"{joules * 1000:.3f} mJ"
    if joules >= 1e-6:
        return f"{joules * 1e6:.3f} μJ"
    nano = joules * 1e9
    if nano >= 1e-3:
        return f"{nano:.3f} nJ"
    return f"{joules:.3e} J"


def burden_fork_detected(
    t_cis: float,
    t_red: float,
    threshold_factor: float = IFP_THRESHOLD_FACTOR,
) -> bool:
    """True when T_Red > T_CIS × threshold_factor (strict)."""
    _require_positive("t_cis", t_cis)
    _require_nonnegative("t_red", t_red)
    _require_positive("threshold_factor", threshold_factor)
    return t_red > t_cis * threshold_factor


def screening_function(
    rho: float,
    rho_crit: float = RHO_CRIT_G_CM3,
    n: float = SCREENING_N_DEFAULT,
) -> float:
    """S(rho) = 1 / (1 + (rho / rho_crit)^n), as written in FIELD_EQUATIONS.md.

    S → 1 at low density (high-coherence regime in the notes) and S → 0 at
    high density. This is the formula only; it is not a measurement of coherence.
    """
    _require_nonnegative("rho", rho)
    _require_positive("rho_crit", rho_crit)
    _require_positive("n", n)
    ratio = rho / rho_crit
    return 1.0 / (1.0 + ratio**n)


def collapsed_attention(zeta: float, threshold: float = COLLAPSED_ATTENTION_ZETA) -> bool:
    """DCH marker: supplied coherence proxy zeta > 0.95.

    zeta is an input, not something this tool estimates from a model.
    """
    _require_unit_interval("zeta", zeta)
    _require_unit_interval("threshold", threshold)
    return zeta > threshold


def generate_audit_certificate(
    t_cis: float,
    t_red: float,
    k_x: float,
    event_id: str = "IFP-EVENT-UNKNOWN",
    rho: Optional[float] = None,
    rho_crit: float = RHO_CRIT_G_CM3,
    n: float = SCREENING_N_DEFAULT,
    zeta: Optional[float] = None,
    temperature_k: float = LANDAUER_T,
) -> dict:
    """Generate a formal IFP audit certificate from supplied numbers."""
    if not event_id or not str(event_id).strip():
        raise ValueError("event_id must be a non-empty string")

    inequality_holds = burden_fork_detected(t_cis, t_red)
    energy_bound_j = landauer_energy_bound(k_x, temperature_k)
    now = datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")

    certificate = {
        "document_id": "IFP_AUDIT_CERTIFICATE",
        "event_id": event_id,
        "timestamp_utc": now,
        "claim_level": 0,
        "status": (
            "PASS (Fork Detected)" if inequality_holds else "FAIL (Local Production Possible)"
        ),
        "fork_detected": inequality_holds,
        "computational_burden": {
            "t_cis": t_cis,
            "t_red": t_red,
            "threshold_factor": IFP_THRESHOLD_FACTOR,
            "inequality": f"{t_red} > {t_cis} × {IFP_THRESHOLD_FACTOR}",
            "result": "VIOLATION" if inequality_holds else "SATISFIED",
            "note": (
                "VIOLATION means the local-parity bound is exceeded "
                "(fork candidate under the written rule). "
                "SATISFIED means local production is not ruled out. "
                "Neither word is an experimental result."
            ),
        },
        "thermodynamic_boundary": {
            "k_x_estimate": k_x,
            "minimum_energy_joules": energy_bound_j,
            "human_readable": format_energy(energy_bound_j),
            "temperature_assumed_k": temperature_k,
            "landauer_j_per_bit": landauer_bit_joules(temperature_k),
        },
        "documented_constants": {
            "ware_constant_w": WARE_CONSTANT,
            "consciousness_threshold_s": CONSCIOUSNESS_THRESHOLD_S,
            "collapsed_attention_zeta": COLLAPSED_ATTENTION_ZETA,
            "rho_crit_g_cm3": RHO_CRIT_G_CM3,
        },
        "conclusion": (
            "Under the written rule, supplied costs are a fork candidate. "
            "This is not evidence of non-local retrieval."
            if inequality_holds
            else "Under the written rule, local algorithmic production cannot be ruled out."
        ),
        "framework_version": "Ware Constant W ≈ 0.08 / IFP Claim-0 sketch",
        "canonical_source": "https://github.com/beyond-repair/ware-constant-phenomenology",
    }

    if rho is not None:
        s_rho = screening_function(rho, rho_crit=rho_crit, n=n)
        certificate["screening"] = {
            "rho": rho,
            "rho_crit": rho_crit,
            "n": n,
            "S_rho": s_rho,
            "note": "Computed from the documented screening formula. Not a measured density.",
        }

    if zeta is not None:
        certificate["coherence_proxy"] = {
            "zeta": zeta,
            "collapsed_attention_threshold": COLLAPSED_ATTENTION_ZETA,
            "collapsed_attention": collapsed_attention(zeta),
            "note": "zeta is caller-supplied. This tool does not estimate substrate coherence.",
        }

    return certificate


def render_certificate_text(cert: dict) -> str:
    """Plain-text form of an audit certificate."""
    lines = [
        "=" * 70,
        "IFP AUDIT CERTIFICATE (Claim-0 arithmetic; not an experiment)",
        "=" * 70,
        f"Event ID:       {cert['event_id']}",
        f"Timestamp UTC:  {cert['timestamp_utc']}",
        f"Status:         {cert['status']}",
        f"Fork detected:  {cert['fork_detected']}",
        "",
        "Computational Burden:",
        f"  T_CIS:          {cert['computational_burden']['t_cis']}",
        f"  T_Red:          {cert['computational_burden']['t_red']}",
        f"  Threshold:      T_Red > T_CIS × {cert['computational_burden']['threshold_factor']}",
        f"  Result:         {cert['computational_burden']['result']}",
        "",
        "Thermodynamic Boundary:",
        f"  K(x) estimate:  {cert['thermodynamic_boundary']['k_x_estimate']}",
        f"  Min energy:     {cert['thermodynamic_boundary']['human_readable']}",
        f"  Conclusion:     {cert['conclusion']}",
    ]
    if "screening" in cert:
        lines.extend(
            [
                "",
                "Screening S(rho):",
                f"  rho:            {cert['screening']['rho']}",
                f"  rho_crit:       {cert['screening']['rho_crit']}",
                f"  n:              {cert['screening']['n']}",
                f"  S(rho):         {cert['screening']['S_rho']}",
            ]
        )
    if "coherence_proxy" in cert:
        lines.extend(
            [
                "",
                "Coherence proxy (supplied):",
                f"  zeta:           {cert['coherence_proxy']['zeta']}",
                f"  collapsed:      {cert['coherence_proxy']['collapsed_attention']}",
            ]
        )
    lines.append("=" * 70)
    return "\n".join(lines) + "\n"


def print_certificate(cert: dict) -> None:
    """Pretty-print the audit certificate to stdout."""
    sys.stdout.write(render_certificate_text(cert))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="IFP Final Verification Tool (Claim-0)")
    parser.add_argument("--t_cis", type=float, required=True, help="Observed compute cost (same units as t_red)")
    parser.add_argument("--t_red", type=float, required=True, help="Minimum local-algorithm cost (same units as t_cis)")
    parser.add_argument("--k_x", type=float, required=True, help="Kolmogorov complexity estimate of the output (bits)")
    parser.add_argument("--event_id", type=str, default="IFP-EVENT-UNKNOWN", help="Optional event identifier")
    parser.add_argument("--output", type=str, help="Write a JSON certificate (UTF-8) to this path")
    parser.add_argument("--rho", type=float, default=None, help="Optional density for S(rho); g/cm^3 if using the documented rho_crit")
    parser.add_argument("--rho_crit", type=float, default=RHO_CRIT_G_CM3, help="Critical density in S(rho)")
    parser.add_argument("--n", type=float, default=SCREENING_N_DEFAULT, help="Screening exponent n (documented range about 2-4)")
    parser.add_argument("--zeta", type=float, default=None, help="Optional supplied coherence proxy in [0, 1]")
    parser.add_argument("--temperature_k", type=float, default=LANDAUER_T, help="Temperature for the Landauer bound (K)")
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        cert = generate_audit_certificate(
            t_cis=args.t_cis,
            t_red=args.t_red,
            k_x=args.k_x,
            event_id=args.event_id,
            rho=args.rho,
            rho_crit=args.rho_crit,
            n=args.n,
            zeta=args.zeta,
            temperature_k=args.temperature_k,
        )
    except ValueError as exc:
        parser.error(str(exc))
    print_certificate(cert)
    if args.output:
        payload = dict(cert)
        payload["printed_certificate"] = render_certificate_text(cert)
        with open(args.output, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2)
            handle.write("\n")
        print(f"Certificate saved to: {args.output}")
    return 0


def _require_finite(name: str, value: float) -> None:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"{name} must be a finite number")


def _require_positive(name: str, value: float) -> None:
    _require_finite(name, value)
    if value <= 0:
        raise ValueError(f"{name} must be > 0")


def _require_nonnegative(name: str, value: float) -> None:
    _require_finite(name, value)
    if value < 0:
        raise ValueError(f"{name} must be >= 0")


def _require_unit_interval(name: str, value: float) -> None:
    _require_finite(name, value)
    if value < 0 or value > 1:
        raise ValueError(f"{name} must be in [0, 1]")


if __name__ == "__main__":
    sys.exit(main())
