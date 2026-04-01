from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from api.services.recommendation_engine import get_automatic_recommendation
import db_manager

router = APIRouter()

class GetRecommendationRequest(BaseModel):
    current_song: str
    ai_mode: str = 'manual'
    api_key: Optional[str] = None
    local_model: Optional[str] = 'qwen2.5'

class MarkAsProcessedRequest(BaseModel):
    artista: str
    cancion: str

@router.post("/get-next")
async def get_recommendation(request: GetRecommendationRequest):
    try:
        recommendation = await get_automatic_recommendation(
            request.current_song, 
            request.ai_mode,
            request.api_key,
            request.local_model
        )
        
        if recommendation:
            return {
                "success": True,
                **recommendation
            }
        else:
            raise HTTPException(status_code=404, detail="No se pudo obtener recomendación")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/mark-processed")
async def mark_processed(request: MarkAsProcessedRequest):
    try:
        db_manager.guardar_en_historial(request.artista, request.cancion)
        
        return {
            "success": True,
            "message": "Canción marcada como procesada"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history")
async def get_history():
    try:
        import sqlite3
        conn = sqlite3.connect('historial_canciones.db')
        cursor = conn.cursor()
        cursor.execute('SELECT artista, cancion FROM historial ORDER BY id DESC LIMIT 50')
        records = cursor.fetchall()
        count_cursor = cursor.execute('SELECT COUNT(*) FROM historial')
        total = cursor.fetchone()[0]
        conn.close()
        
        history = [{"artista": record[0], "cancion": record[1]} for record in records]
        
        return {
            "success": True,
            "total": total,
            "history": history,
            "message": f"Historial obtenido: {total} canciones"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
