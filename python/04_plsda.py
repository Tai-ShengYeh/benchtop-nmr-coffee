# -*- coding: utf-8 -*-
"""04 PLS-DA：把 16-OMC 高/低當兩類，從 benchtop NMR 指紋分類（真偽快篩 pass/fail）。
PLS-DA = 對 0/1 啞變數做 PLS 回歸再以 0.5 為界。教交叉驗證、混淆矩陣、判別係數。"""
import os, numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from sklearn.cross_decomposition import PLSRegression
from sklearn.model_selection import cross_val_predict, StratifiedKFold
from sklearn.metrics import confusion_matrix, roc_auc_score
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
FIG = os.path.join(HERE, "figures"); os.makedirs(FIG, exist_ok=True)
df = pd.read_csv(os.path.join(ROOT, "data", "coffee_nmr.csv"))
feat = [c for c in df.columns if c.startswith("b")]
binppm = np.array([float(c[1:]) for c in feat])
# ⚠️ 排除標記區段(0.43–0.53 ppm)：分組就是依這算的，留著會資料洩漏
keep = ~((binppm >= 0.43) & (binppm <= 0.53)); binppm = binppm[keep]
X = df[feat].values[:, keep]
y = (df["group"].values == "High-16OMC").astype(int)   # 1=High, 0=Low
HI, LO = "#E36414", "#0E7C7B"
cv = StratifiedKFold(5, shuffle=True, random_state=0)

# 選潛在變數（用交叉驗證準確率）
accs = []
for k in range(1, 9):
    yp = cross_val_predict(PLSRegression(k), X, y.astype(float), cv=cv).ravel()
    accs.append(((yp > 0.5).astype(int) == y).mean())
best = int(np.argmax(accs) + 1)

pls = PLSRegression(best).fit(X, y.astype(float))
ypcv = cross_val_predict(pls, X, y.astype(float), cv=cv).ravel()
pred = (ypcv > 0.5).astype(int)
acc = (pred == y).mean(); auc = roc_auc_score(y, ypcv); cm = confusion_matrix(y, pred)
T = pls.x_scores_   # PLS 潛在變數分數

# 混淆矩陣
plt.figure(figsize=(4.6, 4.2)); plt.imshow(cm, cmap="Greens")
for i in range(2):
    for j in range(2): plt.text(j, i, cm[i, j], ha="center", va="center", fontsize=16, color="#111")
plt.xticks([0, 1], ["Low", "High"]); plt.yticks([0, 1], ["Low", "High"])
plt.xlabel("Predicted"); plt.ylabel("Actual"); plt.title(f"PLS-DA confusion — {best} LV\nacc={acc*100:.0f}%, AUC={auc:.2f}")
plt.tight_layout(); plt.savefig(os.path.join(FIG, "nc10_plsda_cm.png"), dpi=130); plt.close()

# 潛在變數分數圖
plt.figure(figsize=(6.4, 5.4))
for v, c, lab in [(1, HI, "High-16OMC"), (0, LO, "Low-16OMC")]:
    m = y == v; plt.scatter(T[m, 0], T[m, 1], c=c, label=lab, s=55, alpha=.8, edgecolor="white", lw=.6)
plt.axhline(0, color="#ddd", lw=.8); plt.axvline(0, color="#ddd", lw=.8)
plt.xlabel("PLS LV1"); plt.ylabel("PLS LV2"); plt.title("PLS-DA latent space"); plt.legend()
plt.tight_layout(); plt.savefig(os.path.join(FIG, "nc11_plsda_scores.png"), dpi=130); plt.close()

# 判別係數
plt.figure(figsize=(10, 4))
plt.plot(binppm, pls.coef_.ravel(), color="#0E7C7B", lw=1)
plt.axvspan(0.43, 0.53, color=HI, alpha=.18, label="16-OMC marker")
plt.axhline(0, color="#ccc", lw=.8); plt.gca().invert_xaxis()
plt.xlabel("ppm"); plt.ylabel("PLS-DA coefficient"); plt.title("PLS-DA coefficients — which ppm separate High vs Low"); plt.legend()
plt.tight_layout(); plt.savefig(os.path.join(FIG, "nc12_plsda_coef.png"), dpi=130); plt.close()
print(f"acc by LV: {np.round(accs,2)} -> best {best} LV")
print(f"PLS-DA: acc={acc*100:.1f}%  AUC={auc:.3f}  confusion=\n{cm}")
print("[OK] 04 plsda -> nc10/nc11/nc12")
