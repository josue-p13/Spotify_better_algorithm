<template>
  <div class="config-page">
    <div class="config-container">
      <div class="config-header">
        <h1>🎵 Spotify Better Algorithm</h1>
        <p>Configuración Inicial</p>
      </div>

      <div class="config-form">
        <div class="form-section">
          <h2>🔐 Credenciales de Spotify (Obligatorias)</h2>
          <p class="section-desc">
            Obtén tus credenciales en: 
            <a href="https://developer.spotify.com/dashboard" target="_blank">Spotify Developer Dashboard</a>
          </p>

          <div class="form-group">
            <label for="clientId">Client ID:</label>
            <input 
              id="clientId"
              v-model="config.client_id" 
              type="text" 
              placeholder="Tu Client ID de Spotify"
              required
            />
          </div>

          <div class="form-group">
            <label for="clientSecret">Client Secret:</label>
            <input 
              id="clientSecret"
              v-model="config.client_secret" 
              type="password" 
              placeholder="Tu Client Secret de Spotify"
              required
            />
          </div>

          <div class="form-group">
            <label for="redirectUri">Redirect URI:</label>
            <input 
              id="redirectUri"
              v-model="config.redirect_uri" 
              type="text" 
              placeholder="http://127.0.0.1:8888/callback"
              required
            />
            <small>Debe coincidir con la configurada en Spotify Developer Dashboard</small>
          </div>
        </div>

        <div class="form-section">
          <h2>🤖 API Key de Gemini (Opcional)</h2>
          <p class="section-desc">
            Solo necesaria para el modo automático. Obtén tu API Key en: 
            <a href="https://aistudio.google.com/app/apikey" target="_blank">Google AI Studio</a>
          </p>

          <div class="form-group">
            <label for="geminiKey">Gemini API Key:</label>
            <input 
              id="geminiKey"
              v-model="config.gemini_api_key" 
              type="password" 
              placeholder="Tu API Key de Gemini (opcional)"
            />
            <small>Sin esta key, solo funcionará el modo manual</small>
          </div>
        </div>

        <div v-if="error" class="error-message">
          ⚠️ {{ error }}
        </div>

        <div class="form-actions">
          <button 
            @click="saveConfig" 
            class="btn-save"
            :disabled="!isValidConfig"
          >
            ✅ Guardar Configuración
          </button>
        </div>

        <div class="help-section">
          <details>
            <summary>❓ ¿Cómo obtengo las credenciales de Spotify?</summary>
            <ol>
              <li>Ve a <a href="https://developer.spotify.com/dashboard" target="_blank">Spotify Developer Dashboard</a></li>
              <li>Inicia sesión con tu cuenta de Spotify</li>
              <li>Haz clic en "Create an App"</li>
              <li>Dale un nombre y descripción a tu app</li>
              <li>Copia el <strong>Client ID</strong> y <strong>Client Secret</strong></li>
              <li>Haz clic en "Edit Settings"</li>
              <li>En "Redirect URIs", agrega: <code>http://127.0.0.1:8888/callback</code></li>
              <li>Guarda los cambios</li>
            </ol>
          </details>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import type { SpotifyCredentials } from '@/types'

const emit = defineEmits<{
  configured: [credentials: SpotifyCredentials, geminiKey: string]
}>()

const config = ref({
  client_id: '',
  client_secret: '',
  redirect_uri: 'http://127.0.0.1:8888/callback',
  gemini_api_key: ''
})

const error = ref('')

const isValidConfig = computed(() => {
  return config.value.client_id.trim() !== '' &&
         config.value.client_secret.trim() !== '' &&
         config.value.redirect_uri.trim() !== ''
})

const saveConfig = () => {
  if (!isValidConfig.value) {
    error.value = 'Por favor, completa todos los campos obligatorios de Spotify'
    return
  }

  const credentials: SpotifyCredentials = {
    client_id: config.value.client_id.trim(),
    client_secret: config.value.client_secret.trim(),
    redirect_uri: config.value.redirect_uri.trim()
  }

  // Guardar en localStorage
  localStorage.setItem('spotify_credentials', JSON.stringify(credentials))
  localStorage.setItem('gemini_api_key', config.value.gemini_api_key.trim())

  emit('configured', credentials, config.value.gemini_api_key.trim())
}

