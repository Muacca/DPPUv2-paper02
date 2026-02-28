#!/usr/bin/env python3
"""
Critical Value Analysis
=======================

Sweeps the Weyl coupling alpha and tracks the minimum of the effective potential
V_eff(r, epsilon) to identify critical values and phase transitions.
"""

import argparse
import sys
import os
import csv
import numpy as np
from datetime import datetime
from scipy.optimize import minimize, brute

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from dppu.scanning.squashing_scan import get_engine
from dppu.torsion.mode import Mode
from dppu.torsion.nieh_yan import NyVariant

def find_global_minimum(V_func, params, bounds):
    """
    Find global minimum of V_eff(r, epsilon).
    
    Args:
        V_func: Lambdified potential function
        params: Dict of fixed parameters
        bounds: List of (min, max) for [r, epsilon]
        
    Returns:
        (r_min, eps_min, V_min)
    """
    # Parameters for V_func: r, V, eta, theta, L, kappa, epsilon, alpha
    V_val = params.get('V', 1.0)
    eta_val = params.get('eta', 0.0)
    theta_val = params.get('theta_NY', 0.0)
    L_val = params.get('L', 1.0)
    kappa_val = params.get('kappa', 1.0)
    alpha_val = params.get('alpha', 0.0)
    
    def objective(x):
        r, eps = x
        if r <= 0: return 1e50
        return V_func(r, V_val, eta_val, theta_val, L_val, kappa_val, eps, alpha_val)

    # 1. Global search using brute force on a coarse grid to avoid local minima
    # Bounds format for brute: ((r_min, r_max), (eps_min, eps_max))
    # Ns: number of grid points
    rranges = tuple(bounds)
    res_brute = brute(objective, rranges, Ns=20, full_output=True, finish=None)
    x0 = res_brute[0]
    
    # 2. Local refinement
    res = minimize(
        objective, 
        x0, 
        bounds=bounds,
        method='L-BFGS-B'
    )
    
    return res.x[0], res.x[1], res.fun

def run_analysis(args):
    """Run the alpha sweep analysis."""
    
    # Setup engine
    print(f"Initializing engine for {args.topology} ({args.mode}, {args.ny_variant})...")
    mode_enum = Mode[args.mode]
    ny_enum = NyVariant[args.ny_variant]
    engine = get_engine(args.topology, mode_enum, ny_enum)
    engine.run()
    V_func = engine.get_effective_potential_function()
    
    # Setup alpha range
    if args.log_scale:
        if args.alpha_min <= 0:
            print("Error: alpha-min must be > 0 for log scale. Using linear scale or adjusting min.")
            alpha_values = np.logspace(np.log10(1e-4), np.log10(args.alpha_max), args.alpha_points)
        else:
            alpha_values = np.logspace(np.log10(args.alpha_min), np.log10(args.alpha_max), args.alpha_points)
    else:
        alpha_values = np.linspace(args.alpha_min, args.alpha_max, args.alpha_points)
        
    # Fixed parameters
    params = {
        'V': args.V,
        'eta': args.eta,
        'theta_NY': args.theta,
        'kappa': args.kappa,
        'L': args.L
    }
    
    results = []
    
    print(f"Sweeping alpha from {args.alpha_min} to {args.alpha_max} ({args.alpha_points} points)...")
    
    bounds = [(args.r_min, args.r_max), (args.eps_min, args.eps_max)]
    
    for i, alpha in enumerate(alpha_values):
        params['alpha'] = alpha
        
        try:
            r_min, eps_min, v_min = find_global_minimum(V_func, params, bounds)
            
            results.append({
                'alpha': alpha,
                'r_min': r_min,
                'eps_min': eps_min,
                'V_min': v_min
            })
            
            # Simple progress
            if (i+1) % 5 == 0:
                print(f"  Step {i+1}/{len(alpha_values)}: alpha={alpha:.4e} -> r={r_min:.4f}, eps={eps_min:.4f}")
                
        except Exception as e:
            print(f"Error at alpha={alpha}: {e}")
            
    # Save results
    os.makedirs(args.output_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"run_alpha_boundary_scan_{timestamp}.csv"
    filepath = os.path.join(args.output_dir, filename)
    
    print(f"Saving results to {filepath}...")
    
    with open(filepath, 'w', newline='') as f:
        fieldnames = ['alpha', 'r_min', 'eps_min', 'V_min']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        # Write metadata
        f.write(f"# Topology: {args.topology}\n")
        f.write(f"# Mode: {args.mode}\n")
        f.write(f"# NY Variant: {args.ny_variant}\n")
        f.write(f"# Fixed Params: {params}\n")
        
        writer.writeheader()
        writer.writerows(results)
        
    print("Done.")

def main():
    parser = argparse.ArgumentParser(description="Sweep alpha to find critical values.")
    
    # Model config
    parser.add_argument('--topology', type=str, required=True, choices=['S3', 'T3', 'Nil3'])
    parser.add_argument('--mode', type=str, default='MX', choices=['MX', 'AX', 'VT'])
    parser.add_argument('--ny-variant', type=str, default='FULL', choices=['FULL', 'TT', 'REE'])
    
    # Fixed params
    parser.add_argument('--V', type=float, default=1.0)
    parser.add_argument('--eta', type=float, default=0.0)
    parser.add_argument('--theta', type=float, default=0.0)
    parser.add_argument('--kappa', type=float, default=1.0)
    parser.add_argument('--L', type=float, default=1.0)
    
    # Alpha sweep
    parser.add_argument('--alpha-min', type=float, default=0.0)
    parser.add_argument('--alpha-max', type=float, default=10.0)
    parser.add_argument('--alpha-points', type=int, default=50)
    parser.add_argument('--log-scale', action='store_true', help="Use log scale for alpha")
    
    # Search bounds
    parser.add_argument('--r-min', type=float, default=0.1)
    parser.add_argument('--r-max', type=float, default=10.0)
    parser.add_argument('--eps-min', type=float, default=-0.9)
    parser.add_argument('--eps-max', type=float, default=2.0)
    
    parser.add_argument('--output-dir', type=str, default='output',
                        help='Output directory (default: output)')
    
    args = parser.parse_args()
    run_analysis(args)

if __name__ == '__main__':
    main()
