import re
from pathlib import Path
import shutil

# Paths
posts_dir = Path("/Users/skairipa/notebook.hannaskairipa.com/content")
attachments_dir = Path("/Users/skairipa/Documents/obsidian/Attachments")
static_images_dir = Path("/Users/skairipa/Documents/Obsidian/static/images")
static_images_dir.mkdir(parents=True, exist_ok=True)

# Regex to find Obsidian-style image links
obsidian_pattern = re.compile(r'!?\[\[([^]]+\.(?:png|jpg|jpeg|gif))\]\]', re.IGNORECASE)

# Map all images in attachments (including subfolders)
image_map = {img.name: img for img in attachments_dir.rglob("*") if img.is_file()}

for md_file in posts_dir.glob("*.md"):
    content = md_file.read_text(encoding="utf-8")

    for image_name in obsidian_pattern.findall(content):
        # Convert to standard Markdown
        safe_name = image_name.replace(" ", "%20")
        markdown_image = f"![{Path(image_name).stem}](/images/{safe_name})"
        content = re.sub(r'!?\[\[' + re.escape(image_name) + r'\]\]', markdown_image, content)

        # Copy image to Hugo static folder
        source_path = image_map.get(image_name)
        if source_path:
            shutil.copy2(source_path, static_images_dir / image_name)
        else:
            print(f"Image not found: {image_name}")

    md_file.write_text(content, encoding="utf-8")

print("All Obsidian-style image links converted to Markdown for Hugo.")
