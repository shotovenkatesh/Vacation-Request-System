from sqlalchemy import create_engine, Column, Integer, String, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class Employee(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    start_date = Column(Date)
    vacation_days = Column(Integer)
    is_full_time = Column(Boolean)

engine = create_engine('sqlite:///employees.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def get_employee(name):
    return session.query(Employee).filter_by(name=name).first()

def update_vacation_days(name, days):
    employee = get_employee(name)
    if employee:
        employee.vacation_days -= days
        session.commit()

# Example Employee
if not get_employee("John Doe"):
    new_employee = Employee(
        name="John Doe",
        start_date=datetime.strptime("2024-01-01", "%Y-%m-%d"),
        vacation_days=20,
        is_full_time=True
    )
    session.add(new_employee)
    session.commit()

if not get_employee("Jane Smith"):
    new_employee = Employee(
        name="Jane Smith",
        start_date=datetime.strptime("2024-03-01", "%Y-%m-%d"),
        vacation_days=20,
        is_full_time=True
    )
    session.add(new_employee)
    session.commit()
