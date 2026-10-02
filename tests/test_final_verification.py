"""Tests for the Claim-0 IFP audit calculator. No network, no substrate."""

import json
import math
import subprocess
import sys
from pathlib import Path

import pytest

import final_verification as ifp

ROOT = Path(__file__).resolve().parents[1]
DEMO = ["--t_cis", "120.5", "--t_red", "500000", "--k_x", "4200", "--event_id", "IFP-DEMO-001"]


def test_fork_detected_on_documented_demo_numbers():
    cert = ifp.generate_audit_certificate(120.5, 500000, 4200, event_id="IFP-DEMO-001")
    assert cert["fork_detected"] is True
    assert cert["status"].startswith("PASS")
    assert cert["computational_burden"]["result"] == "VIOLATION"
    assert cert["claim_level"] == 0
    assert 500000 > 120.5 * ifp.IFP_THRESHOLD_FACTOR


def test_equality_is_not_a_fork():
    cert = ifp.generate_audit_certificate(1.0, 1000.0, 1.0)
    assert cert["fork_detected"] is False
    assert cert["status"].startswith("FAIL")
    assert cert["computational_burden"]["result"] == "SATISFIED"


def test_just_above_threshold_is_a_fork():
    assert ifp.burden_fork_detected(2.0, 2000.0 + 1e-9) is True
    assert ifp.burden_fork_detected(2.0, 2000.0) is False


def test_landauer_matches_kb_t_ln2():
    k_x = 4200
    expected = k_x * ifp.LANDAUER_KB * ifp.LANDAUER_T * math.log(2)
    got = ifp.landauer_energy_bound(k_x)
    assert got == pytest.approx(expected)
    cert = ifp.generate_audit_certificate(120.5, 500000, k_x)
    assert cert["thermodynamic_boundary"]["minimum_energy_joules"] == pytest.approx(expected)
    readable = cert["thermodynamic_boundary"]["human_readable"]
    assert readable.endswith("J")
    assert "0.000 nJ" not in readable
    assert float(readable.split()[0]) == pytest.approx(expected)


def test_format_energy_units():
    assert ifp.format_energy(1e-3) == "1.000 mJ"
    assert ifp.format_energy(1e-6) == "1.000 μJ"
    assert ifp.format_energy(1e-9) == "1.000 nJ"
    assert ifp.format_energy(0.0) == "0.000e+00 J"


def test_screening_limits_and_midpoint():
    assert ifp.screening_function(0.0) == pytest.approx(1.0)
    assert ifp.screening_function(ifp.RHO_CRIT_G_CM3, n=2) == pytest.approx(0.5)
    assert ifp.screening_function(1e6, rho_crit=1.0, n=4) < 1e-20


def test_low_density_screening_on_certificate():
    cert = ifp.generate_audit_certificate(120.5, 500000, 10, rho=1e-30)
    assert cert["screening"]["S_rho"] == pytest.approx(1.0, abs=1e-12)


def test_collapsed_attention_threshold_is_strict():
    assert ifp.collapsed_attention(0.95) is False
    assert ifp.collapsed_attention(0.9500001) is True
    cert = ifp.generate_audit_certificate(1, 10, 1, zeta=0.97)
    assert cert["coherence_proxy"]["collapsed_attention"] is True
    quiet = ifp.generate_audit_certificate(1, 10, 1, zeta=0.2)
    assert quiet["coherence_proxy"]["collapsed_attention"] is False


def test_rejects_bad_inputs():
    with pytest.raises(ValueError):
        ifp.generate_audit_certificate(0, 10, 1)
    with pytest.raises(ValueError):
        ifp.generate_audit_certificate(-1, 10, 1)
    with pytest.raises(ValueError):
        ifp.generate_audit_certificate(1, -1, 1)
    with pytest.raises(ValueError):
        ifp.generate_audit_certificate(1, 10, -5)
    with pytest.raises(ValueError):
        ifp.generate_audit_certificate(1, 10, 1, event_id="  ")
    with pytest.raises(ValueError):
        ifp.screening_function(-1)
    with pytest.raises(ValueError):
        ifp.collapsed_attention(1.2)
    with pytest.raises(ValueError):
        ifp.generate_audit_certificate(float("nan"), 10, 1)


def test_render_contains_status_and_event():
    cert = ifp.generate_audit_certificate(120.5, 500000, 4200, event_id="IFP-DEMO-001", rho=0.0, zeta=0.99)
    text = ifp.render_certificate_text(cert)
    assert "IFP-DEMO-001" in text
    assert "PASS (Fork Detected)" in text
    assert "S(rho)" in text
    assert "collapsed:" in text


def test_cli_demo_exit_zero_and_json(tmp_path):
    out = tmp_path / "audit_cert.json"
    proc = subprocess.run(
        [sys.executable, str(ROOT / "final_verification.py"), *DEMO, "--rho", "1e-30", "--zeta", "0.97", "--output", str(out)],
        check=False,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr
    assert "PASS (Fork Detected)" in proc.stdout
    assert "Certificate saved to:" in proc.stdout
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["event_id"] == "IFP-DEMO-001"
    assert payload["fork_detected"] is True
    assert payload["screening"]["S_rho"] == pytest.approx(1.0, abs=1e-12)
    assert payload["coherence_proxy"]["collapsed_attention"] is True
    assert "IFP AUDIT CERTIFICATE" in payload["printed_certificate"]


def test_cli_rejects_non_positive_t_cis():
    proc = subprocess.run(
        [sys.executable, str(ROOT / "final_verification.py"), "--t_cis", "0", "--t_red", "1", "--k_x", "1"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 2
    assert "t_cis" in proc.stderr


def test_cli_help_exits_zero():
    proc = subprocess.run(
        [sys.executable, str(ROOT / "final_verification.py"), "--help"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0
    assert "--t_cis" in proc.stdout
