from fastapi import APIRouter, Request, HTTPException
from api.service.card_service import CardService

card_service = CardService()
router = APIRouter()


@router.get("/card")
async def get_first_card(request: Request):
    card = await card_service.get_first_card()
    print("The card is", card)
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    return card
