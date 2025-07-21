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
        playlists = data.playlists || {}; // Load playlists, default to empty object if not found

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
 */
function applyFilterFromURL() {
    const params = new URLSearchParams(window.location.search);
    const genre = params.get('genre');
    const tag = params.get('tag');
    const playlist = params.get('playlist');

    let filteredMusic = musicData; // Default to showing all songs

    if (genre) {
        // Filter by a single genre (case-insensitive)
        filteredMusic = musicData.filter(song => song.genero.toLowerCase().includes(genre.toLowerCase()));
        console.log(`Filtrando por gênero: ${genre}`);
    } else if (tag) {
        // Filter by a single tag (case-insensitive)
        filteredMusic = musicData.filter(song => song.tags && song.tags.some(t => t.toLowerCase() === tag.toLowerCase()));
        console.log(`Filtrando por tag: ${tag}`);
    } else if (playlist && playlists[playlist]) {
        // Filter by a predefined playlist from the JSON
        const playlistTitles = playlists[playlist];
        filteredMusic = musicData.filter(song => playlistTitles.includes(song.titulo));
        console.log(`Carregando playlist: ${playlist}`);
    }

    loadMusicListUI(filteredMusic);
}

/**
 * Renders the provided list of songs into the HTML.
 * @param {Array} songsToDisplay - The array of song objects to show.
 */
function loadMusicListUI(songsToDisplay) {
    musicGrid.innerHTML = ''; // Clear any existing content

    if (!songsToDisplay || songsToDisplay.length === 0) {
         musicGrid.innerHTML = '<p>Nenhuma música encontrada para esta seleção.</p>';
         return;
    }

    songsToDisplay.forEach((musica) => {
        // Find the song's original index in the full musicData array.
        // This is crucial for the player to always know which file to play.
        const originalIndex = musicData.findIndex(item => item.arquivo === musica.arquivo);
        if (originalIndex === -1) return; // Skip if song not found in original data

        const musicItem = document.createElement('div');
        musicItem.className = 'music-item';
        musicItem.setAttribute('data-index', originalIndex);

        musicItem.innerHTML = `
            <div class="music-info">
                <div>
                    <h3>${musica.titulo}</h3>
                    <span class="genre">${musica.genero}</span>
                </div>
                <button class="download-btn" onclick="downloadTrack(event, '${musica.arquivo}')">
                    <i class="fas fa-download"></i>
                </button>
            </div>
        `;
        musicGrid.appendChild(musicItem);
    });
}

// --- Player Control Functions ---

/**
 * Plays a track based on its original index in the musicData array.
 * @param {number} index - The original index of the song.
 */
function playTrack(index) {
    if (index < 0 || index >= musicData.length) {
        console.error("Índice de música inválido:", index);
        return;
    }

    currentTrackIndex = index;
    const musica = musicData[currentTrackIndex];

    audio.src = musica.arquivo;
    audio.play();

    currentSongDisplay.textContent = musica.titulo;
    updatePlayButton(true);
    updatePlayingIndicator(currentTrackIndex);

    progressBar.value = 0;
    currentTimeDisplay.textContent = '0:00';
    totalTimeDisplay.textContent = '0:00'; // Will be updated on 'loadedmetadata'

    console.log(`Tocando: ${musica.titulo}`);
}

function togglePlayPause() {
    if (audio.paused) {
        if (currentTrackIndex === -1 && musicData.length > 0) {
            // If nothing has been played yet, play the first song from the *visible* list
            const firstVisibleItem = musicGrid.querySelector('.music-item');
            if (firstVisibleItem) {
                const firstIndex = parseInt(firstVisibleItem.getAttribute('data-index'));
                playTrack(firstIndex);
            }
        } else if (currentTrackIndex !== -1) {
            audio.play();
            updatePlayButton(true);
            updatePlayingIndicator(currentTrackIndex);
        }
    } else {
        audio.pause();
        updatePlayButton(false);
        updatePlayingIndicator(-1); // Remove highlight on pause
    }
}

function updatePlayButton(isPlaying) {
    const icon = playPauseBtn.querySelector('i');
    icon.className = isPlaying ? 'fas fa-pause' : 'fas fa-play';
}

/**
 * Plays the next track *in the currently visible list*.
 */
