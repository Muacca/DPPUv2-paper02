"""Paper02 classifications at fixed signed torsion inputs, L and kappa.

Joint results implement Sections 7--8 for complete NY on r,x>0.
Radial results concern a fixed admissible shape and U=p*(A*r^3+B*r+D/r).
Inputs are binary floating-point values: zero/boundary tests are exact for
those inputs, with no decimal rounding, epsilon snapping or radius cutoff.
TT/REE are different actions and are deliberately outside this classifier.
"""
from decimal import Decimal, localcontext
from functools import lru_cache
from fractions import Fraction
from ..curvature.rc_weyl import CURVATURE_MODELS
import math

LABELS = {
    'FINITE_MINIMUM': 'Finite minimum',
    'UNATTAINED_INFIMUM': 'Unattained infimum',
    'DEGENERATE_MINIMUM': 'Degenerate minimum set',
    'UNBOUNDED_BELOW': 'Unbounded below',
    'NOT_APPLICABLE': 'Outside complete-NY classification',
    'NUMERIC_UNRESOLVED': 'Numerically unresolved',
}
CLASS_CODES = {name: i for i, name in enumerate(LABELS)}
COLORS = ['#81bda4', '#e4c77a', '#80aad4', '#da8d88', '#d3d3d3', '#c5a0d4']


def _d(x):
    return Decimal.from_float(float(x))


@lru_cache(maxsize=128)
def _shape(epsilon):
    with localcontext() as ctx:
        ctx.prec = 80
        e = _d(epsilon)
        s = 1 + e
        x = s ** (-Decimal(2) / 3)
        # Stable even when epsilon is tiny: do not subtract nearly equal x,1.
        one_minus_x3 = e * (e + 2) / (s*s)
        dx = -one_minus_x3 / (x*x + x + 1)
        return x, dx, one_minus_x3


