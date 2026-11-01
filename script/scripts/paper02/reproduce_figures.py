"""Render the paper's supplied datasets or explicitly recompute them.

Run from any directory. Every output directory must be new. The default
render operation reads data/revised and performs no symbolic recomputation.
"""
from pathlib import Path
import argparse
import csv
import json
import sys

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO/'script'))
NAMES = ['round_reference', 'shape_penalty', 'small_radius', 'nil_torus']


def write_csv(path, rows):
    with path.open('x', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path):
    with path.open(encoding='utf-8', newline='') as f:
        return [{k: float(v) for k, v in row.items()} for row in csv.DictReader(f)]


def recompute(data_dir):
    from dppu.topology.s3s1 import S3S1Engine
    from dppu.topology.t3s1 import T3S1Engine
    from dppu.topology.nil3s1 import Nil3S1Engine
    from dppu.torsion.mode import Mode
    from dppu.torsion.nieh_yan import NyVariant
    from dppu.scanning import classify_configuration
    functions = {}
    for name, cls in [('S3', S3S1Engine), ('T3', T3S1Engine), ('Nil3', Nil3S1Engine)]:
        engine = cls(Mode.MX, NyVariant.FULL, curvature_model='LC')
        engine.run()
        functions[name] = engine.get_effective_potential_function()
        print(f'{name}: complete-NY engine ready', flush=True)

    def value(topology, r, x=1., alpha=0., eta=-2.):
        return float(functions[topology](r, 4., eta, 1., 1., 1., x**(-1.5)-1., alpha))

    rows = []
    for r in np.linspace(.001, 3., 301):
        row = {'r': r, 'old_ny_current_volume': 4*np.pi**2/3*r*r*(r-3)}
        row.update({f'eta_{eta}': value('S3', r, eta=eta) for eta in [-3, -2, 0, 2]})
        rows.append(row)
    write_csv(data_dir/'round_reference.csv', rows)
    write_csv(data_dir/'shape_penalty.csv', [
        {'x': x, **{f'alpha_{alpha}': value('S3', 1., x, alpha)-value('S3', 1., 1., alpha)
                     for alpha in [0., -.01, -.1]}}
        for x in np.linspace(.3, 1.7, 281)])
    write_csv(data_dir/'small_radius.csv', [
        {'r': r, 'S3_nonround': value('S3', r, .7, .01),
         'S3_round': value('S3', r, 1., .01), 'Nil3': value('Nil3', r, .7, .01)}
        for r in np.geomspace(.001, 1., 241)])
    rows = []
    for x in np.geomspace(.02, 1.6, 241):
        A, B, D = 16., 36.+.75*x**4, 4*x**8
        r_slice = np.sqrt(2*D/(B+np.sqrt(B*B+12*A*D)))
        rows.append({'x': x, 'r_slice': r_slice, 'U_slice': value('Nil3', r_slice, x, -1.)})
    write_csv(data_dir/'nil_slices.csv', rows)
    write_csv(data_dir/'torus.csv', [
        {'r': r, **{f'alpha_{alpha}': value('T3', r, .7, alpha)
                     for alpha in [-1., 0., 1.]}}
        for r in np.linspace(.001, 2., 201)])
    # Joint radius/shape classification; Theorem 3 makes it common to all alpha<=0.
    attainment = {'FINITE_MINIMUM': 'UNIQUE_RESTRICTED_MINIMUM', 'UNATTAINED_INFIMUM': 'UNATTAINED_INFIMUM_ZERO'}
    rows = []
    for eta in [-3, -2, 0, 2]:
        result = classify_configuration('S3', 4., eta, 0., 0., curvature_model='LC')
        finite = result['global_class'] == 'FINITE_MINIMUM'
        if not finite and result['global_infimum'] != 0:
            raise RuntimeError(f'Unexpected spherical infimum at eta={eta}')
        rows.append({'eta_code': eta, 'eta_geometric': -eta,
                     'r_stationary': result['global_r'] if finite else '',
                     'U_stationary': result['global_infimum'] if finite else '',
                     'attainment': attainment[result['global_class']]})
    write_csv(data_dir/'stationary_points.csv', rows)
    metadata = {
        'manuscript_version': 'v2', 'action': 'EC + complete NY + LC-Weyl squared',
        'inputs': {'V_code': 4., 'eta_code_default': -2., 'theta_NY': 1., 'L': 1., 'kappa': 1.},
        'dictionary': 'eta_geometric=-eta_code; V_geometric=-V_code; x=(1+epsilon)^(-2/3)',
        'volumes': {'S3': 'pi^2*L*r^3/4', 'T3': '(2*pi)^3*L*r^3', 'Nil3': '(2*pi)^4*L*r^3'},
        'domains': {'round_r': [.001, 3., 301], 'shape_x': [.3, 1.7, 281],
                    'small_radius_r': [.001, 1., 241], 'nil_x': [.02, 1.6, 241],
                    'torus_r': [.001, 2., 201]},
        'old_ny_curve': 'Historical incorrect NY expression, rescaled to the current spherical volume.',
        'interpretation': 'Fixed signed amplitudes and circle length. Finite samples illustrate the analytic proofs; slice extrema are not full-field vacua.'}
    with (data_dir/'parameters.json').open('x', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)


