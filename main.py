from fastapi import FastAPI
import uvicorn
from starlette.middleware.cors import CORSMiddleware

from routers.car_router import car_router
from routers.garage_router import garage_router
from routers.maintenance_router import maintenance_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(garage_router, tags=["Garages API"])
app.include_router(car_router, tags=["Cars API"])
app.include_router(maintenance_router, tags=["Maintenance API"])

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8088)