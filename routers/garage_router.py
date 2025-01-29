from fastapi import APIRouter

from DTOs.dtos import GarageResponse, GarageRequest, GarageDARepostResponse
from services.garage_service import get_garage, get_garages, create_garage, update_garage, delete_garage, \
    get_garage_report

garage_router = APIRouter()

@garage_router.get("/garages", response_model=list[GarageResponse], status_code=200)
def get_all_garages(city: str | None = None) -> list[GarageResponse]:
    return get_garages(city)

@garage_router.get("/garages/{garage_id}", response_model=GarageResponse, status_code=200)
def get_single_garage(garage_id:int):
    return get_garage(garage_id)

@garage_router.post("/garages", response_model=GarageResponse, status_code=201)
def create_new_garage(request: GarageRequest):
    return create_garage(request)

@garage_router.put("/garages/{garage_id}", response_model=GarageResponse, status_code=200)
def update_a_garage(garage_id: int, request: GarageRequest):
    return update_garage(garage_id, request)

@garage_router.delete("/garages/{garage_id}", response_model=GarageResponse, status_code=200)
def delete_a_garage(garage_id: int):
    return delete_garage(garage_id)

@garage_router.get("/garages/dailyAvailabilityReport", response_model=list[GarageDARepostResponse], status_code=200)
def get_report(garageId: int, startDate: str, endDate: str) -> list[GarageDARepostResponse]:
    return get_garage_report(garageId, startDate, endDate)