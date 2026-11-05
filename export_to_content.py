import json
import os

projects_path = r"C:\Users\Dom.Vinicius\portfolio\data\projects.json"
content_dir = r"C:\Users\Dom.Vinicius\portfolio\content\projects"
os.makedirs(content_dir, exist_ok=True)

with open(projects_path, encoding="utf-8") as f:
    projects = json.load(f)

for idx, p in enumerate(projects):
    slug = p["slug"]
    item_data = {
        "title": p.get("title", ""),
        "date": p.get("date", ""),
        "category": p.get("category", "work"),
        "order": idx + 1,
        "slug": slug,
        "cover": p.get("local_cover") or p.get("cover_img", ""),
        "modules": []
    }
    for m in p.get("modules", []):
        if m.get("type") == "image":
            item_data["modules"].append({
                "type": "image",
                "image": m.get("local_src") or m.get("src", "")
            })
        elif m.get("type") == "text":
            item_data["modules"].append({
                "type": "text",
                "text": m.get("content", "")
            })

    file_path = os.path.join(content_dir, f"{slug}.json")
    with open(file_path, "w", encoding="utf-8") as f_out:
        json.dump(item_data, f_out, indent=2, ensure_ascii=False)

print(f"Exported {len(projects)} individual project files to {content_dir}")
