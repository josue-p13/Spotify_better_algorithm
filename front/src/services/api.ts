import type { Track, Recommendation, Suggestion, CleanedTitle, SpotifyCredentials } from '@/types'

const API_URL = 'http://localhost:8000/api'

export const spotifyApi = {
  async getCurrentTrack(credentials: SpotifyCredentials): Promise<Track> {
    const response = await fetch(`${API_URL}/spotify/current-track`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ credentials })
    })
    if (!response.ok) throw new Error('Failed to fetch current track')
    return response.json()
  },

  async addToQueue(credentials: SpotifyCredentials, artista: string, cancion: string) {
    const response = await fetch(`${API_URL}/spotify/add-to-queue`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ credentials, artista, cancion })
    })
    if (!response.ok) throw new Error('Failed to add to queue')
    return response.json()
  },

  async addToQueueManual(credentials: SpotifyCredentials, titulo_limpio: string) {
    const response = await fetch(`${API_URL}/spotify/add-to-queue-manual`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ credentials, titulo_limpio })
    })
    if (!response.ok) throw new Error('Failed to add to queue')
    return response.json()
  },

  // 🎵 Controles de reproducción
  async playMusic(credentials: SpotifyCredentials) {
    const response = await fetch(`${API_URL}/spotify/play`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ credentials })
    })
    if (!response.ok) throw new Error('Failed to play music')
    return response.json()
  },

  async pauseMusic(credentials: SpotifyCredentials) {
    const response = await fetch(`${API_URL}/spotify/pause`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ credentials })
    })
    if (!response.ok) throw new Error('Failed to pause music')
    return response.json()
  },

  async nextTrack(credentials: SpotifyCredentials) {
    const response = await fetch(`${API_URL}/spotify/next`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ credentials })
    })
    if (!response.ok) throw new Error('Failed to skip to next track')
    return response.json()
  },

  async previousTrack(credentials: SpotifyCredentials) {
    const response = await fetch(`${API_URL}/spotify/previous`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ credentials })
    })
    if (!response.ok) throw new Error('Failed to skip to previous track')
    return response.json()
  }
}

export const youtubeApi = {
  async getSuggestions(video_url: string): Promise<{ suggestions: Suggestion[], count: number }> {
    const response = await fetch(`${API_URL}/youtube/suggestions`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ video_url })
    })
    if (!response.ok) throw new Error('Failed to fetch suggestions')
    return response.json()
  },

  async getNextVideo(video_url: string) {
    const response = await fetch(`${API_URL}/youtube/next-video`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ video_url })
    })
    if (!response.ok) throw new Error('Failed to get next video')
    return response.json()
  },

  async cleanTitle(raw_title: string, api_key?: string): Promise<CleanedTitle> {
    const response = await fetch(`${API_URL}/youtube/clean-title`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ raw_title, api_key })
    })
    if (!response.ok) throw new Error('Failed to clean title')
    return response.json()
  }
}

export const recommendationsApi = {
  async getNext(current_song: string, api_key?: string): Promise<Recommendation> {
    const response = await fetch(`${API_URL}/recommendations/get-next`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ current_song, api_key })
    })
    if (!response.ok) throw new Error('Failed to get recommendation')
    return response.json()
  },

  async markProcessed(artista: string, cancion: string) {
    const response = await fetch(`${API_URL}/recommendations/mark-processed`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ artista, cancion })
    })
    if (!response.ok) throw new Error('Failed to mark as processed')
    return response.json()
  }
}