def classify_configuration(topology, V, eta, alpha=0., epsilon=0., *,
                           mode='MX', ny_variant='FULL', theta=1., L=1., kappa=1.,
                           curvature_model='EC_IRR'):
    """Return separate joint/radial outcomes and finite minimizer data.

    ``radial_local_min_r`` may exist while the radial/global infimum is -inf.
    Numeric values that under/overflow float are left empty and flagged; the
    categorical theorem result remains valid. No finite plot window is used.
    """
    if topology not in ('S3', 'T3', 'Nil3') or mode not in ('MX', 'AX', 'VT'):
        raise ValueError('Unknown topology or torsion mode')
    if curvature_model not in CURVATURE_MODELS:
        raise ValueError('Unknown curvature model')
    if ny_variant not in ('FULL', 'TT', 'REE'):
        raise ValueError('Unknown NY action')
    V, eta, alpha, epsilon, theta, L, kappa = map(float, (V,eta,alpha,epsilon,theta,L,kappa))
    if not all(math.isfinite(x) for x in (V,eta,alpha,epsilon,theta,L,kappa)):
        raise ValueError('Inputs must be finite')
    if epsilon <= -1 or L <= 0 or kappa <= 0:
        raise ValueError('Require epsilon > -1, L > 0 and kappa > 0')
    V_effective = 0. if mode == 'AX' else V
    eta_effective = 0. if mode == 'VT' else eta
    result = dict(topology=topology, mode=mode, ny_variant=ny_variant, curvature_model=curvature_model,
                  V_input=V, eta_input=eta, V=V_effective, eta=eta_effective,
                  alpha=alpha, epsilon=epsilon, theta=theta, L=L, kappa=kappa,
                  global_class='NOT_APPLICABLE', global_infimum=None,
                  global_r=None, global_x=None, global_limit='',
                  radial_class='NOT_APPLICABLE', radial_infimum=None,
                  radial_r=None, radial_limit='', radial_local_min_r=None,
                  numeric_status='OK')
    if ny_variant != 'FULL':
        result['global_limit'] = result['radial_limit'] = 'different_action'
        return result

    def number(key, value):
        f = float(value)
        if not math.isfinite(f) or (f == 0 and value != 0):
            result['numeric_status'] = 'VALUE_OUT_OF_FLOAT_RANGE'
        else:
            result[key] = f

    with localcontext() as ctx:
        ctx.prec = 80
        v, h, a, k = map(_d, (V_effective, eta_effective, alpha, kappa))
        x, dx, omx3 = _shape(epsilon)
        A = v*v
        beta = 9*h*h
        beta_sign = 0 if h == 0 else 1
        gap = 9*(2-abs(h))*(2+abs(h))
        if curvature_model == 'EC_TRACEFREE':
            # Exact signs for the supplied binary floats, including cancellation.
            fv, fh, fa, fk = map(Fraction, (V_effective, eta_effective, alpha, kappa))
            beta_exact = fh*fh*(9-16*fk*fk*fa*fv*fv)
            gap_exact = 36-beta_exact
            beta = Decimal(beta_exact.numerator)/Decimal(beta_exact.denominator)
            gap = Decimal(gap_exact.numerator)/Decimal(gap_exact.denominator)
            beta_sign = (beta_exact > 0)-(beta_exact < 0)
        cv = {'S3': math.pi**2/4, 'T3': (2*math.pi)**3, 'Nil3': (2*math.pi)**4}[topology]
        p = _d(cv)*_d(L)/(3*k*k)
        # Joint domain: all positive r and x, not just the plotted shape.
        g, limit, inf = 'UNATTAINED_INFIMUM', 'r_to_zero', Decimal(0)
        if topology == 'S3':
            if a > 0:
                g, limit, inf = 'UNBOUNDED_BELOW', 'r_to_zero_at_nonround_shape', None
            elif gap > 0:
                if v == 0:
                    g, limit, inf = 'UNBOUNDED_BELOW', 'r_to_infinity_on_round', None
                else:
                    g, limit = 'FINITE_MINIMUM', 'unique_round_point'
                    radius = (gap/3).sqrt()/abs(v)
                    inf = -2*p*A*radius**3
                    number('global_r', radius);result['global_x'] = 1.
            elif v == 0 and gap == 0:
                g, limit = 'DEGENERATE_MINIMUM', 'all_r_on_round'
        elif topology == 'T3':
            if beta_sign < 0:
                radius = (-beta/(3*A)).sqrt()
                g, limit = 'DEGENERATE_MINIMUM', 'fixed_r_all_shape'
                inf = -2*p*A*radius**3
                number('global_r', radius)
            elif v == 0 and h == 0:
                g, limit = 'DEGENERATE_MINIMUM', 'all_r_and_shape'
        elif a > 0:
            g, limit, inf = 'UNBOUNDED_BELOW', 'r_to_zero_at_fixed_shape', None
        else:
            limit = 'r_and_shape_to_zero'
        result.update(global_class=g, global_limit=limit)
        if inf is None:result['global_infimum'] = -math.inf
        else:number('global_infimum', inf)

        # Fixed shape: solve 3*A*y^2+B*y-D=0, y=r^2, on y>0.
        if topology == 'S3':
            b0 = -gap
            bs = 12*dx*dx*(x*x+2*x+3)
            B, D = b0+bs, -1024*k*k*a*x*x*omx3*omx3
            uncertain_b = bs != 0 and b0 != 0 and abs(B) <= Decimal('1e-65')*(abs(b0)+abs(bs))
        elif topology == 'T3':
            B, D, uncertain_b = beta, Decimal(0), False
        else:
            B, D = beta+Decimal('0.75')*x**4, -4*k*k*a*x**8
            uncertain_b = beta < 0 and abs(B) <= Decimal('1e-65')*(abs(beta)+Decimal('0.75')*x**4)
        if uncertain_b and D == 0:
            result.update(radial_class='NUMERIC_UNRESOLVED', numeric_status='SHAPE_BOUNDARY_UNRESOLVED')
            return result
        rclass, rlimit, rinf, y = 'UNATTAINED_INFIMUM', 'r_to_zero', Decimal(0), None
        if D < 0:
            rclass, rlimit, rinf = 'UNBOUNDED_BELOW', 'r_to_zero', None
            if A > 0 and B < 0:
                disc = B*B+12*A*D
                scale = B*B+abs(12*A*D)
                if abs(disc) <= Decimal('1e-65')*scale:
                    result['numeric_status'] = 'LOCAL_STATIONARY_BOUNDARY_UNRESOLVED'
                elif disc > 0:
                    number('radial_local_min_r', ((-B+disc.sqrt())/(6*A)).sqrt())
        elif D > 0:
            if A > 0:
                root = (B*B+12*A*D).sqrt()
                y = 2*D/(B+root) if B >= 0 else (-B+root)/(6*A)
            elif B > 0:y = D/B
            elif B == 0:rlimit = 'r_to_infinity'
            else:rclass, rlimit, rinf = 'UNBOUNDED_BELOW', 'r_to_infinity', None
        elif A > 0 and B < 0:y = -B/(3*A)
        elif A == 0:
            if B < 0:rclass, rlimit, rinf = 'UNBOUNDED_BELOW', 'r_to_infinity', None
            elif B == 0:rclass, rlimit = 'DEGENERATE_MINIMUM', 'all_r'
        if y is not None:
            r = y.sqrt()
            rclass, rlimit = 'FINITE_MINIMUM', 'unique_radial_point'
            rinf = p*(A*r**3+B*r+D/r)
            number('radial_r', r);number('radial_local_min_r', r)
        result.update(radial_class=rclass, radial_limit=rlimit)
        if rinf is None:result['radial_infimum'] = -math.inf
        else:number('radial_infimum', rinf)
    return result
