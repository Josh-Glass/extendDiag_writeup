"""DIVA — divergent autoencoder (Kurtz 2007; canonical profile).

DEFAULTS ARE THE KURTZ-CANONICAL PROFILE (meeting with K. Kurtz,
2026-10-25): pm1 coding, sigmoid hidden, LINEAR outputs, bare-Luce
inverse-SSE readout with the 1e-7 floor, uniform-wrange init, free
params {n_hid, lr, wr, beta}.  catlearn/slpDIVA conventions remain
available as config options (see READOUT/OUT_ACT) and are what the
frozen checksum probe exercises.

DIVA recasts supervised classification as reconstructive learning:
there are no category output units at all.  Each category owns a
decoder "channel" trained to reconstruct the stimulus; a test item is
classified by which channel reconstructs it best.  On each supervised
trial only the TRUE category's channel (plus the shared encoder) is
updated -- the channels diverge, hence the name.

ARCHITECTURE (feedforward, Kurtz 2007 Fig. 1):
    input (+bias) --[iw encoder]--> shared hidden (+bias)
        --[ow[:,:,k] decoder k]--> reconstruction on channel k
    channel error = weighted SSE(reconstruction_k, teacher); a choice
    rule maps the per-channel errors to response probabilities

  - shared hidden layer: sigmoid (canonical) or tanh via cfg
  - K=2 decoder channels, each a feature-sized reconstruction head
  - teacher = the input itself (raw under canonical linear outs;
    rescaled to the output range under sigmoid); the category label
    only selects WHICH channel receives the update

PER-TRIAL FLOW (trial()):
    1. forward     -> channel outputs, hidden acts, preactivations
    2. decode_tgt  -> targets rescaled to the output activation's range
    3. backprop    -> updates decoder ow[:,:,y] + shared encoder iw;
                      the other channel's weights are untouched
    4. response()  -> separate call; readout only, no learning

TEACHER    : the input itself, rescaled to the output activation's
             range (sigmoid -> 0/1, tanh -> -1/+1; decode_tgt enforces
             the match -- a mismatched pair biases the gradients).
             out_act='linear' -> teacher = raw coded input (no rescale;
             linear outputs can reach any value).
             
INPUTS     : coding='pm1' -> -1/+1 inputs (canonical); '01' -> 0/1.

INIT       : 'uniform' ~ U(wc-wr, wc+wr) [canonical; catlearn
             wts_range/wts_center]; 'normal' ~ N(wc,wr); 'xavier' ->
             Glorot-uniform from fan-in/out (wr/wc ignored).
             Draw order: encoder weights (iw) then decoder weights (ow).
             
READOUT    : readout='luce'  -> P(k) = (1/SSE_k) / sum_k (1/SSE_k)
             [DEFAULT + PUBLISHED rule: Kurtz 2007 Eq.1, confirmed in
             the 2026-10-25 meeting; Conaway & Kurtz fits use 4 params
             (nhid/lr/wr/beta, no phi); Conaway's MATLAB port
             github.com/nolanbconaway/DIVA implements this form, with
             the same 1e-7 error floor.  phi is IGNORED in luce mode --
             no phi setting recovers bare Luce from the exp map
             (phi=0 -> uniform).]
             readout='exp'   -> P(k) ~ exp(phi * (1/SSE_k))   [catlearn
             slpDIVA; phi is a response-mapping constant grafted from
             ALCOVE's Kruschke 1992 Eq.3 -- NOT in published DIVA.
             Kept as the legacy/exploratory option.]
             SSE is feature-weighted either way: beta=0 -> uniform
             1/n_feat; beta>0 -> focusing weights exp(beta*|o0-o1|)
             per feature, Conaway & Kurtz 2014 (two-category form).
             
PARAMS     : cfg = {n_hid=4, lr=0.15, phi=6.5, beta=0.0, wr=1.0, wc=0.0,
             readout='luce'|'exp',
             activation='sigmoid'|'tanh', coding='pm1'|'01',
             init='uniform'|'normal'|'xavier',
             out_act='linear'|'sigmoid'}
             DEFAULTS = the Kurtz-canonical profile.  Kurtz's own
             free-parameter list (meeting 2026-10-25):
             {#hids, lrate, wrange, beta} -- i.e., phi is NOT a DIVA
             parameter (catlearn graft; ignored under readout='luce').
             
OUT_ACT    : default 'linear' -- the Kurtz-stated canonical (meeting
             2026-10-25: "linear outs without clipping [debatable?]").
             Empirically supported: on the 6-type SHJ battery it is the
             only variant that does not anti-learn Type VI.
             Architecturally self-consistent:
             linear outs reconstruct the raw +-1 coded input, so
             teacher = input with no rescaling.
               'sigmoid' catlearn continuous=FALSE path (the SHJ
               convention we ported) + nconaway's shipped START.m
               example -- kept as the legacy/exploratory option.
             
CROSS-REF  : architecture, backprop, init, coding, and focusing all
             agree with Conaway's MATLAB port
             (github.com/nolanbconaway/DIVA); see READOUT for the
             exp-vs-luce arbitration.  That port is unseeded
             (rng('shuffle')), and its README claims cross-entropy for
             sigmoid outputs though BACKPROP.m uses the SSE delta
             2(o-t) -- we match its code.
             
SOURCE     : numpy port of catlearn's slpDIVA (Wills' R package);
             cross-checked against Conaway's MATLAB port (CROSS-REF).
             Verified on the SHJ Type V transfer probe.

SELF-CHECK : run this file -- verify() prints the deterministic Type V
             probe signature (expected: mean_pB ~ .135, fracB = 0).
"""

