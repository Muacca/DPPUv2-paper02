"""Sample joint and fixed-shape classifications without rounding inputs."""
import csv
from datetime import datetime
from multiprocessing import Pool
from pathlib import Path
import numpy as np
from .classification import classify_configuration


def calculate_single_point(args):
    """Five-item inputs select alpha=epsilon=0 and MX; eight include them."""
    if len(args) == 5:args = (*args, 0., 0., 'MX')
    if len(args) == 8:args = (*args, 'EC_IRR')
    topology, variant, V, eta, theta, alpha, epsilon, mode, curvature_model = args
    return classify_configuration(topology, V, eta, alpha, epsilon,
                                  mode=mode, ny_variant=variant, theta=theta, curvature_model=curvature_model)


def generate_parameter_grid(V_range, eta_range, theta_range, topologies,
                            ny_variants, alphas=(0.,), epsilon=0., mode='MX', curvature_model='EC_IRR'):
    return [(top, ny, V, eta, theta, alpha, epsilon, mode, curvature_model)
            for top in topologies for ny in ny_variants for V in V_range
            for eta in eta_range for theta in theta_range for alpha in alphas]


def run_scan(V_points=6, eta_points=11, theta_points=1, V_min=0., V_max=5.,
             eta_min=-5., eta_max=5., theta_min=1., theta_max=1.,
             topologies=None, ny_variants=None, output_dir='output',
             output_filename=None, n_workers=1, alphas=(0.,), epsilon=0., mode='MX', curvature_model='EC_IRR'):
    """Write full-precision inputs and separate global/radial CSV fields.

    FULL is the default and has no theta dependence. Explicit TT/REE rows
    have NOT_APPLICABLE classifications. No plot bounds enter classification.
    """
    for n in (V_points, eta_points, theta_points):
        if not np.isfinite(n) or int(n) != n or n < 1:
            raise ValueError('Grid counts must be positive integers')
    bounds=(V_min,V_max,eta_min,eta_max,theta_min,theta_max)
    if not all(np.isfinite(v) for v in bounds):raise ValueError('Grid limits must be finite')
    if V_min>V_max or eta_min>eta_max or theta_min>theta_max:raise ValueError('Grid limits must be ordered')
    topologies = ['S3','T3','Nil3'] if topologies is None else topologies
    ny_variants = ['FULL'] if ny_variants is None else ny_variants
    args=generate_parameter_grid(np.linspace(V_min,V_max,int(V_points)),
        np.linspace(eta_min,eta_max,int(eta_points)),np.linspace(theta_min,theta_max,int(theta_points)),
        topologies,ny_variants,alphas,epsilon,mode,curvature_model)
    if not args:raise ValueError('The parameter grid is empty')
    if n_workers is None:n_workers=1
    if int(n_workers)!=n_workers or n_workers<1:raise ValueError('Workers must be a positive integer')
    if n_workers == 1:results=[calculate_single_point(a) for a in args]
    else:
        with Pool(int(n_workers)) as pool:results=pool.map(calculate_single_point,args)
    folder=Path(output_dir);folder.mkdir(parents=True,exist_ok=True)
    name=output_filename or ('dppu_scan_'+datetime.now().strftime('%Y%m%d_%H%M%S_%f')+'.csv')
    if Path(name).name!=name:raise ValueError('output_filename must be a filename')
    with (folder/name).open('x',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=list(results[0]));writer.writeheader();writer.writerows(results)
    print(f'{len(results)} classifications saved to {folder/name}')
    return results
