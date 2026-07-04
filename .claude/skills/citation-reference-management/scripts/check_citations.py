"""比對 Manuscript.md 正文引用與 references.md 書目的一致性。

需在 conda 環境 `research` 下執行（本腳本只用標準庫，免額外套件）。
因 Windows 終端 cp950 編碼與 `conda run -c` 不支援多行/中文輸出，
本腳本一律將報告寫入 UTF-8 檔案，再由 Read 工具讀取，避免編碼錯誤。

產出四類報告：
  ① 孤兒引用    —— 正文引用，但 references.md 無對應條目（最高優先）
  ② 未被引用書目 —— references.md 有條目，但正文未引用
  ③ 待補（被引用）—— 正文有引用且 references.md 仍為「待補」佔位（交查證補齊）
  ④ 年份疑慮    —— 同姓氏但年份相差 ≤1 的可疑配對（如 Glover & Benbasat 2010/2011）

用法範例：
    conda run -n research python .claude/skills/citation-reference-management/scripts/check_citations.py \
        Manuscript.md references.md -o citation_report.md
"""
import argparse
import re
import sys
from collections import defaultdict

# --- 正文引用（括號內並列式）：只抓含四位年份的括號，避免誤抓一般括號 ---
CITE_BLOCK = re.compile(r"\(([^()]*?\b(?:19|20)\d{2}[a-z]?[^()]*?)\)")
# 拆單筆 "作者, 年份[, 年份...]"；要求 author 段＋逗號，純數字片段會被拒
ENTRY = re.compile(
    r"^\s*(?P<authors>.+?),\s*"
    r"(?P<years>(?:19|20)\d{2}[a-z]?(?:\s*,\s*(?:19|20)\d{2}[a-z]?)*)\s*$"
)

# --- 正文引用（敘述式）：作者名在括號外，如 "Burke et al. (2011) noted" ---
_NAME = r"(?:[A-Z][\w.'’-]*|et\s+al\.?|&|and)"
NARRATIVE = re.compile(
    r"(?P<authors>" + _NAME + r"(?:\s+" + _NAME + r")*)\s*"
    r"\((?P<years>(?:19|20)\d{2}[a-z]?(?:\s*,\s*(?:19|20)\d{2}[a-z]?)*)\)"
)

# --- references.md 條目 ---
PLACEHOLDER = re.compile(r"\*\[\s*待補\s*\]\*")
REF_HEAD = re.compile(r"^(?P<authors>[A-ZÀ-Ý].+?)\s*\((?P<year>(?:19|20)\d{2}[a-z]?)\)")
REF_BULLET = re.compile(r"^-\s*(?P<authors>[A-Z].+?)\s*\((?P<year>(?:19|20)\d{2})[^)]*\)")

YEAR_TOKEN = re.compile(r"(?:19|20)\d{2}[a-z]?")

# 敘述式作者段可能誤含的句首虛詞，逐一從左剝除
STOPWORDS = {
    "the", "in", "as", "these", "this", "their", "a", "an", "for", "by", "with",
    "from", "on", "at", "more", "recently", "while", "although", "however", "thus",
    "moreover", "furthermore", "such", "both", "here", "there", "we", "it", "they",
    "its", "our", "that", "when", "where", "using", "based", "see", "of", "to",
    "is", "are", "was", "were", "be", "been", "study", "model", "framework",
}


def first_author_surname(authors: str) -> str:
    """從作者字串取第一作者姓氏（兩端共有的最小公因數）。"""
    s = re.sub(r"['’]s\b", "", authors)  # 去所有格（Endsley's → Endsley）
    s = re.sub(r"\bet\s+al\.?", "", s, flags=re.IGNORECASE).strip()
    # references 端第一作者寫成 "Surname, Initials"；正文端用 & / and 連接
    # 故取「第一個逗號 / & / and 之前」即為第一作者姓氏（含 de/van 等小寫前綴）
    s = re.split(r"\s*(?:,|&|\band\b)\s*", s, maxsplit=1)[0]
    return s.strip()


def normalize_key(authors: str, year: str) -> str:
    surname = first_author_surname(authors)
    surname = re.sub(r"[^\w ]", "", surname, flags=re.UNICODE)  # 去標點（含連字號）
    surname = re.sub(r"\s+", "_", surname.casefold().strip())
    return f"{surname}|{year}"


def year_of(key: str) -> int:
    return int(re.match(r"(\d{4})", key.split("|", 1)[1]).group(1))


def surname_of(key: str) -> str:
    return key.split("|", 1)[0]


def _strip_leading_stopwords(authors: str) -> str:
    tokens = authors.split()
    while tokens and tokens[0].casefold().strip(".") in STOPWORDS:
        tokens.pop(0)
    return " ".join(tokens)


def parse_manuscript(path: str) -> dict:
    """回傳 {key: {"raw": set, "first_line": int, "count": int}}。"""
    cites: dict = defaultdict(lambda: {"raw": set(), "first_line": None, "count": 0})

    def add(authors: str, years: str, line_no: int, display: str) -> None:
        authors = authors.strip()
        # 作者段必須含字母，否則為敘述式內層 (2004, 2006) 被誤判成作者的雜訊
        if not re.search(r"[A-Za-zÀ-ɏ]", authors):
            return
        for yr in YEAR_TOKEN.findall(years):
            key = normalize_key(authors, yr)
            if key.startswith("|"):
                continue
            e = cites[key]
            e["raw"].add(display.strip())
            e["count"] += 1
            if e["first_line"] is None:
                e["first_line"] = line_no

    with open(path, encoding="utf-8") as f:
        for ln, line in enumerate(f, 1):
            # 括號並列式：(Author, year; Author, year)
            for block in CITE_BLOCK.findall(line):
                for piece in block.split(";"):
                    m = ENTRY.match(piece)
                    if m:
                        add(m.group("authors"), m.group("years"), ln, piece)
            # 敘述式：Author et al. (year)
            for m in NARRATIVE.finditer(line):
                authors = _strip_leading_stopwords(m.group("authors"))
                add(authors, m.group("years"), ln, f"{authors} ({m.group('years')})")
    return cites