import numpy as np

# Config keys (DEFAULTS below = the Kurtz-canonical profile; the
# catlearn/legacy alternatives are shown for each option):

#   n_hid      shared hidden units (the model's main capacity knob --
#              Kurtz 2007: use the smallest n that still converges)

#   lr         backprop learning rate (catlearn default .15)

#   phi        response-mapping constant, readout='exp' only (catlearn
#              grafts ALCOVE's Kruschke-92 Eq.3 onto the inverse-SSE
#              rule; ignored under readout='luce')

#   beta       feature-focusing sharpness; 0 = focusing off
#              (Conaway & Kurtz 2014)

#   wr, wc     init half-width / center (catlearn wts_range/wts_center)

#   readout    'luce' (canonical default -- published Kurtz 2007 Eq.1)
#              | 'exp' (catlearn; phi applies only here)

#   activation 'sigmoid' (canonical) | 'tanh'

#   coding     'pm1' (canonical -1/+1) | '01'

#   init       'uniform' (canonical) | 'normal' | 'xavier'

#   out_act    'linear' (canonical default -- Kurtz-stated, meeting
#              2026-10: "linear outs without clipping"; nconaway
#              outputrule='linear', catlearn continuous=TRUE) |
#              'sigmoid' (catlearn continuous=FALSE + nconaway's
#              shipped START.m).  Linear -> teacher = raw coded input
#              (decode_tgt passes x).

DEFAULTS = dict(n_hid=4, lr=.15, phi=6.5, beta=0.0, wr=1.0, wc=0.0,
                readout='luce',           # canonical (Kurtz 2007 Eq.1)
                activation='sigmoid', coding='pm1', init='uniform',
                out_act='linear')         # canonical (Kurtz meeting)


def _cfg(cfg):
    return {**DEFAULTS, **(cfg or {})}


# >>> shared: diva_helpers >>>
def _sig(z):
    """Logistic squashing function; canonical hidden nonlinearity and
    the output nonlinearity unless out_act='linear' (identity output;
    tanh is the only alternative offered via ACT)."""
    return 1 / (1 + np.exp(-z))


# Activation lookup: each entry is (squashing function, its derivative
# wrt the preactivation).  The derivative is used ONLY at the hidden
# layer in backprop -- see the note there about the linear-output
# delta convention shared by catlearn and nconaway.
ACT = {
    'sigmoid': (_sig, lambda z: _sig(z) * (1 - _sig(z))),
    'tanh':    (np.tanh, lambda z: 1 - np.tanh(z) ** 2),
}


def encode(s, coding):
    """Spec 0/1 features -> network inputs: 'pm1' remaps to -1/+1
    (canonical; catlearn requires dichotomous inputs in -1/+1 format),
    '01' keeps the features as-is."""
    return s * 2 - 1 if coding == 'pm1' else s


def decode_tgt(x, coding, activation, out_act='linear'):
    """Network inputs -> reconstruction targets matched to the output
    activation's range: linear targets are the raw coded input (the
    canonical default -- linear outputs can reach any value, so no
    rescale); sigmoid targets are 0/1 (x/2+.5 undoes the pm1 coding;
    catlearn .diva.global_scale), tanh targets are -1/+1.
    A mismatched pair (e.g. pm1 targets on sigmoid outputs that can
    never reach -1) biases the gradients toward an unreachable
    endpoint."""
    if out_act == 'linear':
        return x
    if activation == 'tanh':
        return x if coding == 'pm1' else x * 2 - 1
    return x / 2 + .5 if coding == 'pm1' else x
# <<< shared: diva_helpers <<<

