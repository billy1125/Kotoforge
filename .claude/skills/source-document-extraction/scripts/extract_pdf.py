"""從 drafts/ 的來源論文 PDF 抽取文字，供建立或對照 Manuscript.md。

需在 conda 環境 `research` 下執行（內含 PyMuPDF / pdfplumber）。
因 Windows 終端 cp950 編碼與 `conda run -c` 不支援多行/中文輸出，
本腳本一律將結果寫入 UTF-8 檔案，再由其他工具讀取，避免編碼錯誤。

用法範例：
    # 列出每頁前 N 字，協助定位章節（輸出 -> out.txt）
    conda run -n research python .claude/skills/source-document-extraction/scripts/extract_pdf.py drafts/Manuscript.pdf --outline -o out.txt

    # 抽取指定頁碼（1-indexed，可用逗號與區間）全文
    conda run -n research python .claude/skills/source-document-extraction/scripts/extract_pdf.py drafts/Manuscript.pdf --pages 5-8 -o ch3.txt

    # 抽取整份 -> Manuscript.md
    conda run -n research python .claude/skills/source-document-extraction/scripts/extract_pdf.py drafts/Manuscript.pdf -o Manuscript.md
"""
import argparse
import sys

import fitz  # PyMuPDF


def parse_pages(spec: str, page_count: int) -> list[int]:
    """將 '5-8,10,12' 解析為 0-indexed 頁碼清單。"""
    pages: list[int] = []
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            a, b = part.split("-", 1)
            pages.extend(range(int(a) - 1, int(b)))
        else:
            pages.append(int(part) - 1)
    return [p for p in pages if 0 <= p < page_count]


def main() -> None:
    ap = argparse.ArgumentParser(description="抽取 PDF 文字（輸出 UTF-8 檔案）")
    ap.add_argument("pdf", help="PDF 路徑，例如 drafts/Manuscript.pdf")
    ap.add_argument("--pages", help="頁碼（1-indexed），如 '5-8,10'；省略則全部")
    ap.add_argument("--outline", action="store_true",
                    help="僅輸出每頁前 160 字概覽，協助定位章節")
    ap.add_argument("-n", "--head", type=int, default=160,
                    help="--outline 時每頁取用字數（預設 160）")
    ap.add_argument("-o", "--out", required=True, help="輸出檔路徑（UTF-8）")
    args = ap.parse_args()

    doc = fitz.open(args.pdf)
    indices = (parse_pages(args.pages, doc.page_count)
               if args.pages else list(range(doc.page_count)))

    chunks: list[str] = []
    if args.outline:
        chunks.append(f"total pages: {doc.page_count}")
        for i in indices:
            head = doc[i].get_text().strip().replace("\n", " ")[: args.head]
            chunks.append(f"--- p{i + 1} --- {head}")
    else:
        for i in indices:
            chunks.append(f"\n========== PAGE {i + 1} ==========\n")
            chunks.append(doc[i].get_text())

    with open(args.out, "w", encoding="utf-8") as f:
        f.write("\n".join(chunks) if args.outline else "".join(chunks))

    print(f"done -> {args.out} ({len(indices)} pages)", file=sys.stderr)


if __name__ == "__main__":
    main()
