import os
import json

TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} - Vinicius Domingues</title>
  <meta name="description" content="{meta_desc}" />
  <link rel="stylesheet" href="assets/css/style.css" />
</head>
<body>

  <!-- Site Header -->
  <header class="site-header">
    <div class="logo-area">
      <a href="index.html" class="site-title">Vinicius Domingues</a>
      <span class="site-subtitle">Visualização Arquitetônica & Detalhamento</span>
    </div>

    <nav class="site-nav">
      <a href="index.html" class="nav-link {nav_work_active}">Portfólio</a>
      <a href="detalhamento.html" class="nav-link {nav_det_active}">Portfólio Detalhamento</a>
      <a href="https://www.instagram.com/vini.domingue.s" target="_blank" rel="noopener" class="nav-link nav-social">Instagram</a>
      <a href="https://www.linkedin.com/in/vinicius-domingues-596ab3199/" target="_blank" rel="noopener" class="nav-link nav-social">LinkedIn</a>
      <a href="contact.html" class="nav-link">Contato</a>
    </nav>
  </header>

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

  <!-- Site Footer -->
  <footer class="site-footer">
    <div>&copy; 2026 Vinicius Domingues. Todos os direitos reservados.</div>
    <div>
      <a href="admin/" class="admin-link" title="Painel de Edição">Área de Edição</a>
    </div>
  </footer>

  <script src="assets/js/main.js"></script>
</body>
</html>
"""

def generate_static_pages(base_dir=None, projects=None):
    if base_dir is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))

    if projects is None:
        data_path = os.path.join(base_dir, "data", "projects.json")
        with open(data_path, "r", encoding="utf-8") as f:
            projects = json.load(f)

    for idx, p in enumerate(projects):
        slug = p["slug"]
        title = p["title"]
        date = p.get("date", "")
        category = p.get("category", "work")

        nav_work_active = "active" if category == "work" else ""
        nav_det_active = "active" if category == "detalhamento" else ""
        category_label = "Portfólio Detalhamento" if category == "detalhamento" else "Portfólio 3D"
        date_meta = f"{date} • {category_label}" if date else category_label

        prev_p = projects[idx - 1] if idx > 0 else None
        next_p = projects[idx + 1] if idx < len(projects) - 1 else None

        prev_link = f'<a href="{prev_p["slug"]}.html">← {prev_p["title"]}</a>' if prev_p else ""
        next_link = f'<a href="{next_p["slug"]}.html">{next_p["title"]} →</a>' if next_p else ""
        back_url = "detalhamento.html" if category == "detalhamento" else "index.html"
        back_label = "Portfólio Detalhamento" if category == "detalhamento" else "Portfólio"

        modules_parts = []
        meta_desc_parts = []
        for m in p.get("modules", []):
            if m.get("type") == "text":
                text_content = m.get("content", "").replace("\n", "<br>")
                meta_desc_parts.append(m.get("content", ""))
                modules_parts.append(f"""
                  <div class="module-text-container">
                    <p>{text_content}</p>
                  </div>
                """)
            elif m.get("type") == "image":
                img_src = m.get("local_src") or m.get("src", "")
                modules_parts.append(f"""
                  <div class="module-img-container" onclick="openLightbox('{img_src}')">
                    <img src="{img_src}" alt="{title}" class="module-img" loading="lazy" />
                  </div>
                """)

        meta_desc = (" ".join(meta_desc_parts)[:150] or f"Projeto {title} - {category_label} de Vinicius Domingues.").replace('"', '&quot;')

        rendered_html = TEMPLATE.format(
            title=title,
            meta_desc=meta_desc,
            nav_work_active=nav_work_active,
            nav_det_active=nav_det_active,
            date_meta=date_meta,
            modules_html="\n".join(modules_parts),
            prev_link=prev_link,
            next_link=next_link,
            back_url=back_url,
            back_label=back_label
        )

        out_file = os.path.join(base_dir, f"{slug}.html")
        with open(out_file, "w", encoding="utf-8") as f_out:
            f_out.write(rendered_html)

    print(f"Geradas {len(projects)} páginas estáticas de projetos com sucesso.")

if __name__ == "__main__":
    generate_static_pages()
