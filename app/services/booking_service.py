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

    @staticmethod
    async def delete_booking(db: AsyncSession, booking_id: int):
        result = await db.execute(select(Booking).where(Booking.id == booking_id))
        booking = result.scalar_one_or_none()
        if not booking:
            return None
        await db.delete(booking)
        await db.commit()
        return booking