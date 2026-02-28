#!/usr/bin/env python3
"""
Pontryagin Diagnostic for SD Analysis.

Purpose: Determine whether sd_residual/||R|| = sqrt(2) is
  (A) a physical result (P = <R, *R> = 0 due to torsion structure), or
  (B) an implementation bug (norm/Hodge-dual/flatten inconsistency).

For each topology, evaluates 3 representative points:
  1. Small curvature (||R|| near eps_R)
  2. Medium curvature
  3. Large curvature

Measures: E, P, p, R+/R- norms, cross-check deltas.

Usage:
    python run_pontryagin_diagnostic.py
    python run_pontryagin_diagnostic.py --phase1-dir /path/to/csvs --theta 0.5
"""
import argparse
import csv
import os
import sys
import time
import warnings
from datetime import datetime
from pathlib import Path
sys.path.insert(0, str(__file__).rsplit('scripts', 1)[0])

import numpy as np

from dppu.topology import S3S1Engine, T3S1Engine, Nil3S1Engine
from dppu.torsion import Mode, NyVariant
from dppu.curvature import SDExtensionMixin, CurvatureSDDiagnostics
from dppu.scanning import Phase1ResultsLoader


def print_diagnostic(label: str, result: dict):
    """Print a single point's diagnostic in readable format."""
    tiny = 1e-30
    E = result['E_RR']
    P = result['P_RstarR']
    p = result['p_P_over_E']

    print(f"  --- {label} ---")
    print(f"  ||R||          = {result['curvature_norm']:.6e}")
    print(f"  E = <R,R>      = {E:.6e}")
    print(f"  P = <R,*R>     = {P:.6e}")
    print(f"  p = P/E        = {p:.6e}")
    print(f"  R+_norm2       = {result['Rplus_norm2']:.6e}  "
          f"(frac = {result['Rplus_frac']:.8f})")
    print(f"  R-_norm2       = {result['Rminus_norm2']:.6e}  "
          f"(frac = {result['Rminus_frac']:.8f})")

    # Non-negativity check
    if result['Rplus_norm2'] < -tiny or result['Rminus_norm2'] < -tiny:
        print(f"  *** WARNING: R+_norm2 or R-_norm2 is NEGATIVE! ***")

    # Cross-checks
    print(f"  SD  cross-check: numeric={result['sd_residual2_numeric']:.6e}  "
          f"formula={result['sd_residual2_formula']:.6e}  "
          f"delta={result['sd_residual2_delta']:.2e}")
    print(f"  ASD cross-check: numeric={result['asd_residual2_numeric']:.6e}  "
          f"formula={result['asd_residual2_formula']:.6e}  "
          f"delta={result['asd_residual2_delta']:.2e}")

    # SD/R ratio
    norm = result['curvature_norm']
    if norm > 1e-10:
        sd_ratio = result['sd_residual'] / norm
        asd_ratio = result['asd_residual'] / norm
        print(f"  SD/||R||       = {sd_ratio:.8f}  (sqrt(2) = {np.sqrt(2):.8f})")
        print(f"  ASD/||R||      = {asd_ratio:.8f}")
    print()


