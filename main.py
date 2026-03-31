import time
from spotify_music_now import obtener_cancion_actual_spotify
from serch_youtu_music_now import buscar_cancion_en_youtube
from serch_next import capturar_siguiente_sugerencia
from title_scraper import obtener_titulo_video
from IA_title_cleaner import limpiar_titulo_con_ia
from put_music_on_spotify import agregar_a_cola_spotify
import db_manager  # Importamos nuestro nuevo manejador de base de datos

def procesar_nueva_cancion(cancion_actual):
    print(f"\n=========================================================")
    print(f"🔄 ¡Nueva canción detectada!: {cancion_actual}")
    print(f"=========================================================")
    
    # 1. Buscamos esa canción en YouTube y obtenemos el Mix
    link_inicial = buscar_cancion_en_youtube(cancion_actual)
    
    if link_inicial:
        enlace_actual_busqueda = link_inicial
        
        # Bucle que seguirá buscando sugerencias hasta encontrar una canción nueva
        while True:
            # 2. Ejecutar Playwright silenciado para capturar el siguiente de la lista
            print("\n--- Obteniendo el enlace del siguiente video (sugerencia) ---")
            nuevo_link = capturar_siguiente_sugerencia(enlace_actual_busqueda)
            
            if not nuevo_link:
                print("❌ No se pudo obtener el nuevo enlace de sugerencia.")
                break
                
            # 3. Extraer título original rápido con oEmbed
            print("\n--- Extrayendo el título del nuevo video ---")
            titulo_sucio = obtener_titulo_video(nuevo_link)
            print(f"Título original: {titulo_sucio}")
            
            # 4. Limpiarlo usando IA
            print("\n--- Limpiando el título con IA ---")
            datos_limpios = limpiar_titulo_con_ia(titulo_sucio)
            
            if datos_limpios:
                artista = datos_limpios.get('artista')
                cancion = datos_limpios.get('cancion')
                
                # VERIFICACIÓN EN BASE DE DATOS
                if db_manager.cancion_ya_escuchada(artista, cancion):
                    print(f"\n⚠️ La canción '{artista} - {cancion}' ya está en el historial.")
                    print("➡️ Buscando la sugerencia siguiente de esta...")
                    enlace_actual_busqueda = nuevo_link # Hacemos que el próximo ciclo busque a partir de este video
                    continue # Vuelve al inicio del while
                
                # Si es nueva, continuamos aquí:
                print(f"\n🎉 ¡Nueva Sugerencia perfecta encontrada!")
                print(f"👤 Artista: {artista}")
                print(f"🎵 Canción: {cancion}")
                
                # 5. Añadir la canción estructurada a la cola de Spotify
                agregado = agregar_a_cola_spotify(artista=artista, cancion=cancion)
                
                if agregado:
                    # 6. Guardamos en el historial para no volver a repetirla
                    db_manager.guardar_en_historial(artista, cancion)
                    print("✅ Proceso completado. Canción guardada en el historial local.")
                break # Rompemos el ciclo porque ya encontramos y encolamos una nueva
            else:
                print("\n❌ No se pudo limpiar el título con IA. Saltando sugerencia...")
                enlace_actual_busqueda = nuevo_link
                continue
    else:
        print("❌ No pudimos obtener el link inicial de YouTube.")

def iniciar_daemon():
    db_manager.inicializar_bd() # Creamos la base de datos si no existe
    ultima_cancion = None
    print("🚀 Iniciando el Motor de Recomendaciones Continuo (YouTube -> Spotify)")
    print("Escuchando tu Spotify... (Presiona Ctrl+C para detener)\n")
    
    while True:
        try:
            # Pedimos la canción a Spotify pero en modo silencioso para no spamear la consola
            cancion_actual = obtener_cancion_actual_spotify(silencioso=True)
            
            # Si hay una canción sonando Y es diferente a la última que procesamos:
            if cancion_actual and cancion_actual != ultima_cancion:
                procesar_nueva_cancion(cancion_actual)
                # Actualizamos cuál fue la última canción para no repetir búsquedas
                ultima_cancion = cancion_actual
                print("\n⏳ Esperando a la siguiente canción...")
                
            # Dormimos el programa 10 segundos antes de volver a checar el estado
            time.sleep(10)
            
        except spotipy.exceptions.SpotifyException as e:
            print(f"Error de Spotify: {e}")
            time.sleep(15) # Esperar si hubo un error temporal
        except Exception as e:
            print(f"Error inesperado en el ciclo principal: {e}")
            time.sleep(15)

if __name__ == "__main__":
    try:
        iniciar_daemon()
    except KeyboardInterrupt:
        print("\n\n🛑 Programa detenido por el usuario. ¡Hasta la próxima!")
    finally:
        # Limpieza del historial al cerrar el programa
        db_manager.limpiar_historial()
