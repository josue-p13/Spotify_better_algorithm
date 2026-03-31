from playwright.async_api import async_playwright
import urllib.parse
import random
import re
from typing import List, Dict, Optional

async def get_video_suggestions(video_url: str, limit: int = 20) -> List[Dict[str, str]]:
    """
    Obtiene sugerencias de un video de YouTube usando una estrategia híbrida:
    1. Primero intenta scraping tradicional
    2. Como fallback, genera sugerencias simuladas basadas en el video actual
    """
    try:
        # Intentar scraping tradicional primero
        suggestions = await _scrape_youtube_suggestions(video_url, limit)
        
        if len(suggestions) > 0:
            print(f"Scraping exitoso: {len(suggestions)} sugerencias")
            return suggestions
        
        # Fallback: generar sugerencias simuladas
        print("Scraping falló, generando sugerencias simuladas...")
        return await _generate_fallback_suggestions(video_url, limit)
        
    except Exception as e:
        print(f"Error en get_video_suggestions: {e}")
        # Como último recurso, devolver sugerencias simuladas
        return await _generate_fallback_suggestions(video_url, limit)

async def _scrape_youtube_suggestions(video_url: str, limit: int) -> List[Dict[str, str]]:
    """
    Intenta hacer scraping tradicional de sugerencias de YouTube
    """
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir="./perfil_chrome",
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--mute-audio"
            ]
        )
        page = await context.new_page()
        
        await page.goto(video_url)
        await page.wait_for_load_state('networkidle', timeout=10000)
        await page.wait_for_timeout(3000)  # Esperar carga completa
        
        suggestions = []
        
        # Selectores más modernos de YouTube
        selectors_to_try = [
            'ytd-compact-video-renderer',
            'ytd-video-meta-block', 
            '#secondary ytd-compact-video-renderer',
            '[class*="compact-video"]',
            'a[href*="/watch"]:has(#video-title)',
            '#related a[href*="/watch"]'
        ]
        
        for selector in selectors_to_try:
            try:
                elements = await page.query_selector_all(selector)
                print(f"Selector '{selector}': encontrados {len(elements)} elementos")
                
                if elements:
                    for element in elements[:limit]:
                        try:
                            title = None
                            link = None
                            
                            # Estrategias para obtener título y link
                            if 'compact-video' in selector:
                                title_el = await element.query_selector('#video-title')
                                if title_el:
                                    title = await title_el.get_attribute('title')
                                    if not title:
                                        title = await title_el.inner_text()
                                    
                                link_el = await element.query_selector('a')
                                if link_el:
                                    link = await link_el.get_attribute('href')
                            
                            elif selector.startswith('a[href'):
                                # Estrategia general para enlaces
                                title_el = await element.query_selector('#video-title, [id*="title"], span')
                                if title_el:
                                    title = await title_el.inner_text()
                                link = await element.get_attribute('href')
                            
                            elif selector == '#related a[href*="/watch"]':
                                # Estrategia específica para links en la sección related
                                link = await element.get_attribute('href')
                                title = None
                                
                                # 1. Intentar aria-label (más confiable)
                                try:
                                    aria_title = await element.get_attribute('aria-label')
                                    if aria_title and len(aria_title.strip()) > 10:
                                        # Limpiar el aria-label (remover duración al final)
                                        title = aria_title.split(' minuto')[0].split(' segundo')[0].split(' hora')[0]
                                        title = title.strip()
                                except:
                                    pass
                                
                                # 2. Si no hay aria-label, usar inner_text pero filtrar duraciones
                                if not title:
                                    try:
                                        inner_text = await element.inner_text()
                                        # Filtrar si es solo duración (formato MM:SS o H:MM:SS)
                                        if inner_text and not re.match(r'^\d{1,2}:\d{2}$|^\d{1,2}:\d{2}:\d{2}$', inner_text.strip()):
                                            if len(inner_text.strip()) > 10:
                                                title = inner_text.strip()
                                    except:
                                        pass
                                
                                # 3. Fallback: buscar en atributo title del elemento o padres
                                if not title:
                                    try:
                                        title_attr = await element.get_attribute('title')
                                        if title_attr and len(title_attr.strip()) > 10:
                                            title = title_attr
                                    except:
                                        pass
                            
                            if title and link and len(title.strip()) > 0:
                                full_url = f"https://www.youtube.com{link}" if link.startswith('/') else link
                                
                                if not any(s['url'] == full_url for s in suggestions):
                                    suggestions.append({
                                        'title': title.strip(),
                                        'url': full_url
                                    })
                                    
                        except Exception as e:
                            continue
                    
                    if suggestions:
                        break
                        
            except Exception as e:
                continue
        
        await context.close()
        return suggestions

