"""Paper02 joint/radial classification and engine-direct potential viewer.

The shared classifier implements complete-NY restricted-potential results.
TT/REE remain available for curve exploration, outside that classification.
"""
from pathlib import Path
import sys, os, math, html
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.ticker import FuncFormatter
from matplotlib.patches import Patch
import ipywidgets as widgets
from IPython.display import display, clear_output
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from dppu.torsion import Mode, NyVariant
from dppu.topology import S3S1Engine,T3S1Engine,Nil3S1Engine
from dppu.scanning.classification import classify_configuration, LABELS, CLASS_CODES, COLORS

KAPPA=L_SCALE=1.
ENGINE_CLASSES={'S3':S3S1Engine,'T3':T3S1Engine,'Nil3':Nil3S1Engine}
MODE_ENUMS={'MX':Mode.MX,'AX':Mode.AX,'VT':Mode.VT}
NY_ENUMS={'FULL':NyVariant.FULL,'TT':NyVariant.TT,'REE':NyVariant.REE}
_CURVATURE_LABELS={'EC_IRR':'Irreducible EC-Weyl','LC':'LC-Weyl','EC_TRACEFREE':'Ricci-tracefree EC curvature'}
_TORSION_LABELS={'MX':'Axial + vector trace','AX':'Axial only','VT':'Vector trace only'}
_NY_LABELS={'FULL':'Complete NY','TT':'Torsion product term','REE':'Curvature-coframe term'}
_GEOMETRY_LABELS={'S3':'Sphere x circle','T3':'Torus x circle','Nil3':'Nil quotient x circle'}

_potential_cache={}

def get_potential_function(topology: str, mode: str, ny_variant: str,
                           status_callback=None, curvature_model='EC_IRR'):
    """
    Get (or compute & cache) the potential evaluation function.

    v4 design: ε (squashing) and α_W (Weyl coupling) are kept as symbolic
    parameters. The returned callable accepts them as numerical arguments,
    so a single engine run covers all (ε, α) values.

    Args:
        topology:   'S3', 'T3', or 'Nil3'
        mode:       'MX', 'VT', or 'AX'
        ny_variant: 'FULL', 'TT', or 'REE'
        status_callback: Optional function(str) for progress messages

    Returns:
        Callable: f(r, V_param, eta_param, theta_NY, epsilon, alpha) -> V_eff
    """
    from sympy import lambdify

    key = (topology, mode, ny_variant, curvature_model)

    if key in _potential_cache:
        if status_callback:
            status_callback(
                f"Using cached: {topology}×S¹ / {mode} / {ny_variant} / {curvature_model} "
                f"[ε, α_W evaluated numerically]"
            )
        return _potential_cache[key]

    if status_callback:
        status_callback(
            f"Generating: {topology}×S¹ / {mode} / {ny_variant} / {curvature_model}…"
            f" (30–120 s, ε/α_W will be numerical after this)"
        )

    engine_class = ENGINE_CLASSES[topology]
    mode_enum    = MODE_ENUMS[mode]
    ny_enum      = NY_ENUMS[ny_variant]

    # Run engine with output suppressed (NullLogger used by default)
    _orig_stdout = sys.stdout
    try:
        sys.stdout = open(os.devnull, 'w')
        engine = engine_class(mode=mode_enum, ny_variant=ny_enum, curvature_model=curvature_model)
        engine.run()
    finally:
        sys.stdout.close()
        sys.stdout = _orig_stdout

    params   = engine.data['params']
    sym_expr = engine.data['potential']

    r_sym       = params['r']
    L_sym       = params['L']
    kappa_sym   = params['kappa']
    theta_sym   = params['theta_NY']
    V_sym       = params['V']
    eta_sym     = params['eta']
    epsilon_sym = params['epsilon']
    alpha_sym   = params['alpha']

    # Detect which torsion parameters are actual SymPy symbols
    # (AX mode: V = S.Zero; VT mode: eta = S.Zero)
    def _is_sym(x):
        return hasattr(x, 'is_Symbol') and x.is_Symbol

    V_is_symbol   = _is_sym(V_sym)
    eta_is_symbol = _is_sym(eta_sym)
    # epsilon and alpha are always symbols in v4 engines

    # Build lambdify argument list (only proper Symbol instances)
    lambda_args = [r_sym]
    if V_is_symbol:
        lambda_args.append(V_sym)
    if eta_is_symbol:
        lambda_args.append(eta_sym)
    lambda_args.extend([theta_sym, L_sym, kappa_sym, epsilon_sym, alpha_sym])

    raw_func = lambdify(lambda_args, sym_expr, modules='numpy')

    # Unified wrapper: f(r, V_param, eta_param, theta_NY, epsilon, alpha)
    # V_param / eta_param are ignored in modes where they are not symbols.
    if mode == 'MX':
        def wrapped_func(r, V_param, eta_param, theta_NY, epsilon=0.0, alpha=0.0):
            return raw_func(r, V_param, eta_param, theta_NY,
                            L_SCALE, KAPPA, epsilon, alpha)
    elif mode == 'AX':
        def wrapped_func(r, V_param, eta_param, theta_NY, epsilon=0.0, alpha=0.0):
            # V_param ignored (V = 0 fixed in AX mode)
            return raw_func(r, eta_param, theta_NY,
                            L_SCALE, KAPPA, epsilon, alpha)
    elif mode == 'VT':
        def wrapped_func(r, V_param, eta_param, theta_NY, epsilon=0.0, alpha=0.0):
            # eta_param ignored (η = 0 fixed in VT mode)
            return raw_func(r, V_param, theta_NY,
                            L_SCALE, KAPPA, epsilon, alpha)
    else:
        raise ValueError(f"Unknown mode: {mode}")

    _potential_cache[key] = wrapped_func

    if status_callback:
        status_callback(
            f"✓ Cached: {topology}×S¹ / {mode} / {ny_variant} / {curvature_model} "
            f"[ε/α_W evaluated numerically at scan time]"
        )

    return wrapped_func



