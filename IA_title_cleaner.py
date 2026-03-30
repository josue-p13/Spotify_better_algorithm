import google.generativeai as genai
import json
import os
from dotenv import load_dotenv

# Cargamos las variables de entorno del archivo .env
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

def limpiar_titulo_con_ia(titulo_bruto):
    if not API_KEY:
        print("Error: No se encontró GEMINI_API_KEY en el archivo .env")
        return None
        
    print(f"[{titulo_bruto}] -> Analizando con Gemini...")
    
    # Usamos el modelo gemini-2.5-flash
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = f"""
    Eres un experto musical. Extrae el nombre del artista principal y el nombre de la canción del siguiente título de un video de YouTube:
    "{titulo_bruto}"

    Instrucciones:
    1. Identifica correctamente quién es el artista y cuál es la canción, sin importar el orden en el que aparezcan.
    2. Ignora cualquier texto extra irrelevante como "Official Video", "Letra", "Lyrics", "M/V", fechas, emojis, "feat.", etc.
    3. Responde ÚNICA Y EXCLUSIVAMENTE con un JSON válido con el siguiente formato exacto, sin texto adicional ni bloques de código (```):
    
    {{
        "artista": "Nombre del Artista",
        "cancion": "Nombre de la Canción"
    }}
    """
    
    try:
        respuesta = model.generate_content(prompt)
        # Limpiamos posibles formatos Markdown
        texto_limpio = respuesta.text.strip().replace("```json", "").replace("```", "").strip()
        
        datos_json = json.loads(texto_limpio)
        return datos_json
        
    except json.JSONDecodeError:
        print("Error: La IA no devolvió un formato JSON válido.")
        return None
    except Exception as e:
        print(f"Error al conectar con la API de Gemini: {e}")
        return None

if __name__ == "__main__":
    titulos_prueba = [
        "J. Balvin, Willy William - Mi Gente (Official Video)",
        "Bohemian Rhapsody - Queen (Official Music Video) [HD]"
    ]
    for titulo in titulos_prueba:
        resultado = limpiar_titulo_con_ia(titulo)
        if resultado:
            print(f"👤 Artista: {resultado.get('artista')}\n🎵 Canción: {resultado.get('cancion')}\n")