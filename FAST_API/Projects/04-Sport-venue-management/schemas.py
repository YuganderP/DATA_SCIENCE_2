from pydantic import BaseModel, ConfigDict


class VenueCreate(BaseModel):
    name: str
    location: str
    description: str


class VenueResponse(BaseModel):
    id: int
    name: str
    location: str
    description: str

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    name: str
    email: str
    role: str
    venue_id: int


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    venue_id: int

    model_config = ConfigDict(from_attributes=True)


class FacilityCreate(BaseModel):
    sport_type: str
    description: str
    name: str
    venue_id: int


class FacilityResponse(BaseModel):
    id: int
    sport_type: str
    description: str
    name: str
    venue_id: int
    model_config = ConfigDict(from_attributes=True)


class BookingCreate(BaseModel):
    user_id: int
    facility_id: int
    booking_date: str
    start_time: str
    end_time: str
    status: str


class BookingResponse(BaseModel):
    id: int
    user_id: int
    facility_id: int
    booking_date: str
    start_time: str
    end_time: str
    status: str

    model_config = ConfigDict(from_attributes=True)