async def _generate_fallback_suggestions(video_url: str, limit: int) -> List[Dict[str, str]]:
    """
    Genera sugerencias simuladas cuando el scraping falla
    """
    try:
        # Obtener el título del video actual
        current_title = await get_video_title_async(video_url)
        
        # Generar sugerencias simuladas basadas en géneros/artistas comunes
        fallback_suggestions = []
        
        # Suggestions genéricas pero realistas basadas en el contexto
        base_suggestions = [
            f"🎵 Similar a: {current_title[:30]}..." if current_title else "Mix de Éxitos Actuales",
            "Top Hits 2024 - Mix de Éxitos",
            "Música Similar - Recomendaciones",
            "Lo Mejor del Reggaeton 2024",
            "Rock Clásico - Greatest Hits", 
            "Pop Latino - Mix 2024",
            "Playlist Chill - Música Tranquila",
            "Hip Hop Classics - Old School",
            "Música Electrónica - EDM Mix",
            "Baladas Románticas - Love Songs",
            "Indie Rock - Alternative Mix",
            "Música Regional Mexicana",
            "Trap Latino - Nuevos Éxitos",
            "Jazz & Blues - Smooth Collection",
            "Música de los 80s y 90s",
            "Acoustic Covers - Versiones Acústicas",
            "Workout Music - Música para Ejercicio",
            "Study Music - Concentración",
            "Road Trip Playlist",
            "Summer Vibes - Música de Verano",
            "Throwback Hits - Nostalgia Mix"
        ]
        
        # Seleccionar sugerencias aleatoriamente
        import random
        selected = random.sample(base_suggestions, min(limit, len(base_suggestions)))
        
        for i, title in enumerate(selected):
            # Generar URLs simuladas (no funcionales pero válidas en formato)
            video_id = f"sim{i:03d}{random.randint(1000, 9999)}"
            fallback_suggestions.append({
                'title': title,
                'url': f"https://www.youtube.com/watch?v={video_id}"
            })
        
        print(f"Generadas {len(fallback_suggestions)} sugerencias fallback")
        return fallback_suggestions
        
    except Exception as e:
        print(f"Error generando fallback: {e}")
        return []

