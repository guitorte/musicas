document.addEventListener('DOMContentLoaded', () => {
    
    // ---AS VARIÁVEIS E ESTADO GLOBAL ---
    const appContent = document.getElementById('app-content');
    const themeToggle = document.getElementById('theme-toggle');
    const sunIcon = document.querySelector('.icon-sun');
    const moonIcon = document.querySelector('.icon-moon');
    let bibleData = [];
    let fuse;

    // --- INICIALIZAÇÃO ---
    async function init() {
        // 1. Tema
        setupTheme();
        
        // 2. Carregar dados
        try {
            const response = await fetch('bible.json');
            if (!response.ok) throw new Error('Network response was not ok');
            bibleData = await response.json();
        } catch (error) {
            appContent.innerHTML = `<p>Erro ao carregar os dados. Por favor, tente novamente.</p>`;
            console.error('Fetch error:', error);
            return;
        }

        // 3. Configurar busca
        const fuseOptions = {
            keys: ['Nome', 'Categoria', 'ProblemaQueResolve'],
            includeScore: true,
            threshold: 0.4,
        };
        fuse = new Fuse(bibleData, fuseOptions);

        // 4. Roteamento
        window.addEventListener('hashchange', router);
        router();
    }

    // --- TEMA (DARK/LIGHT MODE) ---
    function setupTheme() {
        const savedTheme = localStorage.getItem('theme') || 'light';
        document.documentElement.setAttribute('data-theme', savedTheme);
        updateThemeIcons(savedTheme);

        themeToggle.addEventListener('click', () => {
            let currentTheme = document.documentElement.getAttribute('data-theme');
            let newTheme = currentTheme === 'light' ? 'dark' : 'light';
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            updateThemeIcons(newTheme);
        });
    }
    
    function updateThemeIcons(theme) {
        if (theme === 'dark') {
            sunIcon.style.display = 'none';
            moonIcon.style.display = 'inline';
        } else {
            sunIcon.style.display = 'inline';
            moonIcon.style.display = 'none';
        }
    }

    // --- ROTEADOR ---
    function router() {
        const hash = window.location.hash.substring(1);
        const params = new URLSearchParams(hash);
        
        if (params.has('id')) {
            renderDetail(params.get('id'));
        } else if (params.has('categoria')) {
            renderListByCategory(params.get('categoria'));
        } else if (params.has('problema')) {
            renderListByProblem(params.get('problema'));
        } else {
            renderHome();
        }
    }

    // --- RENDERIZAÇÃO DE PÁGINAS ---

    // Home / Painel
    function renderHome() {
        const allProblems = [...new Set(bibleData.flatMap(item => item.ProblemaQueResolve))];
        const allCategories = [...new Set(bibleData.map(item => item.Categoria))];

        appContent.innerHTML = `
            <input type="text" id="search-bar" placeholder="Buscar por técnica ou problema...">
            
            <h2 class="section-title">Apagar Incêndios</h2>
            <ul class="tag-list">
                ${allProblems.map(p => `<li><a href="#problema=${encodeURIComponent(p)}">${p}</a></li>`).join('')}
            </ul>

            <h2 class="section-title">Explorar Módulos</h2>
            <ul class="module-list">
                 ${allCategories.map(c => `<li><a href="#categoria=${encodeURIComponent(c)}">${c}</a></li>`).join('')}
            </ul>
        `;
        document.getElementById('search-bar').addEventListener('input', handleSearch);
    }
    
    // Lista (Resultados de Busca/Categoria)
    function renderList(items, title) {
        appContent.innerHTML = `
            <a href="#">&larr; Voltar ao início</a>
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

    // Detalhe da Técnica
    function renderDetail(id) {
        const item = bibleData.find(d => d.ID === id);
        if (!item) {
            window.location.hash = ''; // Volta para home se ID não existe
            return;
        }

        const connectionsHTML = item.Conexoes && item.Conexoes.length > 0 ?
            `<div class="detail-section">
                <h3>Veja Também</h3>
                <ul class="connections-list">
                    ${item.Conexoes.map(connId => {
                        const connItem = bibleData.find(d => d.ID === connId);
                        return connItem ? `<li><a href="#id=${connItem.ID}">${connItem.Nome}</a></li>` : '';
                    }).join('')}
                </ul>
            </div>` : '';

        appContent.innerHTML = `
            <a href="#">&larr; Voltar ao início</a>
            <article class="detail-view">
                <div class="detail-header">
                    <h2>${item.Nome}</h2>
                    <span class="category">${item.Categoria}</span>
                </div>
                
                <div class="detail-section">
                    <h3>Para que serve?</h3>
                    <ul>
                        ${item.ProblemaQueResolve.map(p => `<li>${p}</li>`).join('')}
                    </ul>
                </div>
                
                <div class="detail-section">
                    <h3>A Mecânica</h3>
                    <p><strong>Função:</strong> ${item.Mecanica.Funcao}</p>
                    <p><strong>Mecanismo:</strong> ${item.Mecanica.Mecanismo}</p>
                    <p><strong>Instrução:</strong> ${item.Mecanica.InstrucaoPrescritiva}</p>
                </div>
                
                <div class="detail-section">
                    <h3>A Aplicação</h3>
                    <p>${item.Aplicacao.Analise}</p>
                    ${item.Aplicacao.Exemplos.map(ex => `
                        <div class="example-block">
                            <button class="copy-button" aria-label="Copiar exemplo">Copiar</button>
                            <div class="example-block-title">${ex.Titulo}</div>
                            <pre>${ex.Verso}</pre>
                            <p><em>${ex.Observacao}</em></p>
                        </div>
                    `).join('')}
                </div>

                <div class="detail-section">
                    <h3>Ponto de Atenção</h3>
                    <ul>
                        <li><strong>Risco:</strong> ${item.PontoDeAtencao.Risco}</li>
                        <li><strong>Combinação:</strong> ${item.PontoDeAtencao.Combinacao}</li>
                        <li><strong>Contexto:</strong> ${item.PontoDeAtencao.Contexto}</li>
                    </ul>
                </div>

                ${connectionsHTML}
            </article>
        `;
        
        // Adicionar funcionalidade aos botões de copiar
        document.querySelectorAll('.copy-button').forEach(button => {
            button.addEventListener('click', (e) => {
                const pre = e.target.closest('.example-block').querySelector('pre');
                navigator.clipboard.writeText(pre.innerText).then(() => {
                    e.target.innerText = 'Copiado!';
                    setTimeout(() => { e.target.innerText = 'Copiar'; }, 2000);
                });
            });
        });
    }

    // --- MANIPULADORES DE EVENTOS ---
    function handleSearch(event) {
        const query = event.target.value;
        if (query.length < 2) {
            // Se a busca for curta, limpa os resultados
            if (document.querySelector('.technique-list')) renderHome();
            return;
        }
        const results = fuse.search(query).map(result => result.item);
        renderList(results, `Resultados para "${query}"`);
    }

    // --- INICIA O APLICATIVO ---
    init();
});
