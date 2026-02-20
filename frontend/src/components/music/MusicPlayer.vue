<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { musicApi } from '@/services/api'
import type { Track } from '@/types/metro_music'

// ==================== State ====================
const tracks = ref<Track[]>([])
const currentTrack = ref<Track | null>(null)
const isPlaying = ref(false)
const isLoading = ref(false)
const audio = ref<HTMLAudioElement | null>(null)
const progress = ref(0)
const volume = ref(0.5)
const isMuted = ref(false)
const duration = ref(0)
const currentTime = ref(0)
const error = ref<string | null>(null)
const isDragging = ref(false)
const dragValue = ref(0)

// Playlist management
const playMode = ref<'single' | 'loop' | 'shuffle'>('single')

// Loading state for initial fetch
const loading = ref(true)

// ==================== Computed ====================
const displayProgress = computed(() => isDragging.value ? dragValue.value : progress.value)
const displayVolumeIcon = computed(() => {
  if (isMuted.value || volume.value === 0) return '馃攪'
  if (volume.value < 0.3) return '馃攬'
  if (volume.value < 0.7) return '馃攭'
  return '馃攰'
})
const playModeIcon = computed(() => {
  switch (playMode.value) {
    case 'loop': return '馃攣'
    case 'shuffle': return '馃攢'
    default: return '鈻讹笍'
  }
})
const canPlay = computed(() => !isLoading.value && currentTrack.value !== null)

// ==================== Lifecycle ====================
onMounted(async () => {
  await loadTracks()
  if (audio.value) {
    audio.value.volume = volume.value
  }
  window.addEventListener('keydown', handleKeyboard)
})

onUnmounted(() => {
  if (audio.value) {
    audio.value.pause()
  }
  window.removeEventListener('keydown', handleKeyboard)
})

// ==================== Methods ====================
async function loadTracks() {
  try {
    loading.value = true
    error.value = null
    const res = await musicApi.getTracks()
    tracks.value = res.data || []
    
    if (tracks.value.length > 0 && !currentTrack.value) {
      currentTrack.value = tracks.value[0]
      if (audio.value) {
        audio.value.src = getAudioUrl(tracks.value[0].fileUrl)
        audio.value.load()
      }
    }
  } catch (err: any) {
    console.error('Failed to load tracks', err)
    error.value = err.response?.data?.message || '鏃犳硶鍔犺浇闊充箰鍒楄〃锛岃绋嶅悗閲嶈瘯'
  } finally {
    loading.value = false
  }
}

function getAudioUrl(url: string | undefined): string {
  if (!url) return ''
  if (url.startsWith('http')) return url
  const baseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
  const rootUrl = baseUrl.replace('/api/v1', '')
  return `${rootUrl}${url}`
}

// ==================== Playback Control ====================
async function togglePlay() {
  if (!audio.value || !canPlay.value) return
  
  if (isPlaying.value) {
    audio.value.pause()
    isPlaying.value = false
  } else {
    try {
      await audio.value.play()
      isPlaying.value = true
    } catch (err) {
      console.error('Play failed:', err)
      error.value = '鎾斁澶辫触锛岃妫€鏌ラ煶棰戞枃浠?
    }
  }
}

async function playTrack(track: Track) {
  if (currentTrack.value?.id === track.id) {
    togglePlay()
    return
  }
  
  error.value = null
  currentTrack.value = track
  isLoading.value = true
  
  if (audio.value) {
    audio.value.src = getAudioUrl(track.fileUrl)
    audio.value.load()
    
    try {
      await audio.value.play()
      isPlaying.value = true
    } catch (err) {
      console.error('Play failed:', err)
      error.value = '鎾斁澶辫触锛岄煶棰戞枃浠跺彲鑳戒笉瀛樺湪'
      isPlaying.value = false
    } finally {
      isLoading.value = false
    }
  }
}

function nextTrack() {
  if (!currentTrack.value || tracks.value.length === 0) return
  
  let nextIndex: number
  
  if (playMode.value === 'shuffle') {
    nextIndex = Math.floor(Math.random() * tracks.value.length)
  } else {
    const currentIndex = tracks.value.findIndex(t => t.id === currentTrack.value?.id)
    nextIndex = (currentIndex + 1) % tracks.value.length
  }
  
  playTrack(tracks.value[nextIndex])
}

function prevTrack() {
  if (!currentTrack.value || tracks.value.length === 0) return
  
  const currentIndex = tracks.value.findIndex(t => t.id === currentTrack.value?.id)
  const prevIndex = (currentIndex - 1 + tracks.value.length) % tracks.value.length
  playTrack(tracks.value[prevIndex])
}

