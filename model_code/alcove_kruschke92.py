"""ALCOVE — standard Kruschke (1992) / catlearn 'ex-ALCOVE' variant.

The canonical ALCOVE as published in Kruschke (1992, Psych Review
99:22-44) and fitted to SHJ in catlearn's 'nosof94exalcove_opt' archive
(SSD ~.1419 -- the standard ALCOVE benchmark for comparison against the
BN variant's ~.061).  See alcove_bn94.py for the fitted variant.

ARCHITECTURE (three-layer feedforward, Kruschke 1992):
    input dims --[attention alpha_f]--> exemplar nodes --[assoc w_kj]-->
    category outputs --[decision rule]--> response probabilities

  - 8 exemplar nodes, one per training stimulus; activation =
    exp(-c * attention-weighted generalized-Minkowski distance) [Eq. 1]
  - 2 category outputs, linear: o_k = sum_j w_kj a_j [Eq. 2]
  - w and alpha learned by gradient descent on sum-squared error vs a
    "humble" teacher

PER-TRIAL FLOW (trial()):
    1. _forward  -> distances d, exemplar activations a, outputs o
    2. build humble teacher t (absval=-1 convention)
    3. pe = t - o (prediction error)
    4. _learn    -> association-weight update + attention delta
    5. unconstrained attention update (clip at 0 only)

TEACHER    : humble; absent-category target = -1 (absval=-1).  "Humble":
             t_k = max(1,o_k) for the correct category, t_k =
             min(-1,o_k) for the absent -- outputs already past the
             target are left alone.
ATTENTION  : UNconstrained -- clip at 0 only; NO sum-to-1 enforcement.
             Total attention can grow without bound (observed: final
             alpha ~(9,19,15) on Type V -- attention inflates massively
             once unconstrained).
READOUT    : exponential-ratio (Luce) rule, Kruschke 1992 Eq. 3:
                 P(R_j|x) = exp(phi * o_j) / sum_k exp(phi * o_k)
             phi = response-scaling constant (probability mapping).
PARAMS     : cfg = {c=8.792, phi=20, lam_att=0.9363, lam_assoc=0.99,
             r=1, q=1}  (catlearn nosof94exalcove_opt fit; la/lw renamed
             lam_att/lam_assoc for consistency with alcove_bn94; r,q are
             the generalized-Minkowski exponents, canonical 1)
DIFFERS    : vs alcove_bn94.py -- absval=-1 (not 0) teacher,
             UNconstrained (not sum-to-1) attention, exponential-ratio
             (not background-noise) readout, adds phi + r/q params.
SOURCE     : numpy port of catlearn src/slpalcove.cpp with dec='ER',
             humble=TRUE, attcon=FALSE (see
             nosofsky1994_replication/reference/slpalcove.cpp); params
             from nosof94exalcove_opt cached fit
CHECKSUM   : verify() -> checksums.json['alcove_kruschke92']
"""

import numpy as np

# catlearn nosof94exalcove_opt cached fit:
#   c, phi       specificity + response scaling (Eqs. 1, 3)
#   lam_att      attention learning rate (catlearn 'la')
#   lam_assoc    association learning rate (catlearn 'lw')
#   r, q         generalized-Minkowski exponents (canonical 1,1)
DEFAULTS = dict(c=8.792, phi=20., lam_att=.9363, lam_assoc=.99,
                r=1, q=1)


def _cfg(cfg):
    return {**DEFAULTS, **(cfg or {})}


# >>> shared: typev_spec >>>
# The 8 stimuli: vertices of the binary cube, d1 varying slowest.
STIMULI = np.array(
    [[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1],
     [1, 0, 0], [1, 0, 1], [1, 1, 0], [1, 1, 1]], dtype=float)

# SHJ Type V labels: A = {000,001,010,111}, B = {011,100,101,110}.
LABELS_TV = np.array([0, 0, 0, 1, 1, 1, 1, 0])     # A=0, B=1
HELD = 5                                          # 101 held out
TRAIN = np.array([i for i in range(8) if i != HELD])
# <<< shared: typev_spec <<<


def init(rng, cfg):
    """Uniform attention init (1/3 per dim -- the standard starting
    point even though attention is unconstrained here), zero association
    weights (chance-level outputs).  rng unused; uniform signature."""
    return {'alpha': np.full(3, 1 / 3), 'w': np.zeros((2, 8))}


