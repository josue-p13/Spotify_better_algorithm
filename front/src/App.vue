<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import ConfigPage from './components/ConfigPage.vue'
import CurrentTrack from './components/CurrentTrack.vue'
import PlaybackControls from './components/PlaybackControls.vue'
import ModeSelector from './components/ModeSelector.vue'
import RecommendationCard from './components/RecommendationCard.vue'
import SuggestionsPanel from './components/SuggestionsPanel.vue'
import type { Recommendation, Suggestion, SpotifyCredentials, Track } from './types'
import { recommendationsApi, youtubeApi, spotifyApi } from './services/api'

const isConfigured = ref(false)
const spotifyCredentials = ref<SpotifyCredentials | null>(null)
const geminiApiKey = ref('')

const apiKey = ref('')
const aiMode = ref<'manual' | 'gemini' | 'local'>('manual')
const localModel = ref('qwen2.5')
const currentRecommendation = ref<Recommendation | null>(null)
const loadingRecommendation = ref(false)
const currentVideoUrl = ref('')
const autoMode = ref(false)
const currentTrack = ref<Track | null>(null)

// Verificar si hay configuración guardada
onMounted(() => {
  const savedCreds = localStorage.getItem('spotify_credentials')
  const savedGemini = localStorage.getItem('gemini_api_key')
  const savedMode = localStorage.getItem('ai_mode')
  const savedLocalModel = localStorage.getItem('local_model')
  
  if (savedCreds) {
    spotifyCredentials.value = JSON.parse(savedCreds)
    isConfigured.value = true
  }
  
  if (savedGemini) {
    geminiApiKey.value = savedGemini
    apiKey.value = savedGemini
  }

  if (savedMode) {
    aiMode.value = savedMode as 'manual' | 'gemini' | 'local'
  }

  if (savedLocalModel) {
    localModel.value = savedLocalModel
  }
})

const handleConfigured = (credentials: SpotifyCredentials, geminiKey: string) => {
  spotifyCredentials.value = credentials
  geminiApiKey.value = geminiKey
  apiKey.value = geminiKey
  isConfigured.value = true
}

const resetConfig = () => {
  if (confirm('¿Estás seguro de que quieres borrar la configuración?')) {
    localStorage.removeItem('spotify_credentials')
    localStorage.removeItem('gemini_api_key')
    spotifyCredentials.value = null
    geminiApiKey.value = ''
    apiKey.value = ''
    isConfigured.value = false
  }
}

const handleTrackChanged = (track: Track | null) => {
  // Solo obtener recomendación si la canción realmente cambió
  const prevTrackInfo = currentTrack.value ? 
    `${currentTrack.value.artists?.join(', ')} - ${currentTrack.value.track_name}` : null
  const newTrackInfo = track ? 
    `${track.artists?.join(', ')} - ${track.track_name}` : null
  
  currentTrack.value = track
  
  // Obtener recomendación automáticamente SOLO cuando cambie la canción (no en polling)
  if (track && track.is_playing && newTrackInfo && prevTrackInfo !== newTrackInfo) {
    console.log('🔄 Nueva canción detectada:', newTrackInfo)
    getRecommendation()
  }
}

