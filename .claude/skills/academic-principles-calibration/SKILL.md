---
name: academic-principles-calibration
description: 處理「學術英文原則」——讀使用者從網路蒐集或自行整理的學術英文寫作規則／教材／詞彙表（放 writing-style/academic-principles/sources/ 的 md／docx／pdf，非本人所寫的文章），萃取成一份可操作的規則摘要 writing-style/academic-principles/academic-principles.md，供後續編修與該篇 style-guide.md 參考。當第一次設定學術原則、使用者在 academic-principles/sources/ 新增或更換規則文件、或說「更新學術英文原則／整理我蒐集的寫作規則／重新萃取學術原則」時使用。只處理英文語言層面，不搬運版權原文。個人本人筆法另由 personal-voice-calibration 處理。
---

# 學術英文原則校準（Academic Principles Calibration）

目的：把使用者蒐集或整理的**泛用學術英文寫作原則**（例如大學寫作中心教材、期刊寫作指南、學術詞彙／搭配表、語氣強度對照）蒸餾成一份**可操作的規則摘要**，讓後續編修有一致的「好的學術英文長怎樣」依據。

本技能專責「學術英文原則」——這些是**規則／參考資料**，通常來自網路或使用者自行彙整，**不是使用者本人寫的文章**。使用者本人的筆法由 [`personal-voice-calibration`](../personal-voice-calibration/SKILL.md) 處理；兩者形成一對，只差輸入語料。

## 產出

**共用摘要 `writing-style/academic-principles/academic-principles.md`**（跨所有論文）：從 `writing-style/academic-principles/sources/` 蒸餾的學術英文規則。`personal-voice-calibration` 產生該篇 `style-guide.md` 時會一併讀入這份摘要。

## 何時執行

- 第一次設定學術英文原則。
- 使用者在 `writing-style/academic-principles/sources/` 新增、更換、刪除規則文件後。
- 使用者明確說「更新學術英文原則」「整理我蒐集的寫作規則」「重新萃取學術原則」。

## 步驟

1. **盤點素材**：列出 `writing-style/academic-principles/sources/` 下的檔案。
   - 空 → 不硬產出。以標準說法提示使用者放入蒐集／整理的學術英文原則文件（md／docx／pdf 皆可，如寫作教材、期刊指南、學術詞彙表），並說明沒有這類素材時只能靠通用預設 `style-defaults.md`。
2. **讀取素材**：md 用 Read 直接讀；**docx／pdf 重用** `source-document-extraction` 的腳本在 `research` conda 環境抽成文字再讀（見下「抽取指令」）。
3. **萃取「規則」而非照抄內容**（摘要骨架）：
   - **語域與情態語氣強度**：客觀／正式的達成手段（被動、it-passive、讓證據當主詞）；情態詞強度階梯（must／will＞may／probably＞might／could／seems）。
   - **動詞語氣階梯**：不同證據強度對應的動詞（suggest／indicate＜demonstrate／confirm＜substantiate／refute），何時保守何時可強主張。
   - **名詞化與句法**：名詞化壓縮資訊、主題句 Topic+Comment、句子焦點放抽象概念。
   - **段落與過渡**：主題句功能、常用連接詞分類（增添／對比／因果／舉例／讓步／重述）。
   - **詞彙與搭配**：高頻學術搭配（robust results、pose a challenge、warrant further investigation…）；歸因 vs 背書強度。
   - **常見禁用／改寫**：口語與片語動詞（look into→investigate）、縮寫、絕對化字眼。
4. **寫入 `writing-style/academic-principles/academic-principles.md`**：用下方模板，條列可查閱；每條盡量附一個短例。**更新而非重寫**——保留使用者手動補充區，標出本次新增／變動處。
5. **不刪除 sources**：原始文件一律保留。
6. **回報**：用繁體中文簡述抓到的 3–5 個關鍵原則，提醒使用者可自行補充或覆寫任一條。

## 抽取指令（docx／pdf；先驗證環境）

```bash
conda run -n research python -c "import fitz, pdfplumber"   # 失敗則提示安裝，勿自行改動環境
# Word → 文字（供閱讀萃取，暫存）
conda run -n research python .claude/skills/source-document-extraction/scripts/extract_docx.py "writing-style/academic-principles/sources/<檔>.docx" -o principles.txt
# PDF → 文字
conda run -n research python .claude/skills/source-document-extraction/scripts/extract_pdf.py "writing-style/academic-principles/sources/<檔>.pdf" -o principles.txt
```
用完的暫存 `principles.txt` 請刪除。

## 學術原則摘要模板（寫入 academic-principles.md）

```markdown
# 學術英文原則摘要（Academic Principles）
最後更新：YYYY-MM-DD ｜ 依據：academic-principles/sources/ 內 N 份素材

## 1. 語域與情態語氣強度
- ...
## 2. 動詞語氣階梯（依證據強度）
- 保守：suggest／indicate／imply ｜ 較強：demonstrate／confirm ｜ 批判：refute／overstate（慎用）
## 3. 名詞化與句法
- ...
## 4. 段落與過渡（主題句、連接詞分類）
- ...
## 5. 詞彙與搭配（含歸因 vs 背書強度）
- ...
## 6. 常見禁用／改寫
- 口語→正式：look into→investigate、a lot of→considerable ...
## 7. 使用者手動補充
- （此區塊不由 AI 覆寫）
```

## 界線

- 只描述語言層面，不評論研究品質或邏輯。
- **萃取的是「規則」，不是原文**：不把版權素材（出版教材、他人文章）整段搬進摘要，只歸納可操作的原則與短例。
- **不刪除 `academic-principles/sources/` 內的原始文件。**
