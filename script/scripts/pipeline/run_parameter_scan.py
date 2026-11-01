"""CLI for joint radius/shape and fixed-shape radial classification."""
from pathlib import Path
from collections import Counter
import argparse
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from dppu.scanning import run_scan


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--topologies',nargs='+',choices=['S3','T3','Nil3'],default=['S3','T3','Nil3'])
    p.add_argument('--ny-variants',nargs='+',choices=['FULL','TT','REE'],default=['FULL'],
                   help='TT/REE select the positive torsion-product/curvature-coframe term; classifications are NOT_APPLICABLE')
    p.add_argument('--mode',choices=['MX','AX','VT'],default='MX', help='MX: both torsion components allowed; AX: axial only; VT: vector trace only; zero amplitudes allowed')
    p.add_argument('--V-range',nargs=3,type=float,default=[0,5,6],metavar=('MIN','MAX','COUNT'))
    p.add_argument('--eta-range',nargs=3,type=float,default=[-5,5,11],metavar=('MIN','MAX','COUNT'))
    p.add_argument('--theta-range',nargs=3,type=float,default=[1,1,1],metavar=('MIN','MAX','COUNT'),
                   help='FULL has no theta dependence; one value by default')
    p.add_argument('--alpha',nargs='+',type=float,default=[0.],help='Curvature-squared couplings (sign is not rounded)')
    p.add_argument('--epsilon',type=float,default=0.,help='Shape for radial classification; joint result varies shape')
    p.add_argument('--output-dir',default='output')
    p.add_argument('--workers',type=int,default=1)
    p.add_argument('--curvature-model',choices=['LC','EC_IRR','EC_TRACEFREE'],default='EC_IRR', help='LC: LC-Weyl; EC_IRR: irreducible EC-Weyl; EC_TRACEFREE: Ricci-tracefree EC curvature')
    a=p.parse_args()
    try:
        rows=run_scan(V_points=a.V_range[2],eta_points=a.eta_range[2],theta_points=a.theta_range[2],
            V_min=a.V_range[0],V_max=a.V_range[1],eta_min=a.eta_range[0],eta_max=a.eta_range[1],
            theta_min=a.theta_range[0],theta_max=a.theta_range[1],topologies=a.topologies,
            ny_variants=a.ny_variants,output_dir=a.output_dir,n_workers=a.workers,
            alphas=a.alpha,epsilon=a.epsilon,mode=a.mode,curvature_model=a.curvature_model)
    except ValueError as e:p.error(str(e))
    for field in ['global_class','radial_class']:
        print(field+':')
        for label,count in sorted(Counter(r[field] for r in rows).items()):print(f'  {label}: {count}')

if __name__=='__main__':main()
