"""比對外部編輯的 Word（.docx）與工作稿 Manuscript.md，輸出段落級差異報告。

用途：使用者在別的軟體（Word／Google Docs 匯出的 .docx）改過稿件後，
把該 docx 與目前 Manuscript.md 做段落級比對，產出「哪些段落不同」的報告，
供逐塊人工裁定（哪一版為準、更新到哪個檔）。**本腳本只負責可靠的差異偵測，
不做任何自動合併，也不判斷新舊——新舊與取捨由 SKILL.md 指示 Claude 交叉
revisions/、progress.md、style-guide 後逐塊判讀。**

需在 conda 環境 `research` 下執行（需 mammoth）：
    conda run -n research pip install mammoth

一律將結果寫入 UTF-8 檔案再由 Read 工具讀取，避免 Windows cp950 編碼錯誤。

用法：
    conda run -n research python .claude/skills/docx-manuscript-sync/scripts/diff_docx_md.py \
        papers/<paper>/drafts/edited.docx papers/<paper>/Manuscript.md -o diff-out.txt
    # 只比對到某標題為止（兩份都截斷），例如尚未編修到的章節不比：
    #   --upto "4.3 Research Instrument"
"""
import argparse
import difflib
import re
import sys

ANCHOR = re.compile(r'<a id="[^"]*"></a>')
ESCAPE = re.compile(r'\\(?=[^\w\s])')  # mammoth 在標點前加的跳脫反斜線


def docx_to_markdown(path: str) -> str:
    import mammoth
    with open(path, "rb") as f:
        return mammoth.convert_to_markdown(f).value


def read_text(path: str) -> str:
    if path.lower().endswith(".docx"):
        return docx_to_markdown(path)
    with open(path, encoding="utf-8") as f:
        return f.read()


def normalize(text: str, upto: str | None) -> list[str]:
    text = ANCHOR.sub("", text)
    text = ESCAPE.sub("", text)
    # 統一彎引號為直引號，讓純標點差異不算差異
    text = (text.replace("’", "'").replace("‘", "'")
                .replace("“", '"').replace("”", '"'))
    lines = [ln.strip() for ln in text.split("\n") if ln.strip()]
    if upto:
        for i, ln in enumerate(lines):
            if ln.lstrip("# ").startswith(upto):
                return lines[:i]
    return lines


def main() -> None:
    ap = argparse.ArgumentParser(description="比對 .docx 與 Manuscript.md（段落級差異，輸出 UTF-8 報告）")
    ap.add_argument("docx", help="外部編輯的 .docx 路徑")
    ap.add_argument("md", help="工作稿 Manuscript.md 路徑")
    ap.add_argument("-o", "--out", required=True, help="差異報告輸出檔（UTF-8）")
    ap.add_argument("--upto", default=None,
                    help="只比對到此標題文字為止（去除 # 後 startswith 比對），例如 \"4.3 Research Instrument\"")
    args = ap.parse_args()

    md = normalize(read_text(args.md), args.upto)
    docx = normalize(read_text(args.docx), args.upto)

    sm = difflib.SequenceMatcher(a=md, b=docx, autojunk=False)
    out: list[str] = []
    n = 0
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        n += 1
        out.append(f"=== BLOCK {n} : {tag.upper()} ===")
        if tag in ("replace", "delete"):
            for x in md[i1:i2]:
                out.append("[MD  ] " + x)
        if tag in ("replace", "insert"):
            for x in docx[j1:j2]:
                out.append("[DOCX] " + x)
        out.append("")

    header = (f"# docx vs md 段落級差異\n"
              f"# MD paras: {len(md)}  DOCX paras: {len(docx)}  diff blocks: {n}\n"
              f"# [MD ]=目前工作稿  [DOCX]=外部編輯版。新舊與取捨由人工逐塊判讀，勿預設 docx 為準。\n\n")
    body = "\n".join(out) if out else "NO PARAGRAPH-LEVEL DIFFERENCES（兩份到比對範圍為止相同）"

    with open(args.out, "w", encoding="utf-8") as f:
        f.write(header + body)

    print(f"done -> {args.out}  (blocks: {n})", file=sys.stderr)


if __name__ == "__main__":
    main()