# >>> shared: diva_init >>>
def get_wts(n_feat, n_hid, n_cat, rng, wr=1.0, wc=0.0, init='uniform'):
    """Initial weight draw for a fresh network.

    Shapes: encoder iw is (n_feat+1) x n_hid -- the +1 row carries the
    input-bias unit's connections; decoder ow is (n_hid+1) x n_feat x
    n_cat -- +1 for the hidden-bias unit, one full reconstruction
    matrix per category channel.

    Draw order is iw THEN ow and must not change: seeded probes pin
    the exact rng consumption sequence.

    init='uniform' (canonical; catlearn .diva.get_wts / nconaway
      getweights.m):  wc + wr * U(-1,1) = U(wc-wr, wc+wr) -- wr is the
      half-width, wc the center.
    init='normal':   wc + wr * N(0,1) -- wr is the sd, NOT variance.
    init='xavier':   Glorot-uniform, bounds sqrt(6/(fan_in+fan_out))
      per matrix; wr and wc ignored entirely."""
    if init == 'normal':
        return (wc + wr * rng.standard_normal((n_feat + 1, n_hid)),
                wc + wr * rng.standard_normal((n_hid + 1, n_feat, n_cat)))
    if init == 'xavier':     # Glorot-uniform; wr/wc ignored
        e = (6. / (n_feat + 1 + n_hid)) ** .5
        d = (6. / (n_hid + 1 + n_feat)) ** .5
        return ((rng.random((n_feat + 1, n_hid)) * 2 - 1) * e,
                (rng.random((n_hid + 1, n_feat, n_cat)) * 2 - 1) * d)
    return (wc + wr * (rng.random((n_feat + 1, n_hid)) * 2 - 1),
            wc + wr * (rng.random((n_hid + 1, n_feat, n_cat)) * 2 - 1))
# <<< shared: diva_init <<<


def init(rng, cfg):
    """Fresh network for the SHJ problem size: 3 input features, 2
    category channels, n_hid hidden units.  The rng consumption order
    (iw then ow, inside get_wts) is pinned by the seeded probes."""
    cfg = _cfg(cfg)
    iw, ow = get_wts(3, cfg['n_hid'], 2, rng, cfg['wr'], cfg['wc'],
                     cfg['init'])
    return {'iw': iw, 'ow': ow}


# >>> shared: diva_step >>>
def forward(in_wts, out_wts, x, act, oact=None):
    """Forward pass for one stimulus; returns everything backprop needs:

      ins   = [1, x]                      input + constant-1 bias unit
      h_raw = ins @ iw                    hidden preactivation
      h     = [1, act(h_raw)]             hidden + constant-1 bias unit
      out_k = oact(h @ ow[:,:,k])         reconstruction on channel k

    oact is the OUTPUT nonlinearity -- normally the same squashing fn
    as the hidden layer (act), or the identity for out_act='linear'
    (Kurtz-stated canonical; linear outs without clipping).

    h_raw is kept for the hidden-unit derivative in backprop; ins/h are
    the outer-product factors for the weight updates."""
    if oact is None:
        oact = act
    ins = np.concatenate([[1.0], x])
    h_raw = ins @ in_wts
    h = np.concatenate([[1.0], act(h_raw)])
    return [oact(h @ out_wts[:, :, c]) for c in range(out_wts.shape[2])], \
        h, h_raw, ins


def backprop(out_w, in_wts, out_act, tgt, h, h_raw, ins, lr, act_g):
    """One supervised trial on a single channel's decoder + the shared
    encoder, online SGD (catlearn .diva.backprop / nconaway BACKPROP.m):

      d_out  = 2 (out - tgt)                       SSE delta at output
      d_hid  = (d_out @ out_w^T)[1:] * act'(h_raw) hidden delta
      out_w -= lr * h   (x) d_out                  decoder update
      in_w  -= lr * ins (x) d_hid                  encoder update

    Two conventions that look like bugs but are faithful to both
    reference implementations:
      * d_out is the LINEAR-output SSE delta even when the output
        activation is sigmoid -- neither reference chains the output
        nonlinearity's derivative (nconaway's README claims
        cross-entropy for sigmoid; the code does the SSE delta).
      * d_hid is computed BEFORE the decoder update, so it sees the
        weights that produced this trial's error; [1:] drops the
        hidden-bias column, which has no incoming weights to update."""
    d_out = 2 * (out_act - tgt)
    d_hid = (d_out @ out_w.T)[1:] * act_g(h_raw)     # drop bias col
    out_w -= lr * (h[:, None] @ d_out[None])
    in_wts -= lr * (ins[:, None] @ d_hid[None])
# <<< shared: diva_step <<<


