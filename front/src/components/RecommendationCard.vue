<template>
  <div class="recommendation-card">
    <h3>🎯 Próxima Recomendación</h3>
    
    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>Obteniendo recomendación...</p>
    </div>

    <div v-else-if="recommendation" class="recommendation-content">
      <div class="badge" :class="recommendation.mode">
        {{ recommendation.mode === 'auto' ? '🤖 Automático' : '✋ Manual' }}
      </div>

      <div v-if="recommendation.mode === 'auto'" class="auto-mode">
        <h4>{{ recommendation.artista }}</h4>
        <p class="song-name">{{ recommendation.cancion }}</p>
        <p class="raw-title">Título original: {{ recommendation.raw_title }}</p>
        
        <div class="actions">
          <button @click="addToQueue" class="btn btn-primary" :disabled="addingToQueue">
            <span v-if="!addingToQueue">✅ Agregar a Cola</span>
            <span v-else>⏳ Agregando...</span>
          </button>
          <button @click="skip" class="btn btn-secondary">⏭️ Saltar</button>
        </div>
      </div>

      <div v-else class="manual-mode">
        <p class="label">Título original:</p>
        <p class="raw-title">{{ recommendation.raw_title }}</p>
        
        <label for="cleanedTitle">✏️ Limpia el título:</label>
        <input 
          id="cleanedTitle"
          v-model="cleanedTitle" 
          type="text" 
          placeholder="Artista - Canción"
          class="input-clean"
        />
        
        <div class="actions">
          <button @click="addToQueueManual" class="btn btn-primary" :disabled="!cleanedTitle || addingToQueue">
            <span v-if="!addingToQueue">✅ Agregar a Cola</span>
            <span v-else>⏳ Agregando...</span>
          </button>
          <button @click="skip" class="btn btn-secondary">⏭️ Saltar</button>
        </div>
      </div>
    </div>

    <div v-else class="no-recommendation">
      <p>No hay recomendación disponible</p>
      <button @click="$emit('refresh')" class="btn btn-secondary">🔄 Obtener Recomendación</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import type { Recommendation, SpotifyCredentials } from '@/types'
import { spotifyApi } from '@/services/api'

const props = defineProps<{
  recommendation: Recommendation | null
  loading: boolean
  credentials: SpotifyCredentials
}>()

const emit = defineEmits<{
  refresh: []
  added: []
  skip: []
}>()

const addingToQueue = ref(false)
const cleanedTitle = ref('')

// Pre-llenar el input con el título original cuando cambie la recomendación
watch(() => props.recommendation, (newRec) => {
  if (newRec && newRec.mode === 'manual' && newRec.raw_title) {
    cleanedTitle.value = newRec.raw_title
  }
}, { immediate: true })

const addToQueue = async () => {
  if (!props.recommendation || props.recommendation.mode !== 'auto') return
  
  addingToQueue.value = true
  try {
    await spotifyApi.addToQueue(props.credentials, props.recommendation.artista!, props.recommendation.cancion!)
    emit('added')
  } catch (error) {
    console.error('Error adding to queue (auto):', error)
    
    // 🔄 MANEJO ELEGANTE DEL ERROR
    const errorMessage = error instanceof Error ? error.message : 'Error desconocido'
    
    if (errorMessage.includes('No se encontró') || errorMessage.includes('404')) {
      alert(`⚠️ No se pudo agregar automáticamente a Spotify.\n\nCanción: ${props.recommendation.artista} - ${props.recommendation.cancion}\n\nMotivo: No se encontró en el catálogo de Spotify.\n\n💡 Sugerencia: Usa el modo manual para refinar la búsqueda.`)
    } else {
      alert(`❌ Error agregando a Spotify: ${errorMessage}`)
    }
  } finally {
    addingToQueue.value = false
  }
}

const addToQueueManual = async () => {
  if (!cleanedTitle.value) return
  
  addingToQueue.value = true
  try {
    await spotifyApi.addToQueueManual(props.credentials, cleanedTitle.value)
    cleanedTitle.value = ''
    emit('added')
  } catch (error) {
    console.error('Error adding to queue (manual):', error)
    
    const errorMessage = error instanceof Error ? error.message : 'Error desconocido'
    
    if (errorMessage.includes('No se encontró') || errorMessage.includes('404')) {
      alert(`⚠️ No se encontró la canción en Spotify.\n\nBúsqueda: "${cleanedTitle.value}"\n\n💡 Intenta con términos más específicos o verifica que la canción esté disponible en Spotify.`)
    } else {
      alert(`❌ Error agregando a Spotify: ${errorMessage}`)
    }
  } finally {
    addingToQueue.value = false
  }
}

const skip = () => {
  cleanedTitle.value = ''
  emit('skip')
}
</script>

<style scoped>

.recommendation-card {
  background: var(--spotify-surface);
  border-radius: 8px;
  padding: 1.5rem;
  border: 1px solid var(--spotify-border);
}

.recommendation-card h3 {
  margin: 0 0 1rem;
  font-size: 1.1rem;
  color: var(--spotify-text);
  font-weight: 700;
}

.loading {
  text-align: center;
  padding: 2rem;
  color: var(--spotify-subtext);
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

.recommendation-content {
  animation: fadeIn 0.4s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(5px); }
  to { opacity: 1; transform: translateY(0); }
}

.badge {
  display: inline-block;
  padding: 0.3rem 0.8rem;
  border-radius: 500px;
  font-size: 0.75rem;
  font-weight: 700;
  margin-bottom: 1rem;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.badge.auto {
  background: var(--spotify-green);
  color: var(--spotify-base);
}

.badge.manual {
  background: var(--spotify-surface-hover);
  color: var(--spotify-text);
  border: 1px solid var(--spotify-border);
}

.auto-mode h4 {
  font-size: 1.5rem;
  color: var(--spotify-green);
  margin: 0.5rem 0;
  font-weight: 700;
}

.song-name {
  font-size: 1.2rem;
  font-weight: 700;
  color: var(--spotify-text);
  margin: 0.3rem 0;
}

.raw-title {
  font-size: 0.85rem;
  color: var(--spotify-subtext);
  margin: 0.5rem 0;
}

.manual-mode .label {
  font-weight: 700;
  color: var(--spotify-subtext);
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

.input-clean {
  width: 100%;
  padding: 0.8rem 1rem;
  background: var(--spotify-base);
  border: 1px solid var(--spotify-border);
  color: var(--spotify-text);
  border-radius: 4px;
  font-size: 1rem;
  margin: 0.5rem 0 1rem;
  transition: all 0.3s ease;
}

.input-clean:focus {
  outline: none;
  border-color: var(--spotify-text);
  background: var(--spotify-surface-hover);
}

.actions {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
}

.btn {
  flex: 1;
  padding: 0.8rem 1.5rem;
  border: none;
  border-radius: 500px;
  font-size: 0.95rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none !important;
}

.btn-primary {
  background: var(--spotify-green);
  color: var(--spotify-base);
}

.btn-primary:hover:not(:disabled) {
  transform: scale(1.04);
  background: var(--spotify-green-hover);
}

.btn-secondary {
  background: transparent;
  color: var(--spotify-text);
  border: 1px solid var(--spotify-subtext);
}

.btn-secondary:hover {
  border-color: var(--spotify-text);
  transform: scale(1.04);
}

.no-recommendation {
  text-align: center;
  padding: 2rem;
  color: var(--spotify-subtext);
}

.no-recommendation .btn-secondary {
  margin-top: 1rem;
}

</style>
