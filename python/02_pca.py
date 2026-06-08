# -*- coding: utf-8 -*-
"""02 PCA：分箱光譜標準化後做 PCA，看 16-OMC 高/低在主成分空間怎麼分。"""
import os, numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
FIG = os.path.join(HERE, "figures"); os.makedirs(FIG, exist_ok=True)
df = pd.read_csv(os.path.join(ROOT, "data", "coffee_nmr.csv"))
feat = [c for c in df.columns if c.startswith("b")]
binppm = np.array([float(c[1:]) for c in feat])
grp = df["group"].values; HI, LO = "#E36414", "#0E7C7B"
X = StandardScaler().fit_transform(df[feat].values)
pca = PCA().fit(X); S = pca.transform(X); ev = pca.explained_variance_ratio_ * 100

plt.figure(figsize=(6, 4))
plt.bar(range(1, 11), ev[:10], color="#0E7C7B", alpha=.85, label="individual")
plt.plot(range(1, 11), np.cumsum(ev[:10]), "o-", color="#E36414", label="cumulative")
plt.xlabel("PC"); plt.ylabel("Variance %"); plt.title("PCA scree — coffee NMR (133 bins)"); plt.legend()
plt.tight_layout(); plt.savefig(os.path.join(FIG, "nc04_scree.png"), dpi=130); plt.close()

plt.figure(figsize=(6.6, 5.6))
for g, c in [("High-16OMC", HI), ("Low-16OMC", LO)]:
    m = grp == g; plt.scatter(S[m, 0], S[m, 1], c=c, label=g, s=55, alpha=.8, edgecolor="white", lw=.6)
plt.axhline(0, color="#ddd", lw=.8); plt.axvline(0, color="#ddd", lw=.8)
plt.xlabel(f"PC1 ({ev[0]:.1f}%)"); plt.ylabel(f"PC2 ({ev[1]:.1f}%)")
plt.title("PCA scores — colored by 16-OMC level"); plt.legend()
plt.tight_layout(); plt.savefig(os.path.join(FIG, "nc05_scores.png"), dpi=130); plt.close()

# PC1 負荷 vs ppm（標出標記區）
plt.figure(figsize=(10, 4))
plt.plot(binppm, pca.components_[0], color="#0E7C7B", lw=1)
plt.axvspan(0.43, 0.53, color=HI, alpha=.18, label="16-OMC marker")
plt.axhline(0, color="#ccc", lw=.8); plt.gca().invert_xaxis()
plt.xlabel("ppm"); plt.ylabel("PC1 loading"); plt.title("PC1 loadings — which ppm regions drive variation"); plt.legend()
plt.tight_layout(); plt.savefig(os.path.join(FIG, "nc06_loadings.png"), dpi=130); plt.close()
print("Variance %:", np.round(ev[:4], 1), "cum2:", round(ev[:2].sum(), 1))
print("[OK] 02 pca -> nc04/nc05/nc06")
