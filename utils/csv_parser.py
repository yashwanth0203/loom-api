import sys
sys.path.append('../')
import csv
import logging
from datetime import datetime
from pytz import timezone
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from database.models import Store, StoreHours, StoreStatus

# Set up logging
logging.basicConfig(filename='parsing.log', level=logging.DEBUG)

# Define the database URI
DB_URI = 'sqlite:///../database/database.db'

# Create the engine for interacting with the database
engine = create_engine(DB_URI)

# Create a session for interacting with the database
Session = sessionmaker(bind=engine)
session = Session()

# Function to parse the CSV files and insert data into the database
def parse_csv_and_insert_data():
    # 1. Parse the Store Status CSV file
    with open('../data/store_status.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the first row (column headers)
        for row in reader:
            store_id = int(float(row[0]))
            status = row[1]
            timestamp_value = row[2].rstrip(' UTC')
            print(f"Parsing Store Status: {store_id}, {status}, {timestamp_value}")
            try:
                timestamp_utc = datetime.strptime(timestamp_value, '%Y-%m-%d %H:%M:%S.%f')
                print(f"Parsed timestamp UTC: {timestamp_utc}")
            except ValueError:
                logging.warning(f"Invalid timestamp format: {timestamp_value}. Skipping this entry.")
                continue

            store_status = StoreStatus(
                store_id=store_id,
                timestamp_utc=timestamp_utc,
                status=status
            )
            session.add(store_status)

    # 2. Parse the Store Hours CSV file
    with open('../data/menu_hours.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the first row (column headers)
        for row in reader:
            store_id = int(float(row[0]))
            day_of_week = int(row[1])
            print(f"Parsing Store Hours: {store_id}, {day_of_week}")

            start_time_local = row[2] if row[2] else '00:00:00'
            end_time_local = row[3] if row[3] else '23:59:59'

            try:
                parsed_start_time = datetime.strptime(start_time_local, '%H:%M:%S').time()
                parsed_end_time = datetime.strptime(end_time_local, '%H:%M:%S').time()
                print(f"Parsed start time local: {parsed_start_time}")
                print(f"Parsed end time local: {parsed_end_time}")
            except ValueError:
                logging.warning(f"Invalid time format in Store Hours: {start_time_local}, {end_time_local}. Skipping this entry.")
                continue

            store = session.query(Store).filter_by(store_id=store_id).first()

            if store:
                store_hours = StoreHours(
                    store_id=store_id,
                    day_of_week=day_of_week,
                    start_time_local=parsed_start_time,
                    end_time_local=parsed_end_time
                )
            else:
                store_hours = StoreHours(
                    store_id=store_id,
                    day_of_week=day_of_week,
                    start_time_local=parsed_start_time,
                    end_time_local=parsed_end_time
                )
            session.add(store_hours)

    # 3. Parse the Timezone CSV file
    with open('../data/time_zone.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the first row (column headers)
        for row in reader:
            store_id = int(float(row[0]))
            timezone_str = row[1]
            print(f"Parsing Timezone: {store_id}, {timezone_str}")

            store = session.query(Store).filter_by(store_id=store_id).first()

            if timezone_str:
                if store:
                    store.timezone_str = timezone_str
                else:
                    # Assuming all stores are present, missing timezone only
                    store = Store(store_id=store_id, timezone_str=timezone_str)
            else:
                # Handle missing timezone by assuming it is in America/Chicago timezone
                if store:
                    store.timezone_str = 'America/Chicago'
                else:
                    store = Store(store_id=store_id, timezone_str='America/Chicago')
            session.add(store)

    # Commit the changes to the database
    session.commit()

# Call the function to parse CSV files and insert data into the database
parse_csv_and_insert_data()

# Close the session
session.close()
