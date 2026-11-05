import os
import json
import glob

# ==========================================================
# BUILDER UNIFICADO COM SUPORTE A CATEGORIAS DINÂMICAS
# ==========================================================

HEADER_TEMPLATE = """  <!-- Site Header -->
  <header class="site-header">
    <div class="logo-area">
      <a href="index.html" class="site-title">Vinicius Domingues</a>
      <span class="site-subtitle">Visualização Arquitetônica & Detalhamento</span>
    </div>

    <nav class="site-nav">
{nav_links}
    </nav>
  </header>"""

FOOTER_HTML = """  <!-- Site Footer -->
  <footer class="site-footer">
    <div>&copy; 2026 Vinicius Domingues. Todos os direitos reservados.</div>
    <div>
      <a href="admin/" class="admin-link" title="Painel de Edição">Área de Edição</a>
    </div>
  </footer>"""

GRID_PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{page_title} - Vinicius Domingues</title>
  <meta name="description" content="Projetos de {category_name} - Vinicius Domingues." />
  <link rel="stylesheet" href="assets/css/style.css" />
</head>
<body>

{header}

  <!-- Main Content -->
  <main class="main-content">
    <div class="projects-grid" id="projects-grid">
{cards_html}
    </div>
  </main>

{footer}

  <script src="assets/js/main.js"></script>
</body>
</html>
"""

PROJECT_PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} - Vinicius Domingues</title>
  <meta name="description" content="{meta_desc}" />
  <link rel="stylesheet" href="assets/css/style.css" />
</head>
<body>

{header}

  <!-- Project Container -->
  <main class="main-content" id="project-content">
    <div class="project-header">
      <h1 class="project-detail-title">{title}</h1>
      <div class="project-detail-meta">{date_meta}</div>
    </div>

    <div class="project-modules" id="project-modules">
{modules_html}
    </div>

    <nav class="project-navigation" id="project-nav">
      <div>
        {prev_link}
      </div>
      <div>
        <a href="{back_url}" class="back-link">Voltar para {back_label}</a>
      </div>
      <div>
        {next_link}
      </div>
    </nav>
  </main>

  <!-- Lightbox Modal -->
  <div class="lightbox-modal" id="lightbox-modal" onclick="closeLightbox()">
    <button class="lightbox-close" aria-label="Fechar">&times;</button>
    <img id="lightbox-img" class="lightbox-img" src="" alt="Ampliação" onclick="event.stopPropagation()" />
  </div>

{footer}

  <script src="assets/js/main.js"></script>
</body>
</html>
"""

