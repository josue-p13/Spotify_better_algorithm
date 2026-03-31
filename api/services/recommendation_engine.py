from typing import Optional, Dict
from api.services.youtube_scraper import get_next_video
from api.services.title_cleaner import clean_title_with_ai
from serch_youtu_music_now import buscar_cancion_en_youtube
import db_manager

async def get_automatic_recommendation(current_song: str, api_key: Optional[str] = None) -> Optional[Dict]:
    """
    Obtiene automáticamente la siguiente recomendación basada en la canción actual
    """
    try:
        # 1. Buscar la canción en YouTube
        video_url = buscar_cancion_en_youtube(current_song)
        
        if not video_url:
            return None
        
        # 2. Obtener el siguiente video sugerido
        max_attempts = 5
        attempt = 0
        
        while attempt < max_attempts:
            next_video = await get_next_video(video_url)
            
            if not next_video or not next_video.get('title'):
                return None
            
            # 3. Usar el título que ya viene en next_video
            raw_title = next_video['title']
            
            if api_key:
                # Modo automático con IA
                cleaned = await clean_title_with_ai(raw_title, api_key)
                
                if cleaned:
                    artista = cleaned.get('artista')
                    cancion = cleaned.get('cancion')
                    
                    # Verificar si ya fue escuchada
                    if not db_manager.cancion_ya_escuchada(artista, cancion):
                        return {
                            'mode': 'auto',
                            'video_url': next_video['url'],
                            'raw_title': raw_title,
                            'artista': artista,
                            'cancion': cancion,
                            'is_new': True
                        }
                    else:
                        # Si ya fue escuchada, buscar la siguiente
                        video_url = next_video['url']
                        attempt += 1
                        continue
            else:
                # Modo manual - verificar si el título raw ya fue procesado
                # Como no tenemos IA, verificamos si el raw_title contiene palabras clave 
                # de canciones ya en historial
                
                # Obtener historial para comparación básica
                import sqlite3
                conn = sqlite3.connect('historial_canciones.db')
                cursor = conn.cursor()
                cursor.execute('SELECT artista, cancion FROM historial')
                historial_records = cursor.fetchall()
                conn.close()
                
                # Verificar si el raw_title es muy similar a algo ya en historial
                title_lower = raw_title.lower()
                is_similar = False
                
                for artista, cancion in historial_records:
                    # Verificar si tanto artista como canción están en el título
                    if (artista.lower() in title_lower and 
                        cancion.lower() in title_lower):
                        print(f"🔄 Título similar encontrado en historial: {artista} - {cancion}")
                        is_similar = True
                        break
                
                if not is_similar:
                    # Título no está en historial, devolverlo
                    return {
                        'mode': 'manual',
                        'video_url': next_video['url'],
                        'raw_title': raw_title
                    }
                else:
                    # Similar encontrado, buscar siguiente
                    video_url = next_video['url']
                    attempt += 1
                    continue
            
            attempt += 1
        
        return None
        
    except Exception as e:
        print(f"Error en get_automatic_recommendation: {e}")
        return None
