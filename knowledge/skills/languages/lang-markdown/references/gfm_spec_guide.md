# Quick Reference Guide to GFM and CommonMark Specifications

This document contains summaries of essential syntax and rules according to the official GitHub Flavored Markdown (GFM) and CommonMark specification.

---

## 📌 Key Rendering Rules

1. **Blockquotes and Alerts**:
   - `> [!NOTE]` -> Informational box (Blue)
   - `> [!TIP]` -> Tip or advice (Green)
   - `> [!IMPORTANT]` -> Crucial information (Purple)
   - `> [!WARNING]` -> Attention warning (Yellow/Orange)
   - `> [!CAUTION]` -> Danger or high risk (Red)

2. **Escape Characters**:
   - Use the backslash `\` to escape special Markdown characters: `\*asteriscos\*`, `\[colchetes\]`, `\# tralha`.

3. **Autolinks**:
   - URLs preceded by the `http://` or `https://` protocol are automatically converted into links in GFM when they sit inside `<>`.

4. **Spacing and Paragraph Rules**:
   - Paragraphs require at least one fully blank line between them.
   - Consecutive spaces in the middle of sentences are ignored in the final HTML.
