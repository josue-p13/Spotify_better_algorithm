export interface SpotifyCredentials {
  client_id: string
  client_secret: string
  redirect_uri: string
}

export interface Track {
  is_playing: boolean
  track_name?: string
  artists?: string[]
  album?: string
  duration_ms?: number
  progress_ms?: number
  image_url?: string
  formatted?: string
  message?: string
}

export interface Suggestion {
  title: string
  url: string
}

export interface Recommendation {
  mode: 'auto' | 'manual'
  video_url: string
  raw_title: string
  artista?: string
  cancion?: string
  is_new?: boolean
}

export interface CleanedTitle {
  success: boolean
  mode: 'auto' | 'manual'
  artista?: string
  cancion?: string
  raw_title?: string
  message?: string
}