def parse_references(path: str, include_authored: bool) -> tuple:
    """回傳 (complete, pending, meta, by_surname)。

    complete/pending 為 key 集合；meta[key] = 原始顯示行；
    by_surname[surname] = list[(year_int, status, key)]。
    """
    complete: set = set()
    pending: set = set()
    meta: dict = {}
    by_surname: dict = defaultdict(list)

    with open(path, encoding="utf-8") as f:
        for line in f:
            raw = line.rstrip("\n")
            stripped = raw.strip()
            if not stripped or stripped.startswith("#") or stripped.startswith(">"):
                continue
            m = REF_HEAD.match(stripped)
            status_default = "complete"
            if not m and include_authored:
                m = REF_BULLET.match(stripped)  # "- Lu (2024) — ..."
            if not m:
                continue
            key = normalize_key(m.group("authors"), m.group("year"))
            status = "pending" if PLACEHOLDER.search(stripped) else status_default
            (pending if status == "pending" else complete).add(key)
            meta.setdefault(key, stripped)
            by_surname[surname_of(key)].append((year_of(key), status, key))
    return complete, pending, meta, by_surname


def near_miss(key: str, by_surname: dict, tol: int) -> tuple | None:
    """同姓氏、年份相差 ≤ tol+1 的最接近書目條目；無則 None。"""
    surname, yr = surname_of(key), year_of(key)
    best = None
    for cand_year, status, cand_key in by_surname.get(surname, []):
        diff = abs(cand_year - yr)
        if 0 < diff <= tol + 1:
            if best is None or diff < best[0]:
                best = (diff, cand_key, status)
    return best


def build_report(cites, complete, pending, meta, by_surname, tol, paths) -> str:
    orphans, year_doubts, pending_cited = [], [], []
    for key in cites:
        if key in complete:
            continue
        if key in pending:
            pending_cited.append(key)
            continue
        hit = near_miss(key, by_surname, tol)
        if hit:
            year_doubts.append((key, hit[1]))
        else:
            orphans.append(key)

    cited_keys = set(cites)
    uncited = [k for k in (complete | pending) if k not in cited_keys]

    def disp(key):
        e = cites[key]
        sample = sorted(e["raw"])[0] if e["raw"] else key
        return f"`{key}`（{sample}；行 {e['first_line']}，{e['count']} 次）"

    out = []
    out.append("# 引用一致性報告（manuscript ↔ references）\n")
    out.append(f"- 稿件：`{paths[0]}`")
    out.append(f"- 書目：`{paths[1]}`")
    out.append(
        f"- 統計：正文引用 {len(cites)} 筆（去重）；書目完整 {len(complete)}、"
        f"待補 {len(pending)}\n"
    )

    out.append("## ① 孤兒引用（正文有，references.md 無對應條目）｜最高優先\n")
    if orphans:
        for key in sorted(orphans):
            out.append(f"- {disp(key)}")
    else:
        out.append("（無）")
    out.append("")

    out.append("## ② 未被引用的書目（references.md 有，正文未引用）\n")
    if uncited:
        for key in sorted(uncited):
            status = "待補" if key in pending else "完整"
            out.append(f"- `{key}`（{status}）：{meta.get(key, '')}")
    else:
        out.append("（無）")
    out.append("")

    out.append("## ③ 被引用但仍待補的條目（優先補齊清單，交 Semantic Scholar 查證）\n")
    if pending_cited:
        for key in sorted(pending_cited, key=lambda k: -cites[k]["count"]):
            out.append(f"- {disp(key)} → 現況：{meta.get(key, '')}")
    else:
        out.append("（無）")
    out.append("")

    out.append("## ④ 年份不一致疑慮（同姓氏、年份相差 ≤1，疑為筆誤）\n")
    if year_doubts:
        for key, ref_key in sorted(year_doubts):
            out.append(
                f"- 正文 {disp(key)} ↔ 書目 `{ref_key}`：{meta.get(ref_key, '')}"
            )
    else:
        out.append("（無）")
    out.append("")
    return "\n".join(out)


def main() -> None:
    ap = argparse.ArgumentParser(
        description="比對正文引用與書目一致性（輸出 UTF-8 報告）"
    )
    ap.add_argument("manuscript", help="稿件路徑，例如 Manuscript.md")
    ap.add_argument("references", help="書目路徑，例如 references.md")
    ap.add_argument("-o", "--out", required=True, help="輸出報告路徑（UTF-8）")
    ap.add_argument("--year-tolerance", type=int, default=0,
                    help="年份疑慮的額外容差（預設 0，即比對相差 ≤1）")
    ap.add_argument("--no-authored", action="store_true",
                    help="不把『作者自身著作』bullet 納入完整書目集合")
    args = ap.parse_args()

    cites = parse_manuscript(args.manuscript)
    complete, pending, meta, by_surname = parse_references(
        args.references, include_authored=not args.no_authored
    )
    report = build_report(
        cites, complete, pending, meta, by_surname,
        args.year_tolerance, (args.manuscript, args.references)
    )
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(report)

    print(
        f"done -> {args.out} "
        f"(cites={len(cites)}, complete={len(complete)}, pending={len(pending)})",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
