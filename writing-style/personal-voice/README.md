# personal-voice/ — 你本人的英文筆法（跨論文共用）

放**你自己**寫過、已發表或滿意的英文論文／段落，讓 AI 學你偏好的語氣與筆法，避免把稿件改得不像你。這是跨所有論文共用的一層。

## 怎麼用

1. 把你自己的英文文章放進 `sources/`（`.md`、`.docx`、`.pdf` 皆可）。
2. 請 Claude 執行 **`personal-voice-calibration`** skill，它會讀 `sources/` 蒸餾出一份 `personal-voice.md` 摘要（你的「筆法 DNA」）。
3. 之後每篇論文產生 `style-guide.md` 時，會一併讀入這份摘要。
4. 素材有增減時，重跑一次 `personal-voice-calibration` 更新摘要即可。

- `sources/` 的原始文件**一律保留、不刪除**。
- 這裡放的是**你本人的文章**；別人的寫作教材／規則請放到 [`../academic-principles/`](../academic-principles/)。

## 版控說明（重要）

`sources/` 與產生的 `personal-voice.md` 都是私人內容，已被 [`.gitignore`](../../.gitignore) 忽略、不進版控——只有本 `README.md` 與 `sources/.gitkeep` 進版控。你放進來的檔案只留本機。

⚠️ **請勿把第三方版權素材**（出版教材、他人文章）放這裡；那類內容放 `../academic-principles/sources/`，且僅供個人研究參考、不要 commit。

## 對照

- 泛用學術英文原則（教材、期刊指南、詞彙表）→ [`../academic-principles/`](../academic-principles/)
- 跨論文預設風格基準（語域、時態、格式）→ [`../style-defaults.md`](../style-defaults.md)
