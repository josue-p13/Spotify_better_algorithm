import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# Cargamos el .env
load_dotenv()

def agregar_a_cola_spotify(artista, cancion):
    """
    Busca la canción en Spotify y la añade a la cola de reproducción del usuario.
    Requiere que el usuario tenga Spotify Premium para usar la API de modificación de cola
    y un dispositivo actualmente activo reproduciendo música.
    """
    print("\n--- PASO 6: Añadiendo sugerencia a la cola de Spotify ---")
    
    client_id = os.getenv("SPOTIPY_CLIENT_ID")
    client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
    redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI", "http://127.0.0.1:8888/callback")
    
    if not client_id or not client_secret:
        print("Error: Faltan credenciales de Spotify en .env")
        return False

    # Permisos necesarios para buscar y añadir a la cola
    scope = "user-read-currently-playing user-modify-playback-state"
    
    try:
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope=scope
        ))
        
        # Búsqueda amplia para mayor precisión (los títulos de IA pueden variar un poco)
        busqueda = f"{artista} {cancion}"
        print(f"Buscando en Spotify: '{busqueda}'...")
        
        results = sp.search(q=busqueda, limit=1, type='track')
        tracks = results.get('tracks', {}).get('items', [])
        
        if not tracks:
            print("❌ No se encontró la canción en Spotify.")
            return False
            
        track = tracks[0]
        track_uri = track['uri']
        track_name = track['name']
        track_artist = ", ".join([a['name'] for a in track['artists']])
        
        print(f"🎵 Coincidencia encontrada: {track_artist} - {track_name}")
        
        # Añadir a la cola
        sp.add_to_queue(track_uri)
        print("✅ ¡Canción añadida exitosamente a tu cola de Spotify!")
        return True
        
    except spotipy.exceptions.SpotifyException as e:
        print(f"❌ Error de Spotify: {e}")
        print("Nota: Para añadir a la cola, necesitas:")
        print("1. Cuenta de Spotify Premium (limitación ofical de la API de Spotify).")
        print("2. Tener la app de Spotify abierta y reproduciendo algo en este momento.")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

if __name__ == "__main__":
    # Prueba
    agregar_a_cola_spotify("Daft Punk", "Get Lucky")
