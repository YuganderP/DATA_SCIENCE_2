from fastapi import FastAPI, status, Depends, HTTPException
from schemas import (
    VenueResponse,
    VenueCreate,
    UserCreate,
    UserResponse,
    FacilityCreate,
    FacilityResponse,
    BookingCreate,
    BookingResponse,
)
from database import get_db, Base, db
from sqlalchemy.orm import Session
from sqlalchemy import select
from models import Venue
from models import User
from models import Booking
from models import Facility

Base.metadata.create_all(bind=db)

app = FastAPI()


@app.post("/venues", response_model=VenueResponse)
def create_venue(venue: VenueCreate, db: Session = Depends(get_db)):
    new_venue = Venue(
        name=venue.name, location=venue.location, description=venue.description
    )
    db.add(new_venue)
    db.commit()
    db.refresh(new_venue)
    return new_venue


@app.get("/venues", response_model=list[VenueResponse])
def get_venues(db: Session = Depends(get_db)):
    result = db.execute(select(Venue))
    venues = result.scalars().all()
    return venues


@app.get("/venues/{venue_id}", response_model=VenueResponse)
def get_venue(venue_id: int, db: Session = Depends(get_db)):
    result = db.query(Venue).filter(Venue.id == venue_id).first()
    if result is not None:
        return result
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"Message": "no venue with given venue id found "},
    )


@app.put("/venues/{venue_id}", response_model=VenueResponse)
def update_venue(venue: VenueCreate, venue_id: int, db: Session = Depends(get_db)):
    result = db.query(Venue).filter(Venue.id == venue_id).first()
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"Message": "no venue with given venue id found "},
        )
    else:
        result.name = venue.name
        result.location = venue.location
        result.description = venue.description
        db.commit()
        db.refresh(result)
    return result


@app.delete("/venues/{venue_id}")
def delete_venue(venue_id: int, db: Session = Depends(get_db)):
    result = db.query(Venue).filter(Venue.id == venue_id).first()
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"Message": "no venue with given venue id found "},
        )
    db.delete(result)
    db.commit()
    return {"message": f"{venue_id} venue has been deleted "}


@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(
        name=user.name, email=user.email, role=user.role, venue_id=user.venue_id
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/users", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    result = db.execute(select(User))
    users = result.scalars().all()
    return users


@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    result = db.query(User).filter(User.id == user_id).first()
    if result is not None:
        return result
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"Message": "no venue with given user id found "},
    )


@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user: UserCreate, user_id: int, db: Session = Depends(get_db)):
    result = db.query(User).filter(User.id == user_id).first()
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"Message": "no venue with given user id found "},
        )
    else:
        result.name = user.name
        result.email = user.email
        result.role = user.role
        result.venue_id = user.venue_id
        db.commit()
        db.refresh(result)
    return result


@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    result = db.query(User).filter(User.id == user_id).first()
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"Message": "no user with given user id found "},
        )
    db.delete(result)
    db.commit()
    return {"message": f"{user_id} user has been deleted "}


## Facilities


@app.post("/facilities", response_model=FacilityResponse)
def create_facility(facility: FacilityCreate, db: Session = Depends(get_db)):
    new_facility = Facility(
        sport_type=facility.sport_type,
        description=facility.description,
        name=facility.name,
        venue_id=facility.venue_id,
    )
    db.add(new_facility)
    db.commit()
    db.refresh(new_facility)
    return new_facility


@app.get("/facilities", response_model=list[FacilityResponse])
def facilities(db: Session = Depends(get_db)):
    result = db.execute(select(Facility))
    facilities = result.scalars().all()
    return facilities


@app.get("/facilities/{facility_id}", response_model=FacilityResponse)
def get_facility(facility_id: int, db: Session = Depends(get_db)):
    result = db.query(Facility).filter(Facility.id == facility_id).first()
    if result is not None:
        return result
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"Message": "no facility with given facility id found "},
    )


@app.put("/facilities/{facility_id}", response_model=FacilityResponse)
def update_facility(
    facility: FacilityCreate, facility_id: int, db: Session = Depends(get_db)
):
    result = db.query(Facility).filter(Facility.id == facility_id).first()
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"Message": "no facility with given facility id found"},
        )
    else:
        result.sport_type = facility.sport_type
        result.description = facility.description
        result.name = facility.name
        result.venue_id = facility.venue_id
        db.commit()
        db.refresh(result)
    return result


@app.delete("/facilities/{facility_id}")
def delete_facility(facility_id: int, db: Session = Depends(get_db)):
    result = db.query(Facility).filter(Facility.id == facility_id).first()
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"Message": "no facility with given facility id found "},
        )
    db.delete(result)
    db.commit()
    return {"message": f"{facility_id} facility has been deleted "}


@app.post("/bookings", response_model=BookingResponse)
def create_booking(booking: BookingCreate, db: Session = Depends(get_db)):
    new_booking = Booking(
        user_id=booking.user_id,
        facility_id=booking.facility_id,
        booking_date=booking.booking_date,
        start_time=booking.start_time,
        end_time=booking.end_time,
        status=booking.status,
    )
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking


### BOOKINGS


@app.get("/bookings", response_model=list[BookingResponse])
def get_bookings(db: Session = Depends(get_db)):
    result = db.execute(select(Booking))
    bookings = result.scalars().all()
    return bookings


@app.get("/bookings/{booking_id}", response_model=BookingResponse)
def get_booking(booking_id: int, db: Session = Depends(get_db)):
    result = db.query(Booking).filter(Booking.id == booking_id).first()
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="no booking with given booking found",
        )
    return result


@app.put("/bookings/{booking_id}", response_model=BookingResponse)
def update_booking(
    booking: BookingCreate, booking_id: int, db: Session = Depends(get_db)
):
    result = db.query(Booking).filter(Booking.id == booking_id).first()
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"Message": "no Booking with given booking id found"},
        )
    else:
        result.user_id = booking.user_id
        result.facility_id = booking.facility_id
        result.booking_date = booking.booking_date
        result.start_time = booking.start_time
        result.end_time = booking.end_time
        result.status = booking.status
        db.commit()
        db.refresh(result)
    return result


@app.delete("/bookings/{booking_id}")
def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    result = db.query(Booking).filter(Booking.id == booking_id).first()
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"Message": "no Booking with given booking id found "},
        )
    db.delete(result)
    db.commit()
    return {"message": f"{booking_id} booking has been deleted "}
