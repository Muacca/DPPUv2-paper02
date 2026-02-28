#!/usr/bin/env python3
"""
P = <R, *R> scan across different torsion modes and Nieh-Yan variants.

Purpose: Identify which structural component kills the Pontryagin inner product.

Combinations tested:
  Control:      MX  + FULL (known P=0)
  Direction 1:  AX  + FULL, VT  + FULL  (change torsion mode)
  Direction 2:  MX  + TT,   MX  + REE   (change NY variant)

For each combination x each topology (S3xS1, T3xS1, Nil3xS1):
  Scan over parameter grid, compute P = <R, *R> at each point.

Usage:
    python run_mode_ny_scan.py
    python run_mode_ny_scan.py --topologies S3 T3 --theta 0.5
"""
import argparse
import csv
import os
import sys
import time
import warnings
from datetime import datetime
sys.path.insert(0, str(__file__).rsplit('scripts', 1)[0])

import numpy as np

from dppu.topology import S3S1Engine, T3S1Engine, Nil3S1Engine
from dppu.torsion import Mode, NyVariant
from dppu.curvature import SDExtensionMixin, CurvatureSDDiagnostics


# ============================================================
# Default Configuration
# ============================================================

DEFAULT_THETA_NY = 1.0
L_VAL = 1.0
KAPPA_VAL = 1.0

# Parameter grids
R_VALUES = [0.3, 0.7, 1.0, 2.0, 4.0]
ETA_VALUES = [-3.0, -1.0, 0.0, 1.0, 3.0]
V_VALUES = [0.3, 1.0, 2.0, 3.0, 5.0]

# For MX modes: use fewer r values to keep scan manageable
MX_R_VALUES = [0.5, 1.0, 2.0]


# ============================================================
# Core diagnostic function
# ============================================================

def compute_pontryagin_at_point(diag, params):
    """Compute P = <R, *R> and related quantities at a single point.

    Returns dict with E, P, p, sd_ratio, or None on failure.
    """
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            result = diag.evaluate_sd_status(params)

        E = result['E_RR']
        P = result['P_RstarR']
        p = result['p_P_over_E']
        norm = result['curvature_norm']

        if norm < 1e-15:
            return None  # Trivial curvature

        sd_ratio = result['sd_residual'] / norm

        return {
            'E': E,
            'P': P,
            'p': p,
            'norm': norm,
            'sd_ratio': sd_ratio,
            'Rplus_frac': result['Rplus_frac'],
            'Rminus_frac': result['Rminus_frac'],
        }
    except Exception:
        return None


def scan_combination(engine_class, mode, ny_variant, topo_name,
                     theta_NY, extra_params=None):
    """Run P scan for one (Mode, NyVariant, Topology) combination.

    Returns list of result dicts.
    """
    # Build engine
    t0 = time.time()
    engine = engine_class(mode, ny_variant)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        engine.run()
    SDExtensionMixin.attach_to(engine)
    dt = time.time() - t0

    diag = CurvatureSDDiagnostics(engine)

    mode_name = mode.value
    ny_name = ny_variant.value
    print(f"    Engine ready ({dt:.1f}s): {topo_name} / {mode_name}+{ny_name}")

    # Build parameter grid based on mode
    grid_points = []

    if mode_name == "AX":
        # AX mode: scan r x eta (V internally zero)
        for r_val in R_VALUES:
            for eta_val in ETA_VALUES:
                params = {
                    'r': r_val, 'L': L_VAL, 'eta': eta_val,
                    'kappa': KAPPA_VAL, 'theta_NY': theta_NY
                }
                if extra_params:
                    params.update(extra_params)
                grid_points.append(params)

    elif mode_name == "VT":
        # VT mode: scan r x V (eta internally zero)
        for r_val in R_VALUES:
            for V_val in V_VALUES:
                params = {
                    'r': r_val, 'L': L_VAL, 'V': V_val,
                    'kappa': KAPPA_VAL, 'theta_NY': theta_NY
                }
                if extra_params:
                    params.update(extra_params)
                grid_points.append(params)

    else:
        # MX mode: scan eta x V at a few r values
        for r_val in MX_R_VALUES:
            for eta_val in ETA_VALUES:
                for V_val in V_VALUES:
                    params = {
                        'r': r_val, 'L': L_VAL, 'eta': eta_val, 'V': V_val,
                        'kappa': KAPPA_VAL, 'theta_NY': theta_NY
                    }
                    if extra_params:
                        params.update(extra_params)
                    grid_points.append(params)

    # Evaluate at each grid point
    results = []
    for params in grid_points:
        res = compute_pontryagin_at_point(diag, params)
        if res is not None:
            results.append(res)

    return results


