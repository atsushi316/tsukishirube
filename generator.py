import json
import os
import sys
import re
from datetime import datetime

def generate(new_title=None, new_content=None, new_image=None):
    workspace = "/Users/atsushi/.openclaw/workspace/public_site"
    articles_dir = f"{workspace}/articles"
    os.makedirs(articles_dir, exist_ok=True)

    contents_path = f"{workspace}/contents.json"
    with open(contents_path, "r", encoding="utf-8") as f:
        contents = json.load(f)

    # 1. 匿名化
    for item in contents:
        item['content'] = item['content'].replace("miyaさん", "パートナー").replace("miya さん", "パートナー").replace("miya", "パートナー").replace("Miya", "パートナー")
        item['title'] = item['title'].replace("miyaさん", "パートナー").replace("miya", "パートナー")

    # 2. 新しい記事の追加（もしあれば）
    if new_title and new_content:
        new_entry = {
            "date": datetime.now().strftime("%Y.%m.%d"),
            "title": new_title,
            "content": new_content,
            "highlight": True,
            "image": new_image # 画像パスを確実に保持
        }
        contents.insert(0, new_entry)

    with open(contents_path, "w", encoding="utf-8") as f:
        json.dump(contents, f, ensure_ascii=False, indent=4)

    with open(f"{workspace}/template.html", "r", encoding="utf-8") as f:
        main_template = f.read()

    # 3. HTML生成
    articles_list_html = ""
    total = len(contents)
    
    for idx, item in enumerate(contents):
        safe_title = re.sub(r'[^a-zA-Z0-9]', '', item['title'])[:20]
        filename = f"insight-{item['date'].replace('.', '')}-{safe_title}.html"
        file_path = f"articles/{filename}"
        highlight_class = "highlight" if item.get("highlight") else ""
        
        # アイキャッチ画像のHTML（存在する場合のみ）
        img_html = ""
        if item.get("image"):
            # インデックス用パス
            img_html = f'<div class="insight-eyecatch"><img src="{item["image"]}" alt="{item["title"]}"></div>'
            # 記事詳細用パス調整 (articlesフォルダからassetsへの相対パス)
            detail_img_path = item["image"] if item["image"].startswith("http") else f"../{item['image']}"
            detail_img_html = f'<div class="insight-eyecatch-full"><img src="{detail_img_path}" alt="{item["title"]}"></div>'
        else:
            detail_img_html = ""

        # トップページ用リスト
        articles_list_html += f"""
            <a href="{file_path}" class="insight-card-link">
                <article class="insight-item {highlight_class}">
                    <time class="m3-label">{item['date']}</time>
                    <h3 class="m3-title">{item['title']}</h3>
                    {img_html}
                    <p class="m3-body">{item['content'][:100]}...</p>
                    <span class="m3-indicator">→</span>
                </article>
            </a>
        """

        # ナビゲーション構築
        nav_html = '<div class="article-nav">'
        if idx > 0:
            prev_item = contents[idx-1]
            prev_safe = re.sub(r'[^a-zA-Z0-9]', '', prev_item['title'])[:20]
            prev_file = f"insight-{prev_item['date'].replace('.', '')}-{prev_safe}.html"
            nav_html += f'<a href="{prev_file}" class="nav-btn prev">← 次の新しい記事</a>'
        else:
            nav_html += '<span class="nav-spacer"></span>'
            
        if idx < total - 1:
            next_item = contents[idx+1]
            next_safe = re.sub(r'[^a-zA-Z0-9]', '', next_item['title'])[:20]
            next_file = f"insight-{next_item['date'].replace('.', '')}-{next_safe}.html"
            nav_html += f'<a href="{next_file}" class="nav-btn next">前の古い記事 →</a>'
        nav_html += '</div>'

        display_content = item['content'].replace('\\n', '<br>').replace('\n', '<br>')
        article_page_content = main_template.replace("{{ARTICLES}}", f"""
            <article class="insight-item full-view">
                <time class="m3-label">{item['date']}</time>
                <h3 class="m3-title-large">{item['title']}</h3>
                {detail_img_html}
                <div class="m3-body-large">
                    {display_content}
                </div>
                {nav_html}
                <div class="back-link">
                    <a href="../index.html">← トップページへ戻る</a>
                </div>
            </article>
        """)
        article_page_content = article_page_content.replace('href="style.css"', 'href="../style.css"')
        
        with open(f"{articles_dir}/{filename}", "w", encoding="utf-8") as f:
            f.write(article_page_content)

    final_main_html = main_template.replace("{{ARTICLES}}", articles_list_html)
    with open(f"{workspace}/index.html", "w", encoding="utf-8") as f:
        f.write(final_main_html)
    
    print(f"Successfully generated site with {total} articles, navigation, and images.")

if __name__ == "__main__":
    if len(sys.argv) > 3:
        generate(sys.argv[1], sys.argv[2], sys.argv[3])
    elif len(sys.argv) > 2:
        generate(sys.argv[1], sys.argv[2])
    else:
        generate()
