"""
paper02: Topology Comparison
===================================

Compares V_min across S3, T3, Nil3 to determine the preferred topology
in the presence of Weyl anisotropy.

Plan reference:
  - Same (V, eta, theta_NY, alpha) across 3 topologies
  - alpha in [-5, 5], 21 points (configurable)
"""

import sys
import os
import argparse
from datetime import datetime
import numpy as np
import pandas as pd
from tqdm import tqdm

# Add parent directory
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


def run_comparison(alpha_vals, output_file, eps_bounds=(-0.95, 5.0)):
    print("--- Starting Topology Comparison ---")
    print(f"Epsilon bounds: {eps_bounds}")

    topologies = ["S3", "T3", "Nil3"]
    func_Vs = {}

    # Setup engines
    for topo in topologies:
        print(f"Initializing {topo} engine...")
        eng = get_engine(topo, Mode.MX, NyVariant.FULL)
        eng.run()
        func_Vs[topo] = eng.get_effective_potential_function()

    # Fixed Params (S3-preferred from Phase1)
    phase1_params = {
        'V': 4.0, 'eta': -2.0, 'theta_NY': 1.0,
        'L': 1.0, 'kappa': 1.0
    }

    results = []

    print(f"Scanning {len(alpha_vals)} alpha values...")
    for alpha in tqdm(alpha_vals):
        row = {'alpha': alpha}

        for topo in topologies:
            params = {**phase1_params, 'alpha': alpha}
            r_s, eps_s, v_min, success = find_global_minimum(
                func_Vs[topo], params,
                r_bounds=(0.01, 10.0),
                eps_bounds=eps_bounds,
                coarse_Ns=30,
                n_candidates=8
            )
            row[f'V_min_{topo}'] = v_min
            row[f'r_{topo}'] = r_s
            row[f'eps_{topo}'] = eps_s
            row[f'converged_{topo}'] = success

        # Determine winner
        v_mins = {t: row[f'V_min_{t}'] for t in topologies}
        winner = min(v_mins, key=v_mins.get)
        row['Preferred_Topology'] = winner

        results.append(row)

    df = pd.DataFrame(results)
    os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)
    df.to_csv(output_file, index=False)
    print(f"Saved comparison ({len(df)} points) to {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="paper02: Topology Comparison")
    parser.add_argument("--alpha-min", type=float, default=-5.0)
    parser.add_argument("--alpha-max", type=float, default=5.0)
    parser.add_argument("--alpha-points", type=int, default=21)
    parser.add_argument("--eps-min", type=float, default=-0.95,
                        help="Lower bound of epsilon search range (default: -0.95)")
    parser.add_argument("--eps-max", type=float, default=5.0,
                        help="Upper bound of epsilon search range (default: 5.0; "
                             "covers Nil3 flat limit; use 1.0 for narrower scan)")
    parser.add_argument("--output-dir", type=str, default="output",
                        help="Output directory for CSV files (default: output)")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_path = os.path.join(args.output_dir, f"topology_comparison_{timestamp}.csv")

    alpha_range = np.linspace(args.alpha_min, args.alpha_max, args.alpha_points)

    run_comparison(alpha_range, output_file=output_path,
                   eps_bounds=(args.eps_min, args.eps_max))