def get_cache_status():
    return ', '.join('/'.join(k) for k in _potential_cache) or 'No cached engine'


def clear_cache():
    _potential_cache.clear()


def get_weyl_c2_status(topology, epsilon):
    zero=topology=='T3' or (topology=='S3' and epsilon==0)
    return zero, ('LC-Weyl vanishes on this slice' if zero else 'LC-Weyl is active on this slice'), ('#555' if zero else '#245e83')


class DPPUv2InteractiveViewer:
    """Two complementary domains, three selected points, one shared classifier.

    Apply controls to redraw both panels together. Plot limits never enter
    the analytic classification. FloatText controls accept boundary inputs.
    """
    def __init__(self):
        self.selected_points=[{'V':4.,'eta':0.,'active':True},
                              {'V':4.,'eta':1.999,'active':True},
                              {'V':0.,'eta':2.,'active':True}]
        self.current_point_idx=0
        self.fig=None;self.ax_phase=None;self.ax_potential=None;self.phase_data=None
        self._syncing=False
        style={'description_width':'125px'}
        def num(label,value):
            return widgets.FloatText(value=value,description=label,style=style,layout=widgets.Layout(width='290px'),continuous_update=False)
        def choice(label,options,value):
            return widgets.Dropdown(options=options,value=value,description=label,style=style,layout=widgets.Layout(width='440px'))
        self.w_topology=choice('Geometry',['S3','T3','Nil3'],'S3')
        self.w_curvature_model=choice('Curvature action',[(label,key) for key,label in _CURVATURE_LABELS.items()],'EC_IRR')
        self.w_torsion_mode=choice('Torsion mode',[(label+' ('+key+')',key) for key,label in _TORSION_LABELS.items()],'MX')
        self.w_ny_variant=choice('NY action',[(label+' ('+key+')',key) for key,label in _NY_LABELS.items()],'FULL')
        self.w_scope=choice('Map domain',[('Radius and shape vary','joint'),('Radius varies; shape fixed','radial')],'joint')
        self.w_theta_NY=num('theta NY',1.)
        self.w_epsilon=num('epsilon > -1',0.)
        self.w_alpha_weyl=num('alpha Weyl',0.)
        self.w_V_min=num('Map V min',0.);self.w_V_max=num('Map V max',6.)
        self.w_eta_min=num('Map eta min',-3.);self.w_eta_max=num('Map eta max',3.)
        self.w_grid=widgets.IntSlider(value=61,min=21,max=121,step=10,description='Grid points',style=style,continuous_update=False)
        self.w_r_min=num('Plot r min',.001);self.w_r_max=num('Plot r max',5.)
        self.w_Veff_min=num('Plot U min',-100.);self.w_Veff_max=num('Plot U max',200.)
        self.w_r_scale=choice('r scale',['Linear','Log'],'Linear')
        self.w_Veff_scale=choice('U scale',['Linear','Symlog'],'Linear')
        self.w_point_select=choice('Selected point', [('Point 1',0),('Point 2',1),('Point 3',2)],0)
        self.w_point_V=num('Code V',4.);self.w_point_eta=num('Code eta',0.)
        self.w_point_active=widgets.Checkbox(value=True,description='Show this point')
        self.w_draw_button=widgets.Button(description='Apply & redraw',button_style='primary')
        self.w_update_potential_button=widgets.Button(description='Update plots',button_style='success')
        self.w_fit_U_button=widgets.Button(description='Fit U to curves')
        self.w_clear_cache_button=widgets.Button(description='Clear engine cache')
        self.w_status=widgets.HTML('Ready. Apply controls to draw both panels.')
        self.w_scope_note=widgets.HTML();self.w_summary=widgets.HTML()
        self.output=widgets.Output()
        self.w_draw_button.on_click(self._on_draw_clicked)
        self.w_update_potential_button.on_click(self._on_update_potential_clicked)
        self.w_fit_U_button.on_click(self._on_fit_U_clicked)
        self.w_clear_cache_button.on_click(lambda _:clear_cache())
        self.w_point_select.observe(self._point_selected,names='value')
        for w in (self.w_point_V,self.w_point_eta,self.w_point_active):w.observe(self._point_edited,names='value')
        controls=(self.w_topology,self.w_curvature_model,self.w_torsion_mode,self.w_ny_variant,self.w_scope,self.w_theta_NY,
            self.w_epsilon,self.w_alpha_weyl,self.w_V_min,self.w_V_max,self.w_eta_min,self.w_eta_max,
            self.w_grid,self.w_r_min,self.w_r_max,self.w_Veff_min,self.w_Veff_max,self.w_r_scale,self.w_Veff_scale)
        for w in controls:w.observe(self._controls_changed,names='value')
        self._read_widget_values();self._update_controls_note()

    def _set_status(self,message,color='black'):
        self.w_status.value=f'<span style="color:{color}">{html.escape(message)}</span>'

    def _update_controls_note(self):
        full=self.w_ny_variant.value=='FULL'
        self.w_theta_NY.disabled=full
        self.w_point_V.disabled=self.w_torsion_mode.value=='AX'
        self.w_point_eta.disabled=self.w_torsion_mode.value=='VT'
        domain=('The map varies both radius and shape; epsilon sets the curves only.'
                if self.w_scope.value=='joint' else 'The map varies radius at fixed epsilon. Its minimum need not minimize over both radius and shape.')
        action=('Complete NY: theta has no effect.' if full else 'Component comparison: theorem classifications are not applicable. The selected positive NY component is multiplied by theta; its potential curves are shown.')
        model=('Ricci-tracefree EC curvature includes two sectors beyond Weyl; the corresponding action has its own classification.' if self.w_curvature_model.value=='EC_TRACEFREE' else 'Irreducible EC-Weyl and LC-Weyl agree on the prescribed static family; this does not identify the unrestricted theories.')
        self.w_scope_note.value=f'<p>{domain}<br>{action}<br>{model}<br>Fixed signed torsion inputs, L=kappa=1. These are restricted potentials, not full-field vacuum classifications.</p>'

    def _controls_changed(self,change):
        self._update_controls_note()
        self._set_status('Controls changed. Apply to replace the previous plots.', '#8a5a00')

    def _point_selected(self,change):
        self.current_point_idx=change['new'];p=self.selected_points[self.current_point_idx]
        self._syncing=True
        self.w_point_V.value=p['V'];self.w_point_eta.value=p['eta'];self.w_point_active.value=p['active']
        self._syncing=False

    def _point_edited(self,change):
        if self._syncing:return
        self.selected_points[self.current_point_idx]={'V':self.w_point_V.value,'eta':self.w_point_eta.value,'active':self.w_point_active.value}
        self._set_status('Point changed. Apply to update classifications and curves.', '#8a5a00')

    def _read_widget_values(self):
        numbers=[self.w_V_min.value,self.w_V_max.value,self.w_eta_min.value,self.w_eta_max.value,
                 self.w_r_min.value,self.w_r_max.value,self.w_Veff_min.value,self.w_Veff_max.value]
        if not all(math.isfinite(x) for x in numbers):raise ValueError('Plot limits must be finite')
        if not self.w_V_min.value<self.w_V_max.value or not self.w_eta_min.value<self.w_eta_max.value:raise ValueError('Map minima must be below maxima')
        if not 0<self.w_r_min.value<self.w_r_max.value:raise ValueError('Require 0 < plot r min < max')
        if not self.w_Veff_min.value<self.w_Veff_max.value:raise ValueError('Require plot U min < max')
        for point in self.selected_points:
            classify_configuration(self.w_topology.value,point['V'],point['eta'],self.w_alpha_weyl.value,
                self.w_epsilon.value,mode=self.w_torsion_mode.value,ny_variant=self.w_ny_variant.value,theta=self.w_theta_NY.value,curvature_model=self.w_curvature_model.value)
        self.topology=self.w_topology.value;self.torsion_mode=self.w_torsion_mode.value;self.ny_variant=self.w_ny_variant.value
        self.epsilon=self.w_epsilon.value;self.alpha_weyl=self.w_alpha_weyl.value;self.theta_NY=self.w_theta_NY.value
        self.scope=self.w_scope.value
        self.curvature_model=self.w_curvature_model.value
        self.V_min,self.V_max,self.eta_min,self.eta_max=numbers[:4]
        self.r_min,self.r_max,self.Veff_min,self.Veff_max=numbers[4:]

    def classify_point(self,V,eta):
        return classify_configuration(self.topology,V,eta,self.alpha_weyl,self.epsilon,
            mode=self.torsion_mode,ny_variant=self.ny_variant,theta=self.theta_NY,curvature_model=self.curvature_model)

    def _get_potential_func(self):
        return get_potential_function(self.topology,self.torsion_mode,self.ny_variant,self._set_status,curvature_model=self.curvature_model)

    def _compute_phase_diagram(self):
        def axis(low,high,boundaries):
            return np.unique(np.r_[np.linspace(low,high,self.w_grid.value),[b for b in boundaries if low<=b<=high]])
        vs=axis(self.V_min,self.V_max,[0.]);etas=axis(self.eta_min,self.eta_max,[-2.,0.,2.])
        self.V_grid,self.eta_grid=np.meshgrid(vs,etas)
        key='global_class' if self.scope=='joint' else 'radial_class'
        self.phase_data=np.array([[CLASS_CODES[self.classify_point(V,eta)[key]] for V in vs] for eta in etas])

    def _draw_phase_diagram(self):
        ax=self.ax_phase;ax.clear()
        cmap=mcolors.ListedColormap(COLORS);norm=mcolors.BoundaryNorm(np.arange(len(COLORS)+1)-.5,len(COLORS))
        ax.pcolormesh(self.V_grid,self.eta_grid,self.phase_data,cmap=cmap,norm=norm,shading='auto')
        # Exact boundaries are not inferred by contouring categorical codes.
        if self.scope=='joint' and self.topology=='S3' and self.ny_variant=='FULL' and self.alpha_weyl<=0 and self.torsion_mode!='VT' and self.curvature_model!='EC_TRACEFREE':
            for y in [-2.,2.]:ax.axhline(y,color='#555',ls='--',lw=.8)
        if self.V_min<=0<=self.V_max:ax.axvline(0,color='#555',ls=':',lw=.8)
        for i,p in enumerate(self.selected_points):
            if p['active']:ax.scatter(p['V'],p['eta'],marker=['o','s','^'][i],s=65,facecolors='none',edgecolors=['black','#27652e','#8c3030'][i],zorder=5)
        # Degenerate sets are marked at sampled locations, not drawn as a
        # finite-width phase bounded by interpolated category values.
        deg=self.phase_data==CLASS_CODES['DEGENERATE_MINIMUM']
        if deg.any():ax.scatter(self.V_grid[deg],self.eta_grid[deg],s=18,marker='.',color='#124f82',zorder=4)
        ax.set(xlim=(self.V_min,self.V_max),ylim=(self.eta_min,self.eta_max),xlabel='Code V (ignored in AX)' if self.torsion_mode=='AX' else 'Code V',ylabel='Code eta (ignored in VT)' if self.torsion_mode=='VT' else 'Code eta')
        domain='r > 0 and shape > 0 vary' if self.scope=='joint' else f'r > 0 varies; epsilon={self.epsilon:g} fixed'
        ax.set_title(f'{_CURVATURE_LABELS[self.curvature_model]}\n{_GEOMETRY_LABELS[self.topology]}; {_TORSION_LABELS[self.torsion_mode]}; {_NY_LABELS[self.ny_variant]}\n{domain}; alpha={self.alpha_weyl:g}',fontsize=9)
        used=set(self.phase_data.flat)
        ax.legend(handles=[Patch(facecolor=COLORS[code],label=LABELS[name]) for name,code in CLASS_CODES.items() if code in used],loc='best',fontsize=8)

    def _draw_potential_plot(self):
        ax=self.ax_potential;ax.clear();func=self._get_potential_func()
        rs=(np.geomspace if self.w_r_scale.value=='Log' else np.linspace)(self.r_min,self.r_max,1000)
        self.point_results=[];outside_curves=[]
        for i,p in enumerate(self.selected_points):
            if not p['active']:continue
            result=self.classify_point(p['V'],p['eta']);self.point_results.append((i,result))
            with np.errstate(over='ignore',invalid='ignore',divide='ignore'):
                values=np.broadcast_to(np.asarray(func(rs,p['V'],p['eta'],self.theta_NY,self.epsilon,self.alpha_weyl),dtype=float),rs.shape)
            values=np.where(np.isfinite(values),values,np.nan)
            if not np.any((values>=self.Veff_min)&(values<=self.Veff_max)):
                outside_curves.append(f'P{i+1}')
            ax.plot(rs,values,color=['black','#27652e','#8c3030'][i],ls=['-','--',':'][i],label=f'P{i+1}: V={p["V"]:.8g}, eta={p["eta"]:.8g}')
            r=result['radial_r']
            if r is not None and self.r_min<=r<=self.r_max:
                ax.plot(r,func(r,p['V'],p['eta'],self.theta_NY,self.epsilon,self.alpha_weyl),'o',color=['black','#27652e','#8c3030'][i],ms=4)
        ax.axhline(0,color='#888',lw=.6)
        ax.set(xlim=(self.r_min,self.r_max),ylim=(self.Veff_min,self.Veff_max),xlabel='r (radius scale)',ylabel='U = -S on the prescribed family')
        ax.set_xscale('log' if self.w_r_scale.value=='Log' else 'linear')
        ax.set_yscale('symlog',linthresh=1) if self.w_Veff_scale.value=='Symlog' else ax.set_yscale('linear')
        tick_label=lambda value,_: format(value,'.0e') if abs(value)>=1000 or 0<abs(value)<.01 else format(value,'g')
        if self.w_Veff_scale.value=='Symlog':ax.yaxis.set_major_formatter(FuncFormatter(tick_label))
        if self.w_r_scale.value=='Log':ax.xaxis.set_major_formatter(FuncFormatter(tick_label))
        ax.set_title(f'Potential at fixed shape epsilon={self.epsilon:g}\nalpha={self.alpha_weyl:g}; plot bounds do not restrict classification',fontsize=10)
        if self.point_results:ax.legend(fontsize=8)
        if outside_curves:
            ax.text(.02,.02,'Outside U window: '+', '.join(outside_curves)+'\nUse Fit U to curves; Symlog helps with wide ranges.',
                    transform=ax.transAxes,fontsize=8,va='bottom',bbox={'facecolor':'white','alpha':.9,'edgecolor':'#ddd'})
        ax.grid(alpha=.25)
        def fmt(value):
            return '—' if value is None else format(value,'.17g')
        rows=[]
        for i,r in self.point_results:
            radius=fmt(r['radial_r'])
            if r['radial_r'] is not None and not self.r_min<=r['radial_r']<=self.r_max:radius+=' (outside plot: r)'
            radial_value=fmt(r['radial_infimum'])
            if r['radial_r'] is not None and r['radial_infimum'] is not None and not self.Veff_min<=r['radial_infimum']<=self.Veff_max:
                radial_value+=' (outside plot: U)'
            cells=[f'P{i+1}',fmt(r['V_input']),fmt(r['eta_input']),LABELS[r['global_class']],fmt(r['global_infimum']),
                   LABELS[r['radial_class']],radial_value,radius,fmt(r['radial_local_min_r']),r['numeric_status']]
            rows.append('<tr>'+''.join('<td style="padding:5px;border:1px solid #ddd">'+html.escape(c)+'</td>' for c in cells)+'</tr>')
        heads=['Point','Input V','Input eta','Radius + shape class','Radius + shape infimum','Fixed-shape class','Fixed-shape infimum','Fixed-shape minimizer r','Local radial min r','Numeric values']
        self.w_summary.value='<table style="font-size:12px;border-collapse:collapse"><tr>'+''.join('<th>'+h+'</th>' for h in heads)+'</tr>'+''.join(rows)+'</table><p>Inputs above retain float precision. AX sets effective V=0; VT sets effective eta=0. All modes allow zero amplitudes. A local radius minimum does not establish a minimum over radius and shape.</p>'

    def _draw_all(self):
        with self.output:
            clear_output(wait=True)
            if self.fig is not None:plt.close(self.fig)
            self.fig,(self.ax_phase,self.ax_potential)=plt.subplots(1,2,figsize=(15,5.8),layout='constrained')
            self._draw_phase_diagram();self._draw_potential_plot()
            self.fig.canvas.mpl_connect('button_press_event',self._on_click)
            plt.show()

    def _on_draw_clicked(self,_=None):
        try:
            self._read_widget_values();self._compute_phase_diagram();self._draw_all()
            self._set_status('Updated. '+get_cache_status(),'#27652e')
        except (ValueError,ArithmeticError) as e:
            self._set_status('Not applied; previous plots unchanged: '+str(e),'#a00')

    def _on_update_potential_clicked(self,_=None):
        self._on_draw_clicked()

    def _on_fit_U_clicked(self,_=None):
        """Fit the sampled curve range for display only, preserving classification."""
        try:
            self._read_widget_values();func=self._get_potential_func()
            rs=(np.geomspace if self.w_r_scale.value=='Log' else np.linspace)(self.r_min,self.r_max,1000)
            samples=[]
            for point in self.selected_points:
                if point['active']:
                    with np.errstate(over='ignore',invalid='ignore',divide='ignore'):
                        values=np.asarray(func(rs,point['V'],point['eta'],self.theta_NY,self.epsilon,self.alpha_weyl),dtype=float).ravel()
                    samples.extend(values[np.isfinite(values)])
            if not samples:raise ValueError('No finite active curve samples in the r window')
            low=min(0.,min(samples));high=max(0.,max(samples))
            margin=max(abs(low),abs(high),1.)*.05
            self.w_Veff_min.value=max(-sys.float_info.max,low-margin)
            self.w_Veff_max.value=min(sys.float_info.max,high+margin)
            self._on_draw_clicked()
        except (ValueError,ArithmeticError) as e:
            self._set_status('Cannot fit U: '+str(e),'#a00')

    def _on_click(self,event):
        if event.inaxes!=self.ax_phase or event.xdata is None or event.ydata is None:return
        self.w_point_V.value=float(event.xdata);self.w_point_eta.value=float(event.ydata)
        self._on_draw_clicked()

    def display(self):
        config=widgets.VBox([self.w_topology,self.w_curvature_model,self.w_torsion_mode,self.w_ny_variant,self.w_scope,self.w_theta_NY,self.w_epsilon,self.w_alpha_weyl])
        ranges=widgets.VBox([self.w_V_min,self.w_V_max,self.w_eta_min,self.w_eta_max,self.w_grid,self.w_r_min,self.w_r_max,self.w_Veff_min,self.w_Veff_max,self.w_r_scale,self.w_Veff_scale])
        points=widgets.VBox([self.w_point_select,self.w_point_V,self.w_point_eta,self.w_point_active])
        display(self.w_scope_note,widgets.HBox([config,ranges,points]),widgets.HBox([self.w_draw_button,self.w_update_potential_button,self.w_fit_U_button,self.w_clear_cache_button]),self.w_status,self.output,self.w_summary)