def trial(params, x, y, cfg):
    """One supervised trial: forward pass, then backprop on the TRUE
    category's decoder channel (ow[:,:,y]) plus the shared encoder.
    The other channel's weights are untouched -- that is the
    "divergent" in DIVA: each channel only ever sees its own
    category's items."""
    cfg = _cfg(cfg)
    act, act_g = ACT[cfg['activation']]
    oact = (lambda z: z) if cfg.get('out_act') == 'linear' else act
    acts, h, h_raw, ins = forward(params['iw'], params['ow'], x, act,
                                oact)
    backprop(params['ow'][:, :, y], params['iw'], acts[y],
             decode_tgt(x, cfg['coding'], cfg['activation'],
                        cfg['out_act']),
             h, h_raw, ins, cfg['lr'], act_g)


def response(params, x, cfg):
    """P(category) at a probe item: channel reconstructions ->
    feature-weighted SSE -> inverse-error choice probabilities.

      err[k,f] = max((out_kf - tgt_f)^2, 1e-7)   per-feature error,
                                                 floored (catlearn)
      focusing (beta>0):  fw_f ~ exp(beta * |o0_f - o1_f|), clipped at
                          1e7, normalized -- Conaway & Kurtz 2014;
                          upweights the features the channels disagree
                          on (the two-category form of the pairwise
                          channel-diversity mean)
      SSE_k   = sum_f fw_f * err[k,f]
      inv_k   = 1 / SSE_k                    likelihood-style score

    Two readout maps (see front-matter READOUT for the literature
    arbitration):
      'luce': p = inv / sum(inv)             published Kurtz 2007 Eq.1
      'exp':  inv -= max(inv) then p = exp(phi*inv) / sum   catlearn;
              the max-shift prevents overflow without changing the
              normalized probabilities"""
    cfg = _cfg(cfg)
    act, _ = ACT[cfg['activation']]
    oact = (lambda z: z) if cfg.get('out_act') == 'linear' else act
    acts, _, _, _ = forward(params['iw'], params['ow'], x, act, oact)
    err = np.maximum((np.asarray(acts)
                      - decode_tgt(x, cfg['coding'], cfg['activation'],
                                   cfg['out_act']))
                     ** 2, 1e-7)
    if cfg['beta'] > 0:    # focusing: per-feature weight from divergence
        fd = np.abs(acts[0] - acts[1])
        fw = np.minimum(np.exp(cfg['beta'] * fd), 1e7)
        fw /= fw.sum()
    else:
        fw = np.full(err.shape[-1], 1 / err.shape[-1])
    inv = 1 / (err * fw[None]).sum(-1)
    if cfg['readout'] == 'luce':            # published rule; no exponent
        return inv / inv.sum()
    inv -= inv.max()                        # catlearn stabilization
    p = np.exp(cfg['phi'] * inv)
    return p / p.sum()


# ---- built-in verification probe ----------------------------------------
# The probe runs the canonical profile -- VERIFY_CFG tracks DEFAULTS,
# so the self-check always exercises the model as configured.
# (The legacy catlearn profile remains reachable as a cfg preset:
# readout='exp', out_act='sigmoid'.)
VERIFY_CFG = dict(DEFAULTS)

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

# >>> shared: diva_verify >>>
X_ALL = encode(STIMULI, VERIFY_CFG['coding'])    # -1/+1 inputs


def verify():
    """Type V transfer probe (the diva-family mechanistic invariant):

      * 10 networks, each trained on the 7 non-held items for 32
        sweeps; each sweep = one rng.permutation of TRAIN, so every
        item appears once per sweep in random order.
      * Probe: P(B | item 101) -- what the trained net assigns to the
        held-out item it never saw.
      * seed 7624; VERIFY_CFG tracks DEFAULTS -- the probe runs the
        canonical profile (linear outs + luce readout).

    Expected signature (canonical profile): mean_pB ~ .135, fracB = 0
    -- the A channel reconstructs 101 nearly as well as its trained
    A items, producing a strong A-lean."""
    rng = np.random.default_rng(7624)
    p = np.empty(10)
    for i in range(10):
        prm = init(rng, VERIFY_CFG)
        for _ in range(32):
            for s in rng.permutation(TRAIN):
                trial(prm, X_ALL[s], LABELS_TV[s], VERIFY_CFG)
        p[i] = response(prm, X_ALL[HELD], VERIFY_CFG)[1]
    return {'mean_pB': float(p.mean()), 'fracB': float((p > .5).mean()),
            'n': 10, 'seed': 7624}
# <<< shared: diva_verify <<<


if __name__ == '__main__':
    print(verify())
