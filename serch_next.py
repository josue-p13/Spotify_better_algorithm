from playwright.sync_api import sync_playwright
import urllib.parse

def capturar_siguiente_sugerencia(link):
    with sync_playwright() as p:
        # Usamos un contexto persistente para guardar cookies. Así si resuelves el captcha una vez, no te lo volverá a pedir.
        context = p.chromium.launch_persistent_context(
            user_data_dir="./perfil_chrome",
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled", # Oculta que es un bot
                "--mute-audio" # Mutea todo el navegador desde el inicio
            ] 
        )
        page = context.new_page()
        
        print(f"Navegando al video: {link}")
        page.goto(link)
        
        # Esperamos a que el botón "Siguiente" esté en el DOM
        selector_siguiente = '.ytp-next-button'
        page.wait_for_selector(selector_siguiente, timeout=15000)
        
        print("Extrayendo el enlace directamente del botón 'Siguiente'...")
        
        # Extraemos la propiedad 'href' (el link real) del botón sin hacer clic
        nuevo_link_sucio = page.evaluate("document.querySelector('.ytp-next-button').href")
        
        # Limpieza de la URL para quitar el parámetro '&index=...'
        parsed_url = urllib.parse.urlparse(nuevo_link_sucio)
        query_params = urllib.parse.parse_qs(parsed_url.query)
        
        if 'index' in query_params:
            del query_params['index']  # Eliminamos el index
            
        # Reconstruimos la URL limpia
        nueva_query = urllib.parse.urlencode(query_params, doseq=True)
        nuevo_link = urllib.parse.urlunparse((
            parsed_url.scheme, 
            parsed_url.netloc, 
            parsed_url.path, 
            parsed_url.params, 
            nueva_query, 
            parsed_url.fragment
        ))
        
        print(f"Siguiente video sugerido capturado exitosamente:")
        print(nuevo_link)
        
        context.close()
        return nuevo_link

if __name__ == "__main__":
    link_inicial = "https://www.youtube.com/watch?v=V3R06qkyiUo&list=RDV3R06qkyiUo" 
    capturar_siguiente_sugerencia(link_inicial)