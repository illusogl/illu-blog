#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把 XMind 8 的 .xmind 文件转换成 Markdown。

特点：
  - 保留多层树结构：前两层用标题，后面用嵌套列表
  - 自动提取附件图片（attachments/），并改写为 Markdown 图片链接
  - 自动识别 C / C# 代码片段，包进代码块
  - 支持批量转换整个文件夹
  - 可选 --hexo，生成带 front-matter 的文章并放进 Hexo 目录

用法：
  python xmind2md.py "C:\\path\\note.xmind" -o "D:\\out"
  python xmind2md.py "C:\\path\\notes" -o "D:\\out"
  python xmind2md.py "C:\\path\\notes" --hexo

依赖：Python 3.8+，只用标准库。
"""

import argparse
import html
import json
import os
import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from datetime import datetime

NS = {
    "c": "urn:xmind:xmap:xmlns:content:2.0",
    "xhtml": "http://www.w3.org/1999/xhtml",
    "xlink": "http://www.w3.org/1999/xlink",
}
XHTML_SRC = "{http://www.w3.org/1999/xhtml}src"
XLINK_HREF = "{http://www.w3.org/1999/xlink}href"

HEADING_MAX_DEPTH = 2   # depth 1 -> ##, depth 2 -> ###, 更深的用列表
CODE_RE = re.compile(
    r"(#include|printf|malloc|typedef|struct\s+\w+|void\s+\w+|int\s+\w+|"
    r"return\b|Console\.|Debug\.|public\s+|private\s+|using\s+UnityEngine|"
    r"MonoBehaviour|for\s*\(|while\s*\(|if\s*\()"
)


def slugify(name: str) -> str:
    name = name.strip()
    name = name.replace("C#", "CSharp").replace("c#", "csharp")
    name = name.replace("#", "-")
    name = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "-", name)
    name = re.sub(r"\s+", "-", name)
    name = re.sub(r"-{2,}", "-", name).strip(" .-")
    return name or "xmind"


def escape_md_line(text: str) -> str:
    text = text.replace("\\", "\\\\")
    text = html.escape(text, quote=False)
    for ch in ("`", "*", "_", "[", "]"):
        text = text.replace(ch, "\\" + ch)
    return text


def escape_md(text: str) -> str:
    # 标题里的换行转成 <br>，避免破坏 Markdown 列表结构
    parts = [escape_md_line(line.strip()) for line in text.split("\n") if line.strip()]
    return "<br>".join(parts)


def detect_lang(text: str, default: str = "c") -> str:
    s = text.lstrip()
    if s.startswith("<") and re.search(r"</?[A-Za-z!]", s):
        return "xml"
    if re.search(r"#include|printf|malloc|typedef\s+struct|->|\bNULL\b", text):
        return "c"
    if re.search(
        r"Console\.|Debug\.|public\s+|private\s+|using\s+UnityEngine|"
        r"MonoBehaviour|void\s+(Start|Update|Awake)",
        text,
    ):
        return "csharp"
    return default


def looks_like_code(text: str) -> bool:
    if len(text) < 20:
        return False
    if re.match(r"^\s*<[A-Za-z!/]", text) and text.count(">") >= 2:
        return True
    score = 0
    if "{" in text and "}" in text:
        score += 2
    if ";" in text:
        score += 2
    if "\n" in text:
        score += 1
    if "\t" in text:
        score += 1
    if CODE_RE.search(text):
        score += 2
    return score >= 3


def topic_title(topic) -> str:
    el = topic.find("c:title", NS)
    if el is None:
        return ""
    text = "".join(el.itertext())
    return text.replace("\r\n", "\n").replace("\r", "\n").strip()


def topic_children(topic):
    result = []
    children = topic.find("c:children", NS)
    if children is None:
        return result
    for group in children.findall("c:topics", NS):
        result.extend(group.findall("c:topic", NS))
    return result


def topic_images(topic):
    srcs = []
    for img in topic.findall("xhtml:img", NS):
        src = img.get(XHTML_SRC)
        if src:
            srcs.append(src)
    title_el = topic.find("c:title", NS)
    if title_el is not None:
        for img in title_el.findall(".//xhtml:img", NS):
            src = img.get(XHTML_SRC)
            if src:
                srcs.append(src)
    return list(dict.fromkeys(srcs))


def topic_href(topic) -> str:
    href = topic.get(XLINK_HREF)
    if href:
        return href
    title_el = topic.find("c:title", NS)
    if title_el is not None:
        return title_el.get(XLINK_HREF) or ""
    return ""


def link_text(title: str, href: str) -> str:
    if not href:
        return escape_md(title)
    text = title.replace(href, "").strip()
    if not text:
        text = href
    href = href.replace(" ", "%20").replace(")", "%29")
    return f"[{escape_md(text)}]({href})"


def infer_category(stem: str) -> str:
    s = stem.lower()
    if "unity" in s or "ugui" in s:
        return "Unity"
    if "c#" in s or "csharp" in s:
        return "C#"
    if "数据结构" in stem:
        return "数据结构"
    if "算法" in stem:
        return "算法"
    return "笔记"


class SheetConverter:
    def __init__(self, zf, asset_dir, link_prefix, code_detect=True, default_lang="c"):
        self.zf = zf
        self.asset_dir = asset_dir
        self.link_prefix = link_prefix.rstrip("/")
        self.code_detect = code_detect
        self.default_lang = default_lang
        self.image_map = {}
        self.warnings = []

    def export_image(self, src: str):
        if src in self.image_map:
            return self.image_map[src]
        zip_path = src.split(":", 1)[1] if src.startswith("xap:") else src
        try:
            data = self.zf.read(zip_path)
        except KeyError:
            self.warnings.append(f"图片不存在: {zip_path}")
            return None
        ext = os.path.splitext(zip_path)[1].lower() or ".png"
        name = f"{len(self.image_map) + 1:02d}{ext}"
        os.makedirs(self.asset_dir, exist_ok=True)
        with open(os.path.join(self.asset_dir, name), "wb") as f:
            f.write(data)
        link = f"{self.link_prefix}/{name}" if self.link_prefix else name
        self.image_map[src] = link
        return link

    def render_images(self, topic, lines, indent):
        for src in topic_images(topic):
            link = self.export_image(src)
            if link:
                lines.append(f"{indent}![]({link})")
                lines.append("")

    def render_code(self, text, lines, indent):
        text = text.strip("\n")
        fence = "````" if "```" in text else "```"
        lines.append(f"{indent}{fence}{detect_lang(text, self.default_lang)}")
        for line in text.split("\n"):
            lines.append(f"{indent}{line}" if line.strip() else "")
        lines.append(f"{indent}{fence}")
        lines.append("")

    def render_topic(self, topic, depth, lines):
        title = topic_title(topic)
        children = topic_children(topic)
        imgs = topic_images(topic)
        href = topic_href(topic)

        # 空节点：把子节点提升一层，避免 Markdown 里凭空多出缩进
        if depth > HEADING_MAX_DEPTH and not title and not imgs:
            for child in children:
                self.render_topic(child, depth, lines)
            return
        if depth <= HEADING_MAX_DEPTH and not title and not imgs:
            for child in children:
                self.render_topic(child, depth, lines)
            return

        if depth <= HEADING_MAX_DEPTH:
            if title:
                if lines and lines[-1].strip() != "":
                    lines.append("")
                lines.append(f"{'#' * (depth + 1)} {link_text(title, href)}")
                lines.append("")
            self.render_images(topic, lines, 0)
            for child in children:
                self.render_topic(child, depth + 1, lines)
            return

        indent = "  " * (depth - HEADING_MAX_DEPTH - 1)

        if (
            self.code_detect
            and title
            and not children
            and looks_like_code(title)
        ):
            self.render_code(title, lines, indent)
        else:
            if title:
                lines.append(f"{indent}- {link_text(title, href)}")
                self.render_images(topic, lines, indent + "  ")
            else:
                self.render_images(topic, lines, indent)

        for child in children:
            self.render_topic(child, depth + 1, lines)

    def render(self, root, include_h1=True, fallback_title="未命名"):
        lines = []
        if include_h1:
            lines.append(f"# {escape_md(topic_title(root) or fallback_title)}")
            lines.append("")
        self.render_images(root, lines, 0)
        children = topic_children(root)
        # 有些 XMind 的中心主题是空的，第一个子主题和文件名同名，避免重复标题
        if (
            not topic_title(root)
            and children
            and topic_title(children[0]) == fallback_title
        ):
            first = children[0]
            self.render_images(first, lines, 0)
            for grandchild in topic_children(first):
                self.render_topic(grandchild, 1, lines)
            children = children[1:]
        for child in children:
            self.render_topic(child, 1, lines)
        # 压缩多余空行
        text = "\n".join(lines)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip() + "\n"


def front_matter(title, date, category, tags):
    def q(s):
        return json.dumps(s, ensure_ascii=False)

    lines = [
        "---",
        f"title: {q(title)}",
        f"date: {date}",
        "categories:",
        f"  - {q(category)}",
        "tags:",
    ]
    for tag in tags:
        lines.append(f"  - {q(tag)}")
    lines.extend(["---", ""])
    return "\n".join(lines)


def convert_file(path, args):
    stem = os.path.splitext(os.path.basename(path))[0]
    slug = slugify(stem)

    try:
        zf = zipfile.ZipFile(path)
    except zipfile.BadZipFile:
        print(f"[跳过] 不是有效的 .xmind 文件: {path}", file=sys.stderr)
        return

    if "content.xml" not in zf.namelist():
        print(
            f"[跳过] {os.path.basename(path)} 不是 XMind 8 格式"
            "（没有 content.xml）。当前脚本只支持 XMind 8。",
            file=sys.stderr,
        )
        return

    root = ET.fromstring(zf.read("content.xml"))
    sheets = root.findall("c:sheet", NS)
    if not sheets:
        print(f"[跳过] 没有找到 sheet: {path}", file=sys.stderr)
        return

    mtime = datetime.fromtimestamp(os.path.getmtime(path)).strftime("%Y-%m-%d %H:%M:%S")
    converted = []

    for index, sheet in enumerate(sheets):
        topic = sheet.find("c:topic", NS)
        if topic is None:
            continue
        sheet_title = topic_title(topic) or stem
        if len(sheets) == 1:
            file_stem = slug
        else:
            suffix = slugify(topic_title(topic) or str(index + 1))
            file_stem = f"{slug}-{suffix}"

        asset_dir = os.path.join(args.assets_dir, file_stem)
        link_prefix = f"{args.link_prefix}/{file_stem}" if args.link_prefix else file_stem
        category = args.category or infer_category(stem)
        default_lang = "csharp" if category in ("C#", "Unity") else "c"
        conv = SheetConverter(
            zf,
            asset_dir,
            link_prefix,
            code_detect=not args.no_code,
            default_lang=default_lang,
        )

        body = conv.render(topic, include_h1=not args.hexo, fallback_title=sheet_title)
        content = body
        if args.hexo:
            tags = ["XMind", sheet_title]
            content = front_matter(sheet_title, mtime, category, tags) + body

        os.makedirs(args.out, exist_ok=True)
        out_path = os.path.join(args.out, f"{file_stem}.md")
        with open(out_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(content)

        converted.append(out_path)
        for warning in conv.warnings:
            print(f"[警告] {os.path.basename(path)}: {warning}", file=sys.stderr)

    zf.close()
    return converted


def main():
    parser = argparse.ArgumentParser(
        description="把 XMind 8 思维导图转换成 Markdown（支持图片和代码块）"
    )
    parser.add_argument("input", help=".xmind 文件或包含 .xmind 的文件夹")
    parser.add_argument("-o", "--out", help="Markdown 输出目录")
    parser.add_argument("--assets-dir", help="图片输出目录")
    parser.add_argument("--link-prefix", help="Markdown 里图片链接的前缀")
    parser.add_argument("--hexo", action="store_true", help="生成 Hexo front-matter")
    parser.add_argument("--category", help="Hexo 分类，默认按文件名推断")
    parser.add_argument("--no-code", action="store_true", help="不自动识别代码块")
    args = parser.parse_args()

    cwd = os.getcwd()
    if args.hexo:
        args.out = args.out or os.path.join(cwd, "source", "_posts")
        args.assets_dir = args.assets_dir or os.path.join(cwd, "source", "img", "xmind")
        args.link_prefix = args.link_prefix or "/img/xmind"
    else:
        args.out = args.out or os.path.join(cwd, "xmind-md")
        args.assets_dir = args.assets_dir or os.path.join(args.out, "assets")
        args.link_prefix = args.link_prefix or "assets"

    if os.path.isdir(args.input):
        files = sorted(
            os.path.join(args.input, name)
            for name in os.listdir(args.input)
            if name.lower().endswith(".xmind")
        )
    else:
        files = [args.input]

    if not files:
        print("没有找到 .xmind 文件", file=sys.stderr)
        sys.exit(1)

    total = 0
    for path in files:
        result = convert_file(path, args)
        if result:
            total += len(result)
            for out_path in result:
                print(f"[OK] {os.path.basename(path)} -> {out_path}")

    print(f"\n完成：{total} 个 Markdown 文件，图片在 {args.assets_dir}")


if __name__ == "__main__":
    main()
