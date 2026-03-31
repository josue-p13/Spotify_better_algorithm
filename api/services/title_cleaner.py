from google import genai
from google.genai import types
import json
from typing import Optional, Dict
import asyncio

async def clean_title_with_ai(raw_title: str, api_key: str) -> Optional[Dict[str, str]]:
    """
    Limpia un título de YouTube usando Gemini AI
    """
    try:
        # Ejecutar la llamada a la API en un thread separado para no bloquear
        def _sync_clean():
            client = genai.Client(api_key=api_key)
            
            # 🔍 DEBUG: Listar modelos disponibles si falla el primero
            try:
                print(f"🤖 Intentando usar gemini-2.5-flash para: {raw_title[:50]}...")
                
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
                
                # Intentar con gemini-2.5-flash primero
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt
                )
                
            except Exception as model_error:
                print(f"❌ Error con gemini-2.5-flash: {model_error}")
                print("🔄 Intentando con gemini-1.5-flash...")
                
                try:
                    # Fallback a gemini-1.5-flash
                    response = client.models.generate_content(
                        model='gemini-1.5-flash',
                        contents=prompt
                    )
                    print("✅ Usando gemini-1.5-flash como fallback")
                    
                except Exception as fallback_error:
                    print(f"❌ Error con gemini-1.5-flash: {fallback_error}")
                    print("🔄 Listando modelos disponibles...")
                    
                    try:
                        # Listar modelos disponibles para debug
                        models = client.models.list()
                        available_models = [model.name for model in models]
                        print(f"📋 Modelos disponibles: {available_models[:5]}...")  # Solo primeros 5
                        
                        # Intentar con el primer modelo generativo disponible
                        for model_name in available_models:
                            if 'gemini' in model_name.lower() and 'generate' in str(model_name):
                                print(f"🔄 Intentando con: {model_name}")
                                response = client.models.generate_content(
                                    model=model_name,
                                    contents=prompt
                                )
                                break
                        else:
                            raise Exception("No se encontró ningún modelo gemini compatible")
                            
                    except Exception as list_error:
                        print(f"❌ Error listando modelos: {list_error}")
                        raise list_error
            
            texto_limpio = response.text.strip().replace("```json", "").replace("```", "").strip()
            print(f"🤖 Respuesta IA: {texto_limpio}")
            return json.loads(texto_limpio)
        
        # Ejecutar en thread pool para no bloquear el event loop
        loop = asyncio.get_event_loop()
        datos_json = await loop.run_in_executor(None, _sync_clean)
        return datos_json
        
    except json.JSONDecodeError:
        return None
    except Exception as e:
        print(f"Error in clean_title_with_ai: {e}")
        return None
