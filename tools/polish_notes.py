#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
给 XMind 转换出来的博客文章做一次轻量排版：
  1. 给 h2 / h3 加编号（1.、1.1）
  2. 在文章开头加一句导语
  3. 每个 h2 开头加一句过渡
  4. 每个章节里第一张图片前加“如下图所示：”
  5. 每个章节里第一段代码前加“示例代码如下：”
  6. 把有子项的短列表标题加粗

只处理 front-matter 里带 XMind 标签的文章，不改原文措辞。

用法：
  python polish_notes.py --dry-run source/_posts/misc/数据结构.md
  python polish_notes.py
"""

import argparse
import html
import os
import re
import sys
from pathlib import Path

from xmind2md import detect_lang, looks_like_code

POSTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "source", "_posts")

H2_LEADS = [
    "这一节先整理{title}。",
    "接下来整理{title}。",
    "再整理{title}。",
    "接着整理{title}。",
    "最后整理{title}。",
]


def h2_lead(index, total, title):
    if index == 1:
        return f"这一节先整理{title}。"
    if index == total:
        return f"最后整理{title}。"
    middle = ["接下来整理{title}。", "再整理{title}。", "接着整理{title}。"]
    return middle[(index - 2) % len(middle)].format(title=title)

INTROS = [
    "> 这是「{title}」的学习笔记，按知识结构整理，方便以后回看。",
    "> 这篇「{title}」笔记记录了学习过程中的主要知识点。",
    "> 这里整理「{title}」相关的内容，按章节顺序展开。",
]

NUM_RE = re.compile(r"^\d+(?:\.\d+)*(?:[.、]\s*|\s+)")


def split_front_matter(text):
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            return text[: end + 5], text[end + 5 :].lstrip("\n")
    return "", text


def get_title(front_matter):
    m = re.search(r'^title:\s*"(.*)"\s*$', front_matter, re.M)
    if m:
        return m.group(1).replace('\\"', '"')
    m = re.search(r"^title:\s*(.+)$", front_matter, re.M)
    if m:
        return m.group(1).strip().strip('"')
    return ""


def is_xmind_post(front_matter):
    return "XMind" in front_matter and "tags:" in front_matter


def strip_existing_number(title):
    return NUM_RE.sub("", title.strip()).strip()


def unescape_md(text):
    text = html.unescape(text)
    return re.sub(r"\\([\\`*_\[\]])", r"\1", text)


def will_demote(lines, index):
    if index >= len(lines):
        return False
    m = re.match(r"^### (.+)$", lines[index])
    if not m:
        return False
    j = index + 1
    while j < len(lines) and lines[j].strip() == "":
        j += 1
    return j >= len(lines) or lines[j].startswith("#")


def demote_empty_h3(body):
    """没有内容的三级标题改成列表项，避免博客里出现空标题。"""
    lines = body.splitlines()
    out = []
    in_fence = False
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.strip().startswith("```"):
            in_fence = not in_fence
            out.append(line)
            i += 1
            continue
        if in_fence:
            out.append(line)
            i += 1
            continue
        m = re.match(r"^### (.+)$", line)
        if m:
            j = i + 1
            while j < len(lines) and lines[j].strip() == "":
                j += 1
            if j >= len(lines) or lines[j].startswith("#"):
                title = strip_existing_number(m.group(1).strip())
                if title:
                    text = unescape_md(title.replace("<br>", "\n"))
                    is_code = looks_like_code(text) and ("\n" in text or ("{" in text and "}" in text))
                    if is_code:
                        lang = detect_lang(text, "xml" if text.lstrip().startswith("<") else "c")
                        out.append(f"```{lang}")
                        out.extend(text.split("\n"))
                        out.append("```")
                        out.append("")
                    else:
                        if len(title) <= 80:
                            out.append(f"- **{title}**")
                        else:
                            out.append(f"- {title}")
                        if not will_demote(lines, j):
                            out.append("")
                    i = j
                    continue
        out.append(line)
        i += 1
    return "\n".join(out)


def number_headings(body):
    lines = body.splitlines()
    out = []
    h2 = 0
    h3 = 0
    in_fence = False
    total_h2 = 0
    for l in lines:
        if l.strip().startswith("```"):
            in_fence = not in_fence
        elif not in_fence and re.match(r"^## ", l):
            total_h2 += 1
    in_fence = False
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.strip().startswith("```"):
            in_fence = not in_fence
            out.append(line)
            i += 1
            continue
        if in_fence:
            out.append(line)
            i += 1
            continue

        m2 = re.match(r"^## (.+)$", line)
        m3 = re.match(r"^### (.+)$", line)

        if m2:
            h2 += 1
            h3 = 0
            title = strip_existing_number(m2.group(1))
            out.append(f"## {h2}. {title}")
            i += 1
            while i < len(lines) and lines[i].strip() == "":
                i += 1
            if i < len(lines) and lines[i].startswith(
                ("这一节", "接下来", "再整理", "接着整理", "最后整理")
            ):
                out.append("")
                continue
            if i < len(lines) and not lines[i].startswith("## "):
                out.append("")
                lead = h2_lead(h2, total_h2, title)
                out.append(lead)
                out.append("")
            else:
                out.append("")
            continue

        if m3:
            h3 += 1
            title = strip_existing_number(m3.group(1))
            out.append(f"### {h2}.{h3} {title}")
            i += 1
            while i < len(lines) and lines[i].strip() == "":
                i += 1
            out.append("")
            # 如果这个三级标题下面有 3 个以上并列条目，加一句引导
            j = i
            count = 0
            while j < len(lines):
                lj = lines[j]
                if lj.startswith("#") or lj.strip().startswith("```"):
                    break
                if lj.startswith("- "):
                    count += 1
                j += 1
            if count >= 3 and not (i < len(lines) and lines[i].strip() == "主要包括："):
                out.append("主要包括：")
                out.append("")
            continue

        out.append(line)
        i += 1

    return "\n".join(out)


def add_intro(body, title):
    stripped = body.lstrip("\n")
    if stripped.startswith(">"):
        return body
    template = INTROS[sum(ord(c) for c in title) % len(INTROS)]
    return template.format(title=title) + "\n\n" + stripped


def bold_parent_items(lines):
    out = []
    in_fence = False
    for i, line in enumerate(lines):
        if line.strip().startswith("```"):
            in_fence = not in_fence
            out.append(line)
            continue
        if in_fence:
            out.append(line)
            continue

        m = re.match(r"^(\s*)- (.*)$", line)
        if m:
            indent, text = m.groups()
            j = i + 1
            while j < len(lines) and lines[j].strip() == "":
                j += 1
            if j < len(lines):
                child = re.match(r"^(\s*)- ", lines[j])
                if (
                    child
                    and len(child.group(1)) > len(indent)
                    and 0 < len(text) <= 40
                    and not text.startswith("**")
                    and not text.startswith("![")
                ):
                    if text.endswith("：") or text.endswith(":"):
                        text = f"**{text[:-1]}**{text[-1]}"
                    else:
                        text = f"**{text}**"
                    line = f"{indent}- {text}"
        out.append(line)
    return out


def add_leads(lines):
    out = []
    in_fence = False
    image_lead_done = False
    code_lead_done = False
    prev_nonblank = ""

    for line in lines:
        if line.strip().startswith("```"):
            if not in_fence:
                # 代码块开始
                if not code_lead_done:
                    indent = line[: len(line) - len(line.lstrip())]
                    prev = prev_nonblank.rstrip()
                    if not prev.endswith(("：", ":")) and "如下" not in prev and "示例" not in prev:
                        if out and out[-1].strip() != "":
                            out.append("")
                        out.append(f"{indent}示例代码如下：")
                        out.append("")
                    code_lead_done = True
                in_fence = True
            else:
                in_fence = False
            out.append(line)
            if line.strip():
                prev_nonblank = line
            continue

        if in_fence:
            out.append(line)
            if line.strip():
                prev_nonblank = line
            continue

        if re.match(r"^#{1,6} ", line):
            image_lead_done = False
            code_lead_done = False

        m = re.match(r"^(\s*)!\[.*?\]\(.*?\)\s*$", line)
        if m and not image_lead_done:
            indent = m.group(1)
            prev = prev_nonblank.rstrip()
            if not prev.endswith(("：", ":")) and "如下" not in prev:
                if out and out[-1].strip() != "":
                    out.append("")
                out.append(f"{indent}如下图所示：")
                out.append("")
            image_lead_done = True

        out.append(line)
        if line.strip():
            prev_nonblank = line

    return out


def polish(text):
    front_matter, body = split_front_matter(text)
    title = get_title(front_matter)
    body = demote_empty_h3(body)
    body = number_headings(body)
    body = add_intro(body, title)
    lines = bold_parent_items(body.splitlines())
    lines = add_leads(lines)
    body = "\n".join(lines)
    body = re.sub(r"\n{3,}", "\n\n", body).strip() + "\n"
    return front_matter + "\n" + body


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="*", help="要处理的文件，默认处理 source/_posts 下所有 XMind 文章")
    parser.add_argument("--dry-run", action="store_true", help="只打印结果，不写入")
    args = parser.parse_args()

    if args.files:
        files = args.files
    else:
        files = [str(path) for path in sorted(Path(POSTS_DIR).rglob("*.md"))]

    count = 0
    for path in files:
        with open(path, encoding="utf-8") as f:
            text = f.read()
        front_matter, _ = split_front_matter(text)
        if not is_xmind_post(front_matter):
            continue
        result = polish(text)
        if args.dry_run:
            print(result[:4000])
        else:
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write(result)
            print(f"[OK] {path}")
        count += 1

    if not args.dry_run:
        print(f"\n完成：{count} 篇")


if __name__ == "__main__":
    main()
