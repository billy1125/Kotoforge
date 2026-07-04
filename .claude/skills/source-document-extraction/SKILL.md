---
name: source-document-extraction
description: 抽取 papers/<paper>/drafts/ 資料夾內 PDF 或 Word（.docx）來源論文的正文並轉成 Markdown，用以建立或對照編修工作檔 Manuscript.md。當首次設定專案需把來源論文轉成 Manuscript.md、內建 Read 工具無法渲染 PDF、或需在來源文件中定位某章節或頁碼時使用。在 research conda 環境執行內附腳本，並輸出 UTF-8 檔供 Read 工具讀取。
---

# 來源文件文字抽取

抽取 PDF 或 Word（`.docx`）來源論文（通常位於 `papers/<paper>/drafts/`）的正文並轉成 Markdown，用以建立或對照編修工作檔 `Manuscript.md`。本機 Read 工具在此環境無法渲染 PDF（缺 poppler／pdftoppm），故改用本技能抽取。抽取後所有編修一律針對該篇 `papers/<paper>/Manuscript.md`（見 `CLAUDE.md` 第 5 節工作流程），`papers/<paper>/drafts/` 原始檔保留不動。

## 何時使用本技能

- 首次設定專案：把 `papers/<paper>/drafts/` 內的 PDF 或 `.docx` 正文抽成 Markdown，建立該篇 `papers/<paper>/Manuscript.md`。
- 必須讀取 PDF，但 Read 工具無法渲染。
- 需在來源文件中定位特定章節、小節或頁碼範圍。

## 環境需求

本技能在 conda 環境 **`research`**（Python 3.11）執行（**跨平台：Windows／macOS〔含 Apple Silicon〕／Linux 通用**）；完整環境需求另見 `CLAUDE.md` 第 8 節。為方便其他使用者，以下為本技能自含的最小安裝：

```bash
conda create -n research python=3.11 -y                        # 環境不存在時先建立
conda run -n research pip install pymupdf pdfplumber python-docx mammoth
```

所需套件：`pymupdf`（`import fitz`）、`pdfplumber`、`python-docx`、`mammoth`。若不可用，提示使用者執行上述安裝，勿自行改動環境。

## 操作步驟

1. **先驗證環境**；失敗時提示使用者安裝上述套件：
   ```bash
   conda run -n research python -c "import fitz, pdfplumber"
   ```
2. **執行內附腳本**，將結果輸出為 UTF-8 檔（見「指令範例」）。
3. **用 Read 工具開啟輸出檔**閱讀或核對內容。建立 `Manuscript.md` 時直接輸出到該篇 papers/<paper>/；僅供定位的概覽／片段檔則屬暫存。
4. **用完的暫存輸出檔請刪除**（`Manuscript.md` 除外），勿把定位用的暫存檔留在論文資料夾。

### Windows 限制（務必遵守）

- `conda run ... python -c "..."` **不支援含換行的多行腳本**——必須把程式寫成 `.py` 檔再執行（內附腳本已處理）。
- 中文直接 `print` 會觸發 **cp950 編碼錯誤**——腳本一律**將結果寫入 UTF-8 檔案**，再用 Read 讀取，不要 print 到終端。

## 指令範例

```bash
# 首次設定主線：Word 來源論文 → 轉 Markdown 建立該篇 papers/<paper>/Manuscript.md（保留標題層級）
conda run -n research python .claude/skills/source-document-extraction/scripts/extract_docx.py papers/<paper>/drafts/Manuscript.docx --markdown -o papers/<paper>/Manuscript.md

# PDF：列出每頁前 160 字概覽，協助定位章節（1-indexed 頁碼；暫存檔）
conda run -n research python .claude/skills/source-document-extraction/scripts/extract_pdf.py papers/<paper>/drafts/Manuscript.pdf --outline -o outline.txt

# PDF：抽取指定頁全文（支援逗號與區間，如 5-8,10）
conda run -n research python .claude/skills/source-document-extraction/scripts/extract_pdf.py papers/<paper>/drafts/Manuscript.pdf --pages 5-8 -o ch3.txt

# PDF：抽取整份 → Manuscript.md
conda run -n research python .claude/skills/source-document-extraction/scripts/extract_pdf.py papers/<paper>/drafts/Manuscript.pdf -o papers/<paper>/Manuscript.md

# Word：python-docx 抽段落＋表格純文字（預設；供核對定位的暫存檔）
conda run -n research python .claude/skills/source-document-extraction/scripts/extract_docx.py papers/<paper>/drafts/Manuscript.docx -o draft.txt
```

## 內附檔案

- `scripts/extract_pdf.py` —— PyMuPDF 抽取；`--outline` 概覽定位章節、`--pages` 抽特定頁、預設抽全份；輸出 UTF-8 檔。
- `scripts/extract_docx.py` —— python-docx 抽段落／表格純文字，或 `--markdown` 以 mammoth 轉 Markdown。
