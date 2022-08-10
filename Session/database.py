from datetime import datetime
from datetime import timedelta

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Sequence, Column, Integer, String, TEXT, FLOAT
from sqlalchemy.dialects.postgresql import TIMESTAMP

from sqlalchemy import create_engine
from sqlalchemy.orm.session import Session
from sqlalchemy.pool import NullPool

Base = declarative_base()


class Journey(Base):
    # name of the table
    __tablename__ = "journeys_chip"
    id = Column(Integer, primary_key=True)
    departureStation = Column(String(255))
    departureCityId = Column(String(255))
    departureStationId = Column(String(255))
    departureTime = Column(TIMESTAMP)
    arrivalStation = Column(String(255))
    arrivalCityId = Column(String(255))
    arrivalStationId = Column(String(255))
    arrivalTime = Column(TIMESTAMP)
    travelTime = Column(String(255))


def write_to_db(departure, departure_city_id, departure_station_id, departure_datetime, arrival, arrival_city_id,
                arrival_station_id, arrival_datetime, travel_time):
    journey = Journey(
        departureStation=departure, departureCityId=departure_city_id, departureStationId=departure_station_id,
        departureTime=departure_datetime,
        arrivalStation=arrival, arrivalCityId=arrival_city_id, arrivalStationId=arrival_station_id,
        arrivalTime=arrival_datetime, travelTime=travel_time)

    with Session(engine) as session:
        session.add(journey)
        session.commit()


def read_from_db(departure_id, arrival_id, time):
    time_nim = datetime.fromisoformat(time)
    time_max = time_nim + timedelta(hours=23, minutes=59, seconds=59)

    with Session(engine) as session:
        return session.query(Journey).filter(
            Journey.departureTime >= time_nim,
            Journey.departureTime <= time_max,
            Journey.departureCityId == departure_id,
            Journey.arrivalCityId == arrival_id
        ).all()


DATABASE_URL = (
    "postgresql://pythonweekend:2oggOq1e2buHENZa@sql.pythonweekend.skypicker.com/pythonweekend?application_name=pythonweekend_local_dev")
# echo=True shows debug information
# NullPool closes unused connections immediately
engine = create_engine(DATABASE_URL, echo=True, poolclass=NullPool)

if __name__ == '__main__':
    Base.metadata.create_all(engine)