function togglePlayMode() {
  const modes: ('single' | 'loop' | 'shuffle')[] = ['single', 'loop', 'shuffle']
  const currentIndex = modes.indexOf(playMode.value)
  playMode.value = modes[(currentIndex + 1) % modes.length]
}

// ==================== Audio Events ====================
function onTimeUpdate() {
  if (!audio.value || isDragging.value) return
  currentTime.value = audio.value.currentTime
  duration.value = audio.value.duration || 0
  progress.value = duration.value ? (currentTime.value / duration.value) * 100 : 0
}

function onEnded() {
  if (playMode.value === 'loop' && currentTrack.value) {
    if (audio.value) {
      audio.value.currentTime = 0
      audio.value.play()
    }
  } else {
    nextTrack()
  }
}

function onLoadedMetadata() {
  if (audio.value) {
    duration.value = audio.value.duration
  }
  isLoading.value = false
}

function onWaiting() {
  isLoading.value = true
}

function onCanPlay() {
  isLoading.value = false
}

function onError() {
  isLoading.value = false
  isPlaying.value = false
  error.value = '闊抽鍔犺浇澶辫触锛屾枃浠跺彲鑳戒笉瀛樺湪鎴栨牸寮忎笉鏀寔'
}

// ==================== Progress Control ====================
function onSeekStart(event: Event) {
  isDragging.value = true
  const input = event.target as HTMLInputElement
  dragValue.value = parseFloat(input.value)
}

function onSeekInput(event: Event) {
  if (!isDragging.value) return
  const input = event.target as HTMLInputElement
  dragValue.value = parseFloat(input.value)
}

function onSeekEnd(event: Event) {
  const input = event.target as HTMLInputElement
  const value = parseFloat(input.value)
  
  if (audio.value && duration.value) {
    audio.value.currentTime = (value / 100) * duration.value
  }
  
  isDragging.value = false
  dragValue.value = 0
}

// ==================== Volume Control ====================
function toggleMute() {
  if (!audio.value) return
  isMuted.value = !isMuted.value
  audio.value.muted = isMuted.value
}

function updateVolume(event: Event) {
  const input = event.target as HTMLInputElement
  volume.value = parseFloat(input.value)
  
  if (audio.value) {
    audio.value.volume = volume.value
    if (volume.value > 0 && isMuted.value) {
      isMuted.value = false
      audio.value.muted = false
    }
  }
}

// ==================== Utilities ====================
function formatTime(seconds: number): string {
  if (!seconds || isNaN(seconds)) return '0:00'
  const m = Math.floor(seconds / 60)
  const s = Math.floor(seconds % 60)
  return `${m}:${s.toString().padStart(2, '0')}`
}

function handleKeyboard(event: KeyboardEvent) {
  if (event.target instanceof HTMLInputElement || event.target instanceof HTMLTextAreaElement) {
    return
  }
  
  switch (event.code) {
    case 'Space':
      event.preventDefault()
      togglePlay()
      break
    case 'ArrowRight':
      if (audio.value) {
        audio.value.currentTime = Math.min(audio.value.currentTime + 5, duration.value)
      }
      break
    case 'ArrowLeft':
      if (audio.value) {
        audio.value.currentTime = Math.max(audio.value.currentTime - 5, 0)
      }
      break
    case 'ArrowUp':
      event.preventDefault()
      volume.value = Math.min(volume.value + 0.1, 1)
      if (audio.value) audio.value.volume = volume.value
      break
    case 'ArrowDown':
      event.preventDefault()
      volume.value = Math.max(volume.value - 0.1, 0)
      if (audio.value) audio.value.volume = volume.value
      break
  }
}

function retryLoad() {
  loadTracks()
}
</script>

