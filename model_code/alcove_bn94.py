"""ALCOVE — Nosofsky, Gluck, Palmeri, McKinley & Glauthier (1994) variant.

The background-noise ("BN") version of ALCOVE used for the published
Shepard-Hovland-Jenkins fit: ~95.5% variance explained (SSD ~0.061,
blocks 1-16).  This is NOT the vanilla Kruschke (1992) model -- three
conventions differ (see DIFFERS); the standard variant lives in
alcove_kruschke92.py.

ARCHITECTURE (three-layer feedforward, Kruschke 1992):
    input dims --[attention alpha_f]--> exemplar nodes --[assoc w_kj]-->
    category outputs --[decision rule]--> response probabilities

  - 8 exemplar ("hidden") nodes, one per training stimulus; activation
    is similarity = exp(-c * attention-weighted city-block distance)
    [Kruschke 1992, Eq. 1; r=q=1]
  - 2 category ("output") nodes, linear: o_k = sum_j w_kj a_j [Eq. 2]
  - association weights w and attention strengths alpha are BOTH learned
    by gradient descent on sum-squared error vs a "humble" teacher

PER-TRIAL FLOW (trial()):
    1. _forward  -> distances d, exemplar activations a, outputs o
    2. build humble teacher t (absval=0 convention -- see below)
    3. pe = t - o (prediction error)
    4. _learn    -> association-weight update + attention delta
    5. constrained attention update (sum-to-1) -- BN-ALCOVE specific

TEACHER    : humble; absent-category target = 0 (absval=0, NOT -1).
             "Humble" means the teacher only corrects when the output
             is on the wrong side of the target: t_k = max(1,o_k) for
             the correct category (already-above-1 outputs are left
             alone) and t_k = min(0,o_k) for the absent category.
             
ATTENTION  : constrained to sum to 1 after every trial (zero-sum deltas,
             clip >= 0, renormalize).  This is the "attention as a
             limited resource" assumption used for the 1994 fit.
             
READOUT    : background-noise decision rule (Nosofsky et al. 1994,
             Eq. 3):
                 P(R_j|x) = (max(0,o_j)+b) / (sum_k max(0,o_k) + K*b)
             b = "background noise" baseline activation.  NOT the
             standard exponential-ratio rule; the max(0,.) rectifier is
             required though the printed equation omits it (see
             nosofsky1994_replication/AUDIT.md for how this was found).
             
PARAMS     : cfg = {c=6.33, b=0.011, lam_att=0.409, lam_assoc=0.179}
             (published Nosofsky et al. 1994 fit values)
             
DIFFERS    : vs alcove_kruschke92.py -- absval=0 (not -1) teacher,
             constrained (not free) attention, background-noise (not
             exponential-ratio) readout, no phi parameter.
             
SOURCE     : numpy port of catlearn slpALCOVE configured 'nosof94bnalcove'
             (see nosofsky1994_replication/bn_alcove.py; C++ reference at
             nosofsky1994_replication/reference/slpalcove.cpp)
             
CHECKSUM   : verify() -> checksums.json['alcove_bn94']
"""

import numpy as np

# Published BN-ALCOVE parameters (Nosofsky et al. 1994, Table 2-ish):
#   c         exemplar-node specificity (steepness of similarity falloff)
#   b         background noise in the decision rule
#   lam_att   attention-strength learning rate
#   lam_assoc association-weight learning rate
DEFAULTS = dict(c=6.33, b=.011, lam_att=.409, lam_assoc=.179)


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
    """Initial state: uniform attention (1/3 per dim; the sum-to-1
    constraint makes uniform the only natural start), zero association
    weights (no prior exemplar->category knowledge -> outputs start at
    0 -> chance-level responding).  rng unused -- deterministic init;
    kept in the signature for interface uniformity."""
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
    """One supervised trial for the BN variant: forward -> humble
    teacher -> error -> association & attention updates with the
    sum-to-1 constraint on attention."""
    cfg = _cfg(cfg)
    d, a, o = _forward(params, x, cfg)
    # humble teacher with absval=0: correct-cat target = max(1, o),
    # absent-cat target = min(0, o)  -- a "don't overshoot" teacher.
    t = np.where(np.arange(2) == y,
                 np.maximum(1.0, o), np.minimum(0.0, o))
    pe = t - o                                        # prediction error
    da = _learn(params, d, a, pe, cfg)
    # BN constraint: attention is a fixed resource.  Zero-sum the delta,
    # clip at 0, renormalize -- total attention stays 1 after every trial.
    da -= da.mean()
    params['alpha'] = np.maximum(params['alpha'] + da, 0.0)
    params['alpha'] /= params['alpha'].sum()


def response(params, x, cfg):
    """Background-noise decision rule (nosof94 Eq. 3):
    P(R_j|x) = (max(0,o_j) + b) / (sum_k max(0,o_k) + K*b),  K=2 cats.
    Negative outputs are rectified BEFORE the b-offset (the printed
    equation omits max(0,.) but the catlearn C++ implements it; needed
    to keep probabilities in [0,1] when outputs go negative)."""
    cfg = _cfg(cfg)
    _, _, o = _forward(params, x, cfg)
    num = np.maximum(o, 0.0)
    return (num + cfg['b']) / (num.sum() + 2 * cfg['b'])


# ---- built-in verification probe ----------------------------------------
VERIFY_CFG = dict(c=6.33, b=.011, lam_att=.409, lam_assoc=.179)


def verify():
    """Type V transfer probe, replicating the nosof94 presentation
    schedule exactly:

      * 16 blocks x 14 trials.  Block 1 = two INDEPENDENT shuffled
        passes through the 7 training items.  Each later block = one
        shuffle of the 14-trial multiset (each item appearing twice,
        order randomized) -- this is the "blocks 1 and 2 contained 8
        trials" convention of Nosofsky et al. rescaled to the 7-item
        Type V subset.
      * After training, probe P(B | T=101), the held-out item.
      * n=200 simulated subjects, seed 7624.

    Matches typev_experiment/typev_transfer_probe.py (n=500 -> .138);
    this n=200 version is the checksummed fast probe."""
    rng = np.random.default_rng(7624)
    n, blocks, trials = 200, 16, 14
    two = np.concatenate([TRAIN, TRAIN])   # the 14-trial multiset
    pB = np.empty(n)
    alpha_end = np.zeros((n, 3))
    for s in range(n):
        prm = init(rng, VERIFY_CFG)
        # pre-build this subject's full trial sequence, block by block
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
