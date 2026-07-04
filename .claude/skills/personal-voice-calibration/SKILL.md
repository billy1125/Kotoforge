---
name: personal-voice-calibration
description: 處理「個人筆法」——讀使用者自己寫的英文論文／段落（放 writing-style/personal-voice/sources/ 的 md／docx／pdf），萃取其語氣、句構、時態、用詞偏好，蒸餾成共用的 writing-style/personal-voice/personal-voice.md 摘要；再結合學術英文原則摘要、通用預設與該篇 papers/<title>/target-journal-samples/，產生或更新該篇 papers/<title>/style-guide.md。當某篇論文第一次設定、使用者在 personal-voice/sources/ 新增或更換自己的文章、或說「重新校準風格／更新我的筆法／更新風格指引」時使用。這份風格指引是該篇後續所有編修（passage-revision、section-review）的依據。學術英文原則文件（非本人文章）另由 academic-principles-calibration 處理。
---

# 個人筆法校準（Personal Voice Calibration）

目的：把**使用者本人的筆法**與**目標期刊慣例**轉成可操作的風格指引，讓後續編修有所本，而不是憑空套用通用學術英文。本技能專責「個人筆法」；泛用的「學術英文原則」文件（使用者從網路蒐集或自行整理者）由 [`academic-principles-calibration`](../academic-principles-calibration/SKILL.md) 處理。

## 兩件產出（分清楚）

1. **共用摘要 `writing-style/personal-voice/personal-voice.md`**（跨所有論文）：從 `writing-style/personal-voice/sources/` 裡使用者自己寫的文章蒸餾出的「筆法 DNA」。只在個人素材變動時更新。
2. **該篇風格指引 `papers/<paper>/style-guide.md`**（每篇一份）：結合 `personal-voice.md` ＋ `academic-principles.md` ＋ `style-defaults.md` ＋ 該篇 `target-journal-samples/`，落定這一篇實際依循的規範。

## 何時執行

- 專案第一次設定。
- 使用者在 `writing-style/personal-voice/sources/` 或 `papers/<paper>/target-journal-samples/` 新增、更換、刪除檔案後。
- 使用者明確說「重新校準」「更新我的筆法」「更新風格指引」。

## 步驟

### A. 更新共用個人筆法摘要（個人素材有變動時）

1. **盤點素材**：列出 `writing-style/personal-voice/sources/` 下的檔案。
   - 空 → 不硬產出。以標準說法提示使用者把自己寫過、已發表或滿意的英文論文／段落放進去（md／docx／pdf 皆可），並說明沒有個人素材時只能靠學術原則與通用預設。
2. **讀取素材**：md 用 Read 直接讀；**docx／pdf 重用** `source-document-extraction` 的腳本在 `research` conda 環境抽成文字再讀（見下「抽取指令」）。重點看「英文怎麼寫」，不是研究內容。
3. **萃取並寫入 `writing-style/personal-voice/personal-voice.md`**：用下方模板；每條盡量附一個從素材觀察到的短例（節錄 <15 字，不整段照抄）。**更新而非重寫**——保留使用者手動補充區。
4. **不刪除 sources**：原始文件一律保留。

### B. 產生／更新該篇 style-guide.md

1. **讀四類輸入**：`personal-voice.md`（個人筆法）＋ `writing-style/academic-principles/academic-principles.md`（學術原則，若存在）＋ `writing-style/style-defaults.md`（通用預設）＋ 該篇 `papers/<paper>/target-journal-samples/`（期刊範文；空則註明期刊面向資料不足）。
2. **萃取以下面向**（指引骨架）：
   - **正式度與語氣**：學術正式 / 偏敘事 / 直接俐落？是否容許 we、避免縮寫？
   - **人稱與語態**：第一人稱（we／this study）使用程度；主動 vs 被動的比例傾向。
   - **句長與句構**：偏短句俐落，還是長句多子句？常見開頭句型（This paper…、Drawing on…、Prior research suggests…）。
   - **時態慣例**：文獻回顧、方法、結果、討論各段常用時態。
   - **段落與過渡**：如何起承轉合，常用連接詞與過渡語。
   - **用詞偏好**：偏好／避免的字；領域術語的標準寫法。
   - **貢獻與主張的表述強度**：強主張（establishes）還是保守（may indicate）。
   - **個人筆法 vs 期刊慣例衝突**：兩者衝突時分開記錄並標明，供使用者決定優先順序。
3. **寫入 `papers/<paper>/style-guide.md`**：條列、可查閱格式；已存在則更新非重寫，保留使用者手動加註。
4. **回報**：用繁體中文簡述抓到的 3–5 個關鍵特徵，提醒使用者可自行補充或覆寫任一條。

## 抽取指令（docx／pdf；先驗證環境）

```bash
conda run -n research python -c "import fitz, pdfplumber"   # 失敗則提示安裝，勿自行改動環境
# Word → 文字（供閱讀萃取，暫存）
conda run -n research python .claude/skills/source-document-extraction/scripts/extract_docx.py "writing-style/personal-voice/sources/<檔>.docx" -o voice.txt
# PDF → 文字
conda run -n research python .claude/skills/source-document-extraction/scripts/extract_pdf.py "writing-style/personal-voice/sources/<檔>.pdf" -o voice.txt
```
用完的暫存 `voice.txt` 請刪除。

## 個人筆法摘要模板（寫入 personal-voice.md）

```markdown
# 個人筆法摘要（Personal Voice）
最後更新：YYYY-MM-DD ｜ 依據：personal-voice/sources/ 內 N 份素材

## 1. 語氣與正式度
- ...
## 2. 人稱與語態
- ...
## 3. 句構與句長（含偏好開頭句型）
- ...
## 4. 時態慣例（依章節）
- 文獻回顧：... ｜ 方法：... ｜ 結果：... ｜ 討論：...
## 5. 過渡與段落
- ...
## 6. 用詞：偏好／避免（附語詞替換）
- 偏好：... ｜ 避免：...
## 7. 主張強度
- ...
## 8. 使用者手動補充
- （此區塊不由 AI 覆寫）
```

## 風格指引模板（寫入 papers/<paper>/style-guide.md）

```markdown
# 風格指引（Style Guide）
最後更新：YYYY-MM-DD ｜ 依據：個人筆法摘要、學術原則摘要、通用預設、目標期刊範文 M 篇

## 1. 語氣與正式度
## 2. 人稱與語態
## 3. 句構與句長
## 4. 時態慣例（依章節）
## 5. 過渡與段落
## 6. 用詞：偏好／避免
## 7. 主張強度
## 8. 個人筆法 vs 期刊慣例（衝突點）
- （由使用者決定優先順序）
## 9. 使用者手動補充
- （此區塊不由 AI 覆寫）
```

## 界線

- 只描述語言層面，不評論研究品質或邏輯。
- 不把任一素材的內容當成可抄的素材；萃取的是「寫法」不是「內容」。
- **不刪除 `personal-voice/sources/` 內的原始文件。**
