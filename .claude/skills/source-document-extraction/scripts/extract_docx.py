"""從 Word .docx 來源論文抽取文字（段落與表格），供建立或對照 Manuscript.md。

需在 conda 環境 `research` 下執行，並先安裝套件：
    conda run -n research pip install python-docx mammoth

與 extract_pdf.py 相同理由：一律將結果寫入 UTF-8 檔案再由其他工具讀取，
避免 Windows cp950 編碼錯誤與 `conda run -c` 多行限制。

用法範例：
    # 以 python-docx 抽取段落＋表格純文字（預設）
    conda run -n research python .claude/skills/source-document-extraction/scripts/extract_docx.py drafts/Manuscript.docx -o out.txt

    # 以 mammoth 轉為 Markdown（保留標題層級）建立 Manuscript.md
    conda run -n research python .claude/skills/source-document-extraction/scripts/extract_docx.py drafts/Manuscript.docx --markdown -o Manuscript.md
"""
import argparse
import sys


def extract_with_python_docx(path: str) -> str:
    """逐段落輸出；表格以 tab 分隔每列，置於 [TABLE] 標記之間。"""
    import docx  # python-docx

    doc = docx.Document(path)
    lines: list[str] = []
    for para in doc.paragraphs:
        text = para.text.strip()
        if text:
            # 保留標題層級提示，方便辨識章節
            style = (para.style.name or "") if para.style else ""
            prefix = f"[{style}] " if style.lower().startswith("heading") else ""
            lines.append(prefix + text)
    for ti, table in enumerate(doc.tables, 1):
        lines.append(f"\n[TABLE {ti}]")
        for row in table.rows:
            cells = [c.text.strip().replace("\n", " ") for c in row.cells]
            lines.append("\t".join(cells))
        lines.append("[/TABLE]")
    return "\n".join(lines)


def extract_with_mammoth(path: str) -> str:
    """轉為 Markdown，保留標題與清單結構。"""
    import mammoth

    with open(path, "rb") as f:
        result = mammoth.convert_to_markdown(f)
    return result.value


def main() -> None:
    ap = argparse.ArgumentParser(description="抽取 .docx 文字（輸出 UTF-8 檔案）")
    ap.add_argument("docx", help=".docx 路徑，例如 drafts/Manuscript.docx")
    ap.add_argument("--markdown", action="store_true",
                    help="改用 mammoth 轉為 Markdown（預設用 python-docx 抽純文字）")
    ap.add_argument("-o", "--out", required=True, help="輸出檔路徑（UTF-8）")
    args = ap.parse_args()

    text = (extract_with_mammoth(args.docx) if args.markdown
            else extract_with_python_docx(args.docx))

    with open(args.out, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"done -> {args.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
