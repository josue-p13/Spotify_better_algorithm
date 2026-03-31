from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import db_manager

router = APIRouter()

class SpotifyCredentials(BaseModel):
    client_id: str
    client_secret: str
    redirect_uri: str

class CurrentTrackRequest(BaseModel):
    credentials: SpotifyCredentials

class AddToQueueRequest(BaseModel):
    credentials: SpotifyCredentials
    artista: str
    cancion: str

class AddToQueueManualRequest(BaseModel):
    credentials: SpotifyCredentials
    titulo_limpio: str

class PlaybackControlRequest(BaseModel):
    credentials: SpotifyCredentials

def get_spotify_client(credentials: SpotifyCredentials):
    if not credentials.client_id or not credentials.client_secret:
        raise HTTPException(status_code=400, detail="Credenciales de Spotify incompletas")
    
    scope = "user-read-currently-playing user-modify-playback-state"
    
    try:
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=credentials.client_id,
            client_secret=credentials.client_secret,
            redirect_uri=credentials.redirect_uri,
            scope=scope,
            cache_path=f".cache-{credentials.client_id}"
        ))
        return sp
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al conectar con Spotify: {str(e)}")

@router.post("/current-track")
async def get_current_track(request: CurrentTrackRequest):
    try:
        sp = get_spotify_client(request.credentials)
        current_track = sp.current_user_playing_track()
        
        if current_track is not None and current_track.get('item'):
            track = current_track['item']
            return {
                "is_playing": current_track.get('is_playing', False),
                "track_name": track['name'],
                "artists": [artist['name'] for artist in track['artists']],
                "album": track['album']['name'],
                "duration_ms": track['duration_ms'],
                "progress_ms": current_track.get('progress_ms', 0),
                "image_url": track['album']['images'][0]['url'] if track['album']['images'] else None,
                "formatted": f"{', '.join([artist['name'] for artist in track['artists']])} - {track['name']}"
            }
        else:
            return {
                "is_playing": False,
                "message": "No hay ninguna canción reproduciéndose"
            }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/add-to-queue")