function nextTrack() {
    const displayedItems = Array.from(musicGrid.querySelectorAll('.music-item'));
    if (displayedItems.length === 0) return;

    const currentGridIndex = displayedItems.findIndex(item => parseInt(item.dataset.index) === currentTrackIndex);
    
    let nextGridIndex = (currentGridIndex === -1) ? 0 : currentGridIndex + 1;
    if (nextGridIndex >= displayedItems.length) {
        nextGridIndex = 0; // Loop to the start of the visible list
    }
    
    const nextOriginalIndex = parseInt(displayedItems[nextGridIndex].dataset.index);
    playTrack(nextOriginalIndex);
}

/**
 * Plays the previous track *in the currently visible list*.
 */
function prevTrack() {
    const displayedItems = Array.from(musicGrid.querySelectorAll('.music-item'));
    if (displayedItems.length === 0) return;

    const currentGridIndex = displayedItems.findIndex(item => parseInt(item.dataset.index) === currentTrackIndex);

    let prevGridIndex = (currentGridIndex === -1) ? 0 : currentGridIndex - 1;
    if (prevGridIndex < 0) {
        prevGridIndex = displayedItems.length - 1; // Loop to the end of the visible list
    }
    
    const prevOriginalIndex = parseInt(displayedItems[prevGridIndex].dataset.index);
    playTrack(prevOriginalIndex);
}

function updatePlayingIndicator(playingIndex) {
    document.querySelectorAll('.music-item').forEach((item) => {
        const itemIndex = parseInt(item.getAttribute('data-index'));
        if (itemIndex === playingIndex) {
            item.classList.add('active');
        } else {
            item.classList.remove('active');
        }
    });
}

// --- Initialization and Event Listeners ---

function initPlayerControls() {
    // Click listener for the song list
    musicGrid.addEventListener('click', function(event) {
        const musicItem = event.target.closest('.music-item');
        if (!musicItem || event.target.closest('.download-btn')) return;

        const index = parseInt(musicItem.getAttribute('data-index'));
        if (index === currentTrackIndex) {
            togglePlayPause(); // If clicking the same song, toggle play/pause
        } else {
            playTrack(index); // Play the new song
        }
    });

    // Player controls
    playPauseBtn.addEventListener('click', togglePlayPause);
    prevTrackBtn.addEventListener('click', prevTrack);
    nextTrackBtn.addEventListener('click', nextTrack);

    // Audio element events
    audio.addEventListener('timeupdate', () => {
        if (!isNaN(audio.duration)) {
            progressBar.value = (audio.currentTime / audio.duration) * 100 || 0;
            currentTimeDisplay.textContent = formatTime(audio.currentTime);
        }
    });

    audio.addEventListener('loadedmetadata', () => {
         totalTimeDisplay.textContent = formatTime(audio.duration);
    });

    audio.addEventListener('ended', nextTrack);

    audio.addEventListener('error', (e) => {
        console.error("Erro de áudio:", e);
        currentSongDisplay.textContent = "Erro ao carregar a música";
        updatePlayButton(false);
        updatePlayingIndicator(-1);
    });

    // Progress bar seeking
    progressBar.addEventListener('input', () => {
        if (!isNaN(audio.duration)) {
            const seekTime = (progressBar.value / 100) * audio.duration;
            audio.currentTime = seekTime;
        }
    });

    // Volume controls
    volumeSlider.addEventListener('input', () => {
        audio.volume = volumeSlider.value / 100;
        audio.muted = false; // Unmute when user adjusts volume
        updateVolumeIcon();
    });

    volumeIconBtn.addEventListener('click', () => {
        audio.muted = !audio.muted;
        updateVolumeIcon();
    });

    audio.addEventListener('volumechange', updateVolumeIcon); // Sync icon if volume changes elsewhere

    // Initialize volume
    audio.volume = volumeSlider.value / 100;
    updateVolumeIcon();
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


/**
 * Handles the download button click.
 * @param {Event} event - The click event.
 * @param {string} filepath - The path to the audio file.
 */
function downloadTrack(event, filepath) {
    event.stopPropagation(); // Prevent the click from triggering playTrack
    const link = document.createElement('a');
    link.href = filepath;
    link.download = filepath.split('/').pop(); // Suggests a filename to the browser
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// --- App Entry Point ---
document.addEventListener('DOMContentLoaded', fetchMusicData);
