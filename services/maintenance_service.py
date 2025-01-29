from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import select, and_
from DTOs.dtos import CarResponse, CarRequest, MaintenanceResponse, MaintenanceRequest
from models import Car, Maintenance
from db import Session, engine
from sqlalchemy.orm import Session as ORMSession

from services.car_service import get_car_name
from services.garage_service import get_garage, get_garage_name


def get_maintenance_by_id(id_: int, session: ORMSession):
    maintenance = session.get(Maintenance, id_)
    if maintenance is None:
        raise HTTPException(status_code=404, detail="Maintenance not found")
    return maintenance

def get_maintenance(id_:int) -> MaintenanceResponse:
    with Session() as session:
        maintenance = get_maintenance_by_id(id_, session)
        return map_maintenance_to_response(maintenance)

def get_maintenances() -> list[MaintenanceResponse]:
    with Session() as s:
        maintenances = s.query(Maintenance).all()
        return [map_maintenance_to_response(maintenance) for maintenance in maintenances]

def get_maintenance_by_filter(
        carId: int | None = None, garageId: int | None = None,
        startDate: str | None = None, endDate: str | None = None) -> list[MaintenanceResponse]:
    with Session() as s:
        select_query = select(Maintenance)

        filters = []
        if carId:
            filters.append(Maintenance.car_id == carId)
        if garageId:
            filters.append(Maintenance.garage_id == garageId)
        if startDate:
            filters.append(Maintenance.scheduled_date >= startDate)
        if endDate:
            filters.append(Maintenance.scheduled_date <= endDate)

        if filters:
            select_query = select_query.where(and_(*filters))

        maintenances = s.scalars(select_query).all()
        return [map_maintenance_to_response(maintenance) for maintenance in maintenances]


def create_maintenance(request: MaintenanceRequest) -> MaintenanceResponse:
    if not request.serviceType or not request.scheduledDate or not request.carId or not request.garageId:
        raise HTTPException(status_code=400, detail="Invalid data provided")
    new_maintenance = map_request_to_maintenance(request)
    with Session() as s:
        s.add(new_maintenance)
        s.commit()
        s.refresh(new_maintenance)
        return map_maintenance_to_response(new_maintenance)


def update_maintenance(maintenance_id: int, request: MaintenanceRequest) -> MaintenanceResponse:
    with Session() as s:
        maint = get_maintenance_by_id(maintenance_id, s)
        if maint is None:
            raise HTTPException(status_code=404, detail="Car not found")
        if not request.serviceType or not request.scheduledDate or not request.carId or not request.garageId:
            raise HTTPException(status_code=400, detail="Invalid data provided")

        maint.service_type = request.serviceType
        maint.scheduled_date = request.scheduledDate
        maint.car_id = request.carId
        maint.garage_id = request.garageId
        s.commit()
        s.refresh(maint)
        return map_maintenance_to_response(maint)


def delete_maintenance(maintenance_id: int) -> MaintenanceResponse:
    with Session() as s, s.begin():
        maint = get_maintenance_by_id(maintenance_id, s)
        s.delete(maint)
        return map_maintenance_to_response(maint)


def map_maintenance_to_response(maintenance: Maintenance) -> MaintenanceResponse:
    return MaintenanceResponse(
        id=maintenance.id,
        carId=maintenance.car_id,
        carName=maintenance.car_name,
        serviceType=maintenance.service_type,
        scheduledDate=maintenance.scheduled_date,
        garageId=maintenance.garage_id,
        garageName=maintenance.garage_name
        #garages=[get_garage(maintenance.garage_id)]
    )

def map_request_to_maintenance(request: MaintenanceRequest) -> Maintenance:
    return Maintenance(
        car_id=request.carId,
        car_name=get_car_name(request.carId),
        service_type=request.serviceType,
        scheduled_date=request.scheduledDate,
        garage_id=request.garageId,
        garage_name= get_garage_name(request.garageId)
    )
