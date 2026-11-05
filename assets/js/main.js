// ==========================================================
// PORTFÓLIO VINICIUS DOMINGUES - MAIN SCRIPTS
// ==========================================================

let projectsData = [];

// Fetch data
async function loadProjectsData() {
  if (projectsData.length > 0) return projectsData;
  try {
    const res = await fetch('data/projects.json');
    if (!res.ok) throw new Error('Falha ao carregar dados dos projetos');
    projectsData = await res.json();
    return projectsData;
  } catch (err) {
    console.error('Erro ao carregar projetos:', err);
    return [];
  }
}

// Render grid on index.html and detalhamento.html
async function renderGrid(category = 'work', containerId = 'projects-grid') {
  const container = document.getElementById(containerId);
  if (!container) return;

  const data = await loadProjectsData();
  const filtered = data.filter(p => p.category === category);

  container.innerHTML = filtered.map(p => `
    <a href="${p.slug}.html" class="project-card" data-slug="${p.slug}">
      <div class="project-thumb-wrap">
        <img src="${p.local_cover || p.cover_img}" 
             alt="${p.title}" 
             class="project-thumb" 
             loading="lazy" 
             onerror="this.src='${p.cover_img}'" />
      </div>
      <div class="project-info">
        <span class="project-name">${p.title}</span>
        <span class="project-year">${p.date || ''}</span>
      </div>
    </a>
  `).join('');
}

// Render Project Detail View
async function renderProjectDetail() {
  const params = new URLSearchParams(window.location.search);
  const slug = params.get('id');
  if (!slug) {
    window.location.href = 'index.html';
    return;
  }

  const data = await loadProjectsData();
  const projectIdx = data.findIndex(p => p.slug === slug);
  if (projectIdx === -1) {
    document.getElementById('project-content').innerHTML = `
      <div style="text-align: center; padding: 60px;">
        <h2>Projeto não encontrado</h2>
        <p><a href="index.html" class="back-link">← Voltar ao início</a></p>
      </div>
    `;
    return;
  }

  const project = data[projectIdx];
  const prevProject = projectIdx > 0 ? data[projectIdx - 1] : null;
  const nextProject = projectIdx < data.length - 1 ? data[projectIdx + 1] : null;

  // Set page title
  document.title = `${project.title} - Vinicius Domingues`;

  // Title & Header
  document.getElementById('project-title').textContent = project.title;
  const metaEl = document.getElementById('project-meta');
  if (metaEl) {
    const categoryName = project.category === 'detalhamento' ? 'Portfólio Detalhamento' : 'Portfólio 3D';
    metaEl.textContent = `${project.date ? project.date + ' • ' : ''}${categoryName}`;
  }

  // Modules (Images & Texts)
  const modulesContainer = document.getElementById('project-modules');
  if (modulesContainer) {
    modulesContainer.innerHTML = (project.modules || []).map(m => {
      if (m.type === 'text') {
        return `
          <div class="module-text-container">
            <p>${m.content.replace(/\n/g, '<br>')}</p>
          </div>
        `;
      } else if (m.type === 'image') {
        const imgSrc = m.local_src || m.src;
        return `
          <div class="module-img-container" onclick="openLightbox('${imgSrc}')">
            <img src="${imgSrc}" alt="${project.title}" class="module-img" loading="lazy" onerror="this.src='${m.src}'" />
          </div>
        `;
      }
      return '';
    }).join('');
  }

  // Navigation Links
  const navContainer = document.getElementById('project-nav');
  if (navContainer) {
    const backUrl = project.category === 'detalhamento' ? 'detalhamento.html' : 'index.html';
    const backLabel = project.category === 'detalhamento' ? 'Portfólio Detalhamento' : 'Portfólio';

    navContainer.innerHTML = `
      <div>
        ${prevProject ? `<a href="project.html?id=${prevProject.slug}">← ${prevProject.title}</a>` : ''}
      </div>
      <div>
        <a href="${backUrl}" class="back-link">Voltar para ${backLabel}</a>
      </div>
      <div>
        ${nextProject ? `<a href="project.html?id=${nextProject.slug}">${nextProject.title} →</a>` : ''}
      </div>
    `;
  }
}

// Lightbox
function openLightbox(src) {
  const modal = document.getElementById('lightbox-modal');
  const img = document.getElementById('lightbox-img');
  if (modal && img) {
    img.src = src;
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
  }
}

function closeLightbox() {
  const modal = document.getElementById('lightbox-modal');
  if (modal) {
    modal.classList.remove('active');
    document.body.style.overflow = '';
  }
}

// Close lightbox on Escape key
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') closeLightbox();
});

// Mobile menu toggle
function toggleMobileMenu() {
  const nav = document.querySelector('.site-nav');
  if (nav) {
    nav.classList.toggle('open');
  }
}
