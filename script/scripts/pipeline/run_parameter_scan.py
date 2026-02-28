#!/usr/bin/env python3
"""
CLI wrapper for parameter space scanning.

Usage:
    python run_parameter_scan.py --topologies S3 T3 --ny-variants FULL TT
    python run_parameter_scan.py --V-range 0 5 10 --eta-range -5 5 21
"""
import argparse
import os
import sys
from datetime import datetime
sys.path.insert(0, str(__file__).rsplit('scripts', 1)[0])

from dppu.scanning import run_scan


def main():
    parser = argparse.ArgumentParser(
        description="DPPUv2 Parameter Space Scanner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Scan all topologies and NY variants with default grid
  python run_parameter_scan.py

  # Scan only S3 with FULL variant
  python run_parameter_scan.py --topologies S3 --ny-variants FULL

  # Custom parameter ranges
  python run_parameter_scan.py --V-range 0 10 20 --eta-range -6 6 25
        """
    )

    parser.add_argument(
        '--topologies', nargs='+', default=['S3', 'T3', 'Nil3'],
        choices=['S3', 'T3', 'Nil3'],
        help='Topologies to scan (default: all)'
    )
    parser.add_argument(
        '--ny-variants', nargs='+', default=['FULL', 'TT', 'REE'],
        choices=['FULL', 'TT', 'REE'],
        help='Nieh-Yan variants to scan (default: all)'
    )

    parser.add_argument('--V-range', nargs=3, type=float, default=[0.0, 5.0, 6],
                        metavar=('MIN', 'MAX', 'POINTS'),
                        help='V parameter range (default: 0 5 6)')
    parser.add_argument('--eta-range', nargs=3, type=float, default=[-5.0, 5.0, 11],
                        metavar=('MIN', 'MAX', 'POINTS'),
                        help='eta parameter range (default: -5 5 11)')
    parser.add_argument('--theta-range', nargs=3, type=float, default=[0.0, 5.0, 6],
                        metavar=('MIN', 'MAX', 'POINTS'),
                        help='theta parameter range (default: 0 5 6)')

    parser.add_argument('--output-dir', default='output',
                        help='Output directory for CSV files')
    parser.add_argument('--workers', type=int, default=None,
                        help='Number of parallel workers (default: auto)')

    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_filename = f'run_parameter_scan_{timestamp}.csv'

    results = run_scan(
        V_points=int(args.V_range[2]),
        eta_points=int(args.eta_range[2]),
        theta_points=int(args.theta_range[2]),
        V_min=args.V_range[0],
        V_max=args.V_range[1],
        eta_min=args.eta_range[0],
        eta_max=args.eta_range[1],
        theta_min=args.theta_range[0],
        theta_max=args.theta_range[1],
        topologies=args.topologies,
        ny_variants=args.ny_variants,
        output_dir=args.output_dir,
        output_filename=output_filename,
        n_workers=args.workers
    )

    # Summary
    print()
    print("=" * 50)
    print("Scan Summary")
    print("=" * 50)
    print(f"Total points: {len(results)}")

    type_counts = {}
    for r in results:
        t = r['stability_type']
        type_counts[t] = type_counts.get(t, 0) + 1

    for t, c in sorted(type_counts.items()):
        print(f"  {t}: {c} ({100*c/len(results):.1f}%)")


if __name__ == "__main__":
    main()
