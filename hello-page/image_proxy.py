import httpx
from fastapi import APIRouter

router = APIRouter()


@router.get("/unsplash/random")
async def get_random_image():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.unsplash.com/photos/random",
            params={
                "client_id": "nVycJe5FkbwXEs4uSzQpQhk5mWPV4zJ3W25JQa3Nq40",
                "query": "nature",
                "orientation": "landscape",
            },
        )
    return response.json()