# >>> shared: alcove_core >>>
def _forward(params, x, cfg):
    """Kruschke 1992 Eqs. 1-2: distances -> exemplar activations ->
    category outputs.

      d[j,f] = |e_jf - x_f|                       per-dimension distance
      dist_j = ( sum_f alpha_f * d[j,f]^r )^(1/r)  generalized Minkowski
      a_j    = exp(-c * dist_j^q)                  exemplar activation
      o_k    = sum_j w[k,j] * a_j                  linear category output

    r=q=1 (attention-weighted city-block, exponential similarity) is
    the canonical case; r,q are exposed via cfg for generality."""
    d = np.abs(STIMULI - x[None, :])                  # (8, 3) per-dim dist
    if cfg.get('r', 1) == 1:
        dist = (d * params['alpha'][None, :]).sum(1)
    else:
        dist = ((d ** cfg['r']) * params['alpha'][None, :]).sum(1) \
            ** (1.0 / cfg['r'])
    a = np.exp(-cfg['c'] * dist ** cfg.get('q', 1))
    return d, a, params['w'] @ a
# <<< shared: alcove_core <<<

# >>> shared: alcove_learn >>>
def _learn(params, d, a, pe, cfg):
    """Delta-rule association update (in place) + attention gradient,
    BEFORE the variant-specific attention constraint is applied.

      w_kj    += lam_assoc * pe_k * a_j          (nosof94 Eq. 5)
      bp_j     = a_j * sum_k w_old[k,j] pe_k     error backprop to hidden
      dalpha_f = -lam_att * c * sum_j d[j,f] bp_j   (nosof94 Eq. 6)

    bp uses the PRE-update weights (w_old), matching the catlearn
    ordering: the attention gradient sees the weights that produced
    this trial's error, not the corrected ones.  d and a come from
    _forward.  Returns the raw attention delta; the caller applies
    its variant's constraint."""
    w_old = params['w'].copy()
    params['w'] += cfg['lam_assoc'] * pe[:, None] * a[None, :]
    bp = a * (w_old.T @ pe)
    return -cfg['lam_att'] * cfg['c'] * (d * bp[:, None]).sum(0)
# <<< shared: alcove_learn <<<


def trial(params, x, y, cfg):
    """One supervised trial, standard variant: forward -> humble teacher
    (absval=-1) -> error -> association & attention updates, attention
    clipped at 0 but otherwise free to grow."""
    cfg = _cfg(cfg)
    d, a, o = _forward(params, x, cfg)
    # humble teacher with absval=-1: correct-cat target = max(1,o),
    # absent-cat target = min(-1,o)
    t = np.where(np.arange(2) == y,
                 np.maximum(1.0, o), np.minimum(-1.0, o))
    pe = t - o                                        # prediction error
    da = _learn(params, d, a, pe, cfg)
    # UNconstrained attention: no zero-sum, no renormalize -- clip only
    params['alpha'] = np.maximum(params['alpha'] + da, 0.0)


def response(params, x, cfg):
    """Exponential-ratio (Luce) choice rule, Kruschke 1992 Eq. 3:
    P(R_j|x) = exp(phi*o_j) / sum_k exp(phi*o_k).  phi=20 (fitted) is a
    sharp readout -- near-argmax over category outputs."""
    cfg = _cfg(cfg)
    _, _, o = _forward(params, x, cfg)
    e = np.exp(cfg['phi'] * o)
    return e / e.sum()


# ---- built-in verification probe ----------------------------------------
VERIFY_CFG = dict(c=8.792, phi=20., lam_att=.9363, lam_assoc=.99,
                  r=1, q=1)


def verify():
    """Type V transfer probe -- identical schedule to alcove_bn94.verify
    (16 blocks x 14 trials over the 7 trained items; block 1 = two
    independent shuffles, later blocks = one shuffle of the 14-trial
    multiset; P(B|T=101) after training; n=200, seed 7624) so the two
    variants are directly comparable.  The contrast -- constrained
    alpha sums to 1 vs unconstrained alpha inflating to ~(9,19,15) --
    is itself the mechanistic signature of the two variants."""
    rng = np.random.default_rng(7624)
    n, blocks, trials = 200, 16, 14
    two = np.concatenate([TRAIN, TRAIN])
    pB = np.empty(n)
    alpha_end = np.zeros((n, 3))
    for s in range(n):
        prm = init(rng, VERIFY_CFG)
        seq = np.empty(blocks * trials, dtype=int)
        for blk in range(blocks):
            if blk == 0:
                seq[:trials] = np.concatenate(
                    [rng.permutation(TRAIN), rng.permutation(TRAIN)])
            else:
                seq[blk * trials:(blk + 1) * trials] = \
                    two[rng.permutation(trials)]
        for st in seq:
            trial(prm, STIMULI[st], LABELS_TV[st], VERIFY_CFG)
        pB[s] = response(prm, STIMULI[HELD], VERIFY_CFG)[1]
        alpha_end[s] = prm['alpha']
    return {'mean_pB': float(pB.mean()),
            'final_alpha': alpha_end.mean(0).tolist(),
            'n': n, 'seed': 7624}


if __name__ == '__main__':
    print(verify())
