"""
paper02: Critical Analysis
=================================

High-resolution analysis of the phase transition near alpha=0.
Tracks epsilon_* (order parameter), r_*, and V_min.

Plan reference:
  - alpha in [-1, 1], step 0.01
  - Fine mode: alpha in [-0.1, 0.1], step 0.005
"""

import sys
import os
import argparse
from datetime import datetime
import numpy as np
import pandas as pd
from tqdm import tqdm
from scipy.optimize import minimize

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from dppu.torsion.mode import Mode
from dppu.torsion.nieh_yan import NyVariant
from dppu.topology.s3s1 import S3S1Engine
from dppu.topology.t3s1 import T3S1Engine
from dppu.topology.nil3s1 import Nil3S1Engine
from optimization_helper import find_global_minimum


def get_engine(topology_name, mode, ny_variant):
    if topology_name == "S3":
        return S3S1Engine(mode, ny_variant)
    elif topology_name == "T3":
        return T3S1Engine(mode, ny_variant)
    elif topology_name == "Nil3":
        return Nil3S1Engine(mode, ny_variant)
    else:
        raise ValueError(f"Unknown topology: {topology_name}")


def analyze_critical_behavior(topology, alpha_range, alpha_step, output_file,
                              phase1_params=None, eps_bounds=(-0.95, 5.0)):
    print(f"--- Starting Critical Analysis: {topology} ---")
    print(f"Alpha range: {alpha_range}, Step: {alpha_step}")
    print(f"Epsilon bounds: {eps_bounds}")

    # Initialize Engine
    mode = Mode.MX
    ny_variant = NyVariant.FULL
    engine = get_engine(topology, mode, ny_variant)
    engine.run()
    V_func = engine.get_effective_potential_function()

    # Fixed Parameters (default or from CLI)
    if phase1_params is None:
        phase1_params = {
            'V': 4.0, 'eta': -2.0, 'theta_NY': 1.0,
            'L': 1.0, 'kappa': 1.0
        }

    # Alpha values
    alpha_vals = np.arange(alpha_range[0], alpha_range[1] + alpha_step / 2, alpha_step)

    # Search bounds (r upper extended to capture minima beyond r=2)
    r_bounds = (0.01, 10.0)

    results = []

    print(f"Scanning {len(alpha_vals)} alpha values...")
    for alpha in tqdm(alpha_vals):
        params = {**phase1_params, 'alpha': alpha}

        r_star, eps_star, v_min, success = find_global_minimum(
            V_func, params,
            r_bounds=r_bounds,
            eps_bounds=eps_bounds,
            coarse_Ns=30,
            n_candidates=8
        )

        results.append({
            'alpha': round(alpha, 6),
            'r_star': r_star,
            'epsilon_star': eps_star,
            'V_min': v_min,
            'topology': topology,
            'converged': success
        })

    # Save
    df = pd.DataFrame(results)
    os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)
    df.to_csv(output_file, index=False)
    print(f"Saved critical analysis ({len(df)} points) to {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="paper02: Critical Analysis")
    parser.add_argument("--topology", type=str, default="S3", choices=["S3", "T3", "Nil3"])
    parser.add_argument("--fine", action="store_true", help="Fine resolution near alpha=0")
    parser.add_argument("--V", type=float, default=4.0)
    parser.add_argument("--eta", type=float, default=-2.0)
    parser.add_argument("--theta", type=float, default=1.0)
    parser.add_argument("--eps-min", type=float, default=-0.95,
                        help="Lower bound of epsilon search range (default: -0.95)")
    parser.add_argument("--eps-max", type=float, default=5.0,
                        help="Upper bound of epsilon search range (default: 5.0; "
                             "covers Nil3 flat limit; use 1.0 for narrower scan)")
    parser.add_argument("--output-dir", type=str, default="output",
                        help="Output directory for CSV files (default: output)")
    args = parser.parse_args()

    phase1_params = {
        'V': args.V, 'eta': args.eta, 'theta_NY': args.theta,
        'L': 1.0, 'kappa': 1.0
    }

    if args.fine:
        alpha_range = (-0.1, 0.1)
        alpha_step = 0.005
    else:
        alpha_range = (-1.0, 1.0)
        alpha_step = 0.01

    os.makedirs(args.output_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_path = os.path.join(args.output_dir, f"critical_analysis_{timestamp}.csv")

    analyze_critical_behavior(args.topology, alpha_range, alpha_step, output_path,
                              phase1_params, eps_bounds=(args.eps_min, args.eps_max))
