# Paperforger — 資管論文英文編修工作台 · Academic English Copy-Editing Workbench for IS Academic Papers

> 以 **Claude Code** 驅動的**資訊管理（IS／MIS）學術論文英文編修**工作台 — A **Claude Code–powered English copy-editing workbench** for **Information Systems (IS/MIS) academic manuscripts**. 逐段多版本潤稿、風格對齊目標期刊、引用查證，**只改英文、不動研究主張**。

![Claude Code](https://img.shields.io/badge/Claude%20Code-Skills-8A2BE2)
![Skills](https://img.shields.io/badge/Skills-9-1857B6)
![Semantic Scholar](https://img.shields.io/badge/Semantic%20Scholar-MCP-1857B6)
![License: MIT](https://img.shields.io/badge/License-MIT-2E9E4F)
![Language](https://img.shields.io/badge/繁體中文%20%2B%20English-bilingual-2E9E4F)

Paperforger 幫資管／資訊系統（Information Management, IS/MIS）研究者把論文的**英文**改到投稿水準：文法校正、學術語氣、敘述方式、用詞精準、句構流暢、時態一致。它的定位是**英文編修者（copy-editor / language editor），不是共同作者**——不動研究邏輯、主張、論點順序、數據或結論。可**同時編修多篇論文**，每篇各自一個資料夾。

Paperforger helps Information Systems (IS/MIS) researchers bring the **English** of their manuscripts to submission quality — grammar, academic tone, narrative style, word choice, sentence flow, and tense consistency — acting strictly as a **copy-editor / language editor, not a co-author**. It never changes the research logic, claims, data, or conclusions.

> 🤖 AI 的完整作業規則見 **[`CLAUDE.md`](CLAUDE.md)**（主指引）；本檔是給人看的快速上手。姊妹專案：文獻搜尋與回顧 [lit-review-kit](https://github.com/billy1125/lit-review-kit)。

## ⚠️ 免責聲明與使用須知 / Disclaimer

> **請先讀完再使用。** 使用本專案即表示你已理解並接受以下事項。**Please read before use.** Using this project means you accept the following.

- **定位 Scope**：**只處理英文語言層面**——文法、tone、narrative style、用詞、句構、時態一致性。**不修改**文章的內部邏輯、研究主張、論點順序、數據、引用或結論；發現疑似邏輯／事實問題時只以「⚠️ 觀察」提醒，由作者定奪。It edits **English only** and is a copy-editor, **not a co-author**.
- **專案性質 Side project**：這是作者**個人研究與測試用的 side project**，內容多為**與 AI 協作產生的初稿**，**測試尚未完整**、可能含錯誤或 bug，並非正式、穩定或經完整驗證的產品。
- **不保證正確 No warranty**：AI 的修改建議、引用查證回填的 metadata（來自 Semantic Scholar：標題／作者／年份／DOI／venue），以及一致性掃描結果**皆不保證正確或完整**。**採用任何一版前請自行檢查**；每次採用都會在 `revisions/` 留底，可隨時回退。作者不對任何因使用本專案而產生的後果負責（一切依 [MIT 授權](LICENSE) 之「AS IS」免責條款）。
- **學術倫理 Academic integrity**：AI 的修改**僅供輔助**；最終文字、研究主張、數據與投稿內容由**作者負全責**，並請遵守你所屬機構與期刊的學術誠信規範。
- **版權與素材 Copyright & materials**：你的稿件仍屬你自己；放入 `target-journal-samples/`、`drafts/` 的第三方期刊文章須為你**有合法權限取得**者，僅供風格對齊之個人研究用途，**勿違反出版商服務條款（ToS）**。
- **使用者自負責任 Use at your own risk.**

## ✨ 特色 / Features

- **多論文佈局 / Multi-paper layout**：每篇論文各自一個 `papers/<title>/`，工作檔互不干擾。
- **風格對齊 / Style calibration**：三個共用風格區塊（個人筆法、學術英文原則、通用預設）＋每篇目標期刊範文，產生該篇專屬 `style-guide.md`。
- **多版本校修 / Multi-version revision**：逐段給 ≤5 個可挑選、可回退的改法，不擅自大改，並提供「最小改動 vs 論述加厚」的密度選擇。
- **可回退 / Reversible**：每次採用的版本都在該篇 `revisions/` 留底。
- **引用查證 / Citation verification**：以 **Semantic Scholar MCP** 查證補齊 APA 書目，不憑記憶捏造。
- **匯出 Word / Word export**：用 Pandoc 把 `Manuscript.md` 轉 `.docx`，可套期刊樣式範本。
- **外部編修同步 / External-edit sync**：在 Word 改一輪後，把 `.docx` 與 `Manuscript.md` 段落級比對，逐塊裁定合併回稿件（先確認兩方檔案、不預設 docx 為準、可回退）。Round-trip changes edited in Word back into the manuscript, block by block.

## 🧩 內建 Skills

| Skill | 用途 |
|---|---|
| `personal-voice-calibration` | 從你本人的文章蒸餾個人筆法摘要，並產生該篇 `style-guide.md` |
| `academic-principles-calibration` | 從你蒐集／整理的學術英文原則文件萃取共用規則摘要 |
| `passage-revision` | 逐段英文校修，多版本供挑選（最常用） |
| `section-review` | 一個範圍的整體彙整審閱，給修改方向 |
| `source-document-extraction` | 從 `drafts/` 的 PDF／Word 抽出文字，建立 Markdown 版本的草稿文件 `Manuscript.md` |
| `citation-reference-management` | 引用一致性檢查、Semantic Scholar 查證補齊書目 |
| `markdown-to-word` | 用 Pandoc 把 `Manuscript.md` 匯出為 `.docx` |
| `docx-manuscript-sync` | 把在 Word 改過的 `.docx` 與 `Manuscript.md` 段落級比對，逐塊裁定後合併回稿件（先確認兩方檔案、可回退） |
| `final-consistency-sweep` | 定稿／匯出前的全文一致性與校對掃描 |

## 🔧 環境需求 / Requirements

需要 conda 環境 `research`（Python 3.11）與 Pandoc；引用查證另需 `uvx`（隨 `uv`）與**選用**的 `SEMANTIC_SCHOLAR_API_KEY`。完整安裝、API key 設定與疑難排解見 **[`docs/SETUP.md`](docs/SETUP.md)**。快速驗證：

```bash
conda run -n research python -c "import fitz, pdfplumber, docx, mammoth, pypandoc; print('imports ok')"
```

## 🚀 開一篇新論文 / Quick start

1. 複製骨架：`papers/_TEMPLATE/` → `papers/<你的論文-slug>/`。
2. 填 `Basic Information.md`（標題、作者、摘要、關鍵字、**目標期刊**）。
3. 把原始論文（`.docx`／`.pdf`）放進該篇 `drafts/`。
4. 請 Claude 用 `source-document-extraction` 抽出正文，建立該篇 `Manuscript.md`。
5. （建議）設定共用風格區塊：把自己的文章放 `writing-style/personal-voice/sources/`、蒐集的寫作原則放 `writing-style/academic-principles/sources/`、把目標期刊範文放該篇 `target-journal-samples/`，請 Claude 執行 `personal-voice-calibration`（與 `academic-principles-calibration`）產生 `style-guide.md`。
6. 開始逐段編修：指出段落與方向，用 `passage-revision` 挑版本；定稿前用 `final-consistency-sweep`、匯出用 `markdown-to-word`。

完整步驟見 **[`docs/NEW-PAPER.md`](docs/NEW-PAPER.md)**。

## 🗣️ 常用指令速查 / Command Cheatsheet

> 這裡的「指令」**不是要輸入的程式或 slash 指令，而是你直接對 Claude 說的話**——Claude 會據此自動選用對應 skill。用詞不必照抄，講清楚「想做什麼、往哪個方向」即可。These are **plain-language requests**, not slash commands.

| 想做的事 | 你可以這樣說 | 對應 skill／動作 |
|---|---|---|
| **切換／確認作用中論文** | 「切到 `<論文名>`」「現在編修的是哪一篇？」 | Claude 會**重新複習該篇** `style-guide.md`（含專屬規則）、`progress.md` 與近期 `revisions/`，並回一行確認後才動手 |
| 逐段潤稿（最常用） | 「這段改得更正式／更簡潔／更強調貢獻」「給我最小改動與論述加厚兩版」 | `passage-revision`（≤5 版供挑選，可回退） |
| 整節彙整審閱 | 「這一節整體看一下」「給我整體修改方向」 | `section-review` |
| 校準個人筆法／更新風格 | 「重新校準風格」「更新我的筆法」 | `personal-voice-calibration`（更新該篇 `style-guide.md`） |
| 更新學術英文原則 | 「更新學術英文原則」「整理我蒐集的寫作規則」 | `academic-principles-calibration` |
| 抽取來源論文正文 | 「把 `drafts/` 的 PDF／Word 抽成 `Manuscript.md`」 | `source-document-extraction` |
| 引用一致性／補書目 | 「檢查引用一致性」「用 Semantic Scholar 補齊書目」 | `citation-reference-management` |
| 定稿前掃描 | 「定稿前掃一遍」「全文一致性檢查」「校對一下」 | `final-consistency-sweep`（出清單，不自行大改） |
| 匯出 Word | 「匯出成 Word」「套期刊樣式轉 `.docx`」 | `markdown-to-word` |
| **同步 Word 改動回稿件** | 「把我在 Word 改的同步回來」「比對這份 `.docx` 與 `Manuscript.md`」 | `docx-manuscript-sync`（會**先跟你確認是哪兩個檔**，再逐塊比對、由你裁定合併，可回退） |
| 回退某段 | 「把這段改回上一版」 | 從該篇 `revisions/` 還原 |

> 小提醒：修改方向可**並用**（例如「更正式＋論述加厚」）；每次採用的版本都會在該篇 `revisions/` 留底，隨時能回退。**多篇並行時，換論文請先用第一列的說法**，避免把 A 篇的規則套到 B 篇。

## 🗂️ 目錄結構 / Structure

```
├── CLAUDE.md              # AI 主指引（跨所有論文）
├── docs/                  # SETUP.md（環境）、NEW-PAPER.md（開新論文）
├── .claude/skills/        # 9 個編修 skill（共用）
├── writing-style/           # 【共用】三個風格區塊
│   ├── style-defaults.md    #   通用預設（可編輯範本，進版控）
│   ├── personal-voice/      #   個人筆法：sources/＋personal-voice.md（git-ignored 私人；僅 README 進版控）
│   └── academic-principles/ #   學術英文原則：sources/＋academic-principles.md（git-ignored 私人；僅 README 進版控）
└── papers/
    ├── README.md         # 工作區說明（進版控）
    ├── _TEMPLATE/         # 新論文骨架，複製改名即可（進版控）
    └── <每篇一夾>/         # 你的論文（git-ignored 私人）：Manuscript.md、references.md…
```

## 📄 授權 / License

[MIT](LICENSE) © 2026 Cho-Hsun Lu (billy1125) — 內容「AS IS」提供，不負擔保責任，另見上方[免責聲明](#️-免責聲明與使用須知-disclaimer)。

本專案**未內含或改寫任何第三方原始碼**；引用查證所用的 Semantic Scholar MCP server（[akapet00/semantic-scholar-mcp](https://github.com/akapet00/semantic-scholar-mcp)）為透過 `.mcp.json` 呼叫的外部相依，非本 repo 的一部分。第三方服務與工具的致謝見 [`NOTICE`](NOTICE)。
