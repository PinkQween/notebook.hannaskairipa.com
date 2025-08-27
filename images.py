import os
import re
import shutil
from pathlib import Path

# Paths
posts_dir = Path("/Users/skairipa/notebook.hannaskairipa.com/content")
attachments_dir = Path("/Users/skairipa/Documents/obsidian/Attachments")
static_images_dir = Path("/Users/skairipa/Documents/Obsidian/static/images")

# Ensure the static images directory exists
static_images_dir.mkdir(parents=True, exist_ok=True)

# Regex to match common image references: [[file.png]] or ![[file.png]]
image_pattern = re.compile(r'!?\[\[([^]]+\.(?:png|jpg|jpeg|gif))\]\]', re.IGNORECASE)

# Build a map of all images in attachments (including subfolders)
image_map = {img.name: img for img in attachments_dir.rglob("*") if img.is_file()}

for md_file in posts_dir.glob("*.md"):
    try:
        content = md_file.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Failed to read {md_file}: {e}")
        continue

    images = image_pattern.findall(content)

    for image_name in images:
        # Clean up filename for Markdown
        safe_name = image_name.replace(" ", "%20")
        markdown_image = f"![{Path(image_name).stem}](/images/{safe_name})"
        content = content.replace(f"[[{image_name}]]", markdown_image).replace(f"![[{image_name}]]", markdown_image)

        # Find image in attachments anywhere
        source_path = image_map.get(image_name)
        if source_path:
            try:
                shutil.copy2(source_path, static_images_dir / image_name)
            except Exception as e:
                print(f"Failed to copy {image_name}: {e}")
        else:
            print(f"Image not found anywhere: {image_name}")

    # Write the updated content back
    try:
        md_file.write_text(content, encoding="utf-8")
    except Exception as e:
        print(f"Failed to write {md_file}: {e}")

print("Markdown files processed and images copied successfully.")
