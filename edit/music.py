#!/usr/bin/env python3
"""Trilha instrumental original (96 BPM, 30 compassos = 75s), sincronizada com os atos do vídeo.
Seções vêm do edl.py: intro | bonés/menino | REVELAÇÃO (REVEAL_BAR) | câmera lenta (DREAM_BAR) | final
"""
import numpy as np, wave, sys

SR = 44100
BPM = 96
BEAT = 60 / BPM
BAR = 4 * BEAT
from edl import EDL, REVEAL_BAR as RV, DREAM_BAR as DR
NBARS = round(sum(e[2] for e in EDL) / (4*60/96))
N = int(SR * NBARS * BAR) + SR * 2
L = np.zeros(N); R = np.zeros(N)
rng = np.random.default_rng(7)


def hz(m): return 440 * 2 ** ((m - 69) / 12)


def add(sig, t, gain=1.0, pan=0.0):
    i = int(t * SR)
    if i >= N: return
    sig = sig[: N - i]
    L[i:i+len(sig)] += sig * gain * (1 - pan) ** 0.5 / 0.707 * 0.707
    R[i:i+len(sig)] += sig * gain * (1 + pan) ** 0.5 / 0.707 * 0.707


def env_t(d): return np.arange(int(d * SR)) / SR


def piano(m, d=1.6, vel=1.0):
    t = env_t(d); f = hz(m)
    s = sum(a * np.sin(2*np.pi*f*k*t) * np.exp(-t*(2.2+k*1.3)) for k, a in [(1,1),(2,.45),(3,.22),(4,.12),(5,.06)])
    s *= np.minimum(1, t/0.004)
    return s * vel * 0.18


def bell(m, d=1.4):
    t = env_t(d); f = hz(m)
    s = np.sin(2*np.pi*f*t + 1.2*np.sin(2*np.pi*f*3.5*t)*np.exp(-t*4)) * np.exp(-t*3.2)
    return s * np.minimum(1, t/0.003) * 0.11


def pad(ms, d):
    t = env_t(d); s = np.zeros_like(t)
    for m in ms:
        for det in (-0.08, 0.0, 0.08):
            f = hz(m + det)
            s += np.sin(2*np.pi*f*t) + 0.3*np.sin(4*np.pi*f*t) + 0.12*np.sin(6*np.pi*f*t)
    a = np.minimum(1, t/0.35) * np.minimum(1, (d - t)/0.35)
    return s * a * 0.022


def bass(m, d):
    t = env_t(d); f = hz(m)
    s = np.sin(2*np.pi*f*t) + 0.25*np.sin(4*np.pi*f*t)
    return s * np.minimum(1, t/0.01) * np.exp(-t*1.2) * np.minimum(1, (d-t)/0.03) * 0.22


def kick(g=1.0):
    t = env_t(0.45)
    ph = 2*np.pi*np.cumsum(45 + 110*np.exp(-t*28)) / SR
    return np.sin(ph) * np.exp(-t*7) * 0.55 * g


def noise(d): return rng.standard_normal(int(d*SR))


def hp(x, a=0.85):
    y = np.empty_like(x); prev_x = 0; prev_y = 0
    # filtro passa-alta de 1 polo (vetorizado aproximado via diferença)
    y = x - np.concatenate([[0], x[:-1]]) * a
    return y


def lp(x, k=8):
    return np.convolve(x, np.ones(k)/k, mode="same")


def clap(g=1.0):
    t = env_t(0.25); n = hp(noise(0.25), 0.6)
    e = np.exp(-t*22) + 0.6*np.exp(-np.maximum(t-0.012, 0)*30)*(t > 0.012)
    return lp(n, 3) * e * 0.16 * g


def hat(g=1.0):
    t = env_t(0.06)
    return hp(noise(0.06), 0.98) * np.exp(-t*70) * 0.05 * g


def crash():
    t = env_t(2.5)
    return hp(noise(2.5), 0.95) * np.exp(-t*2.2) * 0.045


def riser(d):
    t = env_t(d); n = noise(d)
    out = np.zeros_like(n)
    for k in range(4):  # varredura grosseira: passa-baixa cada vez mais aberto
        seg = slice(int(len(n)*k/4), int(len(n)*(k+1)/4))
        out[seg] = lp(n, [24, 12, 6, 2][k])[seg]
    return out * (t/d)**2 * 0.14


