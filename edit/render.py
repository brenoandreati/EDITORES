#!/usr/bin/env python3
"""Renderiza os segmentos do EDL e concatena.
uso: python3 render.py preview|final
"""
import os, sys, subprocess
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(__file__))
from edl import EDL

MODE = sys.argv[1] if len(sys.argv) > 1 else "preview"
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
W, H = (540, 960) if MODE == "preview" else (1080, 1920)
OUT = os.path.join(ROOT, "build", MODE)
os.makedirs(OUT, exist_ok=True)
FPS = 30

TONEMAP = ("zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,"
           "tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p")
GRADE = "eq=contrast=1.07:saturation=1.18:gamma=1.04,colortemperature=temperature=5900:mix=0.5"


def seg_filter(i, out_d, speed, fx, prev_fx):
    f = []
    if MODE == "final":
        f.append(f"scale={W}:{H}:flags=lanczos")  # reduz 4K antes do tonemap (mais rápido)
        f.append(TONEMAP)
    else:
        f.append(f"scale={W}:{H}")
    f.append(f"setpts={1/speed:.4f}*PTS")
    f.append(f"fps={FPS}")
    f.append(GRADE)
    D = out_d
    if fx in ("push", "dream"):
        z = 0.06 if fx == "push" else 0.08
        f.append(f"scale=w='trunc({W}*(1+{z}*t/{D})/2)*2':h=-2:eval=frame,crop={W}:{H}")
    elif fx == "low":
        f.append(f"scale=w={int(W*1.22)//2*2}:h=-2,crop={W}:{H}:(iw-{W})/2:ih-{H}")
    elif fx == "punch":
        f.append(f"scale=w='trunc({W}*(1.0+0.14*exp(-t*6))/2)*2':h=-2:eval=frame,crop={W}:{H}")
    if fx == "dream":
        sig = 18 if MODE == "final" else 9
        f.append(f"format=gbrp,split[a][b];[b]gblur=sigma={sig}[g];[a][g]blend=all_mode=screen:all_opacity=0.25,"
                 "vignette=angle=PI/5,format=yuv420p")
    f.append(f"trim=duration={D:.4f},setpts=PTS-STARTPTS")
    if i == 0:
        f.append("fade=t=in:st=0:d=0.6")
    if i == len(EDL) - 1:
        f.append(f"fade=t=out:st={D-1.2:.3f}:d=1.2")
    if fx == "flash":
        f.append(f"fade=t=out:st={D-0.18:.3f}:d=0.18:color=white")
    if prev_fx == "flash":
        f.append("fade=t=in:st=0:d=0.3:color=white")
    f.append("format=yuv420p")
    return ",".join(f)


def render(i):
    take, start, out_d, speed, fx, _ = EDL[i]
    prev_fx = EDL[i-1][4] if i else ""
    src = (os.path.join(ROOT, "proxy", f"IMG_{take}.mp4") if MODE == "preview"
           else os.path.join(ROOT, "raw", f"IMG_{take}.MOV"))
    src_d = out_d * speed + 0.3
    dst = os.path.join(OUT, f"seg_{i:02d}.mp4")
    cmd = ["ffmpeg", "-v", "error", "-y", "-ss", f"{start}", "-t", f"{src_d}", "-i", src,
           "-an", "-filter_complex", "[0:v:0]" + seg_filter(i, out_d, speed, fx, prev_fx) + "[out]", "-map", "[out]",
           "-c:v", "libx264", "-preset", "veryfast" if MODE == "preview" else "medium",
           "-crf", "22" if MODE == "preview" else "16", "-r", str(FPS), dst]
    subprocess.run(cmd, check=True)
    return dst


with ThreadPoolExecutor(4) as ex:
    segs = list(ex.map(render, range(len(EDL))))

lst = os.path.join(OUT, "list.txt")
with open(lst, "w") as fh:
    for s in segs:
        fh.write(f"file '{s}'\n")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst,
                "-c", "copy", os.path.join(OUT, "video_mudo.mp4")], check=True)
total = sum(e[2] for e in EDL)
print(f"ok {len(segs)} segmentos, {total:.2f}s")
