<template>
  <div class="current-track-card">
    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>Cargando...</p>
    </div>

    <div v-else-if="track && track.is_playing" class="track-content">
      <img v-if="track.image_url" :src="track.image_url" alt="Album cover" class="album-cover" />
      <div class="track-info">
        <h2>🎵 Reproduciendo ahora</h2>
        <h3 class="track-name">{{ track.track_name }}</h3>
        <p class="artists">{{ track.artists?.join(', ') }}</p>
        <p class="album">{{ track.album }}</p>
        <div class="progress-bar">
          <div class="progress-fill" :style="{ width: progressPercentage + '%' }"></div>
        </div>
        <p class="time">{{ formatTime(track.progress_ms) }} / {{ formatTime(track.duration_ms) }}</p>
      </div>
    </div>

    <div v-else class="no-track">
      <p>⏸️ No hay ninguna canción reproduciéndose</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import type { Track, SpotifyCredentials } from '@/types'
import { spotifyApi } from '@/services/api'

const props = defineProps<{
  credentials: SpotifyCredentials
}>()

const emit = defineEmits<{
  trackChanged: [track: Track | null]
}>()

const track = ref<Track | null>(null)
const loading = ref(true)
let intervalId: number | null = null

const progressPercentage = computed(() => {
  if (!track.value || !track.value.duration_ms || !track.value.progress_ms) return 0
  return (track.value.progress_ms / track.value.duration_ms) * 100
})

const formatTime = (ms: number | undefined) => {
  if (!ms) return '0:00'
  const seconds = Math.floor(ms / 1000)
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

const fetchCurrentTrack = async () => {
  try {
    track.value = await spotifyApi.getCurrentTrack(props.credentials)
    emit('trackChanged', track.value)
  } catch (error) {
    console.error('Error fetching current track:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchCurrentTrack()
  intervalId = window.setInterval(fetchCurrentTrack, 5000)
})

onUnmounted(() => {
  if (intervalId) clearInterval(intervalId)
})
</script>

<style scoped>

.current-track-card {
  background: var(--spotify-surface);
  border-radius: 8px;
  padding: 1.5rem;
  color: var(--spotify-text);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
  min-height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid var(--spotify-border);
}

.loading {
  text-align: center;
}

.spinner {
  border: 4px solid var(--spotify-surface-hover);
  border-top: 4px solid var(--spotify-green);
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.track-content {
  display: flex;
  gap: 1.5rem;
  width: 100%;
  align-items: center;
}

.album-cover {
  width: 160px;
  height: 160px;
  border-radius: 4px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
  object-fit: cover;
}

.track-info {
  flex: 1;
}

.track-info h2 {
  font-size: 0.8rem;
  color: var(--spotify-subtext);
  margin-bottom: 0.5rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.track-name {
  font-size: 2rem;
  font-weight: 900;
  margin: 0.2rem 0;
  color: var(--spotify-text);
}

.artists {
  font-size: 1rem;
  color: var(--spotify-subtext);
  margin: 0.2rem 0;
  font-weight: 500;
}

.album {
  font-size: 0.9rem;
  color: var(--spotify-subtext);
  margin: 0.2rem 0;
}

.progress-bar {
  background: var(--spotify-surface-hover);
  border-radius: 4px;
  height: 4px;
  margin: 1rem 0 0.5rem;
  overflow: hidden;
}

.progress-fill {
  background: var(--spotify-text);
  height: 100%;
  border-radius: 4px;
  transition: width 0.3s ease;
}

.progress-bar:hover .progress-fill {
  background: var(--spotify-green);
}

.time {
  font-size: 0.75rem;
  color: var(--spotify-subtext);
  font-weight: 400;
  display: flex;
  justify-content: flex-end;
}

.no-track {
  text-align: center;
  color: var(--spotify-subtext);
  font-size: 1.1rem;
  font-weight: 500;
}

</style>
