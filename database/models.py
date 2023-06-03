from sqlalchemy import Column, Integer, String, DateTime, ForeignKey,Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Store(Base):
    __tablename__ = 'store'

    id = Column(Integer, primary_key=True)
    store_id = Column(Integer, unique=True, nullable=False)
    timezone_str = Column(String(50), default='America/Chicago')


class StoreHours(Base):
    __tablename__ = 'store_hours'

    id = Column(Integer, primary_key=True)
    store_id = Column(Integer, ForeignKey('store.store_id'), nullable=False)
    day_of_week = Column(Integer, nullable=False)
    start_time_local = Column(Time)
    end_time_local = Column(Time)
    store = relationship('Store', backref='store_hours')


class StoreStatus(Base):
    __tablename__ = 'store_status'

    id = Column(Integer, primary_key=True)
    store_id = Column(Integer, ForeignKey('store.store_id'), nullable=False)
    timestamp_utc = Column(DateTime, nullable=False)
    status = Column(String(10))
    store = relationship('Store', backref='store_status')