<template>
  <div class="music-player-container">
    <!-- Error Notification -->
    <Transition name="slide-down">
      <div v-if="error" class="error-notification">
        <span class="error-icon">鈿狅笍</span>
        <span class="error-text">{{ error }}</span>
        <button class="error-close" @click="error = null">鉁?/button>
        <button class="error-retry" @click="retryLoad">閲嶈瘯</button>
      </div>
    </Transition>

    <div class="player-card">
      <!-- Visualizer -->
      <div class="visualizer" :class="{ playing: isPlaying }">
        <div 
          v-for="n in 20" 
          :key="n" 
          class="bar"
          :style="{ 
            animationDelay: `${n * 0.05}s`,
            height: isPlaying ? `${20 + Math.random() * 80}%` : '10%'
          }"
        ></div>
      </div>
      
      <!-- Track Info -->
      <div class="track-info">
        <div v-if="loading" class="track-loading">
          <span class="loading-spinner"></span>
          鍔犺浇涓?..
        </div>
        <template v-else>
          <h2 v-if="currentTrack">{{ currentTrack.title }}</h2>
          <h2 v-else-if="tracks.length === 0">鏆傛棤闊充箰</h2>
          <h2 v-else>閫夋嫨涓€棣栨瓕鏇?/h2>
          <p v-if="currentTrack && currentTrack.artists?.length">
            {{ currentTrack.artists.map(a => a.name).join(', ') }}
          </p>
          <p v-else-if="currentTrack" class="no-artist">鏈煡鑹烘湳瀹?/p>
        </template>
      </div>
      
      <!-- Controls -->
      <div class="controls">
        <button @click="togglePlayMode" class="control-btn mode-btn" :title="`鎾斁妯″紡: ${playMode}`">
          {{ playModeIcon }}
        </button>
        <button @click="prevTrack" class="control-btn" :disabled="!canPlay" title="涓婁竴棣?>
          鈴?        </button>
        <button 
          @click="togglePlay" 
          class="control-btn play-btn" 
          :disabled="!canPlay || isLoading"
          :class="{ loading: isLoading }"
          title="鎾斁/鏆傚仠 (Space)"
        >
          <span v-if="isLoading" class="btn-spinner"></span>
          <span v-else>{{ isPlaying ? '鈴? : '鈻? }}</span>
        </button>
        <button @click="nextTrack" class="control-btn" :disabled="!canPlay" title="涓嬩竴棣?>
          鈴?        </button>
      </div>
      
      <!-- Progress -->
      <div class="progress-container">
        <span class="time">{{ formatTime(currentTime) }}</span>
        <div class="slider-wrapper">
          <input 
            type="range" 
            min="0" 
            max="100"
            step="0.1"
            :value="displayProgress"
            @mousedown="onSeekStart"
            @input="onSeekInput"
            @mouseup="onSeekEnd"
            @touchstart="onSeekStart"
            @touchmove="onSeekInput"
            @touchend="onSeekEnd"
            class="seek-slider"
            :disabled="!canPlay"
          />
          <div class="progress-fill" :style="{ width: `${displayProgress}%` }"></div>
        </div>
        <span class="time">{{ formatTime(duration) }}</span>
      </div>
      
      <!-- Volume -->
      <div class="volume-container">
        <button class="mute-btn" @click="toggleMute" :title="isMuted ? '鍙栨秷闈欓煶' : '闈欓煶'">
          {{ displayVolumeIcon }}
        </button>
        <div class="slider-wrapper">
          <input 
            type="range" 
            min="0" 
            max="1" 
            step="0.01" 
            :value="volume" 
            @input="updateVolume"
            class="volume-slider"
          />
          <div class="volume-fill" :style="{ width: `${volume * 100}%` }"></div>
        </div>
      </div>
      
      <!-- Keyboard Hints -->
      <div class="keyboard-hints">
        <span>Space: 鎾斁/鏆傚仠</span>
        <span>鈫?鈫? 蹇繘/蹇€€</span>
        <span>鈫?鈫? 闊抽噺</span>
      </div>
      
      <!-- Audio Element -->
      <audio 
        ref="audio" 
        @timeupdate="onTimeUpdate" 
        @ended="onEnded"
        @loadedmetadata="onLoadedMetadata"
        @waiting="onWaiting"
        @canplay="onCanPlay"
        @error="onError"
        preload="metadata"
      ></audio>
    </div>
    
    <!-- Playlist -->
    <div class="playlist">
      <div class="playlist-header">
        <h3>鎾斁鍒楄〃</h3>
        <span class="track-count">{{ tracks.length }} 棣?/span>
      </div>
      
      <div v-if="loading" class="playlist-loading">
        <span class="loading-spinner"></span>
        鍔犺浇涓?..
      </div>
      
      <div v-else-if="tracks.length === 0" class="playlist-empty">
        <span class="empty-icon">馃幍</span>
        <p>鏆傛棤闊充箰</p>
        <button @click="retryLoad" class="retry-btn">閲嶆柊鍔犺浇</button>
      </div>
      
      <ul v-else>
        <li 
          v-for="(track, index) in tracks" 
          :key="track.id"
          @click="playTrack(track)"
          :class="{ 
            active: currentTrack?.id === track.id,
            playing: currentTrack?.id === track.id && isPlaying
          }"
        >
          <div class="track-number-wrapper">
            <span class="track-number">{{ index + 1 }}</span>
            <span v-if="currentTrack?.id === track.id" class="playing-indicator">
              {{ isPlaying ? '鈻? : '鈴? }}
            </span>
          </div>
          <div class="track-info-wrapper">
            <span class="track-title">{{ track.title }}</span>
            <span class="track-artist" v-if="track.artists?.length">
              {{ track.artists[0].name }}
            </span>
          </div>
          <span class="track-duration" v-if="track.duration">
            {{ formatTime(track.duration) }}
          </span>
        </li>
      </ul>
    </div>
  </div>