CHORDS = [(48, [60, 64, 67]), (43, [59, 62, 67]), (45, [60, 64, 69]), (41, [60, 65, 69])]  # C G Am F
MELODY = [[76, 79, 76, 74], [74, 71, 74, 79], [76, 72, 76, 81], [77, 76, 74, 72]]

for b in range(NBARS):
    t0 = b * BAR
    root, tri = CHORDS[b % 4]
    intro = b < 4; build = 4 <= b <= RV-1; full = RV <= b <= DR-1; dream = DR <= b <= NBARS-3; outro = b >= NBARS-2
    # piano: arpejo em colcheias
    arp = [tri[0], tri[1], tri[2], tri[1]+12, tri[2], tri[1], tri[0]+12, tri[2]]
    if not (b == RV-1):
        for k, m in enumerate(arp):
            v = 0.8 if (intro or dream or outro) else 0.65
            add(piano(m, 1.4, v), t0 + k*BEAT/2, pan=(-0.3 if k % 2 else 0.3))
    else:
        for k, m in enumerate(arp[:6]):
            add(piano(m, 1.0, 0.6), t0 + k*BEAT/2)
    # pad
    if not intro or b >= 2:
        add(pad(tri + [tri[0]-12], BAR + 0.3), t0, gain=0.8 if dream else 1.0)
    # baixo
    if build or full:
        for k in range(4 if full else 2):
            dur = BEAT if full else 2*BEAT
            if b == RV-1 and k*dur >= 3*BEAT: continue
            add(bass(root, dur*0.95), t0 + k*dur)
    if dream:
        add(bass(root, BAR), t0, gain=0.8)
    # bateria
    if build:
        add(kick(0.8), t0); add(kick(0.7), t0 + 2*BEAT) if b != RV-1 else None
        if b != RV-1:
            add(clap(0.6), t0 + BEAT); add(clap(0.6), t0 + 3*BEAT)
            for k in range(8): add(hat(0.6 if k % 2 else 0.35), t0 + k*BEAT/2, pan=0.25)
        else:
            add(riser(3*BEAT + BEAT*0.5), t0 + 0.3*BEAT)
            for k in range(8): add(clap(0.25 + 0.06*k), t0 + 2*BEAT + k*BEAT/8)
    if full:
        for k in range(4): add(kick(1.0), t0 + k*BEAT)
        add(clap(1.0), t0 + BEAT); add(clap(1.0), t0 + 3*BEAT)
        for k in range(8): add(hat(1.0 if k % 2 else 0.5), t0 + k*BEAT/2, pan=0.3)
        for k, m in enumerate(MELODY[b % 4]): add(bell(m), t0 + k*BEAT, pan=-0.2)
        if b == DR-1:
            add(riser(2*BEAT), t0 + 2*BEAT, gain=0.8)
    if dream:
        add(kick(0.6), t0)
        for k, m in enumerate(MELODY[b % 4][::2]): add(bell(m+12, 2.0), t0 + k*2*BEAT, gain=0.7)
    if b in (RV, DR): add(crash(), t0)
    if b == RV: add(kick(1.3), t0)
    if outro:
        add(piano(tri[0]-12, 3.0, 0.7), t0)

# reverb (convolução com ruído decaindo)
def reverb(x, seed):
    r = np.random.default_rng(seed)
    t = env_t(2.2)
    ir = r.standard_normal(len(t)) * np.exp(-t*2.6)
    ir = lp(ir, 4); ir[0] = 0; ir /= np.abs(ir).sum() / 6
    n = len(x) + len(ir)
    fft = 1 << (n - 1).bit_length()
    return np.fft.irfft(np.fft.rfft(x, fft) * np.fft.rfft(ir, fft), fft)[:len(x)]

wetL = reverb(L, 1); wetR = reverb(R, 2)
L2 = L + 0.22*wetL; R2 = R + 0.22*wetR
total = NBARS * BAR
T = np.arange(N) / SR
fade = np.clip((total + 0.5 - T) / 4.0, 0, 1)  # fade final
fade *= np.clip(T / 0.4, 0, 1)
L2 *= fade; R2 *= fade
out = np.stack([L2, R2], 1)[: int((total + 0.5) * SR)]
out = np.tanh(out / np.abs(out).max() * 1.4) * 0.89
pcm = (out * 32767).astype(np.int16)
fn = sys.argv[1] if len(sys.argv) > 1 else "trilha.wav"
with wave.open(fn, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print("ok", fn, total)