def render(data_dir, figure_dir):
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 11,
                         'axes.spines.top': False, 'axes.spines.right': False,
                         'axes.grid': True, 'grid.alpha': .2, 'savefig.dpi': 220})
    blue, orange, green = '#2563a8', '#c05b16', '#23856a'
    def series(rows, key): return np.array([row[key] for row in rows])
    def finish(fig, name):
        fig.savefig(figure_dir/f'{name}.png', facecolor='white')
        plt.close(fig)
    rows=read_csv(data_dir/'round_reference.csv');r=series(rows,'r')
    fig,ax=plt.subplots(1,2,figsize=(10.2,4.3),layout='constrained')
    ax[0].plot(r,series(rows,'old_ny_current_volume'),color=orange,ls='--',label='Old NY, rescaled volume')
    ax[0].plot(r,series(rows,'eta_-2'),color=blue,label='Complete NY')
    ax[0].set(title='Former reference input',xlabel='$r$',ylabel='$U_{S^3}$')
    ax[0].legend(fontsize=9)
    for eta,label,col in [(-3,r'$\eta_\tau=-3$',orange),(-2,r'$\eta_\tau=\pm2$',blue),(0,r'$\eta_\tau=0$',green)]:
        ax[1].plot(r,series(rows,f'eta_{eta}'),label=label,color=col)
    ax[1].plot(np.sqrt(3)/2,-np.sqrt(3)*np.pi**2,'o',color=green,ms=5)
    ax[1].axhline(0,color='#999999',lw=.7)
    ax[1].set(title='Corrected round slices',xlabel='$r$',ylabel='$U_{S^3}$',xlim=(0,1.7),ylim=(-30,160))
    ax[1].legend(fontsize=9)
    finish(fig,'round_reference')

    rows=read_csv(data_dir/'shape_penalty.csv');x=series(rows,'x')
    fig,ax=plt.subplots(figsize=(8.8,4.3),layout='constrained')
    for alpha,col in [(0.,green),(-.01,blue),(-.1,orange)]:
        ax.plot(x,series(rows,f'alpha_{alpha}'),label=rf'$\alpha={alpha:g}$',color=col)
    ax.set(xlabel=r'$x=(1+\epsilon)^{-2/3}$',ylabel='$U(r,x)-U(r,1)$',
           title='Spherical shape penalty at fixed radius',yscale='symlog',ylim=(-.2,8000))
    ax.axvline(1,color='#777777',ls=':',lw=.9);ax.legend()
    finish(fig,'shape_penalty')

    rows=read_csv(data_dir/'small_radius.csv');r=series(rows,'r')
    fig,ax=plt.subplots(figsize=(8.8,4.3),layout='constrained')
    ax.plot(r,series(rows,'S3_nonround')/(np.pi**2/4),color=blue,label=r'$S^3$, $x=0.7$')
    ax.plot(r,series(rows,'S3_round')/(np.pi**2/4),color=green,ls=':',label=r'$S^3$, $x=1$')
    ax.plot(r,series(rows,'Nil3')/(2*np.pi)**4,color=orange,ls='--',label=r'Nil$^3$, $x=0.7$')
    ax.set(xlabel='$r$',ylabel='$U/(c_M L)$',title='Positive coupling: fixed-shape small-radius limits',
           xscale='log',yscale='symlog');ax.legend()
    finish(fig,'small_radius')

    rows=read_csv(data_dir/'nil_slices.csv');tor=read_csv(data_dir/'torus.csv')
    fig,ax=plt.subplots(1,2,figsize=(10.2,4.3),layout='constrained')
    ax[0].plot(series(rows,'x'),series(rows,'U_slice')/(2*np.pi)**4,color=orange)
    ax[0].set(xlabel='$x$',ylabel=r'$U_{\mathrm{slice}}/(c_{\mathrm{Nil}}L)$',xscale='log',yscale='log',
              title='Nil: radial minima at fixed shape')
    ax[1].plot(series(tor,'r'),series(tor,'alpha_0.0')/(2*np.pi)**3,color=blue,
               label=r'$\alpha=-1,0,+1$ (coincident)')
    ax[1].set(xlabel='$r$',ylabel='$U_{T^3}/(c_{T^3}L)$',title='Torus: no Weyl dependence')
    ax[1].legend(fontsize=9)
    finish(fig,'nil_torus')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation',choices=['render','recompute'])
    parser.add_argument('--output-dir',type=Path,required=True,help='New directory; existing paths are rejected.')
    parser.add_argument('--data-dir',type=Path,default=REPO/'data/revised',help='Saved input for render only.')
    args=parser.parse_args()
    args.output_dir.mkdir(parents=True,exist_ok=False)
    figures=args.output_dir/'figures';figures.mkdir()
    if args.operation=='recompute':
        data=args.output_dir/'data';data.mkdir()
        recompute(data)
    else:data=args.data_dir
    render(data,figures)
    print(f'Four figures written to {figures}')


if __name__=='__main__': main()
