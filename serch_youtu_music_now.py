import urllib.request
import urllib.parse
import re

def buscar_cancion_en_youtube(query):
    """
    Busca la canción en YouTube y devuelve el primer link encontrado adaptado como Mix (Playlist).
    """
    print("\n--- PASO 2: Buscando canción en YouTube ---")
    print(f"Buscando: '{query}'")
    
    # Codificamos la cadena de texto para la URL (convierte espacios en %20, etc.)
    query_encoded = urllib.parse.quote(query)
    url = f"https://www.youtube.com/results?search_query={query_encoded}"
    
    try:
        # Añadimos un user-agent básico para que YouTube nos dé respuesta como si fuéramos un navegador
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req).read().decode('utf-8')
        
        # Usamos una expresión regular para encontrar todos los identificadores de videos de YouTube (tienen 11 caracteres)
        video_ids = re.findall(r"\"videoId\":\"([a-zA-Z0-9_-]{11})\"", html)
        
        if video_ids:
            primer_video_id = video_ids[0]
            # Creamos un link de tipo "Mix" de YouTube, para que exista un "Siguiente video" garantizado
            mix_url = f"https://www.youtube.com/watch?v={primer_video_id}&list=RD{primer_video_id}"
            print(f"✅ Video encontrado: {mix_url}")
            return mix_url
        else:
            print("❌ No se encontraron resultados en YouTube.")
            return None
            
    except Exception as e:
        print(f"❌ Error al buscar en YouTube: {e}")
        return None

if __name__ == "__main__":
    link = buscar_cancion_en_youtube("Daft Punk - Get Lucky")
    print(link)
