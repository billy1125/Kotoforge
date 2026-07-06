---
name: docx-manuscript-sync
description: 使用者在別的軟體（Word／匯出的 .docx）改過稿件後，把該 docx 與作用中論文的 Manuscript.md 做段落級比對，逐塊呈現差異與建議，讓使用者裁定「哪一版為準、更新到哪個檔」，再把採用的改動合併回 Manuscript.md（留底可回退），選配用最終 md 重匯 Word 讓外部端同步。適合定期回合：在 Word 改一輪→比對→合併回稿件。當使用者說「把 Word 改的同步回來／比對 docx 與稿件／外部編輯合併回 Manuscript／定期同步 docx」時使用。**動手前必須先與使用者確認兩方檔案的確切路徑（md 端＋docx 端）並取得回覆，絕不自行猜測。** 只呈現與合併語言層差異，不自行判定研究邏輯或主張的更動——逐塊交使用者決定。
---

# Word（docx）↔ Manuscript.md 同步比對

使用者常在別的軟體（多為 Word）編修稿件、另存 `.docx`。本技能把該 docx 與**作用中論文**的
`papers/<paper>/Manuscript.md` 做**段落級比對**，逐塊呈現差異＋建議，讓使用者**逐塊裁定**
「哪一版為準、更新到哪個檔」，再把採用的改動合併回 `Manuscript.md`（依 `CLAUDE.md` §5 留底可回退）；
需要時用最終 md 以 `markdown-to-word` 重匯一份 Word，讓外部端同步到最新。可作為**定期回合**：
Word 改一輪 → 本技能比對 → 合併回稿件 → 選配重匯 Word。

## 何時使用
- 使用者在 Word／其他軟體改過稿，要把改動比對並合併回 `Manuscript.md`。
- 想定期（例如每次外部編修後）同步兩邊。
- 想在合併前先看清「哪些段落不同、各段哪版較新」。

## 最重要的原則：**不預設 docx 為準**
外部 docx **未必比 md 新**——它可能是較早的匯出，缺了近期在 md 裡做的編修。
逐塊判讀「哪一版較新／較好」時，**交叉下列訊號**，不要一律採 docx，也不要一律採 md：
- `papers/<paper>/revisions/` 最近數筆：md 端最近改了什麼、何時改的。
- `papers/<paper>/progress.md`：各節狀態（已定稿的節若 docx 是舊版，採 docx 即回退）。
- `papers/<paper>/style-guide.md`（尤其 §9 使用者規則）：術語統一、縮寫慣例、自稱用語、列舉標記等；
  某版若違反已確立規則（如縮寫重複展開、構念名不一致、`this study` 而非 `the present study`），通常是較舊／較差版。
- 內容訊號：某版含已被清除的冗長段、舊術語、舊拼寫 → 較舊。
> 若某塊 docx 疑似含**使用者在外部刻意做的實質內容更動**（新增句子、改引用、改主張／數據），
> **不要自行併入**，以「⚠️ 觀察」標出，明確請使用者確認那是不是他要保留的改動。

## 環境需求
conda 環境 `research`（見 `CLAUDE.md` §8）。本技能腳本需 `mammoth`：
```bash
conda run -n research pip install mammoth
```
先驗證；失敗則提示使用者安裝，勿自行改動環境：
```bash
conda run -n research python -c "import mammoth; print('mammoth ok')"
```

