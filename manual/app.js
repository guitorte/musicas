document.addEventListener('DOMContentLoaded', () => {

    // --- ELEMENTOS DO DOM E ESTADO ---
    const tocContainer = document.getElementById('table-of-contents');
    const contentContainer = document.getElementById('content-container');
    const menuToggle = document.getElementById('menu-toggle');
    const sidebar = document.getElementById('sidebar-nav');
    const themeToggle = document.getElementById('theme-toggle');

    const indexStructure = [
        { title: "Parte I: Vogais e Consoantes", categories: ["Engenharia Sônica"] },
        { title: "Parte II: Recursos de Linguagem", categories: ["Mecânica do Verso"] },
        { title: "Parte III: Arquitetura dos Blocos", categories: ["Arquitetura da Canção"] },
        { title: "Parte IV: Análises e Ferramentas", categories: ["Laboratório Criativo", "Análise Comparativa", "Métricas e Visualizações", "Desconstrução de Clássicos"] }
    ];

    // --- INICIALIZAÇÃO ---
    async function init() {
        setupTheme();
        setupMobileMenu();
        
        try {
            const response = await fetch('bible.json');
            if (!response.ok) throw new Error('Falha ao carregar dados.');
            const bibleData = await response.json();
            
            buildTableOfContents(bibleData);
            renderFullContent(bibleData);

        } catch (error) {
            contentContainer.innerHTML = `<p><strong>Erro:</strong> ${error.message}</p>`;
            console.error(error);
        }
    }

    // --- CONSTRUÇÃO DA INTERFACE ---
    function buildTableOfContents(data) {
        let tocHTML = '<ul>';
        indexStructure.forEach(part => {
            tocHTML += `<li><a href="#part-${slugify(part.title)}">${part.title}</a><ul>`;
            part.categories.forEach(category => {
                const items = data.filter(item => item.Categoria === category);
                items.forEach(item => {
                    tocHTML += `<li><a href="#${item.ID}">${item.ID}: ${item.Nome}</a></li>`;
                });
            });
            tocHTML += '</ul></li>';
        });
        tocHTML += '</ul>';
        tocContainer.innerHTML = tocHTML;
        
        // Adiciona evento de clique para fechar menu no mobile
        tocContainer.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                sidebar.classList.remove('open');
            });
        });
    }

    function renderFullContent(data) {
        let contentHTML = '';
        indexStructure.forEach(part => {
            contentHTML += `<section id="part-${slugify(part.title)}"><h2>${part.title}</h2>`;
            part.categories.forEach(category => {
                const items = data.filter(item => item.Categoria === category);
                items.forEach(item => {
                    const connectionsHTML = item.Conexoes && item.Conexoes.length > 0 ?
                        `<h4>Veja Também:</h4>
                        <ul>${item.Conexoes.map(connId => {
                            const connItem = data.find(d => d.ID === connId);
                            return connItem ? `<li><a href="#${connItem.ID}">${connItem.Nome}</a></li>` : '';
                        }).join('')}</ul>` : '';

                    contentHTML += `
                        <article id="${item.ID}">
                            <h3>${item.Nome} (${item.ID})</h3>
                            <h4>Para que serve?</h4>
                            <ul>${item.ProblemaQueResolve.map(p => `<li>${p}</li>`).join('')}</ul>
                            
                            <h4>A Mecânica</h4>
                            <p><strong>Função:</strong> ${item.Mecanica.Funcao}</p>
                            <p><strong>Mecanismo:</strong> ${item.Mecanica.Mecanismo}</p>
                            <p><strong>Instrução:</strong> ${item.Mecanica.InstrucaoPrescritiva}</p>
                            
                            <h4>A Aplicação</h4>
                            <p>${item.Aplicacao.Analise}</p>
                            ${item.Aplicacao.Exemplos.map(ex => `
                                <div class="example-block">
                                    <div class="example-block-title">${ex.Titulo}</div>
                                    <pre><code>${ex.Verso}</code></pre>
                                    <p><em>${ex.Observacao}</em></p>
                                </div>
                            `).join('')}
                            
                            <h4>Ponto de Atenção</h4>
                            <ul>
                                ${item.PontoDeAtencao.Risco ? `<li><strong>Risco:</strong> ${item.PontoDeAtencao.Risco}</li>` : ''}
                                ${item.PontoDeAtencao.Combinacao ? `<li><strong>Combinação:</strong> ${item.PontoDeAtencao.Combinacao}</li>` : ''}
                                ${item.PontoDeAtencao.Contexto ? `<li><strong>Contexto:</strong> ${item.PontoDeAtencao.Contexto}</li>` : ''}
                            </ul>
                            ${connectionsHTML}
                        </article>`;
                });
            });
            contentHTML += '</section>';
        });
        contentContainer.innerHTML = contentHTML;
    }

    // --- UTILITÁRIOS ---
    function slugify(text) {
        return text.toString().toLowerCase()
            .replace(/\s+/g, '-')
            .replace(/[^\w\-]+/g, '')
            .replace(/\-\-+/g, '-')
            .replace(/^-+/, '')
            .replace(/-+$/, '');
    }

    function setupMobileMenu() {
        menuToggle.addEventListener('click', () => {
            sidebar.classList.toggle('open');
        });
    }

    // Lógica de tema (idêntica à versão anterior)
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
        const sunIcon = themeToggle.querySelector('.icon-sun');
        const moonIcon = themeToggle.querySelector('.icon-moon');
        sunIcon.style.display = theme === 'light' ? 'block' : 'none';
        moonIcon.style.display = theme === 'dark' ? 'block' : 'none';
    }

    // --- INICIA O APLICATIVO ---
    init();
});
