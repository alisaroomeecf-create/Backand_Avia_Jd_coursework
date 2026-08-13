from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import Booking


class BookingService:
    @staticmethod
    async def create_booking(db:AsyncSession,data):
        booking=Booking(**data.dict())
        db.add(booking)
        await db.commit()
        return booking
    @staticmethod
    async def get_all(db:AsyncSession):
        bookings=await db.execute(select(Booking))
        return bookings.scalars().all()