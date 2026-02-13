import json
import os

def generate():
    workspace = "/Users/atsushi/.openclaw/workspace/projects/tsukishirube"
    with open(f"{workspace}/contents.json", "r") as f:
        contents = json.load(f)

    with open(f"{workspace}/template.html", "r") as f:
        template = f.read()

    articles_html = ""
    for item in contents:
        highlight_class = "highlight" if item.get("highlight") else ""
        articles_html += f"""
            <article class="insight-item {highlight_class}">
                <time>{item['date']}</time>
                <h3>{item['title']}</h3>
                <p>{item['content']}</p>
            </article>
            <hr class="divider">
        """

    # Remove the last divider
    if articles_html.endswith('<hr class="divider">'):
        articles_html = articles_html[:-len('<hr class="divider">')]

    final_html = template.replace("{{ARTICLES}}", articles_html)

    with open(f"{workspace}/index.html", "w") as f:
        f.write(final_html)
    print("Successfully generated index.html")

if __name__ == "__main__":
    generate()