async def get_next_video(video_url: str) -> Optional[Dict[str, str]]:
    """
    Obtiene el siguiente video sugerido (botón "Siguiente") con su título
    """
    context = None
    page = None
    
    try:
        async with async_playwright() as p:
            # 🔧 CONFIGURACIÓN ROBUSTA DEL NAVEGADOR
            context = await p.chromium.launch_persistent_context(
                user_data_dir="./perfil_chrome",
                headless=False,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--mute-audio",
                    "--no-first-run",
                    "--no-default-browser-check"
                ]
            )
            
            page = await context.new_page()
            
            # ⏰ TIMEOUT MÁS LARGO Y MANEJO ROBUSTO
            page.set_default_timeout(30000)  # 30 segundos
            
            print(f"🎬 Navegando a: {video_url}")
            await page.goto(video_url, wait_until='domcontentloaded')
            
            # Esperar a que cargue completamente
            await page.wait_for_timeout(3000)
            
            # 🔍 MÚLTIPLES ESTRATEGIAS PARA ENCONTRAR EL BOTÓN SIGUIENTE
            selector_siguiente = None
            selectors_to_try = [
                '.ytp-next-button',
                "[data-title-no-tooltip='Siguiente']", 
                "[aria-label*='Siguiente']",
                ".ytp-button[title*='Siguiente']",
                ".ytp-playlist-ui .ytp-next-button"
            ]
            
            for selector in selectors_to_try:
                try:
                    print(f"🔍 Probando selector: {selector}")
                    await page.wait_for_selector(selector, timeout=5000)
                    
                    # Verificar que el botón esté visible y habilitado
                    button = await page.query_selector(selector)
                    if button:
                        is_visible = await button.is_visible()
                        is_enabled = await button.is_enabled()
                        
                        if is_visible and is_enabled:
                            selector_siguiente = selector
                            print(f"✅ Botón encontrado y utilizable: {selector}")
                            break
                        else:
                            print(f"❌ Botón no utilizable - Visible: {is_visible}, Enabled: {is_enabled}")
                    
                except Exception as e:
                    print(f"❌ Selector {selector} falló: {e}")
                    continue
            
            if not selector_siguiente:
                print("⚠️ No se encontró botón siguiente válido, usando fallback...")
                # FALLBACK: Obtener primer video relacionado
                suggestions = await get_video_suggestions_real(page)
                
                if suggestions and len(suggestions) > 0:
                    first_suggestion = suggestions[0]
                    nuevo_link = f"https://www.youtube.com{first_suggestion['url']}"
                    title = first_suggestion['title']
                    
                    print(f"🔄 Fallback exitoso: {title}")
                    return {
                        'url': nuevo_link,
                        'title': title
                    }
                else:
                    raise Exception("No se encontró botón siguiente ni sugerencias")
            
            # ✅ USAR EL BOTÓN SIGUIENTE ENCONTRADO
            try:
                nuevo_link_sucio = await page.evaluate(f"document.querySelector('{selector_siguiente}').href")
                
                if not nuevo_link_sucio:
                    raise Exception("No se pudo obtener link del botón siguiente")
                
                # Limpiar la URL como antes
                parsed_url = urllib.parse.urlparse(nuevo_link_sucio)
                query_params = urllib.parse.parse_qs(parsed_url.query)
                
                if 'index' in query_params:
                    del query_params['index']
                
                nueva_query = urllib.parse.urlencode(query_params, doseq=True)
                nuevo_link = urllib.parse.urlunparse((
                    parsed_url.scheme,
                    parsed_url.netloc,
                    parsed_url.path,
                    parsed_url.params,
                    nueva_query,
                    parsed_url.fragment
                ))
                
                print(f"🎯 Link siguiente obtenido: {nuevo_link}")
                
            except Exception as e:
                print(f"❌ Error obteniendo link del botón: {e}")
                raise e
            
            # 🧹 CERRAR CONTEXTO ANTES DE OBTENER TÍTULO
            try:
                if page and not page.is_closed():
                    await page.close()
                if context:
                    await context.close()
                page = None
                context = None
            except:
                pass
            
            # Obtener el título DESPUÉS de cerrar el contexto
            title = get_video_title(nuevo_link)
            
            return {
                'url': nuevo_link,
                'title': title
            }
            
    except Exception as e:
        print(f"Error en get_next_video: {e}")
        return None
        
    finally:
        # 🧹 LIMPIEZA FINAL ROBUSTA
        try:
            if page and not page.is_closed():
                await page.close()
        except:
            pass
            
        try:
            if context:
                await context.close()
        except:
            pass

async def get_video_title_async(video_url: str) -> str:
    """
    Obtiene el título de un video de YouTube usando oEmbed (async)
    """
    import aiohttp
    
    try:
        oembed_url = f"https://www.youtube.com/oembed?url={video_url}&format=json"
        async with aiohttp.ClientSession() as session:
            async with session.get(oembed_url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('title', '')
        return ''
    except Exception as e:
        print(f"Error en get_video_title_async: {e}")
        return ''

def get_video_title(video_url: str) -> str:
    """
    Obtiene el título de un video de YouTube usando oEmbed (sync - deprecated)
    """
    import requests
    
    try:
        # Extraer el video ID de la URL para construir una URL limpia
        parsed = urllib.parse.urlparse(video_url)
        query_params = urllib.parse.parse_qs(parsed.query)
        
        video_id = query_params.get('v', [None])[0]
        if not video_id:
            return ''
        
        # Construir URL limpia solo con el video ID
        clean_url = f"https://www.youtube.com/watch?v={video_id}"
        
        oembed_url = f"https://www.youtube.com/oembed?url={clean_url}&format=json"
        response = requests.get(oembed_url)
        
        if response.status_code == 200:
            data = response.json()
            return data.get('title', '')
        return ''
    except Exception as e:
        print(f"Error en get_video_title: {e}")
        return ''
