# 編修歷程紀錄格式（revisions/）

每次採用一個版本就存成**一個獨立檔**，放在該篇 `revisions/`，命名 `YYYY-MM-DD-<段落標記>.md`。

- `<段落標記>`：簡短 kebab-case，例如 `intro-p2`、`method-p1`、`discussion-p5`；同段同日多次編修加序號（`...-2`、`...-3`）。
- 內文固定用以下模板：

```markdown
---
date: YYYY-MM-DD
section: <章節，如 Introduction>
locator: <段落定位，如 第2段 / 開頭句>
skill: passage-revision | section-review
chosen: <採用版本，如 V2；混搭則註明，如 V2+第二句用V3>
---
## 原文
<原始英文段落>

## 採用版本
<最終定稿英文段落>

## 備註
<使用者方向、混搭說明、⚠️ 觀察等；可留空>
```

> 本檔是格式範本，不是實際紀錄；`_TEMPLATE/` 複製成新論文後可保留供參照。
