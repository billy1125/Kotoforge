---
name: citation-reference-management
description: 管理 references.md 與 Manuscript.md 的引用一致性，並用 Semantic Scholar 查證補齊待補書目。當需要檢查孤兒引用／未被引用書目／待補清單、用真實資料庫查證並補齊 APA 書目、從 source PDF 重建參考清單、或定稿前產生 References 章節時使用。在 research conda 環境執行內附腳本，輸出 UTF-8 報告。
---

# 引用與參考文獻管理

管理單一書目來源 `references.md` 與 `Manuscript.md` 正文引用的一致性，並提供以 **Semantic Scholar** 查證真實書目、補齊 APA 7th 條目的能力。

> **核心鐵則（承襲 paper-search）：所有補入的書目一律來自 Semantic Scholar 實際回傳，絕不憑記憶捏造標題、作者、年份、期刊或引用數。** 工具不可用時引導使用者排查環境，而非臆造書目。

## 何時使用本技能

- 檢查正文引用與 `references.md` 是否一致（孤兒引用／未被引用／待補）。
- 補齊 `references.md` 中的 `*[ 待補 ]*` 佔位條目。
- 從 `papers/<paper>/drafts/Manuscript.pdf` 參考清單頁的內容重建書目。
- 稿件定稿前，從 `references.md` 產生稿件 References 章節。

## 環境需求

本技能在 conda 環境 **`research`** 執行（**跨平台：Windows／macOS〔含 Apple Silicon〕／Linux 通用**）；完整環境需求另見 `CLAUDE.md` 第 8 節。為方便其他使用者，自含設定如下：

```bash
conda create -n research python=3.11 -y       # 環境不存在時先建立；check_citations.py 僅用標準庫，免額外套件
```

- 書目查證需 **Semantic Scholar MCP**（見「MCP 設定」節），執行需 `uvx`（隨 uv 安裝：`pip install uv`，或見 <https://docs.astral.sh/uv/>）。`SEMANTIC_SCHOLAR_API_KEY` 選用（留空可用，速率較低）。

## 操作步驟（三條工作流程）

### 工作流程 a：一致性檢查

1. 跑 `check_citations.py`（見「指令範例」），輸出 UTF-8 報告。
2. 用 Read 工具開啟報告，依四類處理：
   - **① 孤兒引用**（正文有、書目無）與 **④ 年份疑慮**：回報主線／作者裁示。
   - **② 未被引用書目**：回報主線確認是否刪除（多為舊 FinTech 殘留）。
   - **③ 被引用但待補**：即「優先補齊清單」，交工作流程 b。
3. 用完的暫存報告檔請刪除，勿留在論文資料夾。

### 工作流程 b：Semantic Scholar 查證補齊

1. 取工作流程 a 的 **③ 待補清單**，逐筆以「作者 + 年份 + 題名關鍵詞」查 Semantic Scholar MCP。
2. 從 MCP 回傳挑出正確命中（**逐筆核對 title／authors／venue／year**，命中存疑時擱置回報，不得臆造）。
3. 轉為 APA 7th 條目（作者姓氏排序、斜體期刊名、卷期頁、DOI）。
4. 回報主線，由主線寫入 `references.md` 取代佔位——**本技能不直接改 `references.md`**，以符合 CLAUDE.md「補書目 → 確認 → 寫入」流程與稽核獨立原則。

### 工作流程 c：從 PDF 第 27–28 頁重建清單

1. 以 `Skill` 工具呼叫 **`source-document-extraction`**，抽 `papers/<paper>/drafts/Manuscript.pdf` 參考清單所在頁（如 `--pages 27-28`）——不重複 PDF 抽取邏輯，一律委派該技能。
2. Read 抽出的參考清單文字，對照工作流程 a 的 ①③ 結果，確認本稿實際引用的條目。
3. 逐條以 Semantic Scholar 查證 venue／DOI，組為 APA 7th。
4. 回報主線重建 `references.md`（取代與本稿不符的舊 FinTech「待補」清單）。

## MCP 設定（Semantic Scholar）

專案根目錄 `.mcp.json` 已設定 `semantic-scholar` server。**API key 以環境變數注入，不寫死於 `.mcp.json`**（`.mcp.json` 會進版控）：

```json
{
  "mcpServers": {
    "semantic-scholar": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/akapet00/semantic-scholar-mcp", "semantic-scholar-mcp"],
      "env": { "SEMANTIC_SCHOLAR_API_KEY": "${SEMANTIC_SCHOLAR_API_KEY:-}" }
    }
  }
}
```

**真實 key 放在 `.claude/settings.local.json`（專案內、預設被 git 忽略、不進版控）的 `env` 欄位：**

```json
{
  "env": { "SEMANTIC_SCHOLAR_API_KEY": "s2k-你的金鑰" }
}
```

- 運作方式：Claude Code 啟動時注入 `settings.local.json` 的 `env`，`.mcp.json` 的 `${SEMANTIC_SCHOLAR_API_KEY:-}` 即由此展開；`:-` 預設空字串，**未設 key 時仍可免金鑰運作**（速率較低）。申請免費 key：<https://www.semanticscholar.org/product/api>。
- **絕不把真實 key 寫進 `.mcp.json` 或任何進版控的檔案**；一律放 `.claude/settings.local.json`（已被全域 `~/.config/git/ignore` 之 `**/.claude/settings.local.json` 忽略）。
- 修改 `.mcp.json` 或 `settings.local.json` 後需**重啟 session** 才會載入；以 `/mcp` 確認 `semantic-scholar` 連線狀態。

### Windows 限制（務必遵守）

- `conda run ... python -c "..."` **不支援含換行的多行腳本**——程式已寫成 `.py` 檔。
- 中文直接 `print` 會觸發 **cp950 編碼錯誤**——腳本一律**將報告寫入 UTF-8 檔案**，再用 Read 讀取，不要 print 到終端。

## 指令範例

```bash
# 一致性檢查：比對正文引用 ↔ references.md，輸出四類報告
conda run -n research python .claude/skills/citation-reference-management/scripts/check_citations.py papers/<paper>/Manuscript.md papers/<paper>/references.md -o citation_report.md

# 重建清單前：抽 PDF 第 27–28 頁參考清單（委派 source-document-extraction）
conda run -n research python .claude/skills/source-document-extraction/scripts/extract_pdf.py papers/<paper>/drafts/Manuscript.pdf --pages 27-28 -o refs_pdf.txt
```

## 內附檔案

- `scripts/check_citations.py` —— 比對 `Manuscript.md` 正文引用與 `references.md` 書目；解析括號並列式與敘述式引用、區分完整／待補條目；輸出四類報告（① 孤兒引用、② 未被引用書目、③ 待補優先清單、④ 年份疑慮）。輸出 UTF-8 檔。
