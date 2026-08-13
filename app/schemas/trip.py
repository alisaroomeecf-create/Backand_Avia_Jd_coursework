from pydantic import BaseModel


class TripCreate(BaseModel):
    from_city: str| None=None
    to_city: str| None=None
    price: float