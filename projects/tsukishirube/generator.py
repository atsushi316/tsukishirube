import json
import os

def generate():
    workspace = "/Users/atsushi/.openclaw/workspace/projects/tsukishirube"
    articles_dir = f"{workspace}/articles"
    os.makedirs(articles_dir, exist_ok=True)

    with open(f"{workspace}/contents.json", "r") as f:
        contents = json.load(f)

    with open(f"{workspace}/template.html", "r") as f:
        main_template = f.read()

    # 記事一覧用のHTML
    articles_list_html = ""
    for idx, item in enumerate(contents):
        # ファイル名を日付とIDから生成
        filename = f"insight-{item['date'].replace('.', '')}-{idx}.html"
        file_path = f"articles/{filename}"
        
        highlight_class = "highlight" if item.get("highlight") else ""
        
        # トップページ用のリストアイテム（リンク付き）
        articles_list_html += f"""
            <article class="insight-item {highlight_class}">
                <time>{item['date']}</time>
                <h3><a href="{file_path}">{item['title']}</a></h3>
                <p>{item['content'][:100]}...</p>
            </article>
            <hr class="divider">
        """

        # 個別記事ページの生成
        article_page_content = main_template.replace("{{ARTICLES}}", f"""
            <article class="insight-item highlight">
                <time>{item['date']}</time>
                <h3>{item['title']}</h3>
                <div class="full-content">
                    <p>{item['content']}</p>
                </div>
                <div class="back-link">
                    <a href="../index.html">← トップページへ戻る</a>
                </div>
            </article>
        """)
        # 個別ページ用にCSSパスを調整
        article_page_content = article_page_content.replace('href="style.css"', 'href="../style.css"')
        
        with open(f"{articles_dir}/{filename}", "w") as f:
            f.write(article_page_content)

    # メインの index.html 生成
    final_main_html = main_template.replace("{{ARTICLES}}", articles_list_html)
    with open(f"{workspace}/index.html", "w") as f:
        f.write(final_main_html)
    
    print("Successfully generated index.html and individual article pages.")

if __name__ == "__main__":
    generate()