// Cargar configuración guardada si existe
const loadSavedConfig = () => {
  const savedCreds = localStorage.getItem('spotify_credentials')
  const savedGemini = localStorage.getItem('gemini_api_key')
  
  if (savedCreds) {
    const creds = JSON.parse(savedCreds)
    config.value.client_id = creds.client_id
    config.value.client_secret = creds.client_secret
    config.value.redirect_uri = creds.redirect_uri
  }
  
  if (savedGemini) {
    config.value.gemini_api_key = savedGemini
  }
}

loadSavedConfig()
</script>

<style scoped>

.config-page {
  min-height: 100vh;
  background-color: var(--spotify-base);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.config-container {
  background: var(--spotify-surface);
  border-radius: 8px;
  padding: 2.5rem;
  max-width: 600px;
  width: 100%;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5);
  border: 1px solid var(--spotify-border);
}

.config-header {
  text-align: center;
  margin-bottom: 2rem;
}

.config-header h1 {
  font-size: 2rem;
  margin: 0 0 0.5rem;
  color: var(--spotify-green);
  font-weight: 700;
}

.config-header p {
  font-size: 1.1rem;
  color: var(--spotify-subtext);
  margin: 0;
}

.config-form {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.form-section h2 {
  font-size: 1.3rem;
  color: var(--spotify-text);
  margin: 0 0 0.5rem;
  font-weight: 700;
}

.section-desc {
  font-size: 0.95rem;
  color: var(--spotify-subtext);
  margin: 0 0 1rem;
  line-height: 1.5;
}

.section-desc a {
  color: var(--spotify-text);
  text-decoration: none;
  font-weight: 600;
}

.section-desc a:hover {
  text-decoration: underline;
  color: var(--spotify-green);
}

.form-group {
  margin-bottom: 1.2rem;
}

.form-group label {
  display: block;
  font-weight: 700;
  color: var(--spotify-text);
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

.form-group input {
  width: 100%;
  padding: 0.8rem 1rem;
  background: var(--spotify-base);
  border: 1px solid var(--spotify-border);
  color: var(--spotify-text);
  border-radius: 4px;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.form-group input:focus {
  outline: none;
  border-color: var(--spotify-text);
  background: var(--spotify-surface-hover);
}

.form-group input::placeholder {
  color: var(--spotify-subtext);
}

.form-group small {
  display: block;
  margin-top: 0.4rem;
  font-size: 0.8rem;
  color: var(--spotify-subtext);
}

.error-message {
  background: #E22134;
  color: white;
  padding: 1rem;
  border-radius: 4px;
  font-weight: 600;
  font-size: 0.9rem;
}

.form-actions {
  margin-top: 1rem;
}

.btn-save {
  width: 100%;
  padding: 1rem;
  font-size: 1rem;
  font-weight: 700;
  border: none;
  border-radius: 500px;
  background-color: var(--spotify-green);
  color: var(--spotify-base);
  cursor: pointer;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.btn-save:hover:not(:disabled) {
  transform: scale(1.04);
  background-color: var(--spotify-green-hover);
}

.btn-save:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

.help-section {
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--spotify-border);
}

.help-section details {
  background: var(--spotify-base);
  border-radius: 8px;
  padding: 1rem;
  border: 1px solid var(--spotify-border);
}

.help-section summary {
  cursor: pointer;
  font-weight: 700;
  color: var(--spotify-text);
  user-select: none;
}

.help-section summary:hover {
  color: var(--spotify-green);
}

.help-section ol {
  margin: 1rem 0 0;
  padding-left: 1.5rem;
  color: var(--spotify-subtext);
}

.help-section li {
  margin: 0.5rem 0;
  line-height: 1.6;
}

.help-section code {
  background: var(--spotify-surface-hover);
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  font-family: monospace;
  font-size: 0.9em;
  color: var(--spotify-text);
}

.help-section a {
  color: var(--spotify-text);
  text-decoration: underline;
}

.help-section a:hover {
  color: var(--spotify-green);
}

</style>