def print_scan_summary(label, results):
    """Print summary statistics for one scan."""
    if not results:
        print(f"    {label}: NO VALID POINTS")
        return None

    n = len(results)
    P_vals = [r['P'] for r in results]
    p_vals = [r['p'] for r in results]
    E_vals = [r['E'] for r in results]
    sd_ratios = [r['sd_ratio'] for r in results]

    abs_P = [abs(x) for x in P_vals]
    abs_p = [abs(x) for x in p_vals]

    max_absP = max(abs_P)
    max_absp = max(abs_p)
    mean_absP = np.mean(abs_P)
    mean_absp = np.mean(abs_p)
    min_sd_ratio = min(sd_ratios)
    max_sd_ratio = max(sd_ratios)

    # Determine P status
    if max_absp < 1e-8:
        p_status = "P = 0 (algebraic)"
    elif max_absp < 1e-3:
        p_status = "P ~ 0 (near-zero)"
    else:
        # Check sign consistency
        P_positive = sum(1 for x in P_vals if x > 1e-8)
        P_negative = sum(1 for x in P_vals if x < -1e-8)
        P_zero = n - P_positive - P_negative
        p_status = f"P != 0 (pos:{P_positive}, neg:{P_negative}, ~0:{P_zero})"

    print(f"    {label}: {n} pts | max|P|={max_absP:.4e} | max|p|={max_absp:.4e} "
          f"| SD/R=[{min_sd_ratio:.4f},{max_sd_ratio:.4f}] | {p_status}")

    return {
        'n_points': n,
        'max_absP': max_absP,
        'max_absp': max_absp,
        'mean_absP': mean_absP,
        'mean_absp': mean_absp,
        'min_sd_ratio': min_sd_ratio,
        'max_sd_ratio': max_sd_ratio,
        'p_status': p_status,
        'P_vals': P_vals,
        'p_vals': p_vals,
        'E_vals': E_vals,
    }