const getRecommendation = async (songName?: string) => {
  loadingRecommendation.value = true
  try {
    // Construir el nombre de la canción desde la información actual de Spotify
    let song = songName
    if (!song && currentTrack.value) {
      const artists = currentTrack.value.artists?.join(', ') || ''
      const trackName = currentTrack.value.track_name || ''
      song = `${artists} - ${trackName}`
    }
    
    // Fallback si no hay información
    if (!song) {
      song = 'Current Song'
    }
    
    console.log('🎵 Buscando recomendación para:', song)
    
    const recommendation = await recommendationsApi.getNext(
      song, 
      aiMode.value,
      aiMode.value === 'gemini' ? apiKey.value : undefined,
      aiMode.value === 'local' ? localModel.value : undefined
    )
    currentRecommendation.value = recommendation
    currentVideoUrl.value = recommendation.video_url
    
    if (aiMode.value !== 'manual' && recommendation.mode === 'auto' && autoMode.value && spotifyCredentials.value) {
      try {
        await spotifyApi.addToQueue(spotifyCredentials.value, recommendation.artista!, recommendation.cancion!)
        console.log('✅ Canción agregada automáticamente a Spotify')
      } catch (autoQueueError) {
        console.warn('⚠️ No se pudo agregar automáticamente a Spotify:', autoQueueError)
        // No mostrar error al usuario, solo continuar en modo manual
        console.log('🔄 Continuando en modo semi-automático - usuario puede agregar manualmente')
      }
    }
  } catch (error) {
    console.error('Error getting recommendation:', error)
    alert('Error al obtener recomendación')
  } finally {
    loadingRecommendation.value = false
  }
}

const handleSuggestionSelect = async (suggestion: Suggestion) => {
  if (!spotifyCredentials.value) return
  
  loadingRecommendation.value = true
  try {
    const title = await youtubeApi.getNextVideo(suggestion.url)
    
    if (aiMode.value !== 'manual') {
      const cleaned = await youtubeApi.cleanTitle(
        title.raw_title, 
        aiMode.value,
        aiMode.value === 'gemini' ? apiKey.value : undefined,
        aiMode.value === 'local' ? localModel.value : undefined
      )
      
      if (cleaned.mode === 'auto' && cleaned.artista && cleaned.cancion) {
        await spotifyApi.addToQueue(spotifyCredentials.value, cleaned.artista, cleaned.cancion)
        currentRecommendation.value = {
          mode: 'auto',
          video_url: suggestion.url,
          raw_title: title.raw_title,
          artista: cleaned.artista,
          cancion: cleaned.cancion
        }
      }
    } else {
      currentRecommendation.value = {
        mode: 'manual',
        video_url: suggestion.url,
        raw_title: title.raw_title
      }
    }
    
    currentVideoUrl.value = suggestion.url
  } catch (error) {
    console.error('Error selecting suggestion:', error)
    alert('Error al procesar sugerencia')
  } finally {
    loadingRecommendation.value = false
  }
}

const handleAdded = () => {
  alert('✅ Canción agregada a la cola de Spotify')
  currentRecommendation.value = null
}

const handleSkip = () => {
  currentRecommendation.value = null
}

// Nueva función para refrescar el track actual
const refreshCurrentTrack = async () => {
  if (!spotifyCredentials.value) return
  
  try {
    const track = await spotifyApi.getCurrentTrack(spotifyCredentials.value)
    currentTrack.value = track
    console.log('🔄 Track refreshed:', track)
  } catch (error) {
    console.error('Error refreshing track:', error)
  }
}

watch([aiMode, apiKey, localModel], () => {
  currentRecommendation.value = null
  // Guardar preferencias
  localStorage.setItem('ai_mode', aiMode.value)
  if (apiKey.value) {
    localStorage.setItem('gemini_api_key', apiKey.value)
  }
  if (localModel.value) {
    localStorage.setItem('local_model', localModel.value)
  }
})
</script>

