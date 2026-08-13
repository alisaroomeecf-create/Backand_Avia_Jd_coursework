from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.trip import TripCreate
from app.services.trip_service import TripService
from database import get_db

router=APIRouter(prefix="/trips",tags=["Trips"])

@router.post("/")
async def create_trip(data:TripCreate,db:AsyncSession=Depends(get_db)):
    return await TripService.create_trip(db,data)

@router.get("/")
async def get_trips(from_city:str|None=None,
                   to_city:str|None=None,
                   db:AsyncSession=Depends(get_db)):

    return await TripService.get_all(db,from_city,to_city)

@router.get("/{trip_id}")
async def get_trip(trip_id:int,db:AsyncSession=Depends(get_db)):
     trip=await TripService.get_by_id(db,trip_id)
     if not trip:
         raise HTTPException(status_code=404, detail="Trip not found")
     return trip