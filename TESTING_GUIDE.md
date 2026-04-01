# 🧪 Guía de Prueba - IA Local con Ollama

## ✅ Verificación Pre-Inicio

### 1. Verificar que Ollama esté instalado
```bash
ollama --version
```

### 2. Verificar que Ollama esté corriendo
```bash
# En una terminal, mantén esto corriendo:
ollama serve
```

### 3. Verificar que el modelo esté descargado
```bash
ollama list
```

Deberías ver `qwen2.5` en la lista. Si no, descárgalo:
```bash
ollama pull qwen2.5
```

### 4. Probar conexión a Ollama
```bash
curl http://localhost:11434/api/version
```

## 🚀 Iniciar la Aplicación

### 1. Activar entorno virtual
```bash
source .venv/bin/activate  # Linux/Mac
# o
.venv\Scripts\activate     # Windows
```

### 2. Iniciar servidor
```bash
python run_server.py
```

### 3. Abrir en navegador
```
http://localhost:5173
```

## 🧪 Probar la Funcionalidad

### Test 1: Verificar selector de modo
1. Abre la aplicación
2. Busca la sección **⚙️ Modo de Operación**
3. Deberías ver 3 botones:
   - ✋ Manual
   - 🤖 IA Gemini
   - 💻 IA Local

### Test 2: Configurar IA Local
1. Click en **💻 IA Local**
2. Aparece un campo de texto "🧠 Modelo de Ollama"
3. Escribe: `qwen2.5` (o el modelo que tengas)
4. Verifica el mensaje: "Asegúrate de que Ollama esté ejecutándose en http://localhost:11434"

### Test 3: Probar limpieza de título
1. Asegúrate de tener Spotify reproduciendo una canción
2. La app detectará la canción actual
3. Click en el botón 🔄 para obtener recomendación
4. El sistema debería:
   - Buscar en YouTube
   - Obtener título raw
   - Enviarlo a Ollama
   - Mostrar artista y canción limpios
   - Permitir agregar a Spotify

### Test 4: Script de prueba manual (opcional)
```bash
python test_ollama.py
```

Este script prueba la limpieza con 3 títulos de ejemplo.

## 🐛 Solución de Problemas

### Error: "No se pudo conectar con Ollama"
**Causa**: Ollama no está corriendo
**Solución**:
```bash
# Terminal 1
ollama serve

# Terminal 2 (verificar)
curl http://localhost:11434/api/version
```

### Error: "Modelo no encontrado"
**Causa**: El modelo no está descargado
**Solución**:
```bash
ollama pull qwen2.5
```

### Error: "Respuesta JSON inválida"
**Causa**: El modelo no devolvió JSON válido
**Solución**:
- Prueba con un modelo más grande (qwen2.5:7b)
- O mejora el prompt (edita `api/services/ollama_cleaner.py`)

### Frontend no muestra la nueva opción
**Causa**: Frontend no está actualizado
**Solución**:
```bash
cd front
npm run build
cd ..
python run_server.py
```

## 📊 Resultados Esperados

### Ejemplo de título procesado:
```
Input:  "J. Balvin, Willy William - Mi Gente (Official Video)"
Output: 
  Artista: "J. Balvin"
  Canción: "Mi Gente"
```

### En la consola del backend verás:
```
🤖 Procesando con Ollama (qwen2.5): J. Balvin, Willy William - Mi Gente...
🤖 Respuesta Ollama: {"artista": "J. Balvin", "cancion": "Mi Gente"}
```

## ✅ Checklist de Validación

- [ ] Ollama instalado y corriendo
- [ ] Modelo qwen2.5 descargado
- [ ] Frontend muestra 3 opciones de modo
- [ ] Puedo seleccionar "💻 IA Local"
- [ ] Aparece campo para ingresar modelo
- [ ] Al obtener recomendación, el título se limpia correctamente
- [ ] Artista y canción se muestran por separado
- [ ] Puedo agregar la canción a Spotify

## 🎉 ¡Todo Funciona!

Si todos los checks están marcados, la integración con Ollama está completa y funcionando.

**Ventajas que ahora tienes:**
- ✅ Sin límites de API
- ✅ Gratis
- ✅ Privado
- ✅ Rápido (especialmente con modelos pequeños)
- ✅ Funciona offline

---

Para cualquier problema, revisa los logs del backend y verifica que Ollama esté corriendo correctamente.