def build():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    cat_dir = os.path.join(base_dir, "content", "categories")
    proj_dir = os.path.join(base_dir, "content", "projects")
    data_dir = os.path.join(base_dir, "data")
    os.makedirs(data_dir, exist_ok=True)

    # 1. Carregar Categorias
    categories = []
    if os.path.exists(cat_dir):
        for f in glob.glob(os.path.join(cat_dir, "*.json")):
            with open(f, "r", encoding="utf-8") as fp:
                try:
                    c = json.load(fp)
                    categories.append(c)
                except Exception as e:
                    print(f"Erro lendo categoria {f}: {e}")

    # Fallback se não houver categorias gravadas
    if not categories:
        categories = [
            {"name": "Portfólio 3D", "slug": "work", "order": 1},
            {"name": "Portfólio Detalhamento", "slug": "detalhamento", "order": 2}
        ]

    categories.sort(key=lambda x: x.get("order", 999))
    with open(os.path.join(data_dir, "categories.json"), "w", encoding="utf-8") as fp:
        json.dump(categories, fp, indent=2, ensure_ascii=False)

    cat_map = {c["slug"]: c["name"] for c in categories}

    # 2. Carregar Projetos
    projects = []
    if os.path.exists(proj_dir):
        for f in glob.glob(os.path.join(proj_dir, "*.json")):
            with open(f, "r", encoding="utf-8") as fp:
                try:
                    data = json.load(fp)
                    slug = data.get("slug") or os.path.splitext(os.path.basename(f))[0]
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
                except Exception as e:
                    print(f"Erro lendo projeto {f}: {e}")

    projects.sort(key=lambda x: x.get("order", 999))
    with open(os.path.join(data_dir, "projects.json"), "w", encoding="utf-8") as fp:
        json.dump(projects, fp, indent=2, ensure_ascii=False)

    print(f"[1/3] Banco compilado: {len(categories)} categorias e {len(projects)} projetos.")

    # 3. Função auxiliar para gerar menu de navegação
    def render_nav(active_slug):
        links = []
        for c in categories:
            c_slug = c["slug"]
            c_name = c["name"]
            url = "index.html" if c_slug == "work" else f"{c_slug}.html"
            is_active = " active" if active_slug == c_slug else ""
            links.append(f'      <a href="{url}" class="nav-link{is_active}">{c_name}</a>')
        
        links.append('      <a href="https://www.instagram.com/vini.domingue.s" target="_blank" rel="noopener" class="nav-link nav-social">Instagram</a>')
        links.append('      <a href="https://www.linkedin.com/in/vinicius-domingues-596ab3199/" target="_blank" rel="noopener" class="nav-link nav-social">LinkedIn</a>')
        contact_active = " active" if active_slug == "contact" else ""
        links.append(f'      <a href="contact.html" class="nav-link{contact_active}">Contato</a>')
        return "\n".join(links)

    # 4. Gerar Páginas de Grade de cada Categoria
    for c in categories:
        c_slug = c["slug"]
        c_name = c["name"]
        cat_projects = [p for p in projects if p["category"] == c_slug]

        cards = []
        for p in cat_projects:
            cards.append(f"""      <a href="{p['slug']}.html" class="project-card" data-slug="{p['slug']}">
        <div class="project-thumb-wrap">
          <img src="{p['local_cover']}" alt="{p['title']}" class="project-thumb" loading="lazy" />
        </div>
        <div class="project-info">
          <span class="project-name">{p['title']}</span>
          <span class="project-year">{p.get('date', '')}</span>
        </div>
      </a>""")

        page_html = GRID_PAGE_TEMPLATE.format(
            page_title=c_name,
            category_name=c_name,
            header=HEADER_TEMPLATE.format(nav_links=render_nav(c_slug)),
            cards_html="\n".join(cards) if cards else '<p style="text-align:center; grid-column: 1/-1; padding: 40px; color:#888;">Nenhum projeto cadastrado nesta categoria ainda.</p>',
            footer=FOOTER_HTML
        )

        # Se for "work", grava index.html e também work.html
        if c_slug == "work":
            with open(os.path.join(base_dir, "index.html"), "w", encoding="utf-8") as fp:
                fp.write(page_html)
            with open(os.path.join(base_dir, "work.html"), "w", encoding="utf-8") as fp:
                fp.write(page_html)
        else:
            with open(os.path.join(base_dir, f"{c_slug}.html"), "w", encoding="utf-8") as fp:
                fp.write(page_html)

    # Atualizar contact.html com os links dinâmicos do cabeçalho
    contact_path = os.path.join(base_dir, "contact.html")
    if os.path.exists(contact_path):
        with open(contact_path, "r", encoding="utf-8") as fp:
            c_content = fp.read()
        # Substitui apenas a tag <nav class="site-nav">...</nav>
        import re
        c_content = re.sub(r'<nav class="site-nav">.*?</nav>', f'<nav class="site-nav">\n{render_nav("contact")}\n    </nav>', c_content, flags=re.DOTALL)
        with open(contact_path, "w", encoding="utf-8") as fp:
            fp.write(c_content)

    print(f"[2/3] Páginas de grade de todas as {len(categories)} categorias geradas com sucesso.")

    # 5. Gerar Páginas Individuais de Projetos
    for idx, p in enumerate(projects):
        slug = p["slug"]
        title = p["title"]
        date = p.get("date", "")
        category = p.get("category", "work")
        cat_name = cat_map.get(category, "Portfólio")

        date_meta = f"{date} • {cat_name}" if date else cat_name
        prev_p = projects[idx - 1] if idx > 0 else None
        next_p = projects[idx + 1] if idx < len(projects) - 1 else None

        prev_link = f'<a href="{prev_p["slug"]}.html">← {prev_p["title"]}</a>' if prev_p else ""
        next_link = f'<a href="{next_p["slug"]}.html">{next_p["title"]} →</a>' if next_p else ""
        back_url = "index.html" if category == "work" else f"{category}.html"

        modules_parts = []
        meta_desc_parts = []
        for m in p.get("modules", []):
            if m.get("type") == "text":
                text_content = m.get("content", "").replace("\n", "<br>")
                meta_desc_parts.append(m.get("content", ""))
                modules_parts.append(f"""      <div class="module-text-container">
        <p>{text_content}</p>
      </div>""")
            elif m.get("type") == "image":
                img_src = m.get("local_src") or m.get("src", "")
                modules_parts.append(f"""      <div class="module-img-container" onclick="openLightbox('{img_src}')">
        <img src="{img_src}" alt="{title}" class="module-img" loading="lazy" />
      </div>""")

        meta_desc = (" ".join(meta_desc_parts)[:150] or f"Projeto {title} - {cat_name} de Vinicius Domingues.").replace('"', '&quot;')

        proj_html = PROJECT_PAGE_TEMPLATE.format(
            title=title,
            meta_desc=meta_desc,
            header=HEADER_TEMPLATE.format(nav_links=render_nav(category)),
            date_meta=date_meta,
            modules_html="\n".join(modules_parts),
            prev_link=prev_link,
            next_link=next_link,
            back_url=back_url,
            back_label=cat_name,
            footer=FOOTER_HTML
        )

        with open(os.path.join(base_dir, f"{slug}.html"), "w", encoding="utf-8") as fp:
            fp.write(proj_html)

    print(f"[3/3] Todas as {len(projects)} páginas estáticas de projetos geradas com sucesso!")

if __name__ == "__main__":
    build()
