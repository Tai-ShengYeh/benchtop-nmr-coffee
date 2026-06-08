# -*- coding: utf-8 -*-
"""01 探索：平均光譜、16-OMC 標記區段（高/低組對照）、標記量箱形圖。"""
import os, numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
FIG = os.path.join(HERE, "figures"); os.makedirs(FIG, exist_ok=True)
ppm = np.load(os.path.join(HERE, "_ppm.npy")); Xn = np.load(os.path.join(HERE, "_Xn.npy"))
df = pd.read_csv(os.path.join(ROOT, "data", "coffee_nmr.csv"))
grp = df["group"].values; marker = df["marker_score"].values
HI, LO = "#E36414", "#0E7C7B"

# 平均全譜 + 標記區段
plt.figure(figsize=(10, 4))
plt.plot(ppm, Xn.mean(0), color="#333", lw=.8)
plt.axvspan(0.43, 0.53, color=HI, alpha=.18, label="16-OMC marker (~0.46 ppm)")
plt.gca().invert_xaxis(); plt.xlabel("Chemical shift (ppm)"); plt.ylabel("Norm. intensity")
plt.title("Benchtop 60 MHz NMR — mean coffee spectrum (60 samples)"); plt.legend()
plt.tight_layout(); plt.savefig(os.path.join(FIG, "nc01_meanspec.png"), dpi=130); plt.close()

# 標記區段放大：高 vs 低組
m = (ppm >= 0.33) & (ppm <= 0.80)
plt.figure(figsize=(7, 4.6))
for g, c in [("High-16OMC", HI), ("Low-16OMC", LO)]:
    sel = grp == g
    plt.plot(ppm[m], Xn[sel][:, m].mean(0), color=c, lw=1.8, label=f"{g} (n={sel.sum()})")
plt.axvspan(0.43, 0.53, color=HI, alpha=.12)
plt.gca().invert_xaxis(); plt.xlabel("ppm"); plt.ylabel("Norm. intensity")
plt.title("16-OMC marker region — High vs Low 16-OMC"); plt.legend()
plt.tight_layout(); plt.savefig(os.path.join(FIG, "nc02_marker_zoom.png"), dpi=130); plt.close()

# 標記量箱形圖
plt.figure(figsize=(5, 4.6))
bp = plt.boxplot([marker[grp == g] * 1000 for g in ["Low-16OMC", "High-16OMC"]], patch_artist=True, widths=.6)
plt.xticks([1, 2], ["Low", "High"])
for p, c in zip(bp["boxes"], [LO, HI]): p.set_facecolor(c); p.set_alpha(.75)
plt.ylabel("16-OMC marker score (×1000)"); plt.title("Marker score by group (median split)")
plt.tight_layout(); plt.savefig(os.path.join(FIG, "nc03_marker_box.png"), dpi=130); plt.close()
print("[OK] 01 explore -> nc01/nc02/nc03")
