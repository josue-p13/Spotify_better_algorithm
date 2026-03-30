import urllib.request
import urllib.parse
import json

# Importamos todo nuestro ecosistema
from spotify_music_now import obtener_cancion_actual_spotify
from serch_youtu_music_now import buscar_cancion_en_youtube
from serch_next import capturar_siguiente_sugerencia
from IA_title_cleaner import limpiar_titulo_con_ia
from put_music_on_spotify import agregar_a_cola_spotify

def obtener_titulo_video(url):
    print(f"Obteniendo el título de: {url}")
    
    # ¡AQUÍ ESTÁ LA MAGIA! Codificamos la URL para que los '&' y '=' no rompan la API
    url_codificada = urllib.parse.quote(url)
    
    # Usamos la API pública oEmbed de YouTube
    oembed_url = f"https://www.youtube.com/oembed?url={url_codificada}&format=json"
    
    try:
        with urllib.request.urlopen(oembed_url) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data.get("title", "Título desconocido")
    except Exception as e:
        print(f"Error al consultar el título: {e}")
        return "No se pudo obtener el título"

if __name__ == "__main__":
    # PASO 1: Qué canción hay en Spotify?
    cancion_actual = obtener_cancion_actual_spotify()
    
    if cancion_actual:
        # PASO 2: Buscar esa canción en YouTube y obtener el Mix
        link_inicial = buscar_cancion_en_youtube(cancion_actual)
        
        if link_inicial:
            # PASO 3: Ejecutar Playwright silenciado para capturar el siguiente de la lista
            print("\n--- PASO 3: Obteniendo el enlace del siguiente video (sugerencia) ---")
            nuevo_link = capturar_siguiente_sugerencia(link_inicial)
            
            if nuevo_link:
                # PASO 4: Extraer título original rápido con oEmbed
                print("\n--- PASO 4: Extrayendo el título del nuevo video ---")
                titulo_sucio = obtener_titulo_video(nuevo_link)
                print(f"Título original: {titulo_sucio}")
                
                # PASO 5: Limpiarlo usando IA
                print("\n--- PASO 5: Limpiando el título con IA ---")
                datos_limpios = limpiar_titulo_con_ia(titulo_sucio)
                
                if datos_limpios:
                    print(f"\n🎉 ¡Sugerencia perfecta encontrada!")
                    print(f"👤 Artista: {datos_limpios.get('artista')}")
                    print(f"🎵 Canción: {datos_limpios.get('cancion')}")
                    
                    # PASO 6: Añadir la canción limpia extraída a la cola de Spotify
                    agregar_a_cola_spotify(
                        artista=datos_limpios.get('artista'),
                        cancion=datos_limpios.get('cancion')
                    )
                    
                else:
                    print("\nNo se pudo limpiar el título con IA.")
            else:
                print("No se pudo obtener el nuevo enlace de sugerencia.")
        else:
            print("No pudimos obtener el link inicial de YouTube.")
    else:
        print("Asegúrate de tener la app de Spotify abierta y reproduciendo una canción.")
