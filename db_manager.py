import sqlite3

DB_NAME = "historial_canciones.db"

def inicializar_bd():
    """Crea la tabla si no existe en la base de datos local."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS historial (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            artista TEXT COLLATE NOCASE,
            cancion TEXT COLLATE NOCASE
        )
    ''')
    conn.commit()
    conn.close()

def cancion_ya_escuchada(artista, cancion):
    """Verifica si la canción ya existe en el historial."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Buscamos ignorando mayúsculas/minúsculas para evitar falsos negativos
    cursor.execute('''
        SELECT 1 FROM historial 
        WHERE artista = ? AND cancion = ?
    ''', (artista, cancion))
    
    resultado = cursor.fetchone()
    conn.close()
    
    return resultado is not None

def guardar_en_historial(artista, cancion):
    """Guarda la canción en el historial."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO historial (artista, cancion) 
        VALUES (?, ?)
    ''', (artista, cancion))
    conn.commit()
    conn.close()

def limpiar_historial():
    """Elimina todos los registros del historial al cerrar el programa."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM historial')
    conn.commit()
    conn.close()
    print("🧹 Historial limpiado correctamente.")
