from pydantic import BaseModel, Field
from typing import List


class GarageRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=20, description="Garage name must be between 2 and 20 characters.")
    location: str = Field(..., min_length=2, max_length=20, description="Location must be between 2 and 20 characters.")
    city: str = Field(..., min_length=2, max_length=20, description="City must be between 2 and 20 characters.")
    capacity: int = Field(..., ge=1, le=1000, description="Capacity must be between 1 and 1000.")


class Maintenance(BaseModel):
    id: int
    service_type: str
    scheduled_date: str


class GarageResponse(BaseModel):
    id: int
    name: str
    location: str
    city: str
    capacity: int
    #maintenances: List[Maintenance]

class CarRequest(BaseModel):
    make: str = Field(..., min_length=2, max_length=20, description="Car make must be between 2 and 20 characters.")
    model: str = Field(..., min_length=2, max_length=20, description="Car model must be between 2 and 20 characters.")
    productionYear: int = Field(..., ge=1800, description="Production year must be grater than 1799.")
    licensePlate: str = Field(..., min_length=7, max_length=8, description="Licence plate must be exactly 7 to 8 characters.")
    garageIds: list[int] = Field(..., description="Garage_Id is mandatory.")


class MaintenanceCar(BaseModel):
    id: int
    service_type: str
    scheduled_date: str

class CarResponse(BaseModel):
    id: int
    make: str
    model: str
    productionYear: int
    licensePlate: str
    garages: list[GarageResponse]

class MaintenanceRequest(BaseModel):
    service_type: str
    scheduled_date: str
    car_id: int
    garage_id: int


class MaintenanceResponse(BaseModel):
    id: int
    car_id: int
    car_name: str
    service_type: str
    scheduled_date: str
    #garageId
    #garageName
    #car: CarResponse
    garage: GarageResponse

class GarageDARepostResponse(BaseModel):
    date: str
    requests: int
    availableCapacity: int