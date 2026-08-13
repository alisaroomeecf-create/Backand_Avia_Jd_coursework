from sqlalchemy import String, Float, ForeignKey, Boolean, Enum as SQLEnum
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship, mapped_column
from enum import Enum
from datetime import datetime


class Base(DeclarativeBase):
    pass


class BookingStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    password: Mapped[str] = mapped_column(String)
    full_name: Mapped[str] = mapped_column(String, nullable=True)
    phone: Mapped[str] = mapped_column(String, nullable=True)
    role: Mapped[str] = mapped_column(String, default='user')

    # Связь: один пользователь -> много бронирований
    bookings: Mapped[list["Booking"]] = relationship(back_populates="user")


class Trip(Base):
    __tablename__ = 'trips'
    id: Mapped[int] = mapped_column(primary_key=True)
    from_city: Mapped[str] = mapped_column(String)
    to_city: Mapped[str] = mapped_column(String)
    price: Mapped[float] = mapped_column(Float)
    # Можно добавить дату, если нужно: departure_date: Mapped[datetime] = mapped_column(nullable=False)

    # Связь: один рейс -> много бронирований
    bookings: Mapped[list["Booking"]] = relationship(back_populates="trip")


class Booking(Base):
    __tablename__ = 'bookings'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    trip_id: Mapped[int] = mapped_column(ForeignKey('trips.id'))

    # Используем Enum для надежности, но храним как строку в БД
    status: Mapped[str] = mapped_column(SQLEnum(BookingStatus), default=BookingStatus.PENDING)
    is_paid: Mapped[bool] = mapped_column(Boolean, default=False)

    # Обратные связи
    user: Mapped["User"] = relationship(back_populates="bookings")
    trip: Mapped["Trip"] = relationship(back_populates="bookings")
