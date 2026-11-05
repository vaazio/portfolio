# Portfólio - Vinicius Domingues

Portfólio moderno, ultrarrápido e responsivo de Visualização Arquitetônica (3D) e Detalhamento Executivo (2D), migrado do Adobe Portfolio para arquitetura estática independente com custo de hospedagem **R$ 0,00/mês**.

---

## 🚀 Como testar localmente no seu computador

1. Abra o PowerShell ou Terminal nesta pasta:
   ```bash
   cd "C:\Users\Dom.Vinicius\portfolio"
   ```
2. Inicie o servidor local:
   ```bash
   python -m http.server 8080
   ```
3. Abra seu navegador em:
   - **Site:** [http://localhost:8080](http://localhost:8080)
   - **Portfólio 3D:** [http://localhost:8080/index.html](http://localhost:8080/index.html)
   - **Portfólio Detalhamento:** [http://localhost:8080/detalhamento.html](http://localhost:8080/detalhamento.html)
   - **Contato:** [http://localhost:8080/contact.html](http://localhost:8080/contact.html)
   - **Painel de Edição:** [http://localhost:8080/admin/](http://localhost:8080/admin/)

---

## 📝 Como funciona a Edição de Novos Projetos

O site conta com o **Sveltia CMS** integrado na pasta `/admin`. Ele oferece uma interface visual simples (estilo Adobe Portfolio / WordPress):

- **Adicionar Novo Projeto:** Preencha Título, Ano, selecione a categoria (3D ou Detalhamento), envie a imagem de capa e as imagens/renderizações em alta resolução.
- **Editar Projetos Existentes:** Você pode alterar textos, descrições, trocar imagens ou reordenar projetos.
- **Salvar/Publicar:** Ao clicar em salvar, a alteração é gravada e o site é republicado automaticamente.

### Edição Local Direta:
Se preferir criar ou alterar arquivos manualmente no seu computador:
1. Os projetos ficam salvos como arquivos JSON legíveis na pasta `content/projects/<slug>.json`.
2. Para compilar e gerar todas as páginas estáticas instantaneamente, basta rodar:
   ```bash
   python build.py
   ```

---

## 🌐 Como colocar no ar gratuitamente (Passo a Passo)

Para ter seu site no ar na internet com link público (ex: `viniciusdomingues.pages.dev` ou seu próprio domínio) sem pagar nada:

### Opção Recomendada: Cloudflare Pages (100% Grátis para sempre)

1. **Crie um repositório no GitHub:**
   - Acesse [github.com](https://github.com) e crie um novo repositório (ex: `portfolio`).
   - No terminal da pasta do seu portfólio, suba os arquivos:
     ```bash
     git init
     git add .
     git commit -m "Meu novo portfólio"
     git branch -M main
     git remote add origin https://github.com/SEU-USUARIO/portfolio.git
     git push -u origin main
     ```

2. **Conecte na Cloudflare Pages:**
   - Acesse o painel gratuito em [dash.cloudflare.com](https://dash.cloudflare.com)
   - Vá em **Workers & Pages** > **Create application** > **Pages** > **Connect to Git**.
   - Selecione seu repositório `portfolio`.
   - Em *Build settings*:
     - **Framework preset:** `None`
     - **Build command:** `python build.py`
     - **Build output directory:** `.` (raiz)
   - Clique em **Save and Deploy**.

Em cerca de 1 minuto seu site estará online com certificado SSL (HTTPS) gratuito, CDN global ultrarrápida e largura de banda ilimitada!

---

## 🏷️ Como adicionar seu Domínio Próprio no futuro
Quando você registrar um domínio (por exemplo, `viniciusdomingues.com.br` no Registro.br por ~R$ 40/ano):
1. No painel da Cloudflare Pages, clique em **Custom Domains**.
2. Digite seu domínio.
3. A Cloudflare configura o SSL e ativa seu site nele automaticamente, com mensalidade zero!