def run_topology_diagnostic(topo_name, engine_class, csv_path, theta_fixed,
                            extra_params=None):
    """Run 3-point diagnostic for one topology."""
    print("=" * 70)
    print(f"Topology: {topo_name}")
    print("=" * 70)
    print()

    # Load Phase 1 data
    if not csv_path.exists():
        print(f"  [SKIP] Phase 1 data not found: {csv_path}")
        print()
        return None

    # Extract topology key (e.g. "S3xS1" -> "S3") for combined-CSV filtering
    topo_key = topo_name.replace('xS1', '')
    try:
        loader = Phase1ResultsLoader.from_csv(
            csv_path, theta_fixed=theta_fixed, topology=topo_key
        )
    except ValueError as e:
        print(f"  [SKIP] {e}")
        print()
        return None
    summary = loader.summary()
    print(f"  Phase 1: {summary['stable_points']} stable / "
          f"{summary['total_points']} total points")
    print(f"  Bounds: eta in {loader.eta_bounds}, V in {loader.V_bounds}")
    print()

    # Run engine
    print(f"  Running {topo_name} engine (MX, FULL)...")
    t0 = time.time()
    engine = engine_class(Mode.MX, NyVariant.FULL)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        engine.run()
    SDExtensionMixin.attach_to(engine)
    print(f"  Engine ready in {time.time()-t0:.1f}s")
    print()

    diag = CurvatureSDDiagnostics(engine)

    # Build candidate points within stable bounds
    eta_arr = np.linspace(loader.eta_bounds[0] + 0.2, loader.eta_bounds[1] - 0.2, 8)
    V_arr = np.linspace(loader.V_bounds[0] + 0.2, loader.V_bounds[1] - 0.2, 8)

    candidates = []
    for eta_val in eta_arr:
        for V_val in V_arr:
            r_star = loader.get_r_star(V_val, eta_val, warn_extrapolation=False)
            if r_star is None or r_star <= 0:
                continue
            params = {
                'r': r_star, 'L': 1.0, 'eta': eta_val, 'V': V_val,
                'kappa': 1.0, 'theta_NY': theta_fixed
            }
            if extra_params:
                params.update(extra_params)
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", RuntimeWarning)
                    R = engine.get_R_ab_cd_numerical(params)
                norm = np.linalg.norm(R)
                if norm > 1e-15:
                    candidates.append((norm, eta_val, V_val, r_star))
            except Exception:
                continue

    if len(candidates) < 3:
        print(f"  [WARN] Only {len(candidates)} valid points found")
        if len(candidates) == 0:
            print()
            return None

    # Sort by curvature norm
    candidates.sort(key=lambda x: x[0])

    # Pick small, medium, large
    indices = [0, len(candidates) // 2, -1]
    labels = ["Small ||R||", "Medium ||R||", "Large ||R||"]
    selected = [candidates[i] for i in indices]

    results = []
    for (norm, eta_val, V_val, r_star), label in zip(selected, labels):
        params = {
            'r': r_star, 'L': 1.0, 'eta': eta_val, 'V': V_val,
            'kappa': 1.0, 'theta_NY': theta_fixed
        }
        if extra_params:
            params.update(extra_params)

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", RuntimeWarning)
            result = diag.evaluate_sd_status(params)

        full_label = (f"{label}: eta={eta_val:+.2f}, V={V_val:.2f}, "
                      f"r*={r_star:.4f}")
        print_diagnostic(full_label, result)
        results.append(result)

    # --- Hodge dual involution check (*^2 = id) ---
    print("  --- Hodge dual involution check (*^2 = id) ---")
    norm, eta_val, V_val, r_star = selected[1]  # Use medium point
    params = {
        'r': r_star, 'L': 1.0, 'eta': eta_val, 'V': V_val,
        'kappa': 1.0, 'theta_NY': theta_fixed
    }
    if extra_params:
        params.update(extra_params)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        R = engine.get_R_ab_cd_numerical(params)
    R_star = diag.compute_hodge_dual(R)
    R_star_star = diag.compute_hodge_dual(R_star)
    involution_err = np.linalg.norm(R_star_star - R) / max(np.linalg.norm(R), 1e-30)
    print(f"  ||**R - R|| / ||R|| = {involution_err:.2e}")
    if involution_err < 1e-10:
        print(f"  [OK] *^2 = id verified")
    else:
        print(f"  *** WARNING: *^2 != id (error = {involution_err:.2e}) ***")
    print()

    # --- Antisymmetry check of R^{ab}_{cd} ---
    print("  --- Antisymmetry check ---")
    max_ab_err = 0.0
    max_cd_err = 0.0
    for a in range(4):
        for b in range(4):
            for c in range(4):
                for d in range(4):
                    ab_err = abs(R[a, b, c, d] + R[b, a, c, d])
                    cd_err = abs(R[a, b, c, d] + R[a, b, d, c])
                    max_ab_err = max(max_ab_err, ab_err)
                    max_cd_err = max(max_cd_err, cd_err)
    R_max = np.max(np.abs(R))
    print(f"  max |R^{{ab}}_{{cd}} + R^{{ba}}_{{cd}}| = {max_ab_err:.2e}  "
          f"(rel: {max_ab_err/max(R_max,1e-30):.2e})")
    print(f"  max |R^{{ab}}_{{cd}} + R^{{ab}}_{{dc}}| = {max_cd_err:.2e}  "
          f"(rel: {max_cd_err/max(R_max,1e-30):.2e})")
    if max_ab_err / max(R_max, 1e-30) < 1e-10:
        print(f"  [OK] (ab) antisymmetry verified")
    else:
        print(f"  *** WARNING: (ab) antisymmetry broken ***")
    if max_cd_err / max(R_max, 1e-30) < 1e-10:
        print(f"  [OK] (cd) antisymmetry verified")
    else:
        print(f"  *** WARNING: (cd) antisymmetry broken ***")
    print()

    # --- Summary for this topology ---
    print(f"  === {topo_name} Summary ===")
    all_p = [r['p_P_over_E'] for r in results]
    all_sd_delta = [r['sd_residual2_delta'] for r in results]
    all_asd_delta = [r['asd_residual2_delta'] for r in results]
    all_Rp_frac = [r['Rplus_frac'] for r in results]
    all_Rm_frac = [r['Rminus_frac'] for r in results]

    max_p = max(abs(x) for x in all_p)
    max_sd_d = max(all_sd_delta)
    max_asd_d = max(all_asd_delta)

    print(f"  max |p| = {max_p:.2e}")
    print(f"  max sd_delta = {max_sd_d:.2e}")
    print(f"  max asd_delta = {max_asd_d:.2e}")
    print(f"  R+_frac range: [{min(all_Rp_frac):.6f}, {max(all_Rp_frac):.6f}]")
    print(f"  R-_frac range: [{min(all_Rm_frac):.6f}, {max(all_Rm_frac):.6f}]")

    if max_p < 1e-8 and max_sd_d < 1e-8 and max_asd_d < 1e-8:
        print(f"  >>> Pattern A: P~0 is PHYSICAL (cross-checks pass)")
    elif max_sd_d > 1e-3 or max_asd_d > 1e-3:
        print(f"  >>> Pattern B: Implementation INCONSISTENCY detected")
    else:
        print(f"  >>> Intermediate: further investigation needed")
    print()

    return results


def main():
    parser = argparse.ArgumentParser(
        description="DPPUv2 Pontryagin Diagnostic",
        epilog="Reference: 20260204-01 instruction document"
    )
    parser.add_argument('--input-dir', type=Path, required=True,
                        help='Directory containing input CSV files')
    parser.add_argument('--s3-csv', type=str, default=None,
                        help='S3 CSV filename (default: auto-detect dppu_scan_S3_FULL_*.csv)')
    parser.add_argument('--t3-csv', type=str, default=None,
                        help='T3 CSV filename (default: auto-detect dppu_scan_T3_FULL_*.csv)')
    parser.add_argument('--nil3-csv', type=str, default=None,
                        help='Nil3 CSV filename (default: auto-detect dppu_scan_Nil3_FULL_*.csv)')
    parser.add_argument('--theta', type=float, default=1.0,
                        help='Fixed theta (NY coupling) value (default: 1.0)')
    parser.add_argument('--topologies', nargs='+', default=['S3', 'T3', 'Nil3'],
                        choices=['S3', 'T3', 'Nil3'],
                        help='Topologies to analyze (default: all)')
    parser.add_argument('--output-dir', default='output',
                        help='Output directory (default: output)')

    args = parser.parse_args()

    print()
    print("#" * 70)
    print("# DPPUv2 Pontryagin Diagnostic")
    print("# Ref: 20260204-01 instruction document")
    print("#" * 70)
    print()

    input_dir = args.input_dir
    if not input_dir.exists():
        print(f"ERROR: Input directory not found: {input_dir}")
        return 1

    def resolve_csv(topo_key, cli_arg, pattern_prefix):
        """Resolve CSV path: use CLI arg if given, else glob for pattern.

        Search order:
          1. CLI-specified filename
          2. Topology-specific file: {pattern_prefix}*.csv  (e.g. dppu_scan_S3_FULL_*)
          3. Combined parameter scan file: run_parameter_scan_*.csv
          4. Fallback path (will show SKIP)
        """
        if cli_arg:
            return input_dir / cli_arg
        import glob
        candidates = sorted(glob.glob(str(input_dir / f"{pattern_prefix}*.csv")))
        if candidates:
            return Path(candidates[-1])  # latest by name
        # Fall back to combined parameter scan output
        combined = sorted(glob.glob(str(input_dir / "run_parameter_scan_*.csv")))
        if combined:
            return Path(combined[-1])
        return input_dir / f"{pattern_prefix}.csv"  # fallback (will show SKIP)

    csv_overrides = {
        'S3': args.s3_csv,
        'T3': args.t3_csv,
        'Nil3': args.nil3_csv,
    }

    # Topology configurations
    topo_configs = {
        'S3': (S3S1Engine, "dppu_scan_S3_FULL_", {}),
        'T3': (T3S1Engine, "dppu_scan_T3_FULL_",
               {'R1': 1.0, 'R2': 1.0, 'R3': 1.0}),
        'Nil3': (Nil3S1Engine, "dppu_scan_Nil3_FULL_",
                 {'R': 1.0}),
    }

    all_results = {}

    for topo in args.topologies:
        engine_class, csv_prefix, extra_params = topo_configs[topo]
        csv_path = resolve_csv(topo, csv_overrides[topo], csv_prefix)
        topo_name = f"{topo}xS1"

        all_results[topo_name] = run_topology_diagnostic(
            topo_name, engine_class, csv_path, args.theta, extra_params
        )

    # --- Final Verdict ---
    print()
    print("#" * 70)
    print("# FINAL VERDICT")
    print("#" * 70)
    print()

    verdict_rows = []
    for topo, results in all_results.items():
        if results is None:
            print(f"  {topo}: SKIPPED (no data)")
            verdict_rows.append({'topology': topo, 'max_p': None, 'max_sd_delta': None,
                                 'max_asd_delta': None, 'pattern': 'SKIPPED'})
            continue
        max_p = max(abs(r['p_P_over_E']) for r in results)
        max_sd_delta = max(r['sd_residual2_delta'] for r in results)
        max_asd_delta = max(r['asd_residual2_delta'] for r in results)
        max_delta = max(max_sd_delta, max_asd_delta)
        status = "A (physical)" if max_p < 1e-8 and max_delta < 1e-8 else "B (bug?)"
        print(f"  {topo:10s}: max|p|={max_p:.2e}, max_delta={max_delta:.2e}  "
              f"=> Pattern {status}")
        verdict_rows.append({'topology': topo, 'max_p': max_p,
                             'max_sd_delta': max_sd_delta, 'max_asd_delta': max_asd_delta,
                             'pattern': status})

    # Save verdict CSV
    os.makedirs(args.output_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    csv_path = os.path.join(args.output_dir, f'run_pontryagin_diagnostic_{timestamp}.csv')
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['topology', 'max_p', 'max_sd_delta',
                                               'max_asd_delta', 'pattern'])
        writer.writeheader()
        writer.writerows(verdict_rows)
    print(f"\nVerdict saved to: {csv_path}")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
