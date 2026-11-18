#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 cpp-algorithms 下的文章合成一份 A4 打印版 HTML/PDF。

用法：
  python tools/build_cheatsheet.py
  python tools/build_cheatsheet.py --code-size 8.6
  python tools/build_cheatsheet.py --no-pdf

输出：
  print/cpp-cheatsheet.html
  print/cpp-cheatsheet.pdf
"""

import argparse
import html
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from datetime import datetime
from itertools import groupby
from pathlib import Path

try:
    import pymupdf as fitz
except ImportError:  # 旧版 PyMuPDF
    import fitz

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = ROOT / "source" / "_posts" / "cpp-algorithms"
DEFAULT_OUT = ROOT / "print"

GROUP_ORDER = {"图论": 1, "数论": 2, "杂项": 3, "对拍": 4, "DP": 5}

CSS = r"""
:root {
  --code-size: __CODE_SIZE__pt;
  --text-size: 9.6pt;
}
@page {
  size: A4;
  margin: 11mm 10mm 13mm 10mm;
  @top-right {
    content: "C++ 算法竞赛速查";
    font-size: 7.2pt;
    color: #777;
  }
  @bottom-center {
    content: counter(page);
    font-size: 8pt;
    color: #555;
  }
}
@page :first {
  @top-right { content: none; }
}
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; }
body {
  font-family: "Microsoft YaHei", "Segoe UI", sans-serif;
  font-size: var(--text-size);
  line-height: 1.55;
  color: #000;
  background: #fff;
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
  orphans: 2;
  widows: 2;
}
a { color: #000; text-decoration: none; }
.cover { padding-top: 1mm; }
.cover h1 {
  font-size: 22pt;
  margin: 0 0 2mm;
  letter-spacing: .5pt;
}
.cover .sub {
  font-size: 9pt;
  color: #555;
  margin-bottom: 3mm;
}
.cover .note {
  font-size: 8pt;
  color: #666;
  border-left: 2pt solid #999;
  padding-left: 3mm;
  margin-bottom: 5mm;
}
.toc-title {
  font-size: 13pt;
  margin: 0 0 2.5mm;
  padding-bottom: 1mm;
  border-bottom: .8pt solid #333;
}
.toc {
  column-count: 2;
  column-gap: 8mm;
  font-size: 9.1pt;
}
.toc-group {
  font-weight: bold;
  margin: 2.2mm 0 1mm;
  color: #222;
  break-inside: avoid;
  page-break-inside: avoid;
}
.toc-group:first-child { margin-top: 0; }
.toc-item {
  margin: .45mm 0;
  break-inside: avoid;
  page-break-inside: avoid;
}
.toc-item a {
  display: flex;
  justify-content: space-between;
  gap: 2mm;
}
.toc-title-text {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.pg {
  min-width: 2.5em;
  text-align: right;
  font-variant-numeric: tabular-nums;
  color: #444;
}
.page-break {
  break-after: page;
  page-break-after: always;
}
.post {
  margin: 0 0 5mm;
  break-inside: avoid;
  page-break-inside: avoid;
}
.post.long {
  break-inside: auto;
  page-break-inside: auto;
}
.post-head {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 3mm;
  border-bottom: .7pt solid #333;
  padding-bottom: 1mm;
  margin-bottom: 2mm;
  break-after: avoid;
  page-break-after: avoid;
}
.post-head h2 {
  font-size: 12.5pt;
  margin: 0;
}
.tag {
  font-size: 8pt;
  color: #555;
  white-space: nowrap;
}
.intro, .outro {
  margin: 0 0 2mm;
  text-align: justify;
}
.intro {
  break-after: avoid;
  page-break-after: avoid;
}
.outro { color: #222; }
.code-label {
  font-size: 7.4pt;
  color: #666;
  margin: 1.5mm 0 .6mm;
}
.code {
  margin: 0 0 2mm;
  padding: 2.2mm 2.6mm;
  border: .4pt solid #bbb;
  background: #f7f7f7;
  font-family: Consolas, "Cascadia Mono", "Microsoft YaHei", monospace;
  font-size: var(--code-size);
  line-height: 1.22;
  white-space: pre;
  overflow: hidden;
  break-inside: auto;
}
.code code { font-family: inherit; }
@media screen {
  body {
    width: 210mm;
    margin: 8mm auto;
    padding: 10mm;
    background: #fff;
    box-shadow: 0 0 8px rgba(0, 0, 0, .15);
  }
}
"""


@dataclass
class Post:
    slug: str
    title: str
    date: datetime
    group: str
    intro: str
    items: list
    anchor: str = ""
    index: int = 0

    @property
    def code_lines(self) -> int:
        return sum(len(item[2].splitlines()) for item in self.items if item[0] == "code")


def md_text(text: str) -> str:
    text = html.escape(text.strip())
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    return "\n".join(f"<p>{p.replace(chr(10), '<br>')}</p>" for p in paras)


def parse_post(path: Path) -> Post:
    text = path.read_text(encoding="utf-8")
    end = text.find("---\n", 4)
    if end == -1:
        raise RuntimeError(f"front matter not found: {path}")
    fm = text[4:end]
    body = text[end + 4:].strip()

    title = re.search(r'^title:\s*"(.*)"\s*$', fm, re.M).group(1)
    date_s = re.search(r"^date:\s*(.+)$", fm, re.M).group(1).strip()
    date = datetime.strptime(date_s, "%Y-%m-%d %H:%M:%S")
    tags_part = fm.split("tags:", 1)[1] if "tags:" in fm else ""
    tags = re.findall(r'^\s*-\s*"(.*)"\s*$', tags_part, re.M)
    group = tags[1] if len(tags) > 1 else "其他"

    intro, rest = body.split("<!-- more -->", 1)
    intro = intro.strip()

    parts = re.split(r"```(\w+)\n(.*?)\n```", rest, flags=re.S)
    items = []
    if parts[0].strip():
        items.append(("text", parts[0].strip()))
    for i in range(1, len(parts), 3):
        lang = parts[i]
        code = parts[i + 1].rstrip()
        items.append(("code", lang, code))
        if i + 2 < len(parts) and parts[i + 2].strip():
            items.append(("text", parts[i + 2].strip()))

    return Post(path.stem, title, date, group, intro, items)


def load_posts() -> list[Post]:
    posts = [parse_post(p) for p in sorted(POSTS_DIR.glob("*.md"))]
    posts.sort(key=lambda p: (GROUP_ORDER.get(p.group, 99), p.date, p.title))
    for i, post in enumerate(posts, 1):
        post.index = i
        post.anchor = f"post-{i:02d}"
    return posts


def code_label(post: Post, lang: str, code_index: int) -> str:
    if post.slug == "对拍" and code_index == 0:
        return "gen.cpp"
    if post.slug == "对拍" and lang == "bat":
        return "duipai.bat"
    if lang == "cpp":
        return "C++ 模板"
    return lang


def render_html(posts: list[Post], page_map: dict, code_size: float) -> str:
    grouped = [
        (group, list(items))
        for group, items in groupby(posts, key=lambda p: p.group)
    ]

    toc = []
    for group, items in grouped:
        toc.append(f'<div class="toc-group">{html.escape(group)}</div>')
        for post in items:
            page = page_map.get(post.anchor, "00")
            toc.append(
                '<div class="toc-item"><a href="#%s">'
                '<span class="toc-title-text">%d. %s</span>'
                '<span class="pg">%s</span></a></div>'
                % (post.anchor, post.index, html.escape(post.title), page)
            )

    sections = []
    for post in posts:
        cls = "post long" if post.code_lines > 65 else "post"
        block = [
            f'<section class="{cls}" id="{post.anchor}">',
            '<div class="post-head">',
            f"<h2>{post.index}. {html.escape(post.title)}</h2>",
            f'<span class="tag">{html.escape(post.group)}</span>',
            "</div>",
            md_text(post.intro),
        ]
        code_index = 0
        for item in post.items:
            if item[0] == "text":
                block.append(md_text(item[1]))
            else:
                lang, code = item[1], item[2]
                block.append(f'<div class="code-label">{html.escape(code_label(post, lang, code_index))}</div>')
                block.append(f'<pre class="code"><code>{html.escape(code)}</code></pre>')
                code_index += 1
        block.append("</section>")
        sections.append("\n".join(block))

    css = CSS.replace("__CODE_SIZE__", str(code_size))
    return (
        "<!doctype html>\n<html lang=\"zh-CN\">\n<head>\n<meta charset=\"utf-8\">\n"
        "<title>C++ 算法竞赛速查</title>\n<style>\n"
        + css
        + "\n</style>\n</head>\n<body>\n"
        "<header class=\"cover\">\n"
        "<h1>C++ 算法竞赛速查</h1>\n"
        "<div class=\"sub\">%d 个模板 · 打印版 · %s</div>\n"
        "<div class=\"note\">A4 打印。代码字号 %spt；需要更大字可修改本文件里的 --code-size。目录页码对应页脚页码。</div>\n"
        "</header>\n"
        "<h2 class=\"toc-title\">目录</h2>\n"
        "<div class=\"toc\">\n%s\n</div>\n"
        "<div class=\"page-break\"></div>\n"
        "%s\n"
        "</body>\n</html>\n"
        % (
            len(posts),
            datetime.now().strftime("%Y-%m-%d"),
            code_size,
            "\n".join(toc),
            "\n".join(sections),
        )
    )


def find_browser() -> Path:
    candidates = [
        Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
        Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
        Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
        Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
    ]
    for p in candidates:
        if p.exists():
            return p
    raise FileNotFoundError("没有找到 Edge 或 Chrome，无法生成 PDF")


def print_pdf(browser: Path, html_path: Path, pdf_path: Path) -> None:
    if pdf_path.exists():
        pdf_path.unlink()
    with tempfile.TemporaryDirectory() as td:
        cmd = [
            str(browser),
            "--headless",
            "--disable-gpu",
            "--no-pdf-header-footer",
            "--no-first-run",
            "--no-default-browser-check",
            f"--user-data-dir={td}",
            "--virtual-time-budget=1000",
            f"--print-to-pdf={pdf_path}",
            html_path.resolve().as_uri(),
        ]
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=120,
        )
    if not pdf_path.exists() or pdf_path.stat().st_size == 0:
        raise RuntimeError(f"PDF 生成失败：{proc.stderr[:800]}")


def read_links(pdf_path: Path) -> dict:
    doc = fitz.open(pdf_path)
    found = {}
    for page in doc:
        for link in page.get_links():
            dest = link.get("nameddest") or ""
            if dest.startswith("post-"):
                found[dest] = link["page"] + 1
    doc.close()
    return found


def set_outline(pdf_path: Path, posts: list[Post], page_map: dict) -> None:
    doc = fitz.open(pdf_path)
    toc = []
    for group, items in groupby(posts, key=lambda p: p.group):
        items = list(items)
        toc.append([1, group, page_map.get(items[0].anchor, 1)])
        for post in items:
            toc.append([2, f"{post.index}. {post.title}", page_map.get(post.anchor, 1)])
    doc.set_toc(toc)
    tmp = pdf_path.with_suffix(".outline.pdf")
    doc.save(tmp, garbage=3, deflate=True)
    doc.close()
    tmp.replace(pdf_path)


def render_previews(pdf_path: Path, posts: list[Post], page_map: dict, out: Path) -> None:
    doc = fitz.open(pdf_path)
    targets = [("toc", 0)]
    if posts:
        targets.append(("first", page_map.get(posts[0].anchor, 2) - 1))
    for post in posts:
        if post.slug == "线段树":
            targets.append(("long", page_map.get(post.anchor, 1) - 1))
            break
    for name, idx in targets:
        if 0 <= idx < doc.page_count:
            pix = doc[idx].get_pixmap(dpi=120)
            pix.save(out / f"preview-{name}.png")
    doc.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(DEFAULT_OUT), help="输出目录")
    parser.add_argument("--code-size", type=float, default=8.2, help="代码字号，默认 8.2")
    parser.add_argument("--no-pdf", action="store_true", help="只生成 HTML")
    args = parser.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    posts = load_posts()
    html_path = out / "cpp-cheatsheet.html"
    pdf_path = out / "cpp-cheatsheet.pdf"

    html_path.write_text(render_html(posts, {}, args.code_size), encoding="utf-8", newline="\n")
    print(f"[HTML] {html_path}")

    if args.no_pdf:
        return

    browser = find_browser()
    print(f"[PDF ] 使用 {browser.name}")

    pass1 = out / ".pass1.pdf"
    print_pdf(browser, html_path, pass1)
    page_map = read_links(pass1)
    missing = [p.slug for p in posts if p.anchor not in page_map]
    if missing:
        raise RuntimeError(f"目录链接缺失：{missing}")

    html_path.write_text(render_html(posts, page_map, args.code_size), encoding="utf-8", newline="\n")
    print_pdf(browser, html_path, pdf_path)
    pass1.unlink(missing_ok=True)

    final_map = read_links(pdf_path)
    set_outline(pdf_path, posts, final_map)
    render_previews(pdf_path, posts, final_map, out)

    doc = fitz.open(pdf_path)
    pages = doc.page_count
    doc.close()
    size_kb = pdf_path.stat().st_size // 1024
    print(f"[PDF ] {pdf_path}  ({pages} 页, {size_kb} KB)")
    print(f"[预览] {out / 'preview-toc.png'}")
    print(f"[预览] {out / 'preview-first.png'}")
    if (out / "preview-long.png").exists():
        print(f"[预览] {out / 'preview-long.png'}")


if __name__ == "__main__":
    main()
