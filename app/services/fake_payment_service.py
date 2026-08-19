import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import Booking, BookingStatus


class FakePaymentService:
    @staticmethod
    async def create_payment(db: AsyncSession, booking_id: int) -> dict:
 
        stmt = select(Booking).where(Booking.id == booking_id)
 
        result = await db.execute(stmt)
        booking = result.scalar_one_or_none()

        if not booking:
            raise ValueError("Бронирование не найдено")

        if booking.status != BookingStatus.PENDING:
            raise ValueError(f"Нельзя оплатить бронирование со статусом {booking.status}")

        fake_payment_id = f"fake_{uuid.uuid4()}"
 
        booking.status = BookingStatus.PAID
        booking.is_paid = True
 
        await db.commit()
        await db.refresh(booking)

        return {
            "booking_id": booking.id,
            "payment_id": fake_payment_id,
            "status": "succeeded",
            "message": "Оплата успешно эмулирована!"
        }

    @staticmethod
    async def confirm_payment(db: AsyncSession, payment_id: str):
    
        return {"status": "confirmed"}
