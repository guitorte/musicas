// --- Global Variables ---
const audio = new Audio();
let currentTrackIndex = -1; // Index in the original full musicData array
let musicData = []; // Will hold all songs from the JSON
let playlists = {}; // Will hold the predefined playlists from the JSON

// --- DOM Element References ---
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
const mainShareBtn = document.getElementById('share');

// --- Utility Functions ---

/**
 * Formats time in seconds to a "MM:SS" string.
 * @param {number} seconds - The time in seconds.
 * @returns {string} The formatted time string.
 */
function formatTime(seconds) {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = Math.floor(seconds % 60);
    const formattedSeconds = remainingSeconds < 10 ? '0' + remainingSeconds : remainingSeconds;
    return `${minutes}:${formattedSeconds}`;
}

// --- Core Logic: Data Fetching and Filtering ---

/**
 * Fetches music data from the JSON file and initializes the player.
 */
async function fetchMusicData() {
    try {
        const response = await fetch('musicas.json');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        musicData = data.musicas;
        playlists = data.playlists || {}; // Load playlists, default to empty object

        applyFilterFromURL(); // Filter songs based on URL parameters
        initPlayerControls(); // Set up all event listeners for the player

        console.log("Dados das músicas carregados com sucesso.");
    } catch (error) {
        console.error("Erro ao carregar dados das músicas:", error);
        musicGrid.innerHTML = '<p>Erro ao carregar as músicas. Tente novamente mais tarde.</p>';
    }
}

/**
 * Reads URL parameters and filters the music list to be displayed.
 * Also checks for a song to autoplay.
 */
function applyFilterFromURL() {
    const params = new URLSearchParams(window.location.search);
    const genre = params.get('genre');
    const tag = params.get('tag');
    const playlist = params.get('playlist');
    const songToPlay = params.get('play');

    let filteredMusic = musicData; // Default to showing all songs

    if (genre) {
        filteredMusic = musicData.filter(song => song.genero.toLowerCase().includes(genre.toLowerCase()));
        console.log(`Filtrando por gênero: ${genre}`);
    } else if (tag) {
        filteredMusic = musicData.filter(song => song.tags && song.tags.some(t => t.toLowerCase() === tag.toLowerCase()));
        console.log(`Filtrando por tag: ${tag}`);
    } else if (playlist && playlists[playlist]) {
        const playlistTitles = playlists[playlist];
        filteredMusic = musicData.filter(song => playlistTitles.includes(song.titulo));
        console.log(`Carregando playlist: ${playlist}`);
    }

    loadMusicListUI(filteredMusic);

    // If a 'play' parameter exists, find and play that song
    if (songToPlay) {
        const songIndex = musicData.findIndex(song => song.titulo === songToPlay);
        if (songIndex !== -1) {
            // A short delay can help ensure the audio context is ready
            setTimeout(() => playTrack(songIndex), 100);
        }
    }
}

/**
 * Renders the provided list of songs into the HTML grid.
 * @param {Array} songsToDisplay - The array of song objects to show.
 */
function loadMusicListUI(songsToDisplay) {
    musicGrid.innerHTML = '';

    if (!songsToDisplay || songsToDisplay.length === 0) {
        musicGrid.innerHTML = '<p>Nenhuma música encontrada para esta seleção.</p>';
        return;
    }

    songsToDisplay.forEach((musica) => {
        const originalIndex = musicData.findIndex(item => item.arquivo === musica.arquivo);
        if (originalIndex === -1) return;

        const musicItem = document.createElement('div');
        musicItem.className = 'music-item';
        musicItem.setAttribute('data-index', originalIndex);

        // Note the updated innerHTML to match your new CSS classes
        musicItem.innerHTML = `
            <div class="music-info">
                <div>
                    <h3>${musica.titulo}</h3>
                    <span class="genre">${musica.genero}</span>
                </div>
                <div class="music-actions">
                    <button class="share-music-btn" title="Copiar link da música" onclick="shareSingleTrackLink(event, '${musica.titulo}')">
                        <i class="fas fa-link"></i>
                    </button>
                    <button class="download-btn" title="Baixar música" onclick="downloadTrack(event, '${musica.arquivo}')">
                        <i class="fas fa-download"></i>
                    </button>
                </div>
            </div>`;
        musicGrid.appendChild(musicItem);
    });
}

// --- Player Control Functions ---

function playTrack(index) {
    if (index < 0 || index >= musicData.length) return;
    currentTrackIndex = index;
    const musica = musicData[currentTrackIndex];
    audio.src = musica.arquivo;
    audio.play();
    currentSongDisplay.textContent = musica.titulo;
    updatePlayButton(true);
    updatePlayingIndicator(currentTrackIndex);
    progressBar.value = 0;
    currentTimeDisplay.textContent = '0:00';
    totalTimeDisplay.textContent = '...'; // Placeholder until metadata loads
}

function togglePlayPause() {
    if (audio.paused) {
        if (currentTrackIndex === -1) {
            const firstItem = musicGrid.querySelector('.music-item');
            if (firstItem) playTrack(parseInt(firstItem.dataset.index));
        } else {
            audio.play();
        }
    } else {
        audio.pause();
    }
    updatePlayButton(!audio.paused);
}

