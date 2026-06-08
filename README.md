# Benchtop NMR × 咖啡真偽 — PCA / PLS / PLS-DA 教學包

用 **60 支市售「Arabica」咖啡的 60 MHz 桌上型 NMR 光譜**（QIB Chemometrics 公開資料），一次教化學計量學三大方法：
**PCA**（非監督探索）、**PLS 回歸**（定量 16-OMC 摻假標記）、**PLS-DA**（真偽快篩高/低分類）。
背景是 Gunning et al. (2018) 用 **16-O-methylcafestol（16-OMC）** 偵測 Arabica 咖啡裡的 Robusta。

**▶ 線上課程頁：** <https://tai-shengyeh.github.io/benchtop-nmr-coffee/teaching.html>

## 📚 教學系列 — 光譜 × 食品分析（化學計量學）

| 課程 | 方法 | 資料 / 應用 | 課程頁 |
|------|------|-----------|--------|
| NIR 近紅外 | PCA + PLS（定量）| Tecator 肉品 | [↗](https://tai-shengyeh.github.io/chemometrics-teaching/) |
| NMR 核磁共振 | PCA + PLS（定量）| 白酒蘋果酸 | [↗](https://tai-shengyeh.github.io/nmr-food-analysis/teaching.html) |
| FTIR 紅外 | PCA + PLS-DA | 咖啡 Arabica/Robusta | [↗](https://tai-shengyeh.github.io/ftir-food-analysis/teaching.html) |
| **Benchtop NMR（本課）** | **PCA + PLS + PLS-DA** | **咖啡 16-OMC 真偽** | [↗](https://tai-shengyeh.github.io/benchtop-nmr-coffee/teaching.html) |
| 咖啡化學成分 | PCA + GMM 集群 | pgmm coffee | [↗](https://tai-shengyeh.github.io/coffee_pgmm_R_code/coffee_pgmm.html) |

> 🔗 與 **FTIR**（咖啡 Arabica/Robusta）和 **coffee_pgmm**（咖啡化學成分）同主題，可串成一條「咖啡真偽鑑別」教學線。
> 🏠 課程總入口：<https://tai-shengyeh.github.io/>

## 交付物

| 交付物 | 路徑 |
|------|------|
| 教學網頁（互動課程頁）| `index.html` → `teaching.html` |
| Python 分析 | `python/00_get_data.py`（取資料）、`01_explore.py`、`02_pca.py`、`03_pls.py`、`04_plsda.py` |
| 科學圖表 | `python/figures/`（平均光譜、標記區、PCA 陡坡/分數/負荷、PLS 預測/係數、PLS-DA 混淆/係數，共 12 張）|
| Orange | `data/coffee_nmr_orange.tab` + [`orange/ORANGE_GUIDE.md`](orange/ORANGE_GUIDE.md) |
| 教學資料表 | `data/coffee_nmr.csv`（60 × 133 分箱 + group + marker_score）|

## 資料來源

**QIBChemometrics / Benchtop-NMR-Coffee-Survey** — 60 支市售「Arabica」烘焙咖啡的親脂萃取物，
60 MHz benchtop ¹H-NMR，0.2–5.8 ppm（本資料 4201 點，以 ~4.28 ppm 甘油酯峰為參考）。
對應 **Gunning et al., "16-O-methylcafestol is present in ground roast Arabica coffees…", *Food Chemistry* 2018, 248:52–60**
（doi:[10.1016/j.foodchem.2017.12.034](https://doi.org/10.1016/j.foodchem.2017.12.034)）。
`python/00_get_data.py` 會自動下載原始 CSV。

## 重現分析

```bash
pip install pyreadr pandas numpy scikit-learn matplotlib
python python/00_get_data.py   # 下載、面積歸一、分箱(133)、算 16-OMC 標記、輸出 CSV/Orange
python python/01_explore.py    # 平均光譜、標記區高/低對照、標記量箱形圖
python python/02_pca.py        # 標準化 + PCA -> 陡坡 / 分數 / 負荷
python python/03_pls.py        # PLS 回歸定量 16-OMC（排除標記區，避免洩漏）
python python/04_plsda.py      # PLS-DA 高/低分類（5-fold CV、混淆矩陣）
```

## 關鍵結果

- **資料只有光譜、沒有標籤**：以 0.43–0.53 ppm 的 **16-OMC 標記峰積分**當「摻假標記量」，連續值給 PLS、中位數切高/低給 PLS-DA。
- **PCA**（133 分箱標準化）：PC1 **62.6%**、PC2 15.4%，前 2 PC ≈ 78%。PC1 與標記量相關 **−0.76**——摻假是「全譜性」變化。
- **PLS 回歸**（⚠️ 排除標記區段，避免資料洩漏）：用「光譜其餘部分」預測 16-OMC，**R²cv ≈ 0.99、RMSECV ≈ 0.08**。
- **PLS-DA**（高 vs 低、5-fold CV）：**準確率 85%、AUC 0.93**；誤判集中在標記量接近中位數者。
- **資料素養**：R² 太完美先查資料洩漏（目標混進輸入）；小樣本（60）＋自訂門檻標籤，屬概念示範，交叉驗證是底線。

## 製作

科學圖以 Python（scikit-learn + matplotlib）產生。屬「光譜 × 食品分析（化學計量學）」教學系列，
配色：teal `#0E7C7B` + coral `#E36414`。
