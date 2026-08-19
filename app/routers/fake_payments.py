from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db   
from app.services.fake_payment_service import FakePaymentService

router = APIRouter(prefix="/fake-payments", tags=["Fake Payments (Dev Only)"])

@router.post("/{booking_id}/init")
async def init_fake_payment(booking_id: int, db: AsyncSession = Depends(get_db)):
 
    try:
 
        result = await FakePaymentService.create_payment(db, booking_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
      
        raise HTTPException(status_code=500, detail="Internal server error")
