# -*- coding: utf-8 -*-
"""03 PLS 回歸：從整段 benchtop NMR 指紋定量 16-OMC 標記量（連續）。
教 RMSECV 選潛在變數、預測 vs 實際、回歸係數的化學解讀。"""
import os, numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from sklearn.cross_decomposition import PLSRegression
from sklearn.model_selection import cross_val_predict, KFold
from sklearn.metrics import r2_score, mean_squared_error
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
FIG = os.path.join(HERE, "figures"); os.makedirs(FIG, exist_ok=True)
df = pd.read_csv(os.path.join(ROOT, "data", "coffee_nmr.csv"))
feat = [c for c in df.columns if c.startswith("b")]
binppm = np.array([float(c[1:]) for c in feat])
# ⚠️ 排除標記區段(0.43–0.53 ppm)：目標就是從這算的，留著會資料洩漏(R²假性接近1)
keep = ~((binppm >= 0.43) & (binppm <= 0.53)); binppm = binppm[keep]
X = df[feat].values[:, keep]; y = df["marker_score"].values * 1000.0   # 放大方便讀
cv = KFold(5, shuffle=True, random_state=0)

# 用 RMSECV 選潛在變數（上限 6，避免過配；60 樣本不宜用太多成分）
NLV = 6; rmsecv = []
for k in range(1, NLV + 1):
    yp = cross_val_predict(PLSRegression(k), X, y, cv=cv)
    rmsecv.append(np.sqrt(mean_squared_error(y, yp)))
best = int(np.argmin(rmsecv) + 1)
plt.figure(figsize=(6, 4))
plt.plot(range(1, NLV + 1), rmsecv, "o-", color="#0E7C7B"); plt.axvline(best, color="#E36414", ls="--", label=f"best = {best} LV")
plt.xlabel("PLS components (LV)"); plt.ylabel("RMSECV"); plt.title("PLS — choosing components"); plt.legend()
plt.tight_layout(); plt.savefig(os.path.join(FIG, "nc07_pls_rmsecv.png"), dpi=130); plt.close()

pls = PLSRegression(best).fit(X, y)
yp = cross_val_predict(pls, X, y, cv=cv)
r2 = r2_score(y, yp); rmse = np.sqrt(mean_squared_error(y, yp))
plt.figure(figsize=(5.6, 5.4))
plt.scatter(y, yp, c="#0E7C7B", s=50, alpha=.8, edgecolor="white", lw=.6)
lim = [min(y.min(), yp.min()), max(y.max(), yp.max())]
plt.plot(lim, lim, "--", color="#888")
plt.xlabel("Measured 16-OMC marker (×1000)"); plt.ylabel("CV-predicted")
plt.title(f"PLS regression — {best} LV,  R²cv={r2:.2f},  RMSECV={rmse:.2f}")
plt.tight_layout(); plt.savefig(os.path.join(FIG, "nc08_pls_pred.png"), dpi=130); plt.close()

plt.figure(figsize=(10, 4))
plt.plot(binppm, pls.coef_.ravel(), color="#0E7C7B", lw=1)
plt.axvspan(0.43, 0.53, color="#E36414", alpha=.18, label="16-OMC marker")
plt.axhline(0, color="#ccc", lw=.8); plt.gca().invert_xaxis()
plt.xlabel("ppm"); plt.ylabel("PLS coefficient"); plt.title("PLS regression coefficients — which ppm predict the marker"); plt.legend()
plt.tight_layout(); plt.savefig(os.path.join(FIG, "nc09_pls_coef.png"), dpi=130); plt.close()
print(f"RMSECV by LV: {np.round(rmsecv,2)} -> best {best} LV")
print(f"PLS: R2cv={r2:.3f}  RMSECV={rmse:.3f}")
print("[OK] 03 pls -> nc07/nc08/nc09")
