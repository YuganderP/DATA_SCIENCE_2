from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from database import Base


class Venue(Base):
    __tablename__ = "venues"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    location: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    users: Mapped[list["User"]] = relationship("User", back_populates="venue")
    facilities: Mapped[list["Facility"]] = relationship(
        "Facility", back_populates="venue"
    )


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(String, nullable=False)
    venue_id: Mapped[int] = mapped_column(ForeignKey("venues.id"))
    venue: Mapped["Venue"] = relationship("Venue", back_populates="users")
    bookings: Mapped[list["Booking"]] = relationship("Booking", back_populates="user")


class Facility(Base):
    __tablename__ = "facilities"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sport_type: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    venue_id: Mapped[int] = mapped_column(ForeignKey("venues.id"))
    venue: Mapped["Venue"] = relationship("Venue", back_populates="facilities")
    bookings: Mapped[list["Booking"]] = relationship(
        "Booking", back_populates="facility"
    )


class Booking(Base):
    __tablename__ = "bookings"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    facility_id: Mapped[int] = mapped_column(Integer, ForeignKey("facilities.id"))
    booking_date: Mapped[str] = mapped_column(String, nullable=False)
    start_time: Mapped[str] = mapped_column(String, nullable=False)
    end_time: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="bookings")
    facility: Mapped["Facility"] = relationship("Facility", back_populates="bookings")
