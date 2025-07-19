const audio = new Audio();
let currentTrackIndex = -1; // Índice da música atual no array musicData
let musicData = []; // Array para armazenar os dados das músicas carregados do JSON
let filteredMusic = []; // Array para armazenar as músicas filtradas/pesquisadas

// Elementos do player
const playPauseBtn = document.getElementById('playPause');
const prevTrackBtn = document.getElementById('prevTrack');
const nextTrackBtn = document.getElementById('nextTrack');
const progressBar = document.getElementById('progress');
const currentSongDisplay = document.getElementById('currentSong');
const currentTimeDisplay = document.getElementById('currentTime');
const totalTimeDisplay = document.getElementById('totalTime');
const volumeSlider = document.getElementById('volume');
const volumeIconBtn = document.getElementById('volumeIcon');
const musicGrid = document.getElementById('todas-musicas');

// Base URL para links únicos
const appBaseUrl = window.location.origin + window.location.pathname;

// --- Funções de Utilitário ---

// Formata o tempo em segundos para MM:SS
function formatTime(seconds) {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = Math.floor(seconds % 60);
    const formattedSeconds = remainingSeconds < 10 ? '0' + remainingSeconds : remainingSeconds;
    return `${minutes}:${formattedSeconds}`;
}

// --- Funções de Carregamento de Dados ---

// Carrega os dados das músicas do arquivo JSON
async function fetchMusicData() {
    try {
        const response = await fetch('musicas.json');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        musicData = data.musicas; // Armazena os dados
        filteredMusic = [...musicData]; // Inicializa filteredMusic com todos os dados
        loadMusicListUI(); // Carrega a interface com os dados
        initPlayerControls(); // Inicializa os controles após carregar a UI
        console.log("Dados das músicas carregados com sucesso.");
    } catch (error) {
        console.error("Erro ao carregar dados das músicas:", error);
        musicGrid.innerHTML = '<p>Erro ao carregar as músicas. Tente novamente mais tarde.</p>';
    }
}

// Carrega a lista de músicas na interface (agora usa filteredMusic)
function loadMusicListUI() {
    musicGrid.innerHTML = ''; // Limpa o conteúdo existente

    if (!filteredMusic || filteredMusic.length === 0) {
         musicGrid.innerHTML = '<p>Nenhuma música disponível no momento.</p>';
         return;
    }

    filteredMusic.forEach((musica) => { // Itera sobre filteredMusic
        // Encontra o índice original da música no array musicData
        // Isso é crucial porque filteredMusic pode ter uma ordem ou subconjunto diferente
        const originalIndex = musicData.findIndex(m => m.arquivo === musica.arquivo);
        if (originalIndex === -1) {
            console.warn(`Música "${musica.titulo}" não encontrada no array original.`);
            return; // Pula se a música não for encontrada no array original
        }

        const musicItem = document.createElement('div');
        musicItem.className = 'music-item';
        // Usa o índice original no array como identificador
        musicItem.setAttribute('data-index', originalIndex);

        musicItem.innerHTML = `
            <div class="music-info">
                <div>
                    <h3>${musica.titulo}</h3>
                    <span class="genre">${musica.genero}</span>
                </div>
                <div class="music-actions">
                    <button class="share-music-btn" title="Copiar link" onclick="copyMusicLink(event, ${originalIndex})">
                        <i class="fas fa-link"></i>
                    </button>
                    <button class="download-btn" onclick="downloadTrack(event, '${musica.arquivo}')">
                        <i class="fas fa-download"></i>
                    </button>
                </div>
            </div>
        `;

        musicGrid.appendChild(musicItem);
    });

    // Certifica-se de que a música atualmente tocando (se houver) esteja destacada
    updatePlayingIndicator(currentTrackIndex);
}

// --- Funções para gerenciar links individuais ---

// Gera um link único para a música (usando hash)
function getMusicShareLink(index) {
    return `${appBaseUrl}#/musica/${index}`;
}

// Extrai o índice da música da URL (hash)
function getMusicIndexFromUrl() {
    const hash = window.location.hash;
    if (hash.startsWith('#/musica/')) {
        const index = parseInt(hash.split('/')[2]);
        // Verifica se o índice é válido em relação ao musicData completo
        if (!isNaN(index) && index >= 0 && index < musicData.length) {
            return index;
        }
    }
    return null;
}

