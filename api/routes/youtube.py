from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from api.services.youtube_scraper import get_video_suggestions, get_next_video, get_video_title
from api.services.title_cleaner import clean_title_with_ai

router = APIRouter()

class GetSuggestionsRequest(BaseModel):
    video_url: str

class GetNextVideoRequest(BaseModel):
    video_url: str

class CleanTitleRequest(BaseModel):
    raw_title: str
    api_key: Optional[str] = None

@router.post("/suggestions")
async def get_suggestions(request: GetSuggestionsRequest):
    try:
        suggestions = await get_video_suggestions(request.video_url)
        
        # Si no hay sugerencias, devolver lista vacía en lugar de error
        return {
            "success": True,
            "count": len(suggestions),
            "suggestions": suggestions
        }
    except Exception as e:
        print(f"Error en /suggestions: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/next-video")
async def get_next(request: GetNextVideoRequest):
    try:
        next_video = await get_next_video(request.video_url)
        
        if not next_video:
            raise HTTPException(status_code=404, detail="No se pudo obtener el siguiente video")
        
        title = get_video_title(next_video['url'])
        
        return {
            "success": True,
            "video_url": next_video['url'],
            "raw_title": title,
            "title": next_video.get('title', title)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/clean-title")
async def clean_title(request: CleanTitleRequest):
    try:
        if request.api_key:
            result = await clean_title_with_ai(request.raw_title, request.api_key)
            
            if result:
                return {
                    "success": True,
                    "mode": "auto",
                    "artista": result.get('artista'),
                    "cancion": result.get('cancion')
                }
            else:
                raise HTTPException(status_code=500, detail="No se pudo limpiar el título con IA")
        else:
            return {
                "success": True,
                "mode": "manual",
                "raw_title": request.raw_title,
                "message": "Modo manual activado"
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
