# 首次設定：為一篇論文建立資料夾與工作檔

本檔是 `CLAUDE.md` §5 抽出的**開新論文一次性流程**，只有「新增一篇論文」時才需要；日常編修循環見 CLAUDE.md §5。（給人看的簡版另見 `README.md`「開一篇新論文」。）

1. **建立論文資料夾**：複製範本骨架 `papers/_TEMPLATE/` 為 `papers/<title>/`（`<title>` 用簡短 kebab-case slug，如 `papers/technological-trust-recommendation-systems`）。骨架已含空的 `Manuscript.md`、`Basic Information.md`、`progress.md`、`references.md`、`style-guide.md` 與 `drafts/`、`target-journal-samples/`、`revisions/` 子夾。之後這篇的所有工作檔都放在此夾內。先填 `Basic Information.md`（含目標期刊）。
2. **放入來源文件**：使用者把原始論文（`.docx`、`.pdf` 等）放在 `papers/<title>/drafts/`（例如 `papers/<title>/drafts/Manuscript.docx`）。
3. **抽取正文成 Markdown**：用 `source-document-extraction` skill 把正文截取出來，存成**該篇的 `papers/<title>/Manuscript.md`**。這是這篇之後**所有編修的唯一工作檔**。
   - 範例指令（以現有論文為例）：
     ```bash
     conda run -n research python .claude/skills/source-document-extraction/scripts/extract_docx.py papers/technological-trust-recommendation-systems/drafts/Manuscript.docx --markdown -o papers/technological-trust-recommendation-systems/Manuscript.md
     ```
   - `drafts/` 的原始檔**保留不動**，僅作對照與回溯來源；**不再直接編輯 `drafts/`**。
4. **建立進度清單 `progress.md`**：在該篇資料夾建一份輕量編修進度表，逐章節標狀態（未動／進行中／已定稿），跨 session 一目了然。每次定稿後更新對應節（見 CLAUDE.md §5 日常編修循環最後一步）。
5. **（建議）風格校準**：把目標期刊範文放進該篇 `target-journal-samples/`，執行 `style-calibration` 產生該篇 `style-guide.md`；未做前以 `writing-style/style-defaults.md` 的預設基準先行。
