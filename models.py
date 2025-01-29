from sqlalchemy import Column, Integer, String, Numeric, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship

#Comments with explanation at the bottom

class Base(DeclarativeBase):
    pass

class Garage(Base):
    __tablename__ = "garages"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    city = Column(String, nullable=False)
    capacity = Column(Integer, nullable=False)

class Car(Base):
    __tablename__ = "cars"
    id = Column(Integer, primary_key=True)
    make = Column(String, nullable=False)
    model = Column(String, nullable=False)
    production_year = Column(Integer, nullable=False)
    license_plate = Column(String, unique=True, nullable=False)
    garage_id = Column(Integer, ForeignKey("garages.id"), nullable=False)

class Maintenance(Base):
    __tablename__ = "maintenances"
    id = Column(Integer, primary_key=True)
    car_id = Column(Integer, ForeignKey("cars.id"), nullable=False)
    car_name = Column(String, nullable=False)
    service_type = Column(String, nullable=False)
    scheduled_date = Column(String, nullable=False)
    garage_id = Column(Integer, ForeignKey("garages.id"), nullable=False)
    garage_name = Column(String, nullable=False)
    #car = relationship("Car", back_populates="maintenances")
    #garage = relationship("Garage", back_populates="maintenances")

""""" 

    # Car to Garage: One-to-Many
Implemented by:
placing "garages = relationship("Garage", cascade="all, delete-orphan")" in Car(Base)
and placing "car_id = Column(Integer, ForeignKey("cars.id"))" in Garage(Base)

"""""