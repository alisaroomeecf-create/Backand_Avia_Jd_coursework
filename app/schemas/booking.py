from pydantic import BaseModel


class BookingCreate(BaseModel):
    user_id: int
    trip_id: int