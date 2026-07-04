---
name: markdown-to-word
description: 使用 Pandoc（透過 pypandoc）將含表格的 Markdown 稿件（如 Manuscript.md）轉為 Word .docx。當使用者想匯出、產生 Word 版稿件、為 docx 套用期刊樣式範本、或建立可編輯的樣式範本時使用。在 research conda 環境執行內附腳本。
---

# Markdown 轉 Word

將含表格的 Markdown 稿件（如 `Manuscript.md`）轉為 Word `.docx`。以 **Pandoc（透過 `pypandoc`）** 為首選方案：GFM pipe table 會轉為 Word 原生表格，標題、引用區塊、斜體、編號清單皆自動正確處理；並可用 `--reference-doc` 套用期刊樣式範本。

## 何時使用本技能

- 使用者要求匯出、產生 Word（`.docx`）版稿件。
- 使用者想為 Word 產出套用期刊樣式範本。
- 使用者想取得可編輯的樣式範本以定義文件樣式。

## 環境需求

本技能在 conda 環境 **`research`**（Python 3.11）執行（**跨平台：Windows／macOS〔含 Apple Silicon／arm64〕／Linux 通用**）；完整環境需求另見 `CLAUDE.md` 第 8 節。為方便其他使用者，以下為本技能自含的最小安裝：

```bash
conda create -n research python=3.11 -y                        # 環境不存在時先建立
conda run -n research pip install pypandoc                      # Python 封裝
conda install -n research -c conda-forge pandoc -y              # 原生 pandoc 二進位，全平台通用
```

> **勿用 `pypandoc_binary`**：其內含的 pandoc 為 x86_64，macOS Apple Silicon 無 Rosetta 時會報 `bad CPU type in executable`。請改用 conda-forge 的原生 `pandoc`（各平台皆有對應 build）。

若 Pandoc 不可用，提示使用者執行上述安裝，勿自行改動環境。

## 操作步驟

1. **先驗證 Pandoc 可用**；失敗時提示使用者安裝上述套件：
   ```bash
   conda run -n research python -c "import pypandoc; print(pypandoc.get_pandoc_path())"
   ```
2. **執行轉換**，產出 `.docx`（見「指令範例」）。
3. **（選用）需符合期刊格式時**：先以 `--make-reference` 產生樣式範本，請使用者在 Word 調整字體／行距／表格樣式後，再以 `--reference-doc` 套用。

## 指令範例

```bash
# 基本轉換
conda run -n research python .claude/skills/markdown-to-word/scripts/md_to_docx.py papers/<paper>/Manuscript.md -o papers/<paper>/Manuscript.docx

# 套用 Word 樣式範本（字體／行距／表格樣式）
conda run -n research python .claude/skills/markdown-to-word/scripts/md_to_docx.py papers/<paper>/Manuscript.md -o papers/<paper>/Manuscript.docx --reference-doc style_reference.docx

# 產生可編輯的預設樣式範本（在 Word 調整後再用 --reference-doc 套用）
conda run -n research python .claude/skills/markdown-to-word/scripts/md_to_docx.py --make-reference style_reference.docx
```

## 已知限制

- Pandoc **不會自動合併**視覺上跨列的儲存格（如表 9 的 α/CR/AVE 只寫在首列），會轉成空白儲存格。若需真正合併，於轉檔後再以 python-docx 後處理。
- 標題層級對應：Markdown `#` → Word Heading 1、`##` → Heading 2，依此類推。若需調整（如讓各章 `##` 變 Heading 1），可加 `--shift-heading-level-by`。

## 內附檔案

- `scripts/md_to_docx.py` —— 以 `pypandoc.convert_file(..., format="gfm", to="docx")` 轉換；支援 `--reference-doc` 套樣式、`--make-reference` 產範本。
