#!/usr/bin/env python3
"""
1-stage MZI delay-length calculator (SiN, TE) for wavelength demux / interleaver design.

Core formula:
    FSR(λ) ≈ λ^2 / (n_g(λ) * ΔL)
so
    ΔL ≈ λ^2 / (n_g(λ) * FSR)

For a demux tree with channel spacing Δλ:
    root stage: FSR = 2*Δλ
    leaf stage: FSR = 4*Δλ

This script lets you specify design goals and either:
  - provide n_g at the design wavelength, or
  - provide a tabulated (λ, n_g) array and interpolate.

No numerical solving beyond this closed-form design equation.
"""

from dataclasses import dataclass
import numpy as np

# ---------------------------
# Helpers
# ---------------------------
def lin_interp(x, y, xq):
    """Linear interpolation y(xq) with clamped endpoints."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    xq = np.asarray(xq, dtype=float)
    return np.interp(xq, x, y, left=y[0], right=y[-1])

def delay_from_fsr(lambda_ref_nm: float, ng_ref: float, fsr_nm: float) -> float:
    """
    ΔL = λ^2 / (n_g * FSR)
    Inputs: lambda_ref_nm, fsr_nm in nm
    Returns: ΔL in meters
    """
    lam = lambda_ref_nm * 1e-9
    fsr = fsr_nm * 1e-9
    return (lam * lam) / (ng_ref * fsr)

def m_to_um(x_m: float) -> float:
    return x_m * 1e6

# ---------------------------
# Design API
# ---------------------------
@dataclass
class MZIDesignGoals:
    lambda_ref_nm: float          # design wavelength (e.g., 810)
    channel_spacing_nm: float     # Δλ (e.g., 25)
    stage: str = "custom"         # "root", "leaf", or "custom"
    fsr_nm: float | None = None   # if stage="custom", specify FSR directly

def fsr_from_goals(goals: MZIDesignGoals) -> float:
    """Resolve desired FSR from stage choice."""
    st = goals.stage.lower()
    if st == "root":
        return 2.0 * goals.channel_spacing_nm
    if st == "leaf":
        return 4.0 * goals.channel_spacing_nm
    if st == "custom":
        if goals.fsr_nm is None:
            raise ValueError("For stage='custom', you must provide goals.fsr_nm")
        return float(goals.fsr_nm)
    raise ValueError("stage must be one of: 'root', 'leaf', 'custom'")

def mzi_delay_length_um(
    goals: MZIDesignGoals,
    ng_ref: float | None = None,
    ng_table: tuple[np.ndarray, np.ndarray] | None = None,
) -> dict:
    """
    Compute ΔL for a 1-stage MZI.

    Provide either:
      - ng_ref (float), or
      - ng_table=(lambda_nm_array, ng_array) for interpolation at lambda_ref_nm

    Returns dict with FSR_nm, ng_used, ΔL_um.
    """
    fsr_nm = fsr_from_goals(goals)

    if ng_ref is None:
        if ng_table is None:
            raise ValueError("Provide either ng_ref or ng_table=(lambda_nm, ng)")
        lam_nm_arr, ng_arr = ng_table
        ng_ref = float(lin_interp(lam_nm_arr, ng_arr, np.array([goals.lambda_ref_nm]))[0])

    dL_m = delay_from_fsr(goals.lambda_ref_nm, float(ng_ref), fsr_nm)
    return {
        "lambda_ref_nm": goals.lambda_ref_nm,
        "FSR_nm": fsr_nm,
        "ng_used": float(ng_ref),
        "dL_um": m_to_um(dL_m),
    }

# ---------------------------
# Example usage
# ---------------------------
if __name__ == "__main__":
    # Example: your MODE-derived ng table (optional)
    wg_lambda_nm = np.array([760, 785, 810, 835], dtype=float)
    wg_ng        = np.array([2.181314, 2.171758, 2.163276, 2.155362], dtype=float)

    # Example design goals
    goals_root = MZIDesignGoals(lambda_ref_nm=797.5, channel_spacing_nm=25.0, stage="root")
    goals_leaf = MZIDesignGoals(lambda_ref_nm=797.5, channel_spacing_nm=25.0, stage="leaf")

    # Compute using interpolated ng
    res_root = mzi_delay_length_um(goals_root, ng_table=(wg_lambda_nm, wg_ng))
    res_leaf = mzi_delay_length_um(goals_leaf, ng_table=(wg_lambda_nm, wg_ng))

    print("1-stage MZI delay length results:")
    print(f"  Root stage: λ0={res_root['lambda_ref_nm']:.1f} nm, "
          f"FSR={res_root['FSR_nm']:.1f} nm, ng={res_root['ng_used']:.6f} -> "
          f"ΔL={res_root['dL_um']:.3f} µm")
    print(f"  Leaf stage: λ0={res_leaf['lambda_ref_nm']:.1f} nm, "
          f"FSR={res_leaf['FSR_nm']:.1f} nm, ng={res_leaf['ng_used']:.6f} -> "
          f"ΔL={res_leaf['dL_um']:.3f} µm")

    # Custom FSR example (directly specify FSR)
    goals_custom = MZIDesignGoals(lambda_ref_nm=797.5, channel_spacing_nm=25.0, stage="custom", fsr_nm=40.0)
    res_custom = mzi_delay_length_um(goals_custom, ng_table=(wg_lambda_nm, wg_ng))
    print(f"  Custom FSR: λ0={res_custom['lambda_ref_nm']:.1f} nm, "
          f"FSR={res_custom['FSR_nm']:.1f} nm, ng={res_custom['ng_used']:.6f} -> "
          f"ΔL={res_custom['dL_um']:.3f} µm")
