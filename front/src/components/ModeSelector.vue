<template>
  <div class="mode-selector">
    <h3>⚙️ Modo de Operación</h3>
    <div class="modes">
      <button 
        :class="['mode-btn', { active: aiMode === 'manual' }]"
        @click="$emit('update:aiMode', 'manual')"
      >
        <span class="icon">✋</span>
        <span class="label">Manual</span>
        <span class="desc">Sin IA</span>
      </button>
      
      <button 
        :class="['mode-btn', { active: aiMode === 'gemini' }]"
        @click="$emit('update:aiMode', 'gemini')"
      >
        <span class="icon">🤖</span>
        <span class="label">IA Gemini</span>
        <span class="desc">API Cloud</span>
      </button>

      <button 
        :class="['mode-btn', { active: aiMode === 'local' }]"
        @click="$emit('update:aiMode', 'local')"
      >
        <span class="icon">💻</span>
        <span class="label">IA Local</span>
        <span class="desc">Ollama</span>
      </button>
    </div>

    <div v-if="aiMode === 'gemini'" class="api-key-input">
      <label for="apiKey">🔑 API Key de Gemini:</label>
      <input 
        id="apiKey"
        type="password" 
        :value="apiKey"
        @input="$emit('update:apiKey', ($event.target as HTMLInputElement).value)"
        placeholder="Ingresa tu API Key de Gemini"
      />
    </div>

    <div v-if="aiMode === 'local'" class="local-ai-input">
      <label for="modelName">🧠 Modelo de Ollama:</label>
      <input 
        id="modelName"
        type="text" 
        :value="localModel"
        @input="$emit('update:localModel', ($event.target as HTMLInputElement).value)"
        placeholder="qwen2.5"
      />
      <small class="hint">Asegúrate de que Ollama esté ejecutándose en http://localhost:11434</small>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  aiMode: 'manual' | 'gemini' | 'local'
  apiKey: string
  localModel: string
}>()

defineEmits<{
  'update:aiMode': [value: 'manual' | 'gemini' | 'local']
  'update:apiKey': [value: string]
  'update:localModel': [value: string]
}>()
</script>

<style scoped>

.mode-selector {
  background: var(--spotify-surface);
  border-radius: 8px;
  padding: 1.5rem;
  border: 1px solid var(--spotify-border);
}

.mode-selector h3 {
  margin: 0 0 1rem;
  font-size: 1.1rem;
  color: var(--spotify-text);
  font-weight: 700;
}

.modes {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 1rem;
  margin-bottom: 1rem;
}

@media (max-width: 768px) {
  .modes {
    grid-template-columns: 1fr;
  }
}

.mode-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  padding: 1.5rem 1rem;
  border: 1px solid var(--spotify-border);
  border-radius: 6px;
  background: var(--spotify-base);
  cursor: pointer;
  transition: all 0.3s ease;
  color: var(--spotify-text);
}

.mode-btn:hover {
  background: var(--spotify-surface-hover);
  border-color: var(--spotify-subtext);
}

.mode-btn.active {
  border-color: var(--spotify-green);
  background: var(--spotify-surface-active);
  color: var(--spotify-green);
}

.mode-btn .icon {
  font-size: 2rem;
}

.mode-btn .label {
  font-size: 1.1rem;
  font-weight: 700;
}

.mode-btn .desc {
  font-size: 0.85rem;
  color: var(--spotify-subtext);
}

.mode-btn.active .desc {
  color: var(--spotify-text);
}

.api-key-input {
  margin-top: 1rem;
  animation: fadeIn 0.3s ease;
}

.local-ai-input {
  margin-top: 1rem;
  animation: fadeIn 0.3s ease;
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

.api-key-input label,
.local-ai-input label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: var(--spotify-text);
  font-size: 0.9rem;
}

.api-key-input input,
.local-ai-input input {
  width: 100%;
  padding: 0.8rem 1rem;
  background: var(--spotify-base);
  border: 1px solid var(--spotify-border);
  border-radius: 4px;
  font-size: 1rem;
  color: var(--spotify-text);
  transition: all 0.3s ease;
}

.api-key-input input:focus,
.local-ai-input input:focus {
  outline: none;
  border-color: var(--spotify-text);
  background: var(--spotify-surface-hover);
}

.api-key-input input::placeholder,
.local-ai-input input::placeholder {
  color: var(--spotify-subtext);
}

.local-ai-input .hint {
  display: block;
  margin-top: 0.5rem;
  font-size: 0.8rem;
  color: var(--spotify-subtext);
  font-style: italic;
}

</style>
