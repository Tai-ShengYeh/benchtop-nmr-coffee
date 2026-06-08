# Orange Data Mining — 咖啡 benchtop NMR（PCA / PLS / PLS-DA）

不寫程式，用拉的就能重現 Python 版結果。
資料檔：[`data/coffee_nmr_orange.tab`](../data/coffee_nmr_orange.tab)
（`sample`=meta、`group`=class（高/低 16-OMC）、`marker_score`=連續、133 個分箱特徵 `b0.42`…）。

## 一、看資料
1. **File** → 開 `data/coffee_nmr_orange.tab` → 接 **Data Table**（60 列）。
2. **Preprocess** → 勾 **Normalize features**（標準化；各桶尺度差很大，務必做）。

## 二、PCA 探索（非監督）
3. **Preprocess → PCA** → 看累積變異（前 2 PC ≈ 78%）。
4. **PCA → Scatter Plot**：x=`PC1`、y=`PC2`、**Color=`group`** → 高/低沿 PC1 分開。

## 三、PLS 回歸（定量 16-OMC）
5. **Select Columns**：把 `marker_score` 設 **Target**、`group` 設 Meta。
6. **PLS**（Number of components ≈ 3–4）→ **Test & Score**（Cross validation）→ 看 **R² / RMSE**。
7. **Predictions** → 散布「預測 vs 實際」。

## 四、PLS-DA / 判別（真偽快篩 高 vs 低）
8. **Select Columns**：把 `group` 設 **Target**（class）。
9. **PLS** 或 **Logistic Regression** → **Test & Score** + **Confusion Matrix** → 看準確率（約 85%）。

## ⚠️ 避免資料洩漏
`marker_score` 與 `group` 都是從 **0.43–0.53 ppm** 算的。要嚴謹，請在 **Select Columns** 把這幾個桶
（`b0.44`、`b0.48`、`b0.52`）設為 **ignore**，逼模型用「光譜其餘部分」預測——否則只是把答案抄回來。

## 教學重點
- 標準化是前提；PCA 先看結構，再決定監督模型。
- 同一套 PLS：目標連續→回歸（定量）、目標類別→判別（分類）。
- 小樣本（60）＋自訂門檻標籤，屬概念示範；交叉驗證是底線。

對應課程：[FTIR × 咖啡 Arabica/Robusta](https://tai-shengyeh.github.io/ftir-food-analysis/teaching.html)
｜[coffee 化學成分 PCA/GMM](https://tai-shengyeh.github.io/coffee_pgmm_R_code/coffee_pgmm.html)