# ============================================================
# Main
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="DPPUv2 Mode/NyVariant Scan: Which structure kills P = <R, *R>?",
        epilog="Reference: Diagnostic Report Section 4.3"
    )
    parser.add_argument('--topologies', nargs='+', default=['S3', 'T3', 'Nil3'],
                        choices=['S3', 'T3', 'Nil3'],
                        help='Topologies to analyze (default: all)')
    parser.add_argument('--theta', type=float, default=DEFAULT_THETA_NY,
                        help=f'Nieh-Yan coupling theta (default: {DEFAULT_THETA_NY})')
    parser.add_argument('--output-dir', default='output',
                        help='Output directory (default: output)')

    args = parser.parse_args()

    print()
    print("#" * 70)
    print("# DPPUv2 Mode/NyVariant Scan: Which structure kills P = <R, *R>?")
    print("# Reference: Diagnostic Report Section 4.3")
    print("#" * 70)
    print()

    # Define combinations to test
    combinations = [
        (Mode.MX,  NyVariant.FULL, "MX+FULL (control)"),
        (Mode.AX,  NyVariant.FULL, "AX+FULL"),
        (Mode.VT,  NyVariant.FULL, "VT+FULL"),
        (Mode.MX,  NyVariant.TT,   "MX+TT"),
        (Mode.MX,  NyVariant.REE,  "MX+REE"),
    ]

    # Define topologies
    topo_configs = {
        'S3': ("S3xS1", S3S1Engine, {}),
        'T3': ("T3xS1", T3S1Engine, {'R1': 1.0, 'R2': 1.0, 'R3': 1.0}),
        'Nil3': ("Nil3xS1", Nil3S1Engine, {'R': 1.0}),
    }

    topologies = [(topo_configs[t][0], topo_configs[t][1], topo_configs[t][2])
                  for t in args.topologies]
    topo_names = [t[0] for t in topologies]

    all_summaries = {}

    for topo_name, engine_class, extra_params in topologies:
        print("=" * 70)
        print(f"Topology: {topo_name}")
        print("=" * 70)
        print()

        for mode, ny_variant, combo_label in combinations:
            try:
                results = scan_combination(
                    engine_class, mode, ny_variant,
                    topo_name, args.theta, extra_params
                )

                summary = print_scan_summary(combo_label, results)
                key = (topo_name, combo_label)
                all_summaries[key] = summary

            except Exception as e:
                print(f"    {combo_label}: ERROR - {e}")
                import traceback
                traceback.print_exc()
                all_summaries[(topo_name, combo_label)] = None

        print()

    # ============================================================
    # Final Summary Table
    # ============================================================
    print()
    print("#" * 70)
    print("# FINAL SUMMARY")
    print("#" * 70)
    print()

    combo_labels = [c[2] for c in combinations]

    # Header
    header = f"{'Combination':<22s}"
    for topo in topo_names:
        header += f" | {topo:>20s}"
    print(header)
    print("-" * len(header))

    for combo_label in combo_labels:
        row = f"{combo_label:<22s}"
        for topo in topo_names:
            s = all_summaries.get((topo, combo_label))
            if s is None:
                row += f" | {'ERROR':>20s}"
            else:
                row += f" | max|p|={s['max_absp']:.2e}"
        print(row)

    print()

    # ============================================================
    # Detailed P statistics per combination
    # ============================================================
    print()
    print("#" * 70)
    print("# DETAILED P STATISTICS (across all topologies)")
    print("#" * 70)
    print()

    for combo_label in combo_labels:
        all_P = []
        all_p = []
        all_E = []
        n_total = 0
        for topo in topo_names:
            s = all_summaries.get((topo, combo_label))
            if s is not None:
                all_P.extend(s['P_vals'])
                all_p.extend(s['p_vals'])
                all_E.extend(s['E_vals'])
                n_total += s['n_points']

        if n_total == 0:
            print(f"  {combo_label}: NO DATA")
            continue

        abs_P = [abs(x) for x in all_P]
        abs_p = [abs(x) for x in all_p]

        print(f"  {combo_label}:")
        print(f"    Total points:  {n_total}")
        print(f"    max |P|:       {max(abs_P):.6e}")
        print(f"    mean |P|:      {np.mean(abs_P):.6e}")
        print(f"    max |p|:       {max(abs_p):.6e}")
        print(f"    mean |p|:      {np.mean(abs_p):.6e}")
        print(f"    P range:       [{min(all_P):.6e}, {max(all_P):.6e}]")
        print(f"    E range:       [{min(all_E):.6e}, {max(all_E):.6e}]")

        # Count P sign distribution
        n_pos = sum(1 for x in all_P if x > 1e-8)
        n_neg = sum(1 for x in all_P if x < -1e-8)
        n_zero = n_total - n_pos - n_neg
        print(f"    P sign dist:   pos={n_pos}, neg={n_neg}, ~0={n_zero}")

        if max(abs_p) < 1e-8:
            print(f"    VERDICT: P = 0 (algebraic identity)")
        elif max(abs_p) < 1e-3:
            print(f"    VERDICT: P ~ 0 (numerically small)")
        else:
            print(f"    VERDICT: P != 0 (structure breaks P=0)")
        print()

    # ============================================================
    # Conclusion
    # ============================================================
    print()
    print("#" * 70)
    print("# CONCLUSION: Which structure kills P?")
    print("#" * 70)
    print()

    # Determine which combinations have P=0 and which don't
    p0_combos = []
    pnz_combos = []

    for combo_label in combo_labels:
        max_p_all = 0.0
        has_data = False
        for topo in topo_names:
            s = all_summaries.get((topo, combo_label))
            if s is not None:
                has_data = True
                max_p_all = max(max_p_all, s['max_absp'])

        if not has_data:
            continue

        if max_p_all < 1e-8:
            p0_combos.append(combo_label)
        else:
            pnz_combos.append(combo_label)

    print("  P = 0 (algebraic):")
    for c in p0_combos:
        print(f"    - {c}")
    if not p0_combos:
        print("    (none)")

    print()
    print("  P != 0 (broken):")
    for c in pnz_combos:
        print(f"    - {c}")
    if not pnz_combos:
        print("    (none)")

    print()

    # Interpretation
    if "AX+FULL" in pnz_combos and "VT+FULL" in pnz_combos:
        print("  Interpretation: Both AX and VT alone break P=0.")
        print("  The MX combination has a cancellation between axial and vector contributions.")
    elif "AX+FULL" in pnz_combos:
        print("  Interpretation: Axial-only (AX) torsion breaks P=0.")
        print("  Vector torsion preserves P=0; the combination (MX) has P=0 from vector.")
    elif "VT+FULL" in pnz_combos:
        print("  Interpretation: Vector-only (VT) torsion breaks P=0.")
        print("  Axial torsion preserves P=0; the combination (MX) has P=0 from axial.")
    elif "AX+FULL" in p0_combos and "VT+FULL" in p0_combos:
        print("  Interpretation: Both AX and VT individually give P=0.")
        print("  P=0 is a property of each torsion component, not just their combination.")

    print()

    if "MX+TT" in pnz_combos and "MX+REE" in pnz_combos:
        print("  NY variant effect: Both TT-only and REE-only break P=0.")
        print("  FULL = TT - REE has a cancellation that restores P=0.")
    elif "MX+TT" in pnz_combos:
        print("  NY variant effect: TT-only breaks P=0; REE preserves it.")
    elif "MX+REE" in pnz_combos:
        print("  NY variant effect: REE-only breaks P=0; TT preserves it.")
    elif "MX+TT" in p0_combos and "MX+REE" in p0_combos:
        print("  NY variant effect: Both TT and REE individually give P=0.")
        print("  P=0 is independent of the Nieh-Yan variant.")

    print()

    # Save summary CSV
    os.makedirs(args.output_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    csv_path = os.path.join(args.output_dir, f'run_mode_ny_scan_{timestamp}.csv')
    fieldnames = ['topology', 'combination', 'n_points', 'max_absP', 'max_absp',
                  'mean_absP', 'mean_absp', 'min_sd_ratio', 'max_sd_ratio', 'p_status']
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for (topo, combo), s in all_summaries.items():
            if s is not None:
                writer.writerow({
                    'topology': topo,
                    'combination': combo,
                    'n_points': s['n_points'],
                    'max_absP': s['max_absP'],
                    'max_absp': s['max_absp'],
                    'mean_absP': s['mean_absP'],
                    'mean_absp': s['mean_absp'],
                    'min_sd_ratio': s['min_sd_ratio'],
                    'max_sd_ratio': s['max_sd_ratio'],
                    'p_status': s['p_status'],
                })
    print(f"Summary saved to: {csv_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
