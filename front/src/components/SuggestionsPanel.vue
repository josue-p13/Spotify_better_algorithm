<template>
  <div class="suggestions-panel">
    <div class="header">
      <h3>💡 Sugerencias de YouTube</h3>
      <button 
        v-if="!showSuggestions" 
        @click="loadSuggestions" 
        class="btn-toggle"
        :disabled="loading"
      >
        {{ loading ? '⏳ Cargando...' : '👁️ Ver Sugerencias' }}
      </button>
      <button 
        v-else 
        @click="showSuggestions = false" 
        class="btn-toggle"
      >
        ❌ Cerrar
      </button>
    </div>

    <div v-if="showSuggestions && suggestions.length > 0" class="suggestions-list">
      <div 
        v-for="(suggestion, index) in suggestions" 
        :key="index"
        class="suggestion-item"
        @click="selectSuggestion(suggestion)"
      >
        <span class="number">{{ index + 1 }}</span>
        <span class="title">{{ suggestion.title }}</span>
        <span class="arrow">→</span>
      </div>
    </div>

    <div v-if="showSuggestions && suggestions.length === 0 && !loading" class="no-suggestions">
      <p>No se encontraron sugerencias</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { Suggestion } from '@/types'
import { youtubeApi } from '@/services/api'

const props = defineProps<{
  videoUrl: string
}>()

const emit = defineEmits<{
  select: [suggestion: Suggestion]
}>()

const showSuggestions = ref(false)
const loading = ref(false)
const suggestions = ref<Suggestion[]>([])

const loadSuggestions = async () => {
  if (!props.videoUrl) return
  
  loading.value = true
  try {
    const result = await youtubeApi.getSuggestions(props.videoUrl)
    suggestions.value = result.suggestions
    showSuggestions.value = true
    
    // Mostrar mensaje si hay sugerencias simuladas
    if (result.suggestions.length > 0 && result.suggestions[0].url.includes('sim')) {
      console.log('💡 Mostrando sugerencias simuladas (YouTube cambió su estructura)')
    }
  } catch (error) {
    console.error('Error al cargar sugerencias:', error)
    // No mostrar alert, solo log en consola
  } finally {
    loading.value = false
  }
}

const selectSuggestion = (suggestion: Suggestion) => {
  // Si es una sugerencia simulada, mostrar mensaje al usuario
  if (suggestion.url.includes('sim')) {
    alert('⚠️ Esta es una sugerencia simulada. Las sugerencias reales de YouTube no están disponibles temporalmente.')
    return
  }
  
  emit('select', suggestion)
  showSuggestions.value = false
}
</script>

<style scoped>

.suggestions-panel {
  background: var(--spotify-surface);
  border-radius: 8px;
  padding: 1.5rem;
  border: 1px solid var(--spotify-border);
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.header h3 {
  margin: 0;
  font-size: 1.1rem;
  color: var(--spotify-text);
  font-weight: 700;
}

.btn-toggle {
  padding: 0.5rem 1rem;
  border: 1px solid var(--spotify-subtext);
  border-radius: 500px;
  background: transparent;
  color: var(--spotify-text);
  font-weight: 700;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.btn-toggle:hover:not(:disabled) {
  transform: scale(1.05);
  border-color: var(--spotify-text);
}

.btn-toggle:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.suggestions-list {
  max-height: 400px;
  overflow-y: auto;
  animation: fadeIn 0.3s ease;
  padding-right: 0.5rem;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-5px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.suggestion-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  border: 1px solid transparent;
  border-radius: 4px;
  margin-bottom: 0.5rem;
  cursor: pointer;
  transition: all 0.2s ease;
  background: var(--spotify-base);
}

.suggestion-item:hover {
  background: var(--spotify-surface-hover);
}

.suggestion-item .number {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 30px;
  height: 30px;
  color: var(--spotify-subtext);
  font-weight: 700;
  font-size: 0.9rem;
  flex-shrink: 0;
}

.suggestion-item:hover .number {
  color: var(--spotify-green);
}

.suggestion-item .title {
  flex: 1;
  color: var(--spotify-text);
  font-size: 0.95rem;
  font-weight: 500;
}

.suggestion-item .arrow {
  font-size: 1.2rem;
  color: var(--spotify-subtext);
  flex-shrink: 0;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.suggestion-item:hover .arrow {
  opacity: 1;
  color: var(--spotify-text);
}

.no-suggestions {
  text-align: center;
  padding: 2rem;
  color: var(--spotify-subtext);
}

</style>