</template>

<style scoped>
/* ==================== Container ==================== */
.music-player-container {
  display: flex;
  gap: 2rem;
  padding: 2rem;
  background: #0a0a0a;
  color: #fff;
  min-height: 80vh;
  font-family: 'Courier New', Courier, monospace;
  position: relative;
}

@media (max-width: 768px) {
  .music-player-container {
    flex-direction: column;
    padding: 1rem;
  }
}

/* ==================== Error Notification ==================== */
.error-notification {
  position: fixed;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(220, 38, 38, 0.95);
  color: white;
  padding: 1rem 1.5rem;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  box-shadow: 0 4px 20px rgba(220, 38, 38, 0.4);
  z-index: 1000;
  backdrop-filter: blur(10px);
}

.error-icon {
  font-size: 1.2rem;
}

.error-text {
  flex: 1;
  font-size: 0.95rem;
}

.error-close, .error-retry {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  padding: 0.4rem 0.8rem;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
}

.error-close:hover, .error-retry:hover {
  background: rgba(255, 255, 255, 0.3);
}

.slide-down-enter-active,
.slide-down-leave-active {
  transition: all 0.3s ease;
}

.slide-down-enter-from,
.slide-down-leave-to {
  opacity: 0;
  transform: translateX(-50%) translateY(-20px);
}

