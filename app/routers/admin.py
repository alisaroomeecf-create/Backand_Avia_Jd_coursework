from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.util import await_only

from app.models.models import Trip
from app.schemas.trip import TripCreate
from app.services.booking_service import BookingService
from app.services.trip_service import TripService
from app.services.user_service import UserService
from database import get_db

router=APIRouter(prefix="/admin",tags=["Admin"])
async def check_admin(db:AsyncSession,admin_id:int):
    admin=await UserService.get_user_by_id(db,admin_id)
    if not admin or admin.role!="admin":
        return None
    return admin
@router.get("/users")
async def get_users(admin_id:int,db:AsyncSession=Depends(get_db)):
    admin=await check_admin(db,admin_id)
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    return await UserService.get_user_all(db)
@router.get("/users/{user_id}")
async def get_user(user_id:int,admin_id:int,db:AsyncSession=Depends(get_db)):
    admin=await check_admin(db,admin_id)
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    user =await UserService.get_user_by_id(db,user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/users/{user_id}")
async def delete_user(user_id:int,admin_id:int,db:AsyncSession=Depends(get_db)):
    admin = await check_admin(db, admin_id)
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    user=await UserService.delete_user(db,user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message":"User deleted"}

@router.post("/trips")
async def create_trips(trip:TripCreate,admin_id:int,db:AsyncSession=Depends(get_db)):
    admin = await check_admin(db, admin_id)
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    return await TripService.create_trip(db,trip)
@router.put("/trips/{trip_id}")
async def update_trips(trip_id:int,data:TripCreate,admin_id:int,db:AsyncSession=Depends(get_db)):
    admin = await check_admin(db, admin_id)
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    trip = await TripService.update_trip(db,trip_id,data)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return {"message":"Trip updated","trip":trip}

@router.delete("/trips/{trip_id}")
async def delete_trips(trip_id:int,admin_id:int,db:AsyncSession=Depends(get_db)):
    admin = await check_admin(db, admin_id)
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    trip =  await TripService.delete_trips(db,trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return {"message":"Trip deleted"}
