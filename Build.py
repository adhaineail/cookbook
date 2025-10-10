import os
import html

# ---------- CONFIGURATION ----------
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CSS_FILE = os.path.join(ROOT_DIR, "Stylesheet.css")
OUTPUT_EXT_HTML = ".html"
INDEX_FILE = os.path.join(ROOT_DIR, "Index.html")
# -----------------------------------

# ---------- RECIPE PARSER ----------
def parse_recipe(path):
    recipe = {"title": "", "serves": "", "prep": "", "cook": "",
              "ingredients": [], "directions": [], "notes": []}
    section = None
    first_line_used = False

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if not first_line_used:
                recipe["title"] = line
                first_line_used = True
                continue
            elif line.startswith("Serves:"):
                recipe["serves"] = line.split(":", 1)[1].strip()
            elif line.startswith("Active Time:"):
                recipe["prep"] = line.split(":", 1)[1].strip()
            elif line.startswith("Total Time:"):
                recipe["cook"] = line.split(":", 1)[1].strip()
            elif line.startswith("Ingredients:"):
                section = "ingredients"
            elif line.startswith("Directions:"):
                section = "directions"
            elif line.startswith("Notes:"):
                section = "notes"
            elif section == "ingredients" and line.startswith("-"):
                recipe["ingredients"].append(line[1:].strip())
            elif section == "directions" and line[:1].isdigit():
                recipe["directions"].append(line[line.find('.') + 1:].strip())
            elif section == "notes" and line.startswith("-"):
                recipe["notes"].append(line[1:].strip())
    return recipe

# ---------- HTML CONVERSION ----------
def recipe_to_html(recipe, dirpath, base_name):
    image_extensions = [".jpg", ".jpeg", ".png", ".webp"]
    image_filename = None
    for ext in image_extensions:
        candidate = os.path.join(dirpath, base_name + ext)
        if os.path.exists(candidate):
            image_filename = base_name + ext
            break

    img_html = ""
    if image_filename:
        img_html = f'<img src="{image_filename}" alt="{recipe["title"]}" class="recipe-image">\n'

    css_rel = os.path.relpath(CSS_FILE, dirpath).replace("\\", "/")

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="{css_rel}">
  <title>{recipe['title']}</title>
</head>
<body>
  <h1>{recipe['title']}</h1>
  {img_html}
  <div class="metadata">
    Serves: {recipe['serves']}<br>
    Active Time: {recipe['prep']} | Total Time: {recipe['cook']}
  </div>
  <h2>Ingredients</h2>
  <ul>
    {''.join(f"<li>{html.escape(ing)}</li>" for ing in recipe['ingredients'])}
  </ul>
  <h2>Directions</h2>
  <ol>
    {''.join(f"<li>{html.escape(step)}</li>" for step in recipe['directions'])}
  </ol>
  <h2>Notes</h2>
  <ul>
    {''.join(f"<li>{html.escape(note)}</li>" for note in recipe['notes'])}
  </ul>
</body>
</html>"""
    return html_content

# ---------- BUILD RECIPES ----------
def build_all_recipes(root):
    print("Building recipe HTML files...")
    for dirpath, _, filenames in os.walk(root):
        # Skip root directory files
        if os.path.abspath(dirpath) == os.path.abspath(root):
            continue
        for file in filenames:
            if not file.lower().endswith(".txt"):
                continue
            base_name = os.path.splitext(file)[0]
            txt_path = os.path.join(dirpath, file)
            html_path = os.path.join(dirpath, base_name + OUTPUT_EXT_HTML)

            recipe = parse_recipe(txt_path)
            html_content = recipe_to_html(recipe, dirpath, base_name)

            with open(html_path, "w", encoding="utf-8") as f:
                f.write(html_content)
            print(f"✅ Created HTML: {html_path}")
    print("All recipes processed successfully!\n")

# ---------- BUILD INDEX ----------
def build_html_list(path, level=0):
    items = []
    entries = sorted(os.listdir(path))
    for name in entries:
        full_path = os.path.join(path, name)
        if name.startswith(".") or name in {"Index.html"}:
            continue

        if os.path.isdir(full_path):
            recipe_file = os.path.join(full_path, f"{name}.html")
            if os.path.isfile(recipe_file):
                rel_path = os.path.relpath(recipe_file, ROOT_DIR).replace("\\", "/")
                items.append(f'<li><a href="{html.escape(rel_path)}">{html.escape(name)}</a></li>')
            else:
                items.append(f'<li class="folder">{html.escape(name)}\n<ul>')
                items.append(build_html_list(full_path, level + 1))
                items.append('</ul></li>')
    return "\n".join(items)

def build_index():
    print("Building index...")
    header = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="Stylesheet.css">
  <title>Recipe Collection</title>
</head>
<body>
<h1>Recipe Collection</h1>
<ul>
"""
    footer = "</ul>\n</body>\n</html>"
    content = build_html_list(ROOT_DIR)
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        f.write(header + content + footer)
    print(f"Index updated: {INDEX_FILE}\n")

# ---------- MAIN ----------
if __name__ == "__main__":
    build_all_recipes(ROOT_DIR)
    build_index()
    print("✅ All done! Recipes and index are up to date.")
