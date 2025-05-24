from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel
from src.shared.response import validate_and_encapsulate
from src.models.Card import Card
import src.services.game_service as game_service
router = APIRouter(prefix = "/game", tags=["game"])




class GameCreateResponse(BaseModel):
    game_id: str;
    deck: list[Card];

@router.post("/start_game")
@validate_and_encapsulate(GameCreateResponse)
async def create_game(request: Request):
    deck, game_id = game_service.initalize_game()
    return {"game_id": game_id, "deck": deck}