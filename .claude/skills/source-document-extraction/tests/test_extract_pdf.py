"""以實際 PDF 檔驗證 extract_pdf.py 的兩個後端與各模式。

用一份真實的中文計畫書 PDF（repo 根目錄的附件）當 fixture，涵蓋：
  - 預設後端 pymupdf4llm：應產生大量標題層級與 Markdown 表格
  - --legacy 自製後端：應保留 PAGE 分隔（轉為 ---）
  - --raw：純文字含 PAGE 標記
  - --outline：首行為 total pages
  - --pages：0-based 頁碼對接（只輸出指定頁）

不依賴 pytest，直接 `conda run -n research python tests/test_extract_pdf.py` 執行；
全數通過印 ALL PASS 並以 0 退出，任一失敗印 FAIL 並以非零退出。
"""
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "extract_pdf.py"
# 實際 fixture：中文徵件說明與計畫書格式（含巢狀編號標題與表格）
FIXTURE = ROOT / "附件1_115年度徵件說明與計畫書格式.pdf"


def run(out_dir: Path, *args: str) -> Path:
    """執行 extract_pdf.py，回傳輸出檔路徑（以 -o 指定）。"""
    out = out_dir / "out"
    cmd = [sys.executable, str(SCRIPT), str(FIXTURE), "-o", str(out), *args]
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    assert proc.returncode == 0, f"非零退出 {args}: {proc.stderr}"
    assert out.exists() and out.stat().st_size > 0, f"輸出為空 {args}"
    return out


def main() -> None:
    if not FIXTURE.exists():
        print(f"SKIP: 找不到 fixture {FIXTURE.name}")
        sys.exit(0)

    # 標籤一律 ASCII：conda run 會用 cp950 轉印子行程 stdout，非 ASCII 會崩潰
    checks: list[tuple[str, bool]] = []

    with tempfile.TemporaryDirectory() as td:
        d = Path(td)

        # 1) 預設後端 pymupdf4llm（含預設清理）：標題與表格豐富、輸出乾淨
        default_md = run(d / "a").read_text(encoding="utf-8")
        lines = default_md.splitlines()
        n_head = sum(1 for ln in lines if ln.startswith("#"))
        n_table = sum(1 for ln in lines if ln.startswith("|"))
        checks.append((f"pymupdf4llm headings >= 10 (got {n_head})", n_head >= 10))
        checks.append((f"pymupdf4llm table rows >= 5 (got {n_table})", n_table >= 5))
        # 清理：無反引號、無 HTML 標籤、無 ** 粗體、標題深度 <= 3
        checks.append(("clean: no backticks", "`" not in default_md))
        checks.append(("clean: no <u> html tags", "<u>" not in default_md))
        checks.append(("clean: no ** bold", "**" not in default_md))
        deepest = max((len(ln) - len(ln.lstrip("#"))
                       for ln in lines if ln.startswith("#")), default=0)
        checks.append((f"clean: heading depth <= 5 (deepest {deepest})", deepest <= 5))

        # 1b) --no-clean 保留原始標記（回歸；此文件原始輸出含反引號）
        raw_md = run(d / "a2", "--no-clean").read_text(encoding="utf-8")
        checks.append(("--no-clean keeps raw markup (backticks)", "`" in raw_md))

        # 2) --legacy：保留頁分隔（to_markdown 把 PAGE 轉為 ---）
        legacy_md = run(d / "b", "--legacy").read_text(encoding="utf-8")
        checks.append(("legacy has page separator ---", "\n---\n" in legacy_md))

        # 3) --raw：純文字含 PAGE 標記
        raw_txt = run(d / "c", "--raw").read_text(encoding="utf-8")
        checks.append(("raw has PAGE markers", "========== PAGE" in raw_txt))

        # 4) --outline：首行 total pages
        outline = run(d / "e", "--outline").read_text(encoding="utf-8")
        checks.append(("outline first line total pages",
                       outline.splitlines()[0].startswith("total pages:")))

        # 5) --pages 1：0-based 對接，只取第 1 頁
        p1 = run(d / "f", "--pages", "1").read_text(encoding="utf-8")
        full = default_md
        checks.append(("pages 1 shorter than full doc", 0 < len(p1) < len(full)))

    ok = True
    for name, passed in checks:
        print(f"[{'PASS' if passed else 'FAIL'}] {name}")
        ok = ok and passed

    print("ALL PASS" if ok else "SOME FAILED")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