<template>
  <!-- Página de configuración si no está configurado -->
  <ConfigPage 
    v-if="!isConfigured"
    @configured="handleConfigured"
  />

  <!-- Aplicación principal si está configurado -->
  <div v-else class="app">
    <header class="app-header">
      <h1>🎵 Spotify Better Algorithm</h1>
      <p>Sistema inteligente de recomendaciones musicales</p>
      <button @click="resetConfig" class="btn-reset">⚙️ Cambiar Configuración</button>
    </header>

    <main class="app-main">
      <div class="container">
        <section class="section">
          <CurrentTrack 
            :credentials="spotifyCredentials!" 
            @track-changed="handleTrackChanged"
          />
        </section>

        <!-- 🎵 CONTROLES DE REPRODUCCIÓN -->
        <section class="section">
          <PlaybackControls 
            :credentials="spotifyCredentials!"
            :current-track="currentTrack"
            @track-changed="refreshCurrentTrack"
          />
        </section>

        <section class="section">
          <ModeSelector 
            v-model:ai-mode="aiMode"
            v-model:api-key="apiKey"
            v-model:local-model="localModel"
          />
        </section>

        <section class="section">
          <div class="auto-mode-toggle">
            <label>
              <input type="checkbox" v-model="autoMode" />
              <span>🤖 Modo Automático Continuo</span>
            </label>
            <button 
              @click="getRecommendation()" 
              class="btn-manual-recommendation"
              :disabled="loadingRecommendation"
              title="Obtener recomendación manualmente"
            >
              {{ loadingRecommendation ? '⏳' : '🔄' }}
            </button>
          </div>
        </section>

        <section v-if="currentRecommendation" class="section">
          <RecommendationCard 
            :recommendation="currentRecommendation"
            :loading="loadingRecommendation"
            :credentials="spotifyCredentials!"
            @refresh="getRecommendation()"
            @added="handleAdded"
            @skip="handleSkip"
          />
        </section>

        <section v-if="currentVideoUrl" class="section">
          <SuggestionsPanel 
            :video-url="currentVideoUrl"
            @select="handleSuggestionSelect"
          />
        </section>
      </div>
    </main>

    <footer class="app-footer">
      <p>Desarrollado con ❤️ usando Vue 3 + FastAPI</p>
    </footer>
  </div>
</template>

<style scoped>
.app {
  min-height: 100vh;
  background-color: var(--spotify-base);
  background: linear-gradient(180deg, #1f1f1f 0%, var(--spotify-base) 100%);
  padding: 2rem 1rem;
}

.app-header {
  text-align: center;
  color: var(--spotify-text);
  margin-bottom: 2rem;
  position: relative;
}

.app-header h1 {
  font-size: 2.5rem;
  margin: 0;
  font-weight: 700;
  color: var(--spotify-green);
}

.app-header p {
  font-size: 1.1rem;
  color: var(--spotify-subtext);
  margin: 0.5rem 0 0;
}

.btn-reset {
  position: absolute;
  top: 0;
  right: 0;
  padding: 0.5rem 1rem;
  background: var(--spotify-surface);
  border: 1px solid var(--spotify-border);
  color: var(--spotify-text);
  border-radius: 500px;
  cursor: pointer;
  font-size: 0.85rem;
  font-weight: 700;
  transition: all 0.3s ease;
}

.btn-reset:hover {
  background: var(--spotify-surface-hover);
  transform: scale(1.05);
  border-color: var(--spotify-text);
}

.app-main {
  max-width: 1200px;
  margin: 0 auto;
}

.container {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.section {
  animation: slideIn 0.5s ease;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.auto-mode-toggle {
  background: var(--spotify-surface);
  border-radius: 8px;
  padding: 1rem 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border: 1px solid var(--spotify-border);
}

.auto-mode-toggle label {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  cursor: pointer;
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--spotify-text);
}

.auto-mode-toggle input[type="checkbox"] {
  width: 18px;
  height: 18px;
  cursor: pointer;
  accent-color: var(--spotify-green);
}

.btn-manual-recommendation {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 500px;
  background-color: var(--spotify-green);
  color: var(--spotify-black);
  cursor: pointer;
  font-size: 1rem;
  font-weight: 700;
  transition: all 0.3s ease;
  min-width: 40px;
}

.btn-manual-recommendation:hover:not(:disabled) {
  background-color: var(--spotify-green-hover);
  transform: scale(1.05);
}

.btn-manual-recommendation:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.app-footer {
  text-align: center;
  color: var(--spotify-subtext);
  margin-top: 3rem;
  font-size: 0.9rem;
}
</style>