function updatePlayButton(isPlaying) {
    const icon = playPauseBtn.querySelector('i');
    icon.className = isPlaying ? 'fas fa-pause' : 'fas fa-play';
    updatePlayingIndicator(isPlaying ? currentTrackIndex : -1);
}

function nextTrack() {
    const displayedItems = Array.from(musicGrid.querySelectorAll('.music-item'));
    if (displayedItems.length <= 1) return;
    const currentGridIndex = displayedItems.findIndex(item => parseInt(item.dataset.index) === currentTrackIndex);
    const nextGridIndex = (currentGridIndex + 1) % displayedItems.length;
    playTrack(parseInt(displayedItems[nextGridIndex].dataset.index));
}

function prevTrack() {
    const displayedItems = Array.from(musicGrid.querySelectorAll('.music-item'));
    if (displayedItems.length <= 1) return;
    const currentGridIndex = displayedItems.findIndex(item => parseInt(item.dataset.index) === currentTrackIndex);
    const prevGridIndex = (currentGridIndex - 1 + displayedItems.length) % displayedItems.length;
    playTrack(parseInt(displayedItems[prevGridIndex].dataset.index));
}

function updatePlayingIndicator(playingIndex) {
    document.querySelectorAll('.music-item').forEach(item => {
        item.classList.toggle('active', parseInt(item.dataset.index) === playingIndex);
    });
}

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

// --- Event Handlers and Initialization ---

function initPlayerControls() {
    musicGrid.addEventListener('click', (event) => {
        const musicItem = event.target.closest('.music-item');
        if (!musicItem || event.target.closest('.music-actions')) return;
        const index = parseInt(musicItem.dataset.index);
        if (index === currentTrackIndex) togglePlayPause();
        else playTrack(index);
    });

    playPauseBtn.addEventListener('click', togglePlayPause);
    prevTrackBtn.addEventListener('click', prevTrack);
    nextTrackBtn.addEventListener('click', nextTrack);

    audio.addEventListener('play', () => updatePlayButton(true));
    audio.addEventListener('pause', () => updatePlayButton(false));
    audio.addEventListener('ended', nextTrack);
    audio.addEventListener('timeupdate', () => {
        if (!isNaN(audio.duration)) {
            progressBar.value = (audio.currentTime / audio.duration) * 100 || 0;
            currentTimeDisplay.textContent = formatTime(audio.currentTime);
        }
    });
    audio.addEventListener('loadedmetadata', () => {
        totalTimeDisplay.textContent = formatTime(audio.duration);
    });
    audio.addEventListener('error', () => {
        currentSongDisplay.textContent = "Erro ao carregar música";
        updatePlayButton(false);
    });

    progressBar.addEventListener('input', () => {
        if (!isNaN(audio.duration)) audio.currentTime = (progressBar.value / 100) * audio.duration;
    });

    volumeSlider.addEventListener('input', () => {
        audio.muted = false;
        audio.volume = volumeSlider.value / 100;
    });
    volumeIconBtn.addEventListener('click', () => {
        audio.muted = !audio.muted;
    });
    audio.addEventListener('volumechange', () => {
        if (!audio.muted) volumeSlider.value = audio.volume * 100;
        updateVolumeIcon();
    });

    // Initialize volume
    audio.volume = volumeSlider.value / 100;
    updateVolumeIcon();
    
    // Main Share Button (Web Share API)
    if (navigator.share) {
        mainShareBtn.addEventListener('click', async () => {
            if (currentTrackIndex === -1) {
                alert("Selecione uma música para compartilhar.");
                return;
            }
            const musica = musicData[currentTrackIndex];
            try {
                await navigator.share({
                    title: `Ouvindo: ${musica.titulo} - Guilherme`,
                    text: `Ouça "${musica.titulo}" de Guilherme!`,
                    url: window.location.href,
                });
            } catch (error) {
                console.error('Erro ao compartilhar:', error);
            }
        });
    } else {
        mainShareBtn.style.display = 'none';
    }
}

/**
 * Copies a direct link to a specific song to the clipboard.
 * @param {Event} event - The click event.
 * @param {string} songTitle - The title of the song to share.
 */
function shareSingleTrackLink(event, songTitle) {
    event.stopPropagation();
    const url = new URL(window.location);
    url.search = `?play=${encodeURIComponent(songTitle)}`;
    
    navigator.clipboard.writeText(url.href).then(() => {
        const button = event.currentTarget;
        const icon = button.querySelector('i');
        const originalIconClass = icon.className;
        
        // Visual feedback
        icon.className = 'fas fa-check';
        button.style.color = '#4CAF50'; // Green success color
        
        setTimeout(() => {
            icon.className = originalIconClass;
            button.style.color = ''; // Revert to original color
        }, 2000);
    }).catch(err => {
        console.error('Falha ao copiar o link:', err);
        alert('Não foi possível copiar o link.');
    });
}

/**
 * Handles the download button click.
 * @param {Event} event - The click event.
 * @param {string} filepath - The path to the audio file.
 */
function downloadTrack(event, filepath) {
    event.stopPropagation();
    const link = document.createElement('a');
    link.href = filepath;
    link.download = filepath.split('/').pop();
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// --- App Entry Point ---
document.addEventListener('DOMContentLoaded', fetchMusicData);
