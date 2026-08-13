from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import Trip


class TripService:
    @staticmethod
    async def create_trip(db:AsyncSession,data):
        trip=Trip(**data.dict())
        db.add(trip)
        await db.commit()
        return trip
    @staticmethod
    async def get_all(db:AsyncSession,
                      from_city:str|None=None,
                      to_city:str|None=None,):
        result_f = select(Trip)
        if from_city:
            result_f = result_f.where(Trip.from_city == from_city)
        if to_city:
            result_f = result_f.where(Trip.to_city == to_city)
        results = await db.execute(result_f)
        return results.scalars().all()
    @staticmethod
    async def get_by_id(db:AsyncSession,trip_id:int):
        result = await db.execute(select(Trip).where(Trip.id == trip_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def delete_trips(db: AsyncSession, user_id: int):
        result = await db.execute(select(Trip).where(Trip.id == user_id))
        trip = result.scalar_one_or_none()
        if not trip:
            return None
        await db.delete(trip)
        await db.commit()
        return trip