<template>
  <div class="playback-controls">
    <h3>🎵 Controles de Reproducción</h3>
    
    <div class="controls-grid">
      <!-- Previous -->
      <button 
        @click="previousTrack" 
        class="control-btn previous"
        :disabled="loading.previous"
      >
        <span v-if="!loading.previous">⏮️</span>
        <span v-else class="spinner-small"></span>
        Anterior
      </button>

      <!-- Play/Pause -->
      <button 
        @click="togglePlayPause" 
        class="control-btn play-pause"
        :disabled="loading.playPause"
      >
        <span v-if="!loading.playPause">
          {{ isPlaying ? '⏸️' : '▶️' }}
        </span>
        <span v-else class="spinner-small"></span>
        {{ isPlaying ? 'Pausar' : 'Reproducir' }}
      </button>

      <!-- Next -->
      <button 
        @click="nextTrack" 
        class="control-btn next"
        :disabled="loading.next"
      >
        <span v-if="!loading.next">⏭️</span>
        <span v-else class="spinner-small"></span>
        Siguiente
      </button>
    </div>

    <!-- Status messages -->
    <div v-if="message" class="status-message" :class="messageType">
      {{ message }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import type { SpotifyCredentials, Track } from '@/types'
import { spotifyApi } from '@/services/api'

const props = defineProps<{
  credentials: SpotifyCredentials
  currentTrack?: Track | null
}>()

const emit = defineEmits<{
  trackChanged: []
}>()

const loading = ref({
  previous: false,
  playPause: false,
  next: false
})

const message = ref('')
const messageType = ref<'success' | 'error' | 'info'>('info')

// Detectar si está reproduciendo basado en el currentTrack
const isPlaying = computed(() => {
  return props.currentTrack?.is_playing ?? false
})

const showMessage = (text: string, type: 'success' | 'error' | 'info' = 'info') => {
  message.value = text
  messageType.value = type
  setTimeout(() => {
    message.value = ''
  }, 3000)
}

const previousTrack = async () => {
  loading.value.previous = true
  try {
    await spotifyApi.previousTrack(props.credentials)
    showMessage('⏮️ Canción anterior', 'success')
    // Emitir evento para que se actualice el track actual
    setTimeout(() => emit('trackChanged'), 1000)
  } catch (error) {
    showMessage(`Error: ${error instanceof Error ? error.message : 'Error desconocido'}`, 'error')
  } finally {
    loading.value.previous = false
  }
}

const togglePlayPause = async () => {
  loading.value.playPause = true
  try {
    if (isPlaying.value) {
      await spotifyApi.pauseMusic(props.credentials)
      showMessage('⏸️ Música pausada', 'success')
    } else {
      await spotifyApi.playMusic(props.credentials)
      showMessage('▶️ Música reproduciendo', 'success')
    }
    // Emitir evento para que se actualice el track actual
    setTimeout(() => emit('trackChanged'), 500)
  } catch (error) {
    showMessage(`Error: ${error instanceof Error ? error.message : 'Error desconocido'}`, 'error')
  } finally {
    loading.value.playPause = false
  }
}

const nextTrack = async () => {
  loading.value.next = true
  try {
    await spotifyApi.nextTrack(props.credentials)
    showMessage('⏭️ Siguiente canción', 'success')
    // Emitir evento para que se actualice el track actual
    setTimeout(() => emit('trackChanged'), 1000)
  } catch (error) {
    showMessage(`Error: ${error instanceof Error ? error.message : 'Error desconocido'}`, 'error')
  } finally {
    loading.value.next = false
  }
}
</script>

<style scoped>
.playback-controls {
  background: var(--spotify-surface);
  border-radius: 8px;
  padding: 1.5rem;
  border: 1px solid var(--spotify-border);
  margin-bottom: 1rem;
}

.playback-controls h3 {
  margin: 0 0 1rem;
  font-size: 1.1rem;
  color: var(--spotify-text);
  font-weight: 700;
  text-align: center;
}

.controls-grid {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 1rem;
  margin-bottom: 1rem;
}

.control-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem;
  background: var(--spotify-surface-hover);
  border: 1px solid var(--spotify-border);
  border-radius: 8px;
  color: var(--spotify-text);
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s ease;
  min-height: 80px;
}

.control-btn:hover:not(:disabled) {
  background: var(--spotify-border);
  border-color: var(--spotify-green);
}

.control-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.control-btn span:first-child {
  font-size: 1.5rem;
}

.play-pause {
  background: var(--spotify-green);
  color: white;
  font-weight: 600;
}

.play-pause:hover:not(:disabled) {
  background: #1ed760;
}

.status-message {
  padding: 0.75rem;
  border-radius: 6px;
  text-align: center;
  font-size: 0.9rem;
  font-weight: 500;
}

.status-message.success {
  background: rgba(30, 215, 96, 0.1);
  color: var(--spotify-green);
  border: 1px solid rgba(30, 215, 96, 0.3);
}

.status-message.error {
  background: rgba(244, 63, 94, 0.1);
  color: #f43f5e;
  border: 1px solid rgba(244, 63, 94, 0.3);
}

.status-message.info {
  background: var(--spotify-surface-hover);
  color: var(--spotify-subtext);
  border: 1px solid var(--spotify-border);
}

.spinner-small {
  display: inline-block;
  width: 16px;
  height: 16px;
  border: 2px solid currentColor;
  border-top: 2px solid transparent;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Responsive */
@media (max-width: 768px) {
  .controls-grid {
    grid-template-columns: 1fr;
    gap: 0.5rem;
  }
  
  .control-btn {
    flex-direction: row;
    justify-content: center;
    padding: 0.75rem;
    min-height: auto;
  }
  
  .control-btn span:first-child {
    font-size: 1.2rem;
    margin-right: 0.5rem;
  }
}
</style>