<template>
  <div class="mode-selector">
    <h3>⚙️ Modo de Operación</h3>
    <div class="modes">
      <button 
        :class="['mode-btn', { active: !useApiKey }]"
        @click="$emit('update:useApiKey', false)"
      >
        <span class="icon">✋</span>
        <span class="label">Manual</span>
        <span class="desc">Sin API Key</span>
      </button>
      
      <button 
        :class="['mode-btn', { active: useApiKey }]"
        @click="$emit('update:useApiKey', true)"
      >
        <span class="icon">🤖</span>
        <span class="label">Automático</span>
        <span class="desc">Con API Key</span>
      </button>
    </div>

    <div v-if="useApiKey" class="api-key-input">
      <label for="apiKey">🔑 API Key de Gemini:</label>
      <input 
        id="apiKey"
        type="password" 
        :value="apiKey"
        @input="$emit('update:apiKey', ($event.target as HTMLInputElement).value)"
        placeholder="Ingresa tu API Key de Gemini"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  useApiKey: boolean
  apiKey: string
}>()

defineEmits<{
  'update:useApiKey': [value: boolean]
  'update:apiKey': [value: string]
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
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-bottom: 1rem;
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

.api-key-input label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: var(--spotify-text);
  font-size: 0.9rem;
}

.api-key-input input {
  width: 100%;
  padding: 0.8rem 1rem;
  background: var(--spotify-base);
  border: 1px solid var(--spotify-border);
  border-radius: 4px;
  font-size: 1rem;
  color: var(--spotify-text);
  transition: all 0.3s ease;
}

.api-key-input input:focus {
  outline: none;
  border-color: var(--spotify-text);
  background: var(--spotify-surface-hover);
}

.api-key-input input::placeholder {
  color: var(--spotify-subtext);
}

</style>
