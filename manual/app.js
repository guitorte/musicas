document.addEventListener('DOMContentLoaded', () => {

    // --- ELEMENTOS DO DOM E ESTADO GLOBAL ---
    const appContent = document.getElementById('app-content');
    const themeToggle = document.getElementById('theme-toggle');
    const sunIcon = document.querySelector('.icon-sun');
    const moonIcon = document.querySelector('.icon-moon');
    let bibleData = [];
    let fuse;

    // --- INICIALIZAÇÃO DO APLICATIVO ---
    async function init() {
        setupTheme();
        try {
            const response = await fetch('bible.json');
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            bibleData = await response.json();
        } catch (error) {
            renderError('Falha ao carregar o banco de dados. Verifique o console para mais detalhes.');
            console.error('Erro ao carregar bible.json:', error);
            return;
        }

        const fuseOptions = {
            keys: ['Nome', 'Categoria', 'ProblemaQueResolve', 'Mecanica.Funcao'],
            includeScore: true,
            threshold: 0.3,
            minMatchCharLength: 2,
        };
        fuse = new Fuse(bibleData, fuseOptions);

        window.addEventListener('hashchange', router);
        router(); // Roda o roteador na carga inicial
    }

    // --- GERENCIAMENTO DE TEMA (DARK/LIGHT) ---
    function setupTheme() {
        const savedTheme = localStorage.getItem('theme') || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
        document.documentElement.setAttribute('data-theme', savedTheme);
        updateThemeIcons(savedTheme);

        themeToggle.addEventListener('click', () => {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'light' ? 'dark' : 'light';
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            updateThemeIcons(newTheme);
            themeToggle.setAttribute('aria-label', `Alternar para tema ${currentTheme}`);
        });
    }

    function updateThemeIcons(theme) {
        sunIcon.style.display = theme === 'light' ? 'block' : 'none';
        moonIcon.style.display = theme === 'dark' ? 'block' : 'none';
    }
    
    // --- ROTEADOR PRINCIPAL ---
    function router() {
        const hash = window.location.hash.substring(1);
        const params = new URLSearchParams(hash);
        
        window.scrollTo(0, 0); // Rola para o topo a cada mudança de rota

        if (params.has('id')) {
            renderDetail(params.get('id'));
        } else if (params.has('categoria')) {
            renderListByCategory(decodeURIComponent(params.get('categoria')));
        } else if (params.has('problema')) {
            renderListByProblem(decodeURIComponent(params.get('problema')));
        } else if (params.has('busca')) {
            handleSearch(decodeURIComponent(params.get('busca')));
        } else {
            renderHome();
        }
    }

    // --- FUNÇÕES DE RENDERIZAÇÃO ---

    function renderError(message) {
        appContent.innerHTML = `<div class="error-message">${message}</div>`;
    }

    // TELA INICIAL
    function renderHome() {
        const allProblems = [...new Set(bibleData.flatMap(item => item.ProblemaQueResolve))].sort();
        const allCategories = [...new Set(bibleData.map(item => item.Categoria))].sort();

        appContent.innerHTML = `
            <div id="search-container">
                <input type="text" id="search-bar" placeholder="Buscar por técnica ou problema..." aria-label="Buscar">
            </div>
            
            <h2 class="section-title">Apagar Incêndios (Problemas)</h2>
            <ul class="tag-list">
                ${allProblems.map(p => `<li><a href="#problema=${encodeURIComponent(p)}">${p}</a></li>`).join('')}
            </ul>

            <h2 class="section-title">Explorar Módulos</h2>
            <ul class="module-list">
                 ${allCategories.map(c => `<li><a href="#categoria=${encodeURIComponent(c)}">${c}</a></li>`).join('')}
            </ul>
        `;
        document.getElementById('search-bar').addEventListener('input', (e) => {
            const query = e.target.value;
            // Atualiza a URL sem recarregar a página para busca em tempo real
            if (query.length > 1) {
                history.replaceState(null, '', `#busca=${encodeURIComponent(query)}`);
                handleSearch(query);
            } else if (query.length === 0) {
                history.replaceState(null, '', '#');
                renderHome(); // Volta para a home se a busca for limpa
            }
        });
    }

    // TELA DE LISTA DE RESULTADOS
    function renderList(items, title) {
        appContent.innerHTML = `
            <a href="#" class="back-link">&larr; Voltar ao início</a>
            <h2 class="section-title" style="margin-top: 16px;">${title}</h2>
            <div class="technique-list">
                ${items.length ? items.map(item => `
                    <a href="#id=${item.ID}">
                        <div class="technique-card-id">${item.ID}</div>
                        <div class="technique-card-name">${item.Nome}</div>
                        <span class="technique-card-category">${item.Categoria}</span>
                    </a>
                `).join('') : '<p>Nenhum resultado encontrado.</p>'}
            </div>
        `;
    }

    function renderListByCategory(category) {
        const items = bibleData.filter(item => item.Categoria === category);
        renderList(items, `Módulo: ${category}`);
    }
    
    function renderListByProblem(problem) {
        const items = bibleData.filter(item => item.ProblemaQueResolve.includes(problem));
        renderList(items, `Resolvendo: "${problem}"`);
    }

    // TELA DE DETALHE
    function renderDetail(id) {
        const item = bibleData.find(d => d.ID === id);
        if (!item) {
            window.location.hash = ''; return;
        }

        const connectionsHTML = item.Conexoes && item.Conexoes.length > 0 ?
            `<div class="detail-section">
                <h3>Veja Também</h3>
                <ul class="connections-list">
                    ${item.Conexoes.map(connId => {
                        const connItem = bibleData.find(d => d.ID === connId);
                        return connItem ? `<li><a href="#id=${connItem.ID}">${connItem.ID}: ${connItem.Nome}</a></li>` : '';
                    }).join('')}
                </ul>
            </div>` : '';

        appContent.innerHTML = `
            <a href="#" class="back-link">&larr; Voltar ao início</a>
            <article class="detail-view">
                <header class="detail-header">
                    <h2>${item.Nome}</h2>
                    <p class="category">${item.Categoria}</p>
                </header>
                
                <section class="detail-section">
                    <h3>Para que serve?</h3>
                    <ul>
                        ${item.ProblemaQueResolve.map(p => `<li>${p}</li>`).join('')}
                    </ul>
                </section>
                
                <section class="detail-section">
                    <h3>A Mecânica</h3>
                    <p><strong>Função:</strong> ${item.Mecanica.Funcao}</p>
                    <p><strong>Mecanismo:</strong> ${item.Mecanica.Mecanismo}</p>
                    <p><strong>Instrução:</strong> ${item.Mecanica.InstrucaoPrescritiva}</p>
                </section>
                
                <section class="detail-section">
                    <h3>A Aplicação</h3>
                    <p>${item.Aplicacao.Analise}</p>
                    ${item.Aplicacao.Exemplos.map(ex => `
                        <div class="example-block">
                            <button class="copy-button" aria-label="Copiar exemplo">Copiar</button>
                            <div class="example-block-title">${ex.Titulo}</div>
                            <pre><code>${ex.Verso}</code></pre>
                            <p><em>${ex.Observacao}</em></p>
                        </div>
                    `).join('')}
                </section>

                <section class="detail-section">
                    <h3>Ponto de Atenção</h3>
                    <ul>
                        ${item.PontoDeAtencao.Risco ? `<li><strong>Risco:</strong> ${item.PontoDeAtencao.Risco}</li>` : ''}
                        ${item.PontoDeAtencao.Combinacao ? `<li><strong>Combinação:</strong> ${item.PontoDeAtencao.Combinacao}</li>` : ''}
                        ${item.PontoDeAtencao.Contexto ? `<li><strong>Contexto:</strong> ${item.PontoDeAtencao.Contexto}</li>` : ''}
                    </ul>
                </section>

                ${connectionsHTML}
            </article>
        `;
        
        // Adicionar funcionalidade aos botões de copiar
        document.querySelectorAll('.copy-button').forEach(button => {
            button.addEventListener('click', (e) => {
                const pre = e.target.closest('.example-block').querySelector('pre code');
                navigator.clipboard.writeText(pre.innerText).then(() => {
                    e.target.innerText = 'Copiado!';
                    setTimeout(() => { e.target.innerText = 'Copiar'; }, 2000);
                });
            });
        });
    }

    // --- MANIPULADORES DE EVENTOS ---
    function handleSearch(query) {
        const results = fuse.search(query).map(result => result.item);
        const searchInput = document.getElementById('search-bar');
        
        // Se a tela de resultados ainda não estiver sendo exibida, renderiza
        if (!document.querySelector('.technique-list')) {
            renderList(results, `Resultados para "${query}"`);
            // E atualiza o valor do input, pois a tela foi redesenhada
            document.getElementById('search-bar').value = query;
            document.getElementById('search-bar').focus();
        } else { // Se já estiver, apenas atualiza a lista
            const listContainer = document.querySelector('.technique-list');
            const title = document.querySelector('.section-title');
            title.innerText = `Resultados para "${query}"`;
            listContainer.innerHTML = results.length ? results.map(item => `
                <a href="#id=${item.ID}">
                    <div class="technique-card-id">${item.ID}</div>
                    <div class="technique-card-name">${item.Nome}</div>
                    <span class="technique-card-category">${item.Categoria}</span>
                </a>
            `).join('') : '<p>Nenhum resultado encontrado.</p>';
        }
    }

    // --- INICIA O APLICATIVO ---
    init();
});
