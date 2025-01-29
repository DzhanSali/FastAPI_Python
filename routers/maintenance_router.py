from fastapi import APIRouter
from DTOs.dtos import MaintenanceResponse, MaintenanceRequest, MonthlyRequestReport
from services.maintenance_service import get_maintenances, get_maintenance_by_filter, create_maintenance, \
    update_maintenance, delete_maintenance, get_monthly_report

maintenance_router = APIRouter()

@maintenance_router.get("/maintenance", response_model=list[MaintenanceResponse], status_code=200)
def get_maintenance(carId: int | None=None, garageId: int | None = None, startDate: str | None = None, endDate: str | None = None):
    if not carId and not garageId and not startDate and not endDate:
        return get_maintenances()
    else:
        return get_maintenance_by_filter(carId, garageId, startDate, endDate)

@maintenance_router.get("/maintenance/monthlyRequestsReport", response_model=list[MonthlyRequestReport], status_code=200)
def get_report(garageId: int, startMonth: str, endMonth: str):
    return get_monthly_report(garageId, startMonth, endMonth)

@maintenance_router.get("/maintenance/{maintenance_id}", response_model=MaintenanceResponse, status_code=200)
def get_single_maintenance(maintenance_id:int):
    return get_maintenance(maintenance_id)

@maintenance_router.post("/maintenance", response_model=MaintenanceResponse, status_code=201)
def create_new_maintenance(request: MaintenanceRequest):
    return create_maintenance(request)

@maintenance_router.put("/maintenance/{maintenance_id}", response_model=MaintenanceResponse, status_code=200)
def update_a_maintenance(maintenance_id: int, request: MaintenanceRequest):
    return update_maintenance(maintenance_id, request)

@maintenance_router.delete("/maintenance/{maintenance_id}", response_model=MaintenanceResponse, status_code=200)
def delete_a_maintenance(maintenance_id: int):
    return delete_maintenance(maintenance_id)