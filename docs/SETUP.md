# 環境需求與設定

本檔是 `CLAUDE.md` §8 抽出的環境設定與疑難排解參考。**首次設定或環境出問題時才需要讀**；日常編修不需要。CLAUDE.md 只保留快速驗證指令與指向本檔的指標。

> 各項「勿自行改動使用者環境」的原則不變：以下建立／安裝指令一律**提示使用者執行**，AI 不自行更動 conda 環境或系統檔案。

## 1. 虛擬環境

- **環境名稱**：`research`
- **建立指令**（環境不存在時提示使用者執行）：
  ```bash
  conda create -n research python=3.11 -y
  ```

## 2. 套件安裝

- **讀 PDF**：`pymupdf`（主要文字抽取，`import fitz`）、`pdfplumber`（雙欄／表格備援）
- **讀 Word `.docx`**：`python-docx`（段落／表格精確擷取，首選）、`mammoth`（轉 Markdown，保留標題層級）
- **Markdown → Word `.docx`（產出稿件）**：`pypandoc`（Pandoc 的 Python 包裝）＋ **conda-forge 原生 `pandoc`**。GFM pipe table → Word 原生表格，可用 `--reference-doc` 套期刊樣式。

- **一次安裝指令（全作業系統通用）**：
  ```bash
  # 讀取類套件（pip）
  conda run -n research pip install pymupdf pdfplumber python-docx mammoth pypandoc
  # Pandoc 本體（conda-forge 各平台皆有原生版：win-64 / osx-64 / osx-arm64 / linux-64 / linux-aarch64）
  conda install -n research -c conda-forge pandoc -y
  ```

  > **不要用 `pypandoc_binary`**：它只附帶 x86_64 二進位，在 Apple Silicon／arm64 會出現 `bad CPU type in executable`。改用 conda-forge 的原生 `pandoc`，由 `pypandoc` 沿 PATH 呼叫，全平台一致、免依作業系統分流。

  > **macOS 殘留 x86_64 pandoc 的警告（已知狀況）**：`pypandoc` 在解析 pandoc 時，會**寫死先掃描** macOS 預設下載位置 `~/Applications/pandoc/pandoc`（早於走 PATH），這與 PATH 順序無關、調 PATH 也繞不過。若該位置殘留舊的 x86_64 版（例如曾用過 `pypandoc.download_pandoc()`），在 arm64 機器上每次轉檔會先噴一段 `[ERROR] Bad CPU type in executable` 警告——但 `pypandoc` 隨後會**自動 fallback** 到環境內的原生版，仍可正常轉檔，該紅字只是探測雜訊。要徹底消除警告，擇一處理：
  > - **移除殘留壞檔（推薦，一勞永逸）**：由使用者手動執行（屬 conda 環境外的系統檔案，勿自行更動）：`rm ~/Applications/pandoc/pandoc`（或改名備份 `mv ~/Applications/pandoc/pandoc ~/Applications/pandoc/pandoc.x86_64.bak`）。
  > - **指定路徑（不動系統檔）**：設環境變數 `PYPANDOC_PANDOC=$CONDA_PREFIX/bin/pandoc`，一旦設定 `pypandoc` 就只用此路徑，不再掃描其他位置。

## 3. 驗證指令

開始作業前先跑，失敗則提示使用者安裝（勿自行 `brew install` 或改動環境）：

```bash
# 一次驗證讀寫所需套件
conda run -n research python -c "import fitz, pdfplumber, docx, mammoth, pypandoc; print('imports ok')"
# 驗證 Pandoc 可用（markdown-to-word 需要）；正常應印出 pandoc 路徑且無 [ERROR] 字樣
conda run -n research python -c "import pypandoc; print(pypandoc.get_pandoc_path()); print(pypandoc.get_pandoc_version())"
```

**若最後一行報「找不到 pandoc」**：代表上面「Pandoc 本體」那步未完成，補跑後再驗證（提示使用者執行）：

```bash
conda install -n research -c conda-forge pandoc -y
```

## 4. Semantic Scholar MCP 與 API key

`citation-reference-management` skill 用 **Semantic Scholar MCP** 查證書目。專案根目錄 `.mcp.json` 已設好該 server（透過 `uvx` 執行）。

**前置需求：** `uvx`（隨 `uv` 一起安裝）。若沒有：`pip install uv`，或見 <https://docs.astral.sh/uv/>。

**API key 是選用的**：不設也能用，只是速率較低。申請免費 key：<https://www.semanticscholar.org/product/api>。

**設定方式（key 放進被 git 忽略的本機設定，不進版控）：** 複製範本 `.claude/settings.local.json.example` 為 `.claude/settings.local.json`，把 `env` 欄位的佔位字串換成你的 key：

```bash
cp .claude/settings.local.json.example .claude/settings.local.json
# 再編輯 .claude/settings.local.json，填入真實 key
```

範本內容：

```json
{
  "env": { "SEMANTIC_SCHOLAR_API_KEY": "s2k-REPLACE-WITH-YOUR-KEY" }
}
```

- 運作方式：Claude Code 啟動時注入 `settings.local.json` 的 `env`，`.mcp.json` 裡的 `"${SEMANTIC_SCHOLAR_API_KEY:-}"` 即由此展開；`:-` 表示未設時預設空字串，故**免 key 仍可運作**。
- **安全**：`.claude/settings.local.json` 已列入 `.gitignore`，**絕不要把真實 key 寫進 `.mcp.json`** 或任何進版控的檔案。
- 改完 `.mcp.json` 或 `settings.local.json` 後需**重啟 session** 才生效；用 `/mcp` 確認 `semantic-scholar` 連線狀態。
