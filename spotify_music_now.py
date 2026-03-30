import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# Cargamos el .env
load_dotenv()

def obtener_cancion_actual_spotify(silencioso=False):
    """
    Conecta a la API de Spotify y devuelve la canción que el usuario está escuchando.
    El formato será: 'Artista(s) - Nombre de la canción'
    """
    if not silencioso:
        print("\n--- PASO 1: Consultando Spotify ---")
    
    client_id = os.getenv("SPOTIPY_CLIENT_ID")
    client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
    redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI", "http://127.0.0.1:8888/callback")
    
    if not client_id or not client_secret:
        print("Error: Credenciales de Spotify (SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET) no están en tu archivo .env")
        return None

    # Permiso para leer la canción y unificamos para modificar el playback
    scope = "user-read-currently-playing user-modify-playback-state"
    
    try:
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope=scope
        ))
        
        current_track = sp.current_user_playing_track()
        
        if current_track is not None and current_track.get('item'):
            track = current_track['item']
            song_name = track['name']
            
            # Formatear múltiples artistas si existen
            artists = ", ".join([artist['name'] for artist in track['artists']])
            title = f"{artists} - {song_name}"
            
            if not silencioso:
                print(f"🎵 Escuchando ahora en Spotify: {title}")
            return title
        else:
            if not silencioso:
                print("No se está reproduciendo ninguna canción en Spotify en este momento.")
            return None
            
    except Exception as e:
        print(f"Error al conectar con Spotify: {e}")
        return None

if __name__ == "__main__":
    obtener_cancion_actual_spotify()
