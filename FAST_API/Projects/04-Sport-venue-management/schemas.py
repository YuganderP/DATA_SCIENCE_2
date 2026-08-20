from pydantic import BaseModel, ConfigDict, Field


class VenueCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    location: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=500)


class VenueResponse(BaseModel):
    id: int
    name: str
    location: str
    description: str

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., min_length=5, max_length=100)
    role: str = Field(..., min_length=1, max_length=50)
    venue_id: int


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    venue_id: int

    model_config = ConfigDict(from_attributes=True)


class FacilityCreate(BaseModel):
    sport_type: str = Field(..., min_length=1, max_length=50)
    description: str = Field(..., min_length=1, max_length=500)
    name: str = Field(..., min_length=1, max_length=100)
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
    booking_date: str = Field(..., min_length=1)
    start_time: str = Field(..., min_length=1)
    end_time: str = Field(..., min_length=1)
    status: str = Field(..., min_length=1, max_length=30)


class BookingResponse(BaseModel):
    id: int
    user_id: int
    facility_id: int
    booking_date: str
    start_time: str
    end_time: str
    status: str

    model_config = ConfigDict(from_attributes=True)