## 操作步驟
1. **【強制關卡】先與使用者確認「兩方到底是哪兩個檔」，取得明確回覆後才動手——絕不自行猜測或沿用。**
   - 逐一列出並請使用者確認：
     - **作用中論文**是哪一篇（哪個 `papers/<title>/`）。
     - **md 端**：目標工作稿路徑（預設 `papers/<title>/Manuscript.md`）。
     - **docx 端**：外部編修檔的**確切路徑與檔名**（可能在 `papers/<title>/drafts/`、論文根目錄，或使用者指定的其他位置；`drafts/` 內常有多個 `.docx`，**務必問清是哪一個**）。
   - **必做核對**：對兩個路徑各跑一次存在性／時間戳檢查並回報給使用者，例如：
     ```bash
     ls -la "papers/<title>/Manuscript.md" "papers/<title>/drafts/<edited>.docx"
     ```
     把兩檔的**修改時間**一併秀出（時間戳只是參考，不取代逐塊判讀新舊）。
   - **輸出一行確認、待使用者回覆「對」再進行**，例如：
     `即將比對 —— md：papers/<title>/Manuscript.md（mtime …）｜docx：papers/<title>/drafts/<edited>.docx（mtime …）。範圍：至 §X。確認？`
   - 兩檔任一不明確、對不上、或使用者未回覆 → **停下來問**，不得逕自往下跑腳本。
2. **執行差異腳本**（僅在步驟 1 已確認後），報告輸出到 scratchpad 暫存（勿放進論文資料夾）。只需比對到已編修的範圍時用 `--upto` 截斷：
   ```bash
   conda run -n research python .claude/skills/docx-manuscript-sync/scripts/diff_docx_md.py \
       papers/<paper>/drafts/<edited>.docx papers/<paper>/Manuscript.md \
       -o <scratchpad>/diff-out.txt --upto "4.3 Research Instrument"
   ```
   腳本會正規化（去 anchor、去 mammoth 跳脫反斜線、統一彎/直引號）後以 difflib 做段落級比對，
   標出 `[MD ]`（目前工作稿）與 `[DOCX]`（外部編輯版）。
3. **用 Read 讀報告**，**逐塊判讀新舊**（見上「不預設 docx 為準」），為每塊擬一句建議。
4. **逐塊呈現給使用者裁定**：每塊列出兩版關鍵差異＋你的建議＋新舊理由，請使用者選
   「① md 為準（不動 md）」或「② docx 為準（更新 md）」；差異瑣碎時可整塊選、或逐點選採。
   一次一塊、確認後再下一塊，避免混淆。
5. **落實採用的改動**（僅針對使用者選「docx 為準」或選採的點）：
   - **先 Read `Manuscript.md` 的 live 目標段落**確認 `old_string` 對得上（使用者可能又手改過），再 Edit。
   - 依 `CLAUDE.md` §5「編修歷程紀錄格式」在 `papers/<paper>/revisions/` 留一筆
     （檔名如 `YYYY-MM-DD-docx-sync-<段落標記>.md`，記錄四/各塊決定與實際改動），確保可回退。
   - 更新 `papers/<paper>/progress.md` 對應節備註。
6. **（選用）重匯 Word 讓外部端同步**：用最終 md 以 `markdown-to-word` 產出，
   輸出到 `papers/<paper>/Manuscript.docx`（工作匯出檔）；**不覆蓋** `drafts/` 的來源檔（`CLAUDE.md` §7：來源保留不動）。
   ```bash
   conda run -n research python .claude/skills/markdown-to-word/scripts/md_to_docx.py \
       papers/<paper>/Manuscript.md -o papers/<paper>/Manuscript.docx
   ```
7. **清理 scratchpad 暫存**（差異報告等），勿留在論文資料夾。

## 界線（務必遵守）
- **【最優先】未與使用者確認「兩方是哪兩個檔」（md 端＋docx 端的確切路徑）並取得回覆前，不得執行任何比對或編修**（見操作步驟 1）。路徑不明、對不上、或有多個候選檔時一律先問。
- 只**呈現**差異並**合併使用者採用的改動**；不自行判定或併入研究邏輯、主張、數據、引用的更動——逐塊交使用者決定。
- 疑似實質內容差異一律以「⚠️ 觀察」標出請使用者確認，不自行處理。
- 合併回 md 前必先 Read live 段落核對，不拿報告裡的舊文字直接替換。
- 與使用者溝通用繁體中文；稿件內容維持英文。

## 內附檔案
- `scripts/diff_docx_md.py` —— 以 mammoth 轉 docx→markdown，正規化後 difflib 段落級比對；`--upto` 可截斷比對範圍；輸出 UTF-8 報告。
