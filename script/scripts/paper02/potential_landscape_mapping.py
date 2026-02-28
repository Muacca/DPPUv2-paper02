"""
paper02: Potential Landscape Mapping
==========================================

Generates (r, epsilon) potential landscapes for specified topology and alpha.
Uses vectorized scan via dppu.scanning.squashing_scan.

Plan reference:
  - r in [0.01, 30], epsilon in [-0.9, 5.0]
  - alpha = -20, -10, -1, 0, 1, 10, 20
  - eps-max=5.0 is the default to cover Nil3's flat limit (eps -> +inf).
    For narrower scans (S3/T3 only), use --eps-max 1.0.
"""

import sys
import os
import argparse
from datetime import datetime
import numpy as np
import pandas as pd

# Add parent directory to path to allow importing dppu
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from dppu.scanning.squashing_scan import scan_potential_landscape


def run_mapping(topology, alpha_val, r_range, eps_range, resolution,
                params_dict=None):
    print(f"--- Starting Mapping: {topology}, alpha={alpha_val} ---")

    # Default Phase1 parameters (Type I representative)
    if params_dict is None:
        params_dict = {
            'V': 4.0, 'eta': -2.0, 'theta_NY': 1.0,
            'L': 1.0, 'kappa': 1.0
        }
    params_dict['alpha'] = alpha_val

    # Build grid arrays
    r_vals = np.linspace(r_range[0], r_range[1], resolution)
    eps_vals = np.linspace(eps_range[0], eps_range[1], resolution)

    print(f"Grid: {resolution}x{resolution}, r=[{r_range[0]}, {r_range[1]}], "
          f"eps=[{eps_range[0]}, {eps_range[1]}]")

    # Use vectorized scan
    result = scan_potential_landscape(
        topology=topology,
        mode="MX",
        ny_variant="FULL",
        params=params_dict,
        r_range=r_vals,
        epsilon_range=eps_vals
    )

    # Flatten meshgrid for CSV output
    df = pd.DataFrame({
        'r': result['R'].flatten(),
        'epsilon': result['Epsilon'].flatten(),
        'V_eff': result['V_eff'].flatten(),
        'alpha': alpha_val,
        'topology': topology
    })

    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="paper02: Potential Landscape Mapping")
    parser.add_argument("--topology", type=str, required=True, choices=["S3", "T3", "Nil3"])
    parser.add_argument("--alpha", type=float, nargs='+',
                        default=[-20, -10, -1, 0, 1, 10, 20],
                        help="Alpha values (space-separated). Default: plan v4.0 set.")
    parser.add_argument("--res", type=int, default=100,
                        help="Grid resolution per axis (default 100)")
    parser.add_argument("--r-min", type=float, default=0.01)
    parser.add_argument("--r-max", type=float, default=30.0)
    parser.add_argument("--eps-min", type=float, default=-0.95)
    parser.add_argument("--eps-max", type=float, default=5.0,
                        help="Upper bound of epsilon range (default: 5.0; use 1.0 for narrower scan)")
    parser.add_argument("--output-dir", type=str, default="output",
                        help="Output directory for CSV files (default: output)")
    args = parser.parse_args()

    r_range = (args.r_min, args.r_max)
    eps_range = (args.eps_min, args.eps_max)

    dfs = []
    for alpha_val in args.alpha:
        df = run_mapping(args.topology, alpha_val, r_range, eps_range, args.res)
        if df is not None:
            dfs.append(df)

    if dfs:
        combined = pd.concat(dfs, ignore_index=True)
        os.makedirs(args.output_dir, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = os.path.join(args.output_dir, f"potential_landscape_mapping_{timestamp}.csv")
        combined.to_csv(output_path, index=False)
        print(f"Combined output saved to: {output_path}")
