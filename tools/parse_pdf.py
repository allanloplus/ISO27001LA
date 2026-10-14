#!/usr/bin/env python3
"""將題庫 PDF 解析為 questions.json 與圖片檔，供測驗網站使用。

用法: python3 tools/parse_pdf.py "ISO-IEC-27001-Lead-Auditor-CN V15.35.pdf" docs
需要: pip install pymupdf
"""
import json
import os
import re
import sys

import pymupdf

Q_RE = re.compile(r"^QUESTION NO:\s*(\d+)")
OPT_RE = re.compile(r"^([A-Z])\s?[.．、]\s*(.*)$")
ANS_RE = re.compile(r"^Answer:\s*(.*)$")
PARA_END_X = 470  # 行右緣小於此值且以句末標點結尾，視為段落結尾
PARA_END_CHARS = "。：？！；:?!.」）)"


def is_ascii_word(ch):
    return ch.isascii() and (ch.isalnum() or ch in ",.;:)!?%'\"")


def join(prev, line):
    if not prev:
        return line
    if prev.endswith("\n"):
        return prev + line
    if is_ascii_word(prev[-1]) and line and is_ascii_word(line[0]):
        return prev + " " + line
    return prev + line


def stream(doc, img_dir):
    """依閱讀順序產生 (kind, payload, x1) 項目。"""
    seen = {}
    for pno, page in enumerate(doc):
        items = []
        for b in page.get_text("dict")["blocks"]:
            if b["type"] != 0:
                continue
            for ln in b["lines"]:
                y0 = ln["bbox"][1]
                if y0 < 55 or y0 > 790:
                    continue  # 頁首、頁碼
                text = "".join(s["text"] for s in ln["spans"]).strip()
                if text:
                    items.append((y0, "text", text, ln["bbox"][2]))
        for info in page.get_image_info(xrefs=True):
            x0, y0, x1, y1 = info["bbox"]
            if y1 < 60 or (y1 - y0) < 60 or not info["xref"]:
                continue
            xref = info["xref"]
            if xref not in seen:
                img = doc.extract_image(xref)
                name = f"p{pno + 1:03d}_{xref}.{img['ext']}"
                with open(os.path.join(img_dir, name), "wb") as f:
                    f.write(img["image"])
                seen[xref] = name
            items.append((y0, "img", seen[xref], x1))
        items.sort(key=lambda t: t[0])
        for _, kind, payload, x1 in items:
            yield kind, payload, x1


def parse(pdf, out_dir):
    img_dir = os.path.join(out_dir, "img")
    os.makedirs(img_dir, exist_ok=True)
    doc = pymupdf.open(pdf)
    questions = []
    q = None
    section = None  # stem / opt / answer / expl

    def append_text(field, text, x1, target=None):
        obj = target if target is not None else q
        val = join(obj[field], text)
        if x1 < PARA_END_X and val and val[-1] in PARA_END_CHARS:
            val += "\n"
        obj[field] = val

    for kind, payload, x1 in stream(doc, img_dir):
        if kind == "text":
            m = Q_RE.match(payload)
            if m:
                q = {"id": int(m.group(1)), "stem": "", "options": [], "answer": [],
                     "explanation": "", "images": [], "answerImages": []}
                questions.append(q)
                section = "stem"
                continue
            if q is None:
                continue
            m = ANS_RE.match(payload)
            if m and section in ("stem", "opt"):
                q["answer"] = [a.strip() for a in m.group(1).split(",") if a.strip()]
                section = "answer"
                continue
            if payload.startswith("Explanation:") and section == "answer":
                section = "expl"
                rest = payload[len("Explanation:"):].strip()
                if rest:
                    append_text("explanation", rest, x1)
                continue
            if section in ("stem", "opt"):
                m = OPT_RE.match(payload)
                expected = chr(ord("A") + len(q["options"]))
                if m and m.group(1) == expected:
                    q["options"].append({"key": m.group(1), "text": m.group(2)})
                    section = "opt"
                    continue
                if section == "opt":
                    o = q["options"][-1]
                    o["text"] = join(o["text"], payload)
                else:
                    append_text("stem", payload, x1)
            elif section == "expl":
                append_text("explanation", payload, x1)
        else:
            if q is None:
                continue
            (q["images"] if section in ("stem", "opt") else q["answerImages"]).append(payload)

    for q in questions:
        q["stem"] = re.sub(r"\n{2,}", "\n", q["stem"]).strip()
        q["explanation"] = q["explanation"].strip()
        if q["answer"] and q["options"]:
            q["type"] = "multi" if len(q["answer"]) > 1 else "single"
        else:
            q["type"] = "match"  # 拖曳 / 配對題，以圖片呈現
    return questions


if __name__ == "__main__":
    pdf, out = sys.argv[1], sys.argv[2]
    qs = parse(pdf, out)
    with open(os.path.join(out, "questions.json"), "w", encoding="utf-8") as f:
        json.dump(qs, f, ensure_ascii=False, indent=1)
    # questions.js 讓網站以 file:// 直接開啟時也能載入題庫
    with open(os.path.join(out, "questions.js"), "w", encoding="utf-8") as f:
        f.write("window.QUESTIONS = ")
        json.dump(qs, f, ensure_ascii=False, separators=(",", ":"))
        f.write(";\n")
    from collections import Counter
    print(len(qs), Counter(q["type"] for q in qs))
