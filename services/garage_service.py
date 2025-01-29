from fastapi import HTTPException
from DTOs.dtos import GarageResponse, GarageRequest, GarageDARepostResponse
from models import Garage
from db import Session, engine
from sqlalchemy.orm import Session as ORMSession

def get_garage_by_id(id_: int, session: ORMSession):
    garage = session.get(Garage, id_)
    if garage is None:
        raise HTTPException(status_code=404, detail="Garage not found")
    return garage

def get_garage(id_: int) -> GarageResponse:
    with Session() as sess:
        garage = get_garage_by_id(id_, sess)
        return map_garage_to_response(garage)

def get_garages(city: str | None = None) -> list[GarageResponse]:
    with Session() as sess:
        if city is None:
            garages = sess.query(Garage).all()
        else:
            search_title = f"%{city}%"
            garages = sess.query(Garage).where(Garage.city.ilike(search_title)).all()
        return [map_garage_to_response(garage) for garage in garages]

def create_garage(request: GarageRequest) -> GarageResponse:
    if not request.name or not request.location or not request.city or request.capacity < 1:
        raise HTTPException(status_code=400, detail="Invalid data provided")

    new_garage = map_request_to_garage(request)
    with Session() as s:
        s.add(new_garage)
        s.commit()
        s.refresh(new_garage)
        return map_garage_to_response(new_garage)

def update_garage(id_: int, request: GarageRequest) -> GarageResponse:
    with Session() as s:
        garage = get_garage_by_id(id_, s)
        if garage is None:
            raise HTTPException(status_code=404, detail="Garage not found")

        if not request.name or not request.location or not request.city or request.capacity < 1:
            raise HTTPException(status_code=400, detail="Invalid data provided")

        garage.name = request.name
        garage.location = request.location
        garage.city = request.city
        garage.capacity = request.capacity
        s.commit()
        s.refresh(garage)
        return map_garage_to_response(garage)

def delete_garage(id_:int) -> GarageResponse:
    with Session() as s, s.begin():
        garage = get_garage_by_id(id_, s)
        s.delete(garage)
        return map_garage_to_response(garage)

def get_garage_report(garageId: int, startDate: str, endDate: str) -> list[GarageDARepostResponse]:
    pass

def map_garage_to_response(garage: Garage) -> GarageResponse:
    return GarageResponse(
        id=garage.id,
        name=garage.name,
        location=garage.location,
        city=garage.city,
        capacity=garage.capacity
    )

def map_request_to_garage(request: GarageRequest) -> Garage:
    return Garage(
        name = request.name,
        location = request.location,
        city = request.city,
        capacity = request.capacity
    )