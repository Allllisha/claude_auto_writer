#!/usr/bin/env python3
"""
MarkdownをHTMLに変換するユーティリティ
"""

import re
from typing import Dict, List, Tuple

def convert_markdown_to_html(markdown_content: str) -> str:
    """MarkdownをWordPress用のHTMLに変換"""
    
    # 最初にタイトル行を除去（# で始まる最初の行）
    lines = markdown_content.split('\n')
    if lines and lines[0].startswith('# '):
        lines = lines[1:]
    content = '\n'.join(lines)
    
    # 見出しの変換（## → h2, ### → h3）
    content = re.sub(r'^### (.+)$', r'<h3>\1</h3>', content, flags=re.MULTILINE)
    content = re.sub(r'^## (.+)$', r'<h2>\1</h2>', content, flags=re.MULTILINE)
    
    # アンカーリンクの処理 {#id} を削除
    content = re.sub(r'\s*\{#[^}]+\}', '', content)
    
    # 太字の変換
    content = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', content)
    
    # リストの変換
    # 番号付きリスト
    content = re.sub(r'^\d+\.\s+(.+)$', r'<li>\1</li>', content, flags=re.MULTILINE)
    
    # 番号なしリスト（-で始まる行）
    content = re.sub(r'^-\s+(.+)$', r'<li>\1</li>', content, flags=re.MULTILINE)
    content = re.sub(r'^✅\s+(.+)$', r'<li>✅ \1</li>', content, flags=re.MULTILINE)
    
    # リストブロックの処理
    lines = content.split('\n')
    in_list = False
    list_type = None
    new_lines = []
    
    for i, line in enumerate(lines):
        if '<li>' in line:
            if not in_list:
                # 前の行が数字で始まっているかチェック
                if i > 0 and re.match(r'^\d+\.', lines[i-1]):
                    list_type = 'ol'
                else:
                    list_type = 'ul'
                new_lines.append(f'<{list_type}>')
                in_list = True
            new_lines.append(line)
        else:
            if in_list and line.strip() == '':
                new_lines.append(f'</{list_type}>')
                in_list = False
                list_type = None
            new_lines.append(line)
    
    if in_list:
        new_lines.append(f'</{list_type}>')
    
    content = '\n'.join(new_lines)
    
    # コードブロックの変換
    def convert_code_block(match):
        language = match.group(1) or ''
        code = match.group(2)
        # HTMLエスケープ
        code = code.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        return f'<pre class="wp-block-code"><code class="language-{language}">{code}</code></pre>'
    
    content = re.sub(r'```(\w*)\n(.*?)\n```', convert_code_block, content, flags=re.DOTALL)
    
    # インラインコードの変換
    content = re.sub(r'`([^`]+)`', r'<code>\1</code>', content)
    
    # リンクの変換
    content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', content)
    
    # 画像の変換（既に追加された画像は変換しない）
    content = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'<img src="\2" alt="\1" />', content)
    
    # テーブルの変換
    def convert_table(match):
        table_content = match.group(0)
        lines = table_content.strip().split('\n')
        
        if len(lines) < 3:
            return table_content
        
        html = '<table class="wp-block-table">\n<thead>\n<tr>\n'
        
        # ヘッダー行
        headers = [cell.strip() for cell in lines[0].split('|') if cell.strip()]
        for header in headers:
            html += f'<th>{header}</th>\n'
        html += '</tr>\n</thead>\n<tbody>\n'
        
        # データ行（セパレータ行をスキップ）
        for line in lines[2:]:
            if line.strip():
                html += '<tr>\n'
                cells = [cell.strip() for cell in line.split('|') if cell.strip()]
                for cell in cells:
                    html += f'<td>{cell}</td>\n'
                html += '</tr>\n'
        
        html += '</tbody>\n</table>'
        return html
    
    # テーブルを検出して変換
    table_pattern = r'\|[^|]+\|.*\n\|[-:\s|]+\|.*(?:\n\|[^|]+\|.*)*'
    content = re.sub(table_pattern, convert_table, content, flags=re.MULTILINE)
    
    # 段落の処理
    paragraphs = content.split('\n\n')
    processed_paragraphs = []
    
    for para in paragraphs:
        para = para.strip()
        if para and not para.startswith('<') and not para.startswith('---'):
            # 既にHTMLタグで始まっていない段落をpタグで囲む
            if not any(para.startswith(tag) for tag in ['<h', '<ul', '<ol', '<pre', '<table', '<figure', '<div']):
                para = f'<p>{para}</p>'
        processed_paragraphs.append(para)
    
    content = '\n\n'.join(processed_paragraphs)
    
    # 水平線の変換
    content = re.sub(r'^---+$', '<hr />', content, flags=re.MULTILINE)
    
    # 絵文字を保持（特に処理は不要）
    
    # 余分な空行を削除
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    return content.strip()