from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db  # Убедись, что эта зависимость возвращает AsyncSession
from app.services.fake_payment_service import FakePaymentService

router = APIRouter(prefix="/fake-payments", tags=["Fake Payments (Dev Only)"])

@router.post("/{booking_id}/init")
async def init_fake_payment(booking_id: int, db: AsyncSession = Depends(get_db)):
    """
    Инициализирует и сразу подтверждает фейковую оплату для сущности Booking.
    """
    try:
        # Вызываем асинхронный метод сервиса
        result = await FakePaymentService.create_payment(db, booking_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Для отладки можно временно вывести ошибку в консоль, но не в ответ API
        raise HTTPException(status_code=500, detail="Internal server error")
