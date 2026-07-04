# academic-principles/ — 學術英文寫作原則（跨論文共用）

放你**從網路蒐集或自行整理**的學術英文寫作原則——寫作中心教材、期刊寫作指南、學術詞彙／搭配表、語氣強度對照等。這些是**通用規則／參考資料**，不是你本人寫的文章。跨所有論文共用。

## 怎麼用

1. 把規則文件放進 `sources/`（`.md`、`.docx`、`.pdf` 皆可）。
2. 請 Claude 執行 **`academic-principles-calibration`** skill，它會讀 `sources/` 萃取出一份 `academic-principles.md` 規則摘要。
3. 之後每篇論文產生 `style-guide.md` 時，會一併讀入這份摘要。
4. 素材有增減時，重跑一次 `academic-principles-calibration` 更新摘要即可。

- `sources/` 的原始文件**一律保留、不刪除**。
- 萃取的是**可操作的規則**，不是整段搬運版權原文。

## 摘要格式（academic-principles.md 骨架範例）

```markdown
# 學術英文原則摘要（Academic Principles）
最後更新：YYYY-MM-DD ｜ 依據：academic-principles/sources/ 內 N 份素材

## 1. 語域與情態語氣強度
## 2. 動詞語氣階梯（依證據強度）
## 3. 名詞化與句法
## 4. 段落與過渡
## 5. 詞彙與搭配
## 6. 常見禁用／改寫
## 7. 使用者手動補充
```

## 版控說明（重要）

`sources/` 與產生的 `academic-principles.md` 都是私人內容，已被 [`.gitignore`](../../.gitignore) 忽略、不進版控——只有本 `README.md` 與 `sources/.gitkeep` 進版控。

⚠️ **請勿把第三方版權素材放到會公開的位置**；留本機參考即可，不要 commit、不要 push。

## 對照

- 你本人的筆法素材（自己寫的文章）→ [`../personal-voice/`](../personal-voice/)
- 跨論文預設風格基準（語域、時態、格式）→ [`../style-defaults.md`](../style-defaults.md)
