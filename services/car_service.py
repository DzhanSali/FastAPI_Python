from fastapi import HTTPException
from sqlalchemy import select
from DTOs.dtos import CarResponse, CarRequest
from models import Car
from db import Session, engine
from sqlalchemy.orm import Session as ORMSession
from services.garage_service import get_garage


def get_car_by_id(id: int, session: ORMSession):
    car = session.get(Car, id)
    if car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    return car

def get_car(id:int) -> CarResponse:
    with Session() as session:
        car = get_car_by_id(id, session)
        return map_car_to_response(car)

def get_car_by_filter(
        carMake: str | None = None,
        garageId: int | None = None,
        fromYear: int | None = None,
        toYear: int | None = None
                                        ) -> list[CarResponse]:
    with Session() as sess:
        select_query = select(Car)

        filters = []
        if carMake:
            filters.append(Car.make.ilike(f"%{carMake}%"))
        if garageId:
            filters.append(Car.garage_id == garageId)
        if fromYear:
            filters.append(Car.production_year >= fromYear)
        if toYear:
            filters.append(Car.production_year <= toYear)
        if filters:
            select_query = select_query.where(*filters)
        cars = sess.scalars(select_query).all()
        return [map_car_to_response(car) for car in cars]

def get_cars() -> list[CarResponse]:
    with Session() as sess:
        cars = sess.query(Car).all()
        return [map_car_to_response(car) for car in cars]

def create_car(request: CarRequest) -> CarResponse:
    if not request.make or not request.model or request.productionYear < 1799 or len(request.licensePlate) < 7 or not request.garageIds:
        raise HTTPException(status_code=400, detail="Invalid data provided")
    new_car = map_request_to_car(request)
    with Session() as s:
        s.add(new_car)
        s.commit()
        s.refresh(new_car)
        return map_car_to_response(new_car)

def update_car(id_: int, request: CarRequest) -> CarResponse:
    with Session() as s:
        car = get_car_by_id(id_, s)
        if car is None:
            raise HTTPException(status_code=404, detail="Car not found")

        if not request.make or not request.model or not request.licensePlate or request.productionYear < 1799 or not request.garageIds:
            raise HTTPException(status_code=400, detail="Invalid data provided")

        car.make = request.make
        car.model = request.model
        car.production_year = request.productionYear
        car.license_plate = request.licensePlate
        car.garage_id = request.garageIds[0]
        s.commit()
        s.refresh(car)
        return map_car_to_response(car)

def delete_car(id_:int) -> CarResponse:
    with Session() as s, s.begin():
        car = get_car_by_id(id_, s)
        s.delete(car)
        return map_car_to_response(car)


def map_request_to_car(request: CarRequest) -> Car:
    return Car(
        make = request.make,
        model = request.model,
        production_year = request.productionYear,
        license_plate = request.licensePlate,
        garage_id = request.garageIds[0]
    )

def map_car_to_response(car: Car) -> CarResponse:
    return CarResponse(
        id=car.id,
        make=car.make,
        model=car.model,
        productionYear = car.production_year,
        licensePlate = car.license_plate,
        garages = [get_garage(car.garage_id)]
    )

def get_car_name(car_id: int) -> str:
    with Session() as s:
        car = get_car_by_id(car_id, s)
        return car.make + " " + car.model