# papers/ — 論文工作區

每一篇要編修的論文各自一個資料夾放在這裡（`papers/<title>/`），所有編修工作檔都在該夾內。

## 開一篇新論文

複製範本骨架，改成簡短 kebab-case slug：

```bash
cp -r papers/_TEMPLATE papers/<your-paper-slug>
```

骨架已含空的 `Manuscript.md`、`Basic Information.md`、`progress.md`、`references.md`、`style-guide.md`，以及 `drafts/`、`target-journal-samples/`、`revisions/` 子夾。完整首次設定步驟見 [`../docs/NEW-PAPER.md`](../docs/NEW-PAPER.md)。

## 版控說明（重要）

**你實際編修的論文資料夾是私人內容，已被 [`.gitignore`](../.gitignore) 忽略、不進版控。** 這個 `papers/` 目錄裡**只有** `_TEMPLATE/`（骨架）與本 `README.md` 會進版控——所以你複製出來的 `papers/<your-paper-slug>/` 不會出現在 `git status`，這是預期行為，你的稿件只留在本機。
