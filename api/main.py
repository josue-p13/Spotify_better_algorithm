from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import spotify, youtube, recommendations
import db_manager

app = FastAPI(title="Spotify Better Algorithm API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(spotify.router, prefix="/api/spotify", tags=["Spotify"])
app.include_router(youtube.router, prefix="/api/youtube", tags=["YouTube"])
app.include_router(recommendations.router, prefix="/api/recommendations", tags=["Recommendations"])

@app.get("/")
async def root():
    return {"message": "Spotify Better Algorithm API", "status": "running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.on_event("startup")
async def startup_event():
    """Evento que se ejecuta al iniciar la aplicación"""
    db_manager.inicializar_bd()
    print("🗄️ Base de datos inicializada correctamente")

@app.on_event("shutdown")
async def shutdown_event():
    """Evento que se ejecuta al detener la aplicación"""
    db_manager.limpiar_historial()
    print("🧹 Base de datos limpiada al cerrar la aplicación")
