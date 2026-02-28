#!/usr/bin/env python3
"""
Self-Duality Analysis with paper02 Integration.

Usage:
    python run_sd_analysis.py --input-csv output/dppu_scan_S3_FULL.csv
    python run_sd_analysis.py --input-csv output/scan.csv --theta 0.0
"""
import argparse
import csv
import dataclasses
import os
import sys
import warnings
from datetime import datetime
sys.path.insert(0, str(__file__).rsplit('scripts', 1)[0])

from dppu.topology import S3S1Engine, T3S1Engine, Nil3S1Engine
from dppu.torsion import Mode, NyVariant
from dppu.curvature import SDExtensionMixin, CurvatureSDDiagnostics
from dppu.scanning import Phase1ResultsLoader, SDDiagnosticsWithPhase1


def main():
    parser = argparse.ArgumentParser(
        description="DPPUv2 Self-Duality Analysis with paper02 Integration"
    )

    parser.add_argument('--input-csv', required=True,
                        help='Path to scan CSV file')
    parser.add_argument('--theta', type=float, default=0.0,
                        help='Fixed theta (NY coupling) value (default: 0.0)')
    parser.add_argument('--topology', default='S3',
                        choices=['S3', 'T3', 'Nil3'],
                        help='Topology to analyze (default: S3)')
    parser.add_argument('--mode', default='MX',
                        choices=['AX', 'VT', 'MX'],
                        help='Torsion mode (default: MX)')
    parser.add_argument('--ny-variant', default='FULL',
                        choices=['TT', 'REE', 'FULL'],
                        help='Nieh-Yan variant (default: FULL)')

    parser.add_argument('--eta-range', nargs=3, type=float, default=[-5.0, 3.0, 50],
                        metavar=('MIN', 'MAX', 'POINTS'))
    parser.add_argument('--V-range', nargs=3, type=float, default=[0.5, 5.0, 50],
                        metavar=('MIN', 'MAX', 'POINTS'))

    parser.add_argument('--eps-sd', type=float, default=1e-6,
                        help='SD threshold (default: 1e-6)')
    parser.add_argument('--eps-R', type=float, default=1e-8,
                        help='Curvature norm threshold (default: 1e-8)')
    parser.add_argument('--quiet', action='store_true',
                        help='Suppress progress output')
    parser.add_argument('--output-dir', default='output',
                        help='Output directory (default: output)')

    args = parser.parse_args()

    print("=" * 60)
    print("DPPUv2 Self-Duality Analysis")
    print("=" * 60)
    print()

    # Load CSV results
    print(f"Loading CSV data: {args.input_csv}")
    loader = Phase1ResultsLoader.from_csv(args.input_csv, theta_fixed=args.theta)
    summary = loader.summary()
    print(f"  Total points: {summary['total_points']}")
    print(f"  Stable points: {summary['stable_points']}")
    print(f"  eta bounds: {loader.eta_bounds}")
    print(f"  V bounds: {loader.V_bounds}")
    print()

    # Create engine
    engine_map = {'S3': S3S1Engine, 'T3': T3S1Engine, 'Nil3': Nil3S1Engine}
    EngineClass = engine_map[args.topology]

    mode = Mode[args.mode]
    ny_variant = NyVariant[args.ny_variant]

    print(f"Building {args.topology}xS1 engine ({args.mode}, {args.ny_variant})...")
    engine = EngineClass(mode, ny_variant)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        engine.run()
    SDExtensionMixin.attach_to(engine)
    print("Engine ready.")
    print()

    # Create SD diagnostics
    sd_diag = SDDiagnosticsWithPhase1(engine, phase1_loader=loader)

    # Run scan
    print("Scanning (eta, V) plane at r*...")
    eta_range = tuple(args.eta_range[:2]) + (int(args.eta_range[2]),)
    V_range = tuple(args.V_range[:2]) + (int(args.V_range[2]),)

    results = sd_diag.scan_with_phase1_rstar(
        eta_range=eta_range,
        V_range=V_range,
        theta_NY=args.theta,
        eps_sd=args.eps_sd,
        eps_R=args.eps_R,
        verbose=not args.quiet
    )

    # Report
    print()
    print("=" * 60)
    print("Results")
    print("=" * 60)
    print(f"Total evaluated: {len(results['results'])}")
    print(f"SD curve points: {len(results['sd_curve'])}")
    print(f"ASD curve points: {len(results['asd_curve'])}")
    print(f"Type I + SD: {len(results['type_I_sd_intersection'])}")
    print(f"Type II + SD: {len(results['type_II_sd_intersection'])}")

    if results['sd_curve']:
        print()
        print("Sample SD points (eta, V):")
        for eta, V in results['sd_curve'][:5]:
            print(f"  ({eta:.3f}, {V:.3f})")
        if len(results['sd_curve']) > 5:
            print(f"  ... and {len(results['sd_curve']) - 5} more")

    # Save CSV
    os.makedirs(args.output_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    csv_path = os.path.join(args.output_dir, f'run_sd_analysis_{timestamp}.csv')
    scan_results = results.get('results', [])
    if scan_results:
        rows = [dataclasses.asdict(r) for r in scan_results]
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
        print(f"\nResults saved to: {csv_path}")


if __name__ == "__main__":
    main()
