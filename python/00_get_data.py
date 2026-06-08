# -*- coding: utf-8 -*-
"""下載 Benchtop NMR 咖啡光譜，處理成教學用資料：
- 面積歸一光譜（samples x ppm）
- Robusta 摻假標記分數 = 0.43–0.53 ppm 區段積分（16-OMC / 二萜類）
- 依標記分數分「Arabica（純）/ Robusta-positive（疑摻假）」
- 分箱(~0.04 ppm)後輸出 Orange .tab + 教學 CSV
"""
import urllib.request, os, re, numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data"); os.makedirs(DATA, exist_ok=True)
raw = os.path.join(HERE, "raw.csv")
URL = "https://raw.githubusercontent.com/QIBChemometrics/Benchtop-NMR-Coffee-Survey/HEAD/Benchtop_NMR_Coffee_Survey.csv"
if not os.path.exists(raw):
    urllib.request.urlretrieve(URL, raw)

df = pd.read_csv(raw); df.columns = [c.strip().lstrip("﻿") for c in df.columns]
ppm = df.iloc[:, 0].values.astype(float)
samples = df.columns[1:].tolist()
X = df.iloc[:, 1:].values.T.astype(float)                 # 60 x 4201
Xn = X / X.sum(axis=1, keepdims=True)                     # 面積歸一

# Robusta 標記分數（16-OMC 區段）
win = (ppm >= 0.43) & (ppm <= 0.53)
marker = Xn[:, win].sum(axis=1)
print("標記分數分布(由高到低前 12):")
for s, m in sorted(zip(samples, marker), key=lambda t: -t[1])[:12]:
    print(f"  {s}: {m:.4f}")
# 以 16-OMC 標記量的中位數分「高/低」兩組（真偽快篩 pass/fail 教學框架）
thr = np.median(marker)
group = np.where(marker >= thr, "High-16OMC", "Low-16OMC")
print(f"\n中位數門檻={thr:.4f} -> High {np.sum(group=='High-16OMC')} / Low {np.sum(group=='Low-16OMC')}")
print("標記量 min/median/max:", round(marker.min(),5), round(thr,5), round(marker.max(),5))

# 分箱（~0.04 ppm）
edges = np.arange(0.4, 5.75, 0.04)
binc = (edges[:-1] + edges[1:]) / 2
B = np.zeros((Xn.shape[0], len(binc)))
for k in range(len(binc)):
    m = (ppm >= edges[k]) & (ppm < edges[k + 1])
    if m.sum(): B[:, k] = Xn[:, m].mean(axis=1)
bcols = [f"b{c:.2f}" for c in binc]
print(f"\n分箱: {len(binc)} 個特徵")

# 教學 CSV（樣本 x 分箱特徵 + group + marker）
out = pd.DataFrame(B, columns=bcols); out.insert(0, "marker_score", marker.round(5))
out.insert(0, "group", group); out.insert(0, "sample", samples)
out.to_csv(os.path.join(DATA, "coffee_nmr.csv"), index=False, encoding="utf-8-sig")
print("[OK] data/coffee_nmr.csv", out.shape)

# Orange .tab（group=class、marker_score=可選 target、特徵=連續）
with open(os.path.join(DATA, "coffee_nmr_orange.tab"), "w", encoding="utf-8") as f:
    cols = ["sample", "group", "marker_score"] + bcols
    f.write("\t".join(cols) + "\n")
    f.write("\t".join(["string", "discrete", "continuous"] + ["continuous"] * len(bcols)) + "\n")
    f.write("\t".join(["meta", "class", "" ] + [""] * len(bcols)) + "\n")
    for i in range(len(samples)):
        f.write("\t".join([samples[i], group[i], f"{marker[i]:.5f}"] + [f"{B[i,k]:.6f}" for k in range(len(binc))]) + "\n")
print("[OK] data/coffee_nmr_orange.tab")
np.save(os.path.join(HERE, "_ppm.npy"), ppm); np.save(os.path.join(HERE, "_Xn.npy"), Xn)  # 供 01 畫全譜
