import json
from typing import Optional, Dict
import asyncio
import aiohttp

async def clean_title_with_ollama(raw_title: str, model_name: str = "qwen2.5") -> Optional[Dict[str, str]]:
    """
    Limpia un título de YouTube usando Ollama (IA local)
    """
    try:
        prompt = f"""
Eres un experto musical. Extrae el nombre del artista principal y el nombre de la canción del siguiente título de un video de YouTube:
"{raw_title}"

Instrucciones:
1. Identifica correctamente quién es el artista y cuál es la canción, sin importar el orden en el que aparezcan.
2. Ignora cualquier texto extra irrelevante como "Official Video", "Letra", "Lyrics", "M/V", fechas, emojis, "feat.", etc.
3. Responde ÚNICA Y EXCLUSIVAMENTE con un JSON válido con el siguiente formato exacto, sin texto adicional ni bloques de código (```):

{{
    "artista": "Nombre del Artista",
    "cancion": "Nombre de la Canción"
}}
"""
        
        print(f"🤖 Procesando con Ollama ({model_name}): {raw_title[:50]}...")
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                'http://localhost:11434/api/generate',
                json={
                    "model": model_name,
                    "prompt": prompt,
                    "stream": False
                }
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    print(f"❌ Error de Ollama: {error_text}")
                    return None
                
                result = await response.json()
                texto_respuesta = result.get('response', '').strip()
                
                texto_limpio = texto_respuesta.replace("```json", "").replace("```", "").strip()
                print(f"🤖 Respuesta Ollama: {texto_limpio}")
                
                datos_json = json.loads(texto_limpio)
                return datos_json
        
    except json.JSONDecodeError as e:
        print(f"❌ Error JSON: {e}")
        print(f"Texto recibido: {texto_limpio if 'texto_limpio' in locals() else 'N/A'}")
        return None
    except aiohttp.ClientError as e:
        print(f"❌ Error de conexión con Ollama: {e}")
        print("⚠️ Verifica que Ollama esté ejecutándose en http://localhost:11434")
        return None
    except Exception as e:
        print(f"❌ Error en clean_title_with_ollama: {e}")
        return None
