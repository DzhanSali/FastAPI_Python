from fastapi import APIRouter
from DTOs.dtos import *
from services.car_service import get_car, get_cars, create_car, get_car_by_filter, update_car, delete_car

car_router = APIRouter()

@car_router.get("/cars", response_model=list[CarResponse], status_code=200)
def get_car(carMake: str | None=None, garageId: int | None = None, fromYear: int | None = None, toYear: int | None = None):
    if not carMake and not garageId and not fromYear and not toYear:
        return get_cars()
    else:
        return get_car_by_filter(carMake, garageId, fromYear, toYear)

@car_router.get("/cars/{car_id}", response_model=CarResponse, status_code=200)
def get_single_car(car_id:int):
    return get_car(car_id)

@car_router.post("/cars", response_model=CarResponse, status_code=201)
def create_new_car(request: CarRequest):
    return create_car(request)

@car_router.put("/cars/{car_id}", response_model=CarResponse, status_code=200)
def update_a_car(car_id: int, request: CarRequest):
    return update_car(car_id, request)

@car_router.delete("/cars/{car_id}", response_model=CarResponse, status_code=200)
def delete_a_car(car_id: int):
    return delete_car(car_id)