// Atualiza a URL quando uma música é selecionada
function updateUrlForMusic(index) {
    const newUrl = getMusicShareLink(index);
    // Evita adicionar estados idênticos ao histórico do navegador
    if (window.location.hash !== newUrl.split('#')[1]) {
        window.history.pushState({}, '', newUrl);
    }
}

// Toca a música baseada na URL ao carregar a página
function playMusicFromUrl() {
    const index = getMusicIndexFromUrl();
    if (index !== null) {
        // Toca a música apenas se não for a mesma já tocando e se o player não estiver ativo
        // ou se for a mesma mas estiver pausada e a URL indica para tocar
        if (index !== currentTrackIndex || audio.paused) {
            playTrack(index);
        }
    }
}

// --- Funções de Controle do Player ---

// Toca uma música pelo índice
function playTrack(index) {
    // Valida o índice em relação ao musicData completo
    if (index < 0 || index >= musicData.length) {
        console.error("Índice de música inválido:", index);
        return;
    }

    currentTrackIndex = index;
    const musica = musicData[currentTrackIndex]; // Pega a música do array original

    audio.src = musica.arquivo; // Usa o caminho completo do JSON
    audio.play();

    currentSongDisplay.textContent = musica.titulo;
    updatePlayButton(true);
    updatePlayingIndicator(currentTrackIndex); // Destaca a música na lista
    updateUrlForMusic(index); // <-- Atualiza a URL aqui

    // Resetar e atualizar tempos e barra de progresso
    progressBar.value = 0;
    currentTimeDisplay.textContent = '0:00';
    totalTimeDisplay.textContent = '0:00'; // Será atualizado no 'loadedmetadata'

    console.log(`Tocando: ${musica.titulo}`);
}

// Alterna entre play e pause
function togglePlayPause() {
    if (audio.paused) {
        if (currentTrackIndex === -1 && musicData.length > 0) {
            // Se nada foi tocado ainda, toca a primeira música
            playTrack(0);
        } else if (currentTrackIndex !== -1) {
            // Se uma música estava pausada, continua tocando
            audio.play();
            updatePlayButton(true);
            updatePlayingIndicator(currentTrackIndex);
        }
    } else {
        audio.pause();
        updatePlayButton(false);
        updatePlayingIndicator(-1); // Remove destaque ao pausar
    }
}

// Atualiza o ícone do botão play/pause
function updatePlayButton(isPlaying) {
    const icon = playPauseBtn.querySelector('i');
    icon.className = isPlaying ? 'fas fa-pause' : 'fas fa-play';
}

// Vai para a próxima música
function nextTrack() {
    if (musicData.length === 0) return;

    let nextIndex = currentTrackIndex + 1;
    if (nextIndex >= musicData.length) {
        nextIndex = 0; // Volta para o início (loop)
    }

    playTrack(nextIndex);
}

// Vai para a música anterior
function prevTrack() {
    if (musicData.length === 0) return;

    let prevIndex = currentTrackIndex - 1;
    if (prevIndex < 0) {
        prevIndex = musicData.length - 1; // Volta para o fim (loop)
    }

    playTrack(prevIndex);
}

// Atualiza o indicador visual da música tocando na lista
function updatePlayingIndicator(playingIndex) {
    document.querySelectorAll('.music-item').forEach((item) => {
        const itemIndex = parseInt(item.getAttribute('data-index'));
        if (itemIndex === playingIndex) {
            item.classList.add('active'); // Adiciona uma classe 'active'
        } else {
            item.classList.remove('active'); // Remove a classe de outros itens
        }
    });
}

// --- Inicialização e Event Listeners ---

