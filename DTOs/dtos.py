from pydantic import BaseModel, Field
from typing import List


class GarageRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=20, description="Garage name must be between 2 and 20 characters.")
    location: str = Field(..., min_length=2, max_length=20, description="Location must be between 2 and 20 characters.")
    city: str = Field(..., min_length=2, max_length=20, description="City must be between 2 and 20 characters.")
    capacity: int = Field(..., ge=1, le=1000, description="Capacity must be between 1 and 1000.")

class GarageResponse(BaseModel):
    id: int
    name: str
    location: str
    city: str
    capacity: int

class CarRequest(BaseModel):
    make: str = Field(..., min_length=2, max_length=20, description="Car make must be between 2 and 20 characters.")
    model: str = Field(..., min_length=2, max_length=20, description="Car model must be between 2 and 20 characters.")
    productionYear: int = Field(..., ge=1800, description="Production year must be grater than 1799.")
    licensePlate: str = Field(..., min_length=7, max_length=8, description="Licence plate must be exactly 7 to 8 characters.")
    garageIds: list[int] = Field(..., description="Garage_Id is mandatory.")

class CarResponse(BaseModel):
    id: int
    make: str
    model: str
    productionYear: int
    licensePlate: str
    garages: list[GarageResponse]

class MaintenanceRequest(BaseModel):
    serviceType: str = Field(..., min_length=2, max_length=50, description="Service type must be between 2 and 50 characters.")
    scheduledDate: str = Field(..., min_length=10, max_length=10, description="Service type must be exactly 10 characters.")
    carId: int = Field(..., description="Car_id cannot be null!")
    garageId: int = Field(..., description="Garage_id cannot be null!")


class MaintenanceResponse(BaseModel):
    id: int
    carId: int
    carName: str
    serviceType: str
    scheduledDate: str
    garageId: int
    garageName: str

class GarageDARepostResponse(BaseModel):
    date: str
    requests: int
    availableCapacity: int