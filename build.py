import os
import json
import glob
from generate_static_projects import generate_static_pages

def build():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    content_dir = os.path.join(base_dir, "content", "projects")
    output_file = os.path.join(base_dir, "data", "projects.json")

    projects = []
    for file_path in glob.glob(os.path.join(content_dir, "*.json")):
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            slug = data.get("slug") or os.path.splitext(os.path.basename(file_path))[0]
            normalized = {
                "slug": slug,
                "title": data.get("title", ""),
                "date": data.get("date", ""),
                "category": data.get("category", "work"),
                "order": data.get("order", 999),
                "local_cover": data.get("cover", ""),
                "cover_img": data.get("cover", ""),
                "modules": []
            }
            for m in data.get("modules", []):
                if m.get("type") == "image":
                    img_src = m.get("image") or m.get("local_src") or m.get("src", "")
                    normalized["modules"].append({
                        "type": "image",
                        "local_src": img_src,
                        "src": img_src
                    })
                elif m.get("type") == "text":
                    normalized["modules"].append({
                        "type": "text",
                        "content": m.get("text") or m.get("content", "")
                    })
            projects.append(normalized)

    # Sort projects by order
    projects.sort(key=lambda x: x.get("order", 999))

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(projects, f, indent=2, ensure_ascii=False)

    print(f"[1/2] Compilação concluída: {len(projects)} projetos gravados em data/projects.json")

    # Generate all static project HTML pages in-process (no subprocess dependency)
    generate_static_pages(base_dir=base_dir, projects=projects)
    print("[2/2] Todas as páginas estáticas geradas com sucesso!")

if __name__ == "__main__":
    build()