// Inicializa os controles do player e adiciona listeners
function initPlayerControls() {
    // Evento delegado para cliques nos itens da lista de músicas
    musicGrid.addEventListener('click', function(event) {
        const musicItem = event.target.closest('.music-item'); // Encontra o item clicado
        if (!musicItem) return; // Sai se não clicou em um item de música

        // Ignora cliques nos botões de ação dentro do item (download/share)
        if (event.target.closest('.download-btn') || event.target.closest('.share-music-btn')) {
             return;
        }

        const index = parseInt(musicItem.getAttribute('data-index'));

        if (index === currentTrackIndex && !audio.paused) {
            // Se a mesma música estiver tocando, pausa
            togglePlayPause();
        } else if (index === currentTrackIndex && audio.paused) {
             // Se a mesma música estiver pausada, toca
            togglePlayPause();
        }
        else {
            // Toca uma nova música
            playTrack(index);
        }
    });

    // Botões do player fixo
    playPauseBtn.addEventListener('click', togglePlayPause);
    prevTrackBtn.addEventListener('click', prevTrack);
    nextTrackBtn.addEventListener('click', nextTrack);

    // Barra de progresso
    audio.addEventListener('timeupdate', () => {
        const { currentTime, duration } = audio;
        progressBar.value = (currentTime / duration) * 100 || 0;
        currentTimeDisplay.textContent = formatTime(currentTime);
    });

    // Atualiza a barra de progresso e o tempo total quando a metadata é carregada
    audio.addEventListener('loadedmetadata', () => {
         totalTimeDisplay.textContent = formatTime(audio.duration);
         progressBar.max = 100; // Garante que o max é 100 para o cálculo de %
    });


    progressBar.addEventListener('input', () => {
        const seekTime = (progressBar.value / 100) * audio.duration;
        audio.currentTime = seekTime;
    });

    // Quando a música termina
    audio.addEventListener('ended', () => {
        console.log("Música terminou. Tocando próxima...");
        nextTrack(); // Toca a próxima música automaticamente
    });

    // Controle de Volume
    volumeSlider.addEventListener('input', () => {
        // Converte o valor do slider (0-100) para o volume do áudio (0.0-1.0)
        audio.volume = volumeSlider.value / 100;
        updateVolumeIcon();
    });

    // Inicializa o volume do áudio com o valor do slider
    audio.volume = volumeSlider.value / 100;
    updateVolumeIcon(); // Define o ícone inicial do volume

    // Opcional: Mute/Unmute ao clicar no ícone de volume
    volumeIconBtn.addEventListener('click', () => {
        if (audio.volume > 0) {
            audio.muted = true; // Muta o áudio
            volumeSlider.setAttribute('data-last-volume', volumeSlider.value); // Salva o volume anterior
            volumeSlider.value = 0; // Move o slider para 0
        } else {
            audio.muted = false; // Desmuta
             // Restaura para o último volume não zero, ou um padrão (ex: 50)
            const lastVolume = volumeSlider.getAttribute('data-last-volume') || 50;
            volumeSlider.value = lastVolume;
            audio.volume = lastVolume / 100;
        }
        updateVolumeIcon();
    });

    // Atualiza o ícone do volume com base no estado/valor
    function updateVolumeIcon() {
        const icon = volumeIconBtn.querySelector('i');
        if (audio.muted || audio.volume === 0) {
            icon.className = 'fas fa-volume-mute';
        } else if (audio.volume < 0.5) {
            icon.className = 'fas fa-volume-down';
        } else {
            icon.className = 'fas fa-volume-up';
        }
    }

    // Botão de Compartilhar (global para a música atual)
    const shareBtn = document.getElementById('share');
    if (navigator.share) { // Verifica se a Web Share API é suportada
        shareBtn.style.display = 'inline-block'; // Mostra o botão se suportado
        shareBtn.addEventListener('click', async () => {
            if (currentTrackIndex === -1) {
                alert("Selecione uma música para compartilhar.");
                return;
            }
            try {
                const musica = musicData[currentTrackIndex];
                await navigator.share({
                    title: `Ouça: ${musica.titulo} - Guilherme`,
                    text: `Confira essa música de Guilherme!`,
                    url: getMusicShareLink(currentTrackIndex) // Usa o link único
                });
                console.log('Conteúdo compartilhado com sucesso!');
            } catch (error) {
                console.error('Erro ao compartilhar:', error);
            }
        });
    } else {
         shareBtn.style.display = 'inline-block'; // Garante que o botão seja visível para o fallback
         console.log("Web Share API não suportada neste navegador. Usando fallback de cópia.");
         // Fallback: Copiar para área de transferência para o botão de compartilhamento global
         shareBtn.addEventListener('click', () => {
             if (currentTrackIndex === -1) {
                 alert("Selecione uma música para compartilhar.");
                 return;
             }
             navigator.clipboard.writeText(getMusicShareLink(currentTrackIndex))
                 .then(() => alert('Link da música atual copiado para a área de transferência! Cole e compartilhe.'))
                 .catch(() => alert('Não foi possível copiar o link da música atual. Seu navegador pode não suportar esta funcionalidade.'));
         });
    }


    // Listener para quando o áudio estiver carregando (opcional, para feedback visual)
    audio.addEventListener('waiting', () => {
        // Pode adicionar uma classe 'loading' ao player ou item ativo
        console.log("Carregando áudio...");
    });
    audio.addEventListener('playing', () => {
        // Remove a classe 'loading'
        console.log("Áudio tocando.");
    });
     audio.addEventListener('error', (e) => {
        console.error("Erro de áudio:", e);
        currentSongDisplay.textContent = "Erro ao carregar a música";
        updatePlayButton(false);
        updatePlayingIndicator(-1);
        // Pode mostrar uma mensagem de erro mais amigável na UI
    });
}

