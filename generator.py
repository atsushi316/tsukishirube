import json
import os
import sys
from datetime import datetime

def generate(new_title=None, new_content=None):
    workspace = "/Users/atsushi/.openclaw/workspace/public_site"
    articles_dir = f"{workspace}/articles"
    os.makedirs(articles_dir, exist_ok=True)

    contents_path = f"{workspace}/contents.json"
    with open(contents_path, "r", encoding="utf-8") as f:
        contents = json.load(f)

    # 1. 既存のデータから「miya/Miya」を排除して一般化する
    for item in contents:
        item['content'] = item['content'].replace("miyaさん", "パートナー").replace("miya さん", "パートナー").replace("miya", "パートナー").replace("Miya", "パートナー")
        item['title'] = item['title'].replace("miyaさん", "パートナー").replace("miya", "パートナー")

    # 2. 新しい記事があれば追加
    if new_title and new_content:
        new_entry = {
            "date": datetime.now().strftime("%Y.%m.%d"),
            "title": new_title,
            "content": new_content,
            "highlight": True
        }
        contents.insert(0, new_entry)

    # 3. データを保存
    with open(contents_path, "w", encoding="utf-8") as f:
        json.dump(contents, f, ensure_ascii=False, indent=4)

    # 4. テンプレート読み込み
    with open(f"{workspace}/template.html", "r", encoding="utf-8") as f:
        main_template = f.read()

    # 5. HTML生成
    articles_list_html = ""
    for idx, item in enumerate(contents):
        # ファイル名をタイトルの一部から生成するように変更し、インデックス依存を排除
        safe_title = "".join(x for x in item['title'] if x.isalnum())[:20]
        filename = f"insight-{item['date'].replace('.', '')}-{safe_title}.html"
        file_path = f"articles/{filename}"
        highlight_class = "highlight" if item.get("highlight") else ""
        
        articles_list_html += f"""
            <a href="{file_path}" class="insight-card-link">
                <article class="insight-item {highlight_class}">
                    <time class="m3-label">{item['date']}</time>
                    <h3 class="m3-title">{item['title']}</h3>
                    <p class="m3-body">{item['content'][:100]}...</p>
                    <span class="m3-indicator">→</span>
                </article>
            </a>
        """

        display_content = item['content'].replace('\\n', '<br>').replace('\n', '<br>')
        article_page_content = main_template.replace("{{ARTICLES}}", f"""
            <article class="insight-item full-view">
                <time class="m3-label">{item['date']}</time>
                <h3 class="m3-title-large">{item['title']}</h3>
                <div class="m3-body-large">
                    {display_content}
                </div>
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
    
    print(f"Successfully generated site with {len(contents)} articles.")

if __name__ == "__main__":
    if len(sys.argv) > 2:
        generate(sys.argv[1], sys.argv[2])
    else:
        generate()
