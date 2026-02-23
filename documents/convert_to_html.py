#!/usr/bin/env python3
import os
import re
import markdown
from pathlib import Path

def convert_md_to_html():
    """Convert all .md files to HTML with MyCa dark theme styling"""

    # ── Template Dark Theme — matches index.html design system ──────────────────
    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>__TITLE__</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
    <style>
        /* ── Design tokens (mirrors index.html) ─────────────────── */
        :root {
            --bg:           #0a0a0f;
            --surface:      #111118;
            --surface2:     #18181f;
            --surface3:     #1e1e28;
            --border:       rgba(255,255,255,0.07);
            --border-soft:  rgba(255,255,255,0.04);
            --accent:       #63b3ed;
            --accent2:      #f6ad55;
            --accent3:      #68d391;
            --accent4:      #9a75ea;
            --text-primary: #f0f0f5;
            --text-secondary:#8888a0;
            --text-dim:     #444455;
            --code-bg:      #13131c;
            --radius:       10px;
        }

        *, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }

        html {
            scroll-behavior: smooth;
            scrollbar-width: thin;
            scrollbar-color: #1e1e28 transparent;
        }
        html::-webkit-scrollbar { width: 6px; }
        html::-webkit-scrollbar-thumb { background: var(--surface2); border-radius: 6px; }

        body {
            font-family: "Inter", "SF Pro Display", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            line-height: 1.75;
            color: var(--text-primary);
            background: var(--bg);
            min-height: 100vh;
            padding: 0;
        }

        /* ── Layout ──────────────────────────────────────────────── */
        .page-wrap {
            display: flex;
            flex-direction: column;
            min-height: 100vh;
        }

        /* ── Top bar ─────────────────────────────────────────────── */
        .doc-topbar {
            position: sticky;
            top: 0;
            z-index: 50;
            height: 52px;
            background: rgba(10,10,15,0.85);
            backdrop-filter: blur(14px);
            border-bottom: 1px solid var(--border);
            display: flex;
            align-items: center;
            padding: 0 32px;
            gap: 16px;
        }
        .doc-topbar-brand {
            display: flex;
            align-items: center;
            gap: 10px;
            text-decoration: none;
        }
        .doc-topbar-icon {
            width: 28px; height: 28px;
            background: linear-gradient(135deg, #63b3ed, #4299e1);
            border-radius: 7px;
            display: flex; align-items: center; justify-content: center;
            font-family: 'Syne', sans-serif;
            font-weight: 800;
            font-size: 12px;
            color: #000;
            letter-spacing: -0.5px;
            box-shadow: 0 2px 10px rgba(99,179,237,0.25);
            flex-shrink: 0;
        }
        .doc-topbar-name {
            font-family: "Inter", "SF Pro Display", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            font-size: 15px;
            font-weight: 700;
            color: var(--text-primary);
            letter-spacing: -0.3px;
        }
        .doc-topbar-sep {
            color: var(--text-dim);
            font-size: 18px;
            font-weight: 300;
        }
        .doc-topbar-title {
            font-family: "Inter", "SF Mono", Monaco, "Cascadia Code", "Roboto Mono", Consolas, monospace;
            font-size: 12px;
            color: var(--accent);
            letter-spacing: 0.3px;
            font-weight: 400;
        }
        .doc-topbar-spacer { flex: 1; }
        .doc-topbar-tag {
            font-family: "Inter", "SF Mono", Monaco, "Cascadia Code", "Roboto Mono", Consolas, monospace;
            font-size: 10px;
            color: var(--text-dim);
            letter-spacing: 1.5px;
            text-transform: uppercase;
            padding: 4px 10px;
            border: 1px solid var(--border);
            border-radius: 6px;
        }

        /* ── Main content ────────────────────────────────────────── */
        .doc-body {
            display: flex;
            flex: 1;
        }

        /* TOC sidebar */
        .doc-toc {
            width: 220px;
            min-width: 220px;
            position: sticky;
            top: 25px;
            align-self: flex-start;
            height: calc(100vh - 52px);
            overflow-y: auto;
            padding: 28px 16px 28px 24px;
            border-right: 1px solid var(--border);
            scrollbar-width: thin;
            scrollbar-color: var(--surface2) transparent;
        }
        .doc-toc::-webkit-scrollbar { width: 4px; }
        .doc-toc::-webkit-scrollbar-thumb { background: var(--surface2); border-radius: 4px; }
        .doc-toc-label {
            font-family: "Inter", "SF Mono", Monaco, "Cascadia Code", "Roboto Mono", Consolas, monospace;
            font-size: 9px;
            font-weight: 500;
            color: var(--text-dim);
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 12px;
        }
        .doc-toc ul {
            list-style: none;
            display: flex;
            flex-direction: column;
            gap: 2px;
        }
        .doc-toc ul li a {
            display: block;
            font-size: 12px;
            color: var(--text-secondary);
            text-decoration: none;
            padding: 5px 8px;
            border-radius: 6px;
            border-left: 2px solid transparent;
            transition: all 0.15s;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .doc-toc ul li a:hover {
            color: var(--accent);
            background: rgba(99,179,237,0.06);
            border-left-color: rgba(99,179,237,0.3);
        }
        .doc-toc ul ul { margin-left: 12px; }
        .doc-toc ul ul li a { font-size: 11px; }

        /* Article */
        .doc-article {
            flex: 1;
            min-width: 0;
            padding: 48px 56px 80px;
            max-width: 860px;
        }

        /* ── Typography ──────────────────────────────────────────── */
        h1, h2, h3, h4, h5, h6 {
            font-family: "Inter", "SF Pro Display", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            font-weight: 700;
            color: var(--text-primary);
            letter-spacing: -0.5px;
            scroll-margin-top: 72px;
        }

        h1 {
            font-size: 32px;
            font-weight: 800;
            letter-spacing: -1.5px;
            margin-bottom: 16px;
            line-height: 1.1;
            background: linear-gradient(135deg, #f0f0f5 30%, var(--accent) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            padding-bottom: 20px;
            border-bottom: 1px solid var(--border);
            margin-bottom: 32px;
        }

        h2 {
            font-size: 22px;
            margin-top: 48px;
            margin-bottom: 16px;
            padding-bottom: 10px;
            border-bottom: 1px solid var(--border);
            color: var(--text-primary);
            display: flex;
            align-items: center;
            gap: 10px;
        }
        h2::before {
            content: '';
            display: inline-block;
            width: 4px;
            height: 20px;
            background: linear-gradient(180deg, var(--accent), var(--accent4));
            border-radius: 2px;
            flex-shrink: 0;
        }

        h3 {
            font-size: 17px;
            margin-top: 32px;
            margin-bottom: 12px;
            color: var(--text-primary);
        }

        h4 {
            font-size: 14px;
            margin-top: 24px;
            margin-bottom: 10px;
            color: var(--accent);
            font-family: "Inter", "SF Mono", Monaco, "Cascadia Code", "Roboto Mono", Consolas, monospace;
            letter-spacing: 0.5px;
            text-transform: uppercase;
        }

        p {
            color: var(--text-secondary);
            font-size: 15px;
            margin-bottom: 16px;
            line-height: 1.8;
        }

        strong { color: var(--text-primary); font-weight: 600; }
        em { color: var(--accent2); font-style: italic; }

        /* ── Links ───────────────────────────────────────────────── */
        a {
            color: var(--accent);
            text-decoration: none;
            border-bottom: 1px solid rgba(99,179,237,0.25);
            transition: border-color 0.15s, color 0.15s;
        }
        a:hover {
            color: #90cdf4;
            border-bottom-color: rgba(99,179,237,0.6);
        }

        /* ── Inline code ─────────────────────────────────────────── */
        code {
            font-family: "Inter", "SF Mono", Monaco, "Cascadia Code", "Roboto Mono", Consolas, monospace;
            font-size: 13px;
            font-weight: 400;
            background: var(--surface3);
            color: var(--accent);
            padding: 2px 7px;
            border-radius: 5px;
            border: 1px solid var(--border);
        }

        /* ── Code blocks ─────────────────────────────────────────── */
        pre {
            background: var(--code-bg);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            padding: 0;
            margin: 24px 0;
            overflow: hidden;
            box-shadow: 0 4px 24px rgba(0,0,0,0.4);
            position: relative;
        }

        /* Code block header bar */
        pre::before {
            content: '';
            display: block;
            height: 36px;
            background: var(--surface2);
            border-bottom: 1px solid var(--border);
            background-image: 
                radial-gradient(circle at 14px 18px, #ff5f57 5px, transparent 5px),
                radial-gradient(circle at 30px 18px, #febc2e 5px, transparent 5px),
                radial-gradient(circle at 46px 18px, #28c840 5px, transparent 5px);
        }

        pre code {
            display: block;
            background: none;
            border: none;
            padding: 20px 24px;
            color: #c9d1d9;
            font-size: 13.5px;
            line-height: 1.65;
            overflow-x: auto;
            white-space: pre;
            scrollbar-width: thin;
            scrollbar-color: var(--surface2) transparent;
        }
        pre code::-webkit-scrollbar { height: 4px; }
        pre code::-webkit-scrollbar-thumb { background: var(--surface2); border-radius: 4px; }

        /* Codehilite wrapper */
        .codehilite {
            background: var(--code-bg);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            margin: 24px 0;
            overflow: hidden;
            box-shadow: 0 4px 24px rgba(0,0,0,0.4);
        }
        .codehilite::before {
            content: '';
            display: block;
            height: 36px;
            background: var(--surface2);
            border-bottom: 1px solid var(--border);
            background-image: 
                radial-gradient(circle at 14px 18px, #ff5f57 5px, transparent 5px),
                radial-gradient(circle at 30px 18px, #febc2e 5px, transparent 5px),
                radial-gradient(circle at 46px 18px, #28c840 5px, transparent 5px);
        }
        .codehilite pre {
            background: none;
            border: none;
            border-radius: 0;
            margin: 0;
            padding: 20px 24px;
            box-shadow: none;
        }
        .codehilite pre::before { display: none; }
        .codehilite pre code { padding: 0; }

        /* ── Syntax highlighting (dark palette) ──────────────────── */
        .codehilite .hll { background-color: #2a2a40 }
        .codehilite .c,
        .codehilite .cm,
        .codehilite .c1,
        .codehilite .cs  { color: #6a737d; font-style: italic }
        .codehilite .cp  { color: #7ecfc0 }
        .codehilite .k,
        .codehilite .kc,
        .codehilite .kd,
        .codehilite .kn,
        .codehilite .kr  { color: #ff79c6; font-weight: 600 }
        .codehilite .kp  { color: #ff79c6 }
        .codehilite .kt  { color: #8be9fd }
        .codehilite .o,
        .codehilite .ow  { color: #ff79c6 }
        .codehilite .m,
        .codehilite .mf,
        .codehilite .mh,
        .codehilite .mi,
        .codehilite .mo,
        .codehilite .il  { color: #bd93f9 }
        .codehilite .s,
        .codehilite .sb,
        .codehilite .sc,
        .codehilite .s2,
        .codehilite .s1,
        .codehilite .sh,
        .codehilite .ss  { color: #f1fa8c }
        .codehilite .sd  { color: #f1fa8c; font-style: italic }
        .codehilite .se  { color: #ffb86c; font-weight: 600 }
        .codehilite .si  { color: #ffb86c }
        .codehilite .sx  { color: #50fa7b }
        .codehilite .sr  { color: #50fa7b }
        .codehilite .na  { color: #50fa7b }
        .codehilite .nb  { color: #8be9fd }
        .codehilite .bp  { color: #8be9fd }
        .codehilite .nc  { color: #8be9fd; font-weight: 600 }
        .codehilite .no  { color: #bd93f9 }
        .codehilite .nd  { color: #50fa7b }
        .codehilite .ni  { color: #ffb86c; font-weight: 600 }
        .codehilite .ne,
        .codehilite .nf  { color: #50fa7b }
        .codehilite .nl  { color: #8be9fd; font-weight: 600 }
        .codehilite .nn  { color: #8be9fd; font-weight: 600 }
        .codehilite .nt  { color: #ff79c6; font-weight: 600 }
        .codehilite .nv,
        .codehilite .vc,
        .codehilite .vg,
        .codehilite .vi  { color: #8be9fd }
        .codehilite .nx  { color: #c9d1d9 }
        .codehilite .w   { color: #c9d1d9 }
        .codehilite .err { color: #ff5555 }
        .codehilite .p   { color: #c9d1d9 }
        .codehilite .ge  { font-style: italic }
        .codehilite .gs  { font-weight: bold }
        .codehilite .gd  { color: #ff5555 }
        .codehilite .gi  { color: #50fa7b }
        .codehilite .go  { color: #6a737d }
        .codehilite .gh  { color: #8be9fd; font-weight: bold }
        .codehilite .gu  { color: #bd93f9; font-weight: bold }
        .codehilite .gt  { color: #8be9fd }
        .codehilite .gr  { color: #ff5555 }
        .codehilite .gp  { color: #ffb86c; font-weight: bold }

        /* ── Blockquote ───────────────────────────────────────────── */
        blockquote {
            border-left: 3px solid var(--accent2);
            margin: 24px 0;
            padding: 14px 20px;
            background: rgba(246,173,85,0.05);
            border-radius: 0 var(--radius) var(--radius) 0;
            color: var(--text-secondary);
            font-style: italic;
        }
        blockquote strong { color: var(--accent2); }
        blockquote p { margin: 0; color: inherit; }

        /* ── Tables ──────────────────────────────────────────────── */
        .table-wrap {
            overflow-x: auto;
            margin: 24px 0;
            border-radius: var(--radius);
            border: 1px solid var(--border);
        }
        table {
            border-collapse: collapse;
            width: 100%;
            font-size: 14px;
        }
        thead tr {
            background: var(--surface2);
            border-bottom: 1px solid var(--border);
        }
        th {
            font-family: "Inter", "SF Mono", Monaco, "Cascadia Code", "Roboto Mono", Consolas, monospace;
            font-size: 11px;
            font-weight: 500;
            color: var(--accent);
            text-transform: uppercase;
            letter-spacing: 1px;
            padding: 12px 16px;
            text-align: left;
            white-space: nowrap;
        }
        td {
            padding: 11px 16px;
            border-bottom: 1px solid var(--border-soft);
            color: var(--text-secondary);
            vertical-align: top;
        }
        tr:last-child td { border-bottom: none; }
        tbody tr:hover { background: rgba(255,255,255,0.02); }

        /* ── Lists ───────────────────────────────────────────────── */
        ul, ol {
            padding-left: 24px;
            margin-bottom: 16px;
            color: var(--text-secondary);
            font-size: 15px;
        }
        ul li, ol li {
            margin-bottom: 6px;
            padding-left: 4px;
            line-height: 1.75;
        }
        ul li::marker { color: var(--accent); }
        ol li::marker { color: var(--accent); font-family: "Inter", "SF Mono", Monaco, "Cascadia Code", "Roboto Mono", Consolas, monospace; font-size: 13px; }
        li > ul, li > ol { margin-top: 6px; margin-bottom: 0; }

        /* ── Horizontal rule ─────────────────────────────────────── */
        hr {
            border: none;
            height: 1px;
            background: linear-gradient(90deg, transparent, var(--border), transparent);
            margin: 40px 0;
        }

        /* ── Mermaid diagrams ────────────────────────────────────── */
        .mermaid {
            margin: 28px 0;
            padding: 28px;
            background: var(--surface2);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            text-align: center;
            overflow-x: auto;
            min-height: 60px;
            position: relative;
        }
        /* Loading shimmer before mermaid renders */
        .mermaid:not([data-processed="true"])::after {
            content: 'Rendering diagram...';
            position: absolute;
            top: 50%; left: 50%;
            transform: translate(-50%, -50%);
            font-family: "Inter", "SF Mono", Monaco, "Cascadia Code", "Roboto Mono", Consolas, monospace;
            font-size: 11px;
            color: var(--text-dim);
            letter-spacing: 1px;
        }
        .mermaid svg {
            max-width: 100%;
            height: auto;
        }

        /* ── Callout / admonition boxes ──────────────────────────── */
        .callout {
            display: flex;
            gap: 14px;
            padding: 16px 18px;
            border-radius: var(--radius);
            margin: 20px 0;
            border: 1px solid;
            font-size: 14px;
        }
        .callout-info    { background: rgba(99,179,237,0.07);  border-color: rgba(99,179,237,0.2); }
        .callout-warning { background: rgba(246,173,85,0.07);  border-color: rgba(246,173,85,0.2); }
        .callout-success { background: rgba(104,211,145,0.07); border-color: rgba(104,211,145,0.2); }

        /* ── Image ───────────────────────────────────────────────── */
        img {
            max-width: 100%;
            border-radius: var(--radius);
            border: 1px solid var(--border);
            margin: 12px 0;
        }

        /* ── Footer ──────────────────────────────────────────────── */
        .doc-footer {
            border-top: 1px solid var(--border);
            padding: 20px 56px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            font-family: "Inter", "SF Mono", Monaco, "Cascadia Code", "Roboto Mono", Consolas, monospace;
            font-size: 11px;
            color: var(--text-dim);
        }
        .doc-footer a {
            color: var(--accent);
            border-bottom: none;
        }

        /* ── Responsive ──────────────────────────────────────────── */
        @media (max-width: 1000px) {
            .doc-toc { display: none; }
            .doc-article { padding: 32px 28px 60px; }
        }
        @media (max-width: 640px) {
            .doc-article { padding: 24px 18px 48px; }
            h1 { font-size: 24px; }
            h2 { font-size: 18px; }
            .doc-topbar { padding: 0 18px; }
            .doc-footer { padding: 16px 18px; flex-direction: column; gap: 4px; text-align: center; }
        }
    </style>
</head>
<body>
    <div class="page-wrap">

        <div class="doc-body">
            <!-- Auto-generated TOC -->
            <nav class="doc-toc" id="docToc">
                <div class="doc-toc-label">On this page</div>
                <div id="tocList"></div>
            </nav>

            <!-- Main article -->
            <article class="doc-article" id="docArticle">
                __CONTENT__
            </article>
        </div>

        <footer class="doc-footer">
            <span>Template · Knowledge Transfer Portal</span>
            <a href="index.html">← Back to index</a>
        </footer>
    </div>

    <script>
        // ── Wrap all tables for horizontal scroll ────────────────
        document.querySelectorAll('article table').forEach(t => {
            const wrap = document.createElement('div');
            wrap.className = 'table-wrap';
            t.parentNode.insertBefore(wrap, t);
            wrap.appendChild(t);
        });

        // ── Auto-build TOC from headings ──────────────────────────
        (function() {
            const headings = document.querySelectorAll('#docArticle h2, #docArticle h3');
            if (headings.length < 2) {
                document.getElementById('docToc').style.display = 'none';
                return;
            }
            const ul = document.createElement('ul');
            headings.forEach((h, i) => {
                if (!h.id) h.id = 'heading-' + i;
                const li  = document.createElement('li');
                const a   = document.createElement('a');
                a.href        = '#' + h.id;
                a.textContent = h.textContent;
                if (h.tagName === 'H3') {
                    const sub = document.createElement('ul');
                    const subLi = document.createElement('li');
                    subLi.appendChild(a);
                    sub.appendChild(subLi);
                    ul.appendChild(sub);
                } else {
                    li.appendChild(a);
                    ul.appendChild(li);
                }
            });
            document.getElementById('tocList').appendChild(ul);

            // Highlight active heading on scroll
            const links = ul.querySelectorAll('a');
            const obs = new IntersectionObserver(entries => {
                entries.forEach(e => {
                    if (e.isIntersecting) {
                        links.forEach(l => l.style.color = '');
                        const active = ul.querySelector('a[href="#' + e.target.id + '"]');
                        if (active) active.style.color = 'var(--accent)';
                    }
                });
            }, { rootMargin: '-20% 0px -75% 0px' });
            headings.forEach(h => obs.observe(h));
        })();

        // ── Smooth back-to-top on logo click ─────────────────────
        document.querySelector('.doc-topbar-brand').addEventListener('click', function(e) {
            if (window.location.pathname.endsWith('index.html') ||
                window.location.pathname.endsWith('/')) {
                e.preventDefault();
                window.scrollTo({ top: 0, behavior: 'smooth' });
            }
        });
    </script>

    <!-- Mermaid: loaded last so DOM is fully ready -->
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <script>
        mermaid.initialize({
            startOnLoad: false,
            theme: 'dark',
            securityLevel: 'loose',
            themeVariables: {
                primaryColor: '#1e1e28',
                primaryTextColor: '#f0f0f5',
                primaryBorderColor: '#63b3ed',
                lineColor: '#444455',
                secondaryColor: '#18181f',
                tertiaryColor: '#111118',
                edgeLabelBackground: '#18181f',
                fontFamily: 'Inter, "SF Pro Display", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'
            }
        });
        // Explicitly render all .mermaid divs after DOM is ready
        document.addEventListener('DOMContentLoaded', function() {
            mermaid.run({ nodes: document.querySelectorAll('.mermaid') });
        });
        // Fallback: if DOMContentLoaded already fired (script at bottom)
        if (document.readyState === 'complete' || document.readyState === 'interactive') {
            mermaid.run({ nodes: document.querySelectorAll('.mermaid') });
        }
    </script>
</body>
</html>"""

    # ── Directory setup ──────────────────────────────────────────────────────
    current_dir = Path('.')
    parent_dir  = Path('..')
    output_dir  = Path('html_output')

    md_files        = list(current_dir.glob('*.md'))
    parent_md_files = list(parent_dir.glob('*.md'))

    readme_file = None
    other_files = []

    for file in parent_md_files:
        if file.name == 'README.md':
            readme_file = file

    for file in md_files:
        if file.name != 'README.md':
            other_files.append(file)

    other_files.sort(key=lambda x: x.name)

    all_files = []
    if readme_file:
        all_files.append(readme_file)
    all_files.extend(other_files)

    print(f"Found {len(md_files)} markdown files:")

    converted_files = []

    for md_file in all_files:
        print(f"Converting {md_file.name}...")

        with open(md_file, 'r', encoding='utf-8') as f:
            md_content = f.read()

        # Fix indented code blocks
        lines = md_content.split('\n')
        fixed_lines = []
        in_code_block    = False
        code_block_indent = 0

        for line in lines:
            stripped = line.lstrip()
            if stripped.startswith('```'):
                if not in_code_block:
                    code_block_indent = len(line) - len(stripped)
                    in_code_block = True
                    fixed_lines.append(stripped)
                else:
                    in_code_block = False
                    fixed_lines.append(stripped)
            elif in_code_block and line.startswith(' ' * code_block_indent):
                fixed_lines.append(line[code_block_indent:])
            else:
                fixed_lines.append(line)

        md_content = '\n'.join(fixed_lines)

        # Extract & preserve mermaid blocks
        # IMPORTANT: placeholder must NOT contain underscores — markdown treats
        # __text__ as <strong>text</strong> which corrupts the placeholder.
        # We use XMERMAIDIDX<n>XEND which markdown cannot interpret as markup.
        mermaid_blocks = []
        def extract_mermaid(match):
            idx = len(mermaid_blocks)
            mermaid_blocks.append(match.group(1))
            return f"\nXMERMAIDIDX{idx}XEND\n"

        md_content = re.sub(
            r'```mermaid\s*\n(.*?)\n\s*```',
            extract_mermaid,
            md_content,
            flags=re.DOTALL
        )

        html_content = markdown.markdown(
            md_content,
            extensions=['codehilite', 'tables', 'toc', 'fenced_code'],
            extension_configs={
                'codehilite': {
                    'css_class': 'codehilite',
                    'use_pygments': True
                }
            }
        )

        # Restore mermaid blocks — regex matches both:
        #   <p>XMERMAIDIDX0XEND</p>   (markdown wraps lone lines in <p>)
        #   XMERMAIDIDX0XEND          (bare, if already inside a block element)
        def restore_mermaid(m):
            idx  = int(m.group(1) if m.group(1) is not None else m.group(2))
            code = mermaid_blocks[idx]
            return f'<div class="mermaid">\n{code}\n</div>'

        html_content = re.sub(
            r'<p>\s*XMERMAIDIDX(\d+)XEND\s*</p>|XMERMAIDIDX(\d+)XEND',
            restore_mermaid,
            html_content
        )

        title      = md_file.stem.replace('_', ' ').replace('-', ' ').title()
        full_html  = html_template.replace("__TITLE__", title).replace("__CONTENT__", html_content)

        html_file = output_dir / f"{md_file.stem}.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(full_html)

        converted_files.append({
            'name':      md_file.name,
            'title':     title,
            'html_file': html_file.name
        })

        print(f"  ✓ Created {html_file}")

    # ── Determine initial iframe src ─────────────────────────────────────────
    if readme_file:
        initial_src = "README.html"
    elif converted_files:
        initial_src = converted_files[0]['html_file']
    else:
        initial_src = 'about:blank'

    print(f"\n✅ Conversion complete!")
    print(f"📁 HTML files saved in: {output_dir.absolute()}")
    print(f"🌐 Open {output_dir}/index.html in your browser to view all documents")


if __name__ == "__main__":
    convert_md_to_html()