import json
import os
import sys

def generate(new_title=None, new_content=None):
    workspace = "public_site"
    articles_dir = f"{workspace}/articles"
    os.makedirs(articles_dir, exist_ok=True)

    contents_path = f"{workspace}/contents.json"
    with open(contents_path, "r") as f:
        contents = json.load(f)

    # もし新しい記事の情報があれば追加
    if new_title and new_content:
        from datetime import datetime
        new_entry = {
            "date": datetime.now().strftime("%Y.%m.%d"),
            "title": new_title,
            "content": new_content,
            "highlight": True
        }
        contents.insert(0, new_entry) # 先頭に追加
        with open(contents_path, "w") as f:
            json.dump(contents, f, ensure_ascii=False, indent=4)

    with open(f"{workspace}/template.html", "r") as f:
        main_template = f.read()

    # 記事一覧用のHTML
    articles_list_html = ""
    for idx, item in enumerate(contents):
        filename = f"insight-{item['date'].replace('.', '')}-{idx}.html"
        file_path = f"articles/{filename}"
        
        highlight_class = "highlight" if item.get("highlight") else ""
        
        # 構造をシンプルに清掃: 余計なタグを排除し、aタグで全体を囲む
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

        article_page_content = main_template.replace("{{ARTICLES}}", f"""
            <article class="insight-item full-view">
                <time class="m3-label">{item['date']}</time>
                <h3 class="m3-title-large">{item['title']}</h3>
                <div class="m3-body-large">
                    {item['content'].replace('\n', '<br>')}
                </div>
                <div class="back-link">
                    <a href="../index.html">← トップページへ戻る</a>
                </div>
            </article>
        """)
        article_page_content = article_page_content.replace('href="style.css"', 'href="../style.css"')
        
        with open(f"{articles_dir}/{filename}", "w") as f:
            f.write(article_page_content)

    final_main_html = main_template.replace("{{ARTICLES}}", articles_list_html)
    with open(f"{workspace}/index.html", "w") as f:
        f.write(final_main_html)
    
    print("Successfully generated clean HTML structure.")

if __name__ == "__main__":
    if len(sys.argv) > 2:
        generate(sys.argv[1], sys.argv[2])
    else:
        generate()