/* ==================== Player Card ==================== */
.player-card {
  flex: 1;
  background: linear-gradient(145deg, #1a1a1a, #0f0f0f);
  border-radius: 16px;
  padding: 2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  box-shadow:
    0 8px 32px rgba(0, 0, 0, 0.6),
    inset 0 1px 0 rgba(255, 255, 255, 0.05);
  border: 1px solid #222;
  max-width: 500px;
}

/* ==================== Visualizer ==================== */
.visualizer {
  display: flex;
  align-items: flex-end;
  justify-content: center;
  gap: 4px;
  height: 120px;
  width: 100%;
  margin-bottom: 2rem;
  padding: 1rem;
  background: radial-gradient(ellipse at center, rgba(0, 255, 136, 0.05) 0%, transparent 70%);
  border-radius: 8px;
}

.bar {
  width: 10px;
  background: linear-gradient(to top, #00ff88, #00cc6a);
  height: 10%;
  border-radius: 2px;
  transition: height 0.15s ease;
  animation: bounce 0.8s infinite ease-in-out alternate;
  animation-play-state: paused;
  box-shadow: 0 0 10px rgba(0, 255, 136, 0.3);
}

.visualizer.playing .bar {
  animation-play-state: running;
}

@keyframes bounce {
  0% {
    height: 10%;
    opacity: 0.5;
  }
  100% {
    height: 100%;
    opacity: 1;
  }
}

/* ==================== Track Info ==================== */
.track-info {
  text-align: center;
  margin-bottom: 2rem;
  min-height: 80px;
}

.track-info h2 {
  font-size: 1.6rem;
  margin: 0 0 0.5rem;
  color: #00ff88;
  text-shadow: 0 0 15px rgba(0, 255, 136, 0.3);
  font-weight: 600;
}

.track-info p {
  margin: 0;
  color: #888;
  font-size: 1rem;
}

.track-info .no-artist {
  color: #555;
}

.track-loading {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  color: #888;
}

.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid #333;
  border-top-color: #00ff88;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* ==================== Controls ==================== */
.controls {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  align-items: center;
}

.control-btn {
  background: rgba(0, 255, 136, 0.05);
  border: 1px solid rgba(0, 255, 136, 0.3);
  color: #00ff88;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  font-size: 1.2rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.control-btn:hover:not(:disabled) {
  background: rgba(0, 255, 136, 0.15);
  transform: scale(1.1);
  box-shadow: 0 0 20px rgba(0, 255, 136, 0.4);
}

.control-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.control-btn.mode-btn {
  width: 40px;
  height: 40px;
  font-size: 1rem;
}

.play-btn {
  width: 70px;
  height: 70px;
  font-size: 1.8rem;
  border-width: 2px;
  background: rgba(0, 255, 136, 0.1);
}

.play-btn.loading {
  font-size: 1rem;
}

.btn-spinner {
  width: 24px;
  height: 24px;
  border: 2px solid transparent;
  border-top-color: #00ff88;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

/* ==================== Progress & Volume Sliders ==================== */
.progress-container, .volume-container {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.progress-container {
  margin-bottom: 1rem;
}

.time {
  font-size: 0.85rem;
  color: #888;
  font-variant-numeric: tabular-nums;
  min-width: 45px;
}

.slider-wrapper {
  flex: 1;
  position: relative;
  height: 24px;
  display: flex;
  align-items: center;
}

input[type="range"] {
  position: absolute;
  width: 100%;
  height: 100%;
  -webkit-appearance: none;
  background: transparent;
  cursor: pointer;
  z-index: 2;
}

input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: #00ff88;
  cursor: pointer;
  box-shadow: 0 0 10px rgba(0, 255, 136, 0.5);
  transition: transform 0.2s;
  margin-top: -6px;
}

input[type="range"]::-webkit-slider-thumb:hover {
  transform: scale(1.2);
}

input[type="range"]:disabled {
  cursor: not-allowed;
}

input[type="range"]:disabled::-webkit-slider-thumb {
  background: #555;
  box-shadow: none;
}

input[type="range"]::-webkit-slider-runnable-track {
  width: 100%;
  height: 4px;
  background: transparent;
  border-radius: 2px;
}

.progress-fill, .volume-fill {
  position: absolute;
  height: 4px;
  background: linear-gradient(to right, #00ff88, #00cc6a);
  border-radius: 2px;
  pointer-events: none;
  z-index: 1;
  box-shadow: 0 0 8px rgba(0, 255, 136, 0.3);
}

.volume-container {
  margin-bottom: 1rem;
}

.mute-btn {
  background: none;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  padding: 0.25rem;
  transition: transform 0.2s;
}

.mute-btn:hover {
  transform: scale(1.1);
}

/* ==================== Keyboard Hints ==================== */
.keyboard-hints {
  display: flex;
  gap: 1rem;
  font-size: 0.75rem;
  color: #555;
  margin-top: auto;
  padding-top: 1rem;
}

.keyboard-hints span {
  background: rgba(255, 255, 255, 0.03);
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  border: 1px solid #333;
}

/* ==================== Playlist ==================== */
.playlist {
  flex: 1;
  background: linear-gradient(145deg, #151515, #0a0a0a);
  border-radius: 16px;
  padding: 1.5rem;
  overflow-y: auto;
  max-height: 600px;
  border: 1px solid #222;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.03);
}

.playlist-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 1rem;
  border-bottom: 1px solid #333;
  margin-bottom: 1rem;
}

.playlist-header h3 {
  margin: 0;
  color: #00ff88;
  font-size: 1.2rem;
}

.track-count {
  font-size: 0.85rem;
  color: #666;
}

.playlist-loading, .playlist-empty {
  text-align: center;
  padding: 3rem 1rem;
  color: #666;
}

.empty-icon {
  font-size: 3rem;
  display: block;
  margin-bottom: 1rem;
}

.retry-btn {
  margin-top: 1rem;
  background: rgba(0, 255, 136, 0.1);
  border: 1px solid #00ff88;
  color: #00ff88;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
}

.retry-btn:hover {
  background: rgba(0, 255, 136, 0.2);
}

.playlist ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.playlist li {
  display: flex;
  align-items: center;
  padding: 0.875rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  gap: 0.75rem;
  margin-bottom: 0.25rem;
}

.playlist li:hover {
  background: rgba(255, 255, 255, 0.03);
}

.playlist li.active {
  background: rgba(0, 255, 136, 0.08);
  border-left: 3px solid #00ff88;
}

.playlist li.playing .track-title {
  color: #00ff88;
}

.track-number-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 30px;
  position: relative;
}

.track-number {
  color: #555;
  font-size: 0.85rem;
}

.playlist li.active .track-number {
  opacity: 0;
}

.playing-indicator {
  position: absolute;
  color: #00ff88;
  font-size: 0.9rem;
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.track-info-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  min-width: 0;
}

.track-title {
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.track-artist {
  color: #666;
  font-size: 0.85rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.track-duration {
  font-size: 0.85rem;
  color: #666;
  font-variant-numeric: tabular-nums;
}

/* ==================== Scrollbar ==================== */
::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background: #333;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: #444;
}
</style>
