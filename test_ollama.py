#!/usr/bin/env python3
"""
Script de prueba para verificar la integración con Ollama
"""
import asyncio
import sys

async def test_ollama():
    try:
        from api.services.ollama_cleaner import clean_title_with_ollama
        
        print("🧪 Probando limpieza de título con Ollama...")
        print("-" * 50)
        
        # Títulos de prueba
        test_titles = [
            "J. Balvin, Willy William - Mi Gente (Official Video)",
            "Queen - Bohemian Rhapsody (Official Video Remastered)",
            "The Weeknd - Blinding Lights (Official Audio)"
        ]
        
        for i, title in enumerate(test_titles, 1):
            print(f"\n{i}. Título original:")
            print(f"   {title}")
            
            result = await clean_title_with_ollama(title, "qwen2.5")
            
            if result:
                print(f"   ✅ Resultado:")
                print(f"   👤 Artista: {result.get('artista')}")
                print(f"   🎵 Canción: {result.get('cancion')}")
            else:
                print(f"   ❌ Error: No se pudo procesar")
        
        print("\n" + "=" * 50)
        print("✅ Prueba completada")
        
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        print("Asegúrate de haber activado el entorno virtual (.venv)")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n⚠️ Verifica que Ollama esté ejecutándose:")
        print("   1. Ejecuta: ollama serve")
        print("   2. Verifica: curl http://localhost:11434/api/version")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(test_ollama())