async def add_to_queue(request: AddToQueueRequest):
    try:
        sp = get_spotify_client(request.credentials)
        
        # 🔍 MÚLTIPLES ESTRATEGIAS DE BÚSQUEDA
        search_queries = [
            f"track:{request.cancion} artist:{request.artista}",  # Búsqueda específica
            f"{request.artista} {request.cancion}",              # Búsqueda general
            f"{request.cancion} {request.artista}",              # Orden invertido
            request.cancion                                       # Solo canción
        ]
        
        track_found = None
        used_query = None
        
        print(f"🔍 Buscando en Spotify: {request.artista} - {request.cancion}")
        
        for i, query in enumerate(search_queries):
            print(f"🔍 Estrategia {i+1}: {query}")
            try:
                resultados = sp.search(q=query, type='track', limit=5)
                
                if resultados['tracks']['items']:
                    # Buscar la mejor coincidencia
                    for track in resultados['tracks']['items']:
                        track_name = track['name'].lower()
                        track_artists = [artist['name'].lower() for artist in track['artists']]
                        
                        cancion_lower = request.cancion.lower()
                        artista_lower = request.artista.lower()
                        
                        # Verificar si el título coincide (al menos 70%)
                        title_similarity = len(set(cancion_lower.split()) & set(track_name.split())) / max(len(cancion_lower.split()), len(track_name.split()))
                        
                        # Verificar si algún artista coincide
                        artist_match = any(artista_lower in track_artist or track_artist in artista_lower for track_artist in track_artists)
                        
                        if title_similarity > 0.6 or artist_match:
                            track_found = track
                            used_query = query
                            print(f"✅ Canción encontrada con estrategia {i+1}: {track['name']} - {', '.join([a['name'] for a in track['artists']])}")
                            break
                    
                    if track_found:
                        break
            except Exception as search_error:
                print(f"❌ Error en búsqueda {i+1}: {search_error}")
                continue
        
        if track_found:
            track_uri = track_found['uri']
            sp.add_to_queue(track_uri)
            
            # 🔥 GUARDAR EN HISTORIAL PARA EVITAR REPETICIONES
            db_manager.guardar_en_historial(request.artista, request.cancion)
            print(f"💾 Guardado en historial: {request.artista} - {request.cancion}")
            
            return {
                "success": True,
                "message": f"Añadida a la cola: {track_found['name']} - {', '.join([a['name'] for a in track_found['artists']])}",
                "track_info": track_found,
                "search_query_used": used_query
            }
        else:
            # 📝 RESPUESTA DETALLADA PARA DEBUGGING
            print(f"❌ No se encontró en Spotify: {request.artista} - {request.cancion}")
            raise HTTPException(
                status_code=404, 
                detail={
                    "error": "No se encontró la canción en Spotify",
                    "artista_buscado": request.artista,
                    "cancion_buscada": request.cancion,
                    "queries_probadas": search_queries,
                    "sugerencia": "La canción puede no estar disponible en Spotify o la IA extrajo mal los datos"
                }
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/add-to-queue-manual")
async def add_to_queue_manual(request: AddToQueueManualRequest):
    try:
        sp = get_spotify_client(request.credentials)
        
        resultados = sp.search(q=request.titulo_limpio, type='track', limit=1)
        
        if resultados['tracks']['items']:
            track = resultados['tracks']['items'][0]
            track_uri = track['uri']
            sp.add_to_queue(track_uri)
            
            # 🔥 GUARDAR EN HISTORIAL PARA EVITAR REPETICIONES
            artista = ', '.join([artist['name'] for artist in track['artists']])
            cancion = track['name']
            db_manager.guardar_en_historial(artista, cancion)
            print(f"💾 Guardado en historial (manual): {artista} - {cancion}")
            
            return {
                "success": True,
                "message": f"Añadida a la cola: {track['name']}",
                "track_info": track
            }
        else:
            raise HTTPException(status_code=404, detail="No se encontró la canción en Spotify")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 🎵 CONTROLES DE REPRODUCCIÓN

@router.post("/play")
async def play_music(request: PlaybackControlRequest):
    """Reproduce o reanuda la música"""
    try:
        sp = get_spotify_client(request.credentials)
        sp.start_playback()
        return {
            "success": True,
            "message": "Reproducción iniciada"
        }
    except HTTPException:
        raise
    except Exception as e:
        # Si no hay dispositivo activo, dar información útil
        if "NO_ACTIVE_DEVICE" in str(e):
            raise HTTPException(
                status_code=404, 
                detail="No hay dispositivos de Spotify activos. Abre Spotify en tu dispositivo primero."
            )
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/pause")
async def pause_music(request: PlaybackControlRequest):
    """Pausa la música"""
    try:
        sp = get_spotify_client(request.credentials)
        sp.pause_playback()
        return {
            "success": True,
            "message": "Reproducción pausada"
        }
    except HTTPException:
        raise
    except Exception as e:
        if "NO_ACTIVE_DEVICE" in str(e):
            raise HTTPException(
                status_code=404, 
                detail="No hay dispositivos de Spotify activos."
            )
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/next")
async def skip_to_next(request: PlaybackControlRequest):
    """Salta a la siguiente canción"""
    try:
        sp = get_spotify_client(request.credentials)
        sp.next_track()
        return {
            "success": True,
            "message": "Saltando a la siguiente canción"
        }
    except HTTPException:
        raise
    except Exception as e:
        if "NO_ACTIVE_DEVICE" in str(e):
            raise HTTPException(
                status_code=404, 
                detail="No hay dispositivos de Spotify activos."
            )
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/previous")
async def skip_to_previous(request: PlaybackControlRequest):
    """Salta a la canción anterior"""
    try:
        sp = get_spotify_client(request.credentials)
        sp.previous_track()
        return {
            "success": True,
            "message": "Saltando a la canción anterior"
        }
    except HTTPException:
        raise
    except Exception as e:
        if "NO_ACTIVE_DEVICE" in str(e):
            raise HTTPException(
                status_code=404, 
                detail="No hay dispositivos de Spotify activos."
            )
        raise HTTPException(status_code=500, detail=str(e))