// Função de download
function downloadTrack(event, filepath) {
    event.stopPropagation(); // Impede que o clique no botão de download toque a música
    const link = document.createElement('a');
    link.href = filepath; // Usa o caminho completo do JSON
    // Extrai o nome do arquivo do caminho para o nome do download
    link.download = filepath.split('/').pop();
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    console.log(`Download iniciado para: ${filepath}`);
}

// Função para copiar link da música (para botões individuais na lista)
function copyMusicLink(event, index) {
    event.stopPropagation(); // Impede que o clique no botão de copiar toque a música
    navigator.clipboard.writeText(getMusicShareLink(index))
        .then(() => {
            // Feedback visual: Muda o ícone para um 'check' temporariamente
            const btn = event.target.closest('button');
            if (btn) { // Garante que o botão foi encontrado
                const originalIcon = btn.innerHTML; // Salva o HTML original (o ícone)
                btn.innerHTML = '<i class="fas fa-check"></i>';
                setTimeout(() => {
                    btn.innerHTML = originalIcon; // Restaura o ícone original
                }, 2000);
            }
        })
        .catch(() => alert('Não foi possível copiar o link. Seu navegador pode não suportar esta funcionalidade ou a permissão não foi concedida.'));
}


// Placeholder para setupSearchAndFilters
function setupSearchAndFilters() {
    // Esta função será responsável por lidar com a busca e filtros.
    // Quando implementada, ela modificará o array `filteredMusic` e então chamará `loadMusicListUI()`
    // para atualizar a exibição da lista.
    console.log("Configurando busca e filtros (placeholder).");
    // Exemplo básico de como um filtro poderia funcionar:
    // const searchInput = document.getElementById('searchInput');
    // searchInput.addEventListener('input', (e) => {
    //     const searchTerm = e.target.value.toLowerCase();
    //     filteredMusic = musicData.filter(musica =>
    //         musica.titulo.toLowerCase().includes(searchTerm) ||
    //         musica.genero.toLowerCase().includes(searchTerm)
    //     );
    //     loadMusicListUI(); // Recarrega a UI com as músicas filtradas
    // });
}


// Inicia tudo quando o DOM carregar
document.addEventListener('DOMContentLoaded', () => {
    fetchMusicData(); // Começa carregando os dados do JSON
    setupSearchAndFilters(); // Chama a função para configurar busca e filtros (mesmo que seja um placeholder por enquanto)

    // Verifica a URL ao carregar e quando o hash muda
    // Usamos 'load' para garantir que musicData esteja carregado antes de tentar tocar
    window.addEventListener('load', playMusicFromUrl);
    window.addEventListener('hashchange', playMusicFromUrl);
});

// Opcional: Registrar Service Worker para PWA (requer um arquivo sw.js)
// if ('serviceWorker' in navigator) {
//   window.addEventListener('load', () => {
//     navigator.serviceWorker.register('/sw.js')
//       .then(registration => {
//         console.log('SW registrado: ', registration);
//       })
//       .catch(registrationError => {
//         console.log('SW falhou: ', registrationError);
//       });
//   });
// }
