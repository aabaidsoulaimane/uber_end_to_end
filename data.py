import random
import uuid
import json
from datetime import datetime, timedelta
from faker import Faker
from azure.eventhub import EventHubProducerClient, EventData
import logging
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file
import os

fake = Faker()


VEHICLE_TYPE_MAPPING = [
    {'vehicle_type_id': 1, 'vehicle_type': 'UberX', 'description': 'Standard', 'base_rate': 2.50, 'per_mile': 1.75, 'per_minute': 0.35},
    {'vehicle_type_id': 2, 'vehicle_type': 'UberXL', 'description': 'Extra Large', 'base_rate': 3.50, 'per_mile': 2.25, 'per_minute': 0.45},
    {'vehicle_type_id': 3, 'vehicle_type': 'UberPOOL', 'description': 'Shared Ride', 'base_rate': 2.00, 'per_mile': 1.50, 'per_minute': 0.30},
    {'vehicle_type_id': 4, 'vehicle_type': 'Uber Comfort', 'description': 'Comfortable', 'base_rate': 3.00, 'per_mile': 2.00, 'per_minute': 0.40},
    {'vehicle_type_id': 5, 'vehicle_type': 'Uber Black', 'description': 'Premium', 'base_rate': 5.00, 'per_mile': 3.50, 'per_minute': 0.60}
]

PAYMENT_METHOD_MAPPING = [
    {'payment_method_id': 1, 'payment_method': 'Credit Card', 'is_card': True, 'requires_auth': True},
    {'payment_method_id': 2, 'payment_method': 'Debit Card', 'is_card': True, 'requires_auth': True},
    {'payment_method_id': 3, 'payment_method': 'Digital Wallet', 'is_card': False, 'requires_auth': False},
    {'payment_method_id': 4, 'payment_method': 'Cash', 'is_card': False, 'requires_auth': False}
]

RIDE_STATUS_MAPPING = [
    {'ride_status_id': 1, 'ride_status': 'Completed', 'is_completed': True},
    {'ride_status_id': 2, 'ride_status': 'Cancelled', 'is_completed': False}
]

VEHICLE_MAKE_MAPPING = [
    {'vehicle_make_id': 1, 'vehicle_make': 'Toyota'},
    {'vehicle_make_id': 2, 'vehicle_make': 'Honda'},
    {'vehicle_make_id': 3, 'vehicle_make': 'Ford'},
    {'vehicle_make_id': 4, 'vehicle_make': 'Chevrolet'},
    {'vehicle_make_id': 5, 'vehicle_make': 'Nissan'},
    {'vehicle_make_id': 6, 'vehicle_make': 'BMW'},
    {'vehicle_make_id': 7, 'vehicle_make': 'Mercedes'}
]

VEHICLE_MAKES_LIST = [m['vehicle_make'] for m in VEHICLE_MAKE_MAPPING]
VEHICLE_MAKE_ID_MAP = {m['vehicle_make']: m['vehicle_make_id'] for m in VEHICLE_MAKE_MAPPING}

VEHICLE_TYPES_LIST = [t['vehicle_type'] for t in VEHICLE_TYPE_MAPPING]
VEHICLE_TYPE_ID_MAP = {t['vehicle_type']: t['vehicle_type_id'] for t in VEHICLE_TYPE_MAPPING}

PAYMENT_METHODS_LIST = [p['payment_method'] for p in PAYMENT_METHOD_MAPPING]
PAYMENT_METHOD_ID_MAP = {p['payment_method']: p['payment_method_id'] for p in PAYMENT_METHOD_MAPPING}

RIDE_STATUSES_LIST = [s['ride_status'] for s in RIDE_STATUS_MAPPING]
RIDE_STATUS_ID_MAP = {s['ride_status']: s['ride_status_id'] for s in RIDE_STATUS_MAPPING}

CITY_MAPPING = [
    {'city_id': 1, 'city': 'New York', 'state': 'NY', 'region': 'Northeast'},
    {'city_id': 2, 'city': 'Los Angeles', 'state': 'CA', 'region': 'West'},
    {'city_id': 3, 'city': 'Chicago', 'state': 'IL', 'region': 'Midwest'},
    {'city_id': 4, 'city': 'Houston', 'state': 'TX', 'region': 'South'},
    {'city_id': 5, 'city': 'Phoenix', 'state': 'AZ', 'region': 'Southwest'},
    {'city_id': 6, 'city': 'Philadelphia', 'state': 'PA', 'region': 'Northeast'},
    {'city_id': 7, 'city': 'San Antonio', 'state': 'TX', 'region': 'South'},
    {'city_id': 8, 'city': 'San Diego', 'state': 'CA', 'region': 'West'},
    {'city_id': 9, 'city': 'Dallas', 'state': 'TX', 'region': 'South'},
    {'city_id': 10, 'city': 'San Jose', 'state': 'CA', 'region': 'West'}
]

CITY_LIST = [c['city'] for c in CITY_MAPPING]
CITY_ID_MAP = {c['city']: c['city_id'] for c in CITY_MAPPING}

CANCELLATION_REASON_MAPPING = [
    {'cancellation_reason_id': 1, 'cancellation_reason': 'Driver cancelled'},
    {'cancellation_reason_id': 2, 'cancellation_reason': 'Passenger cancelled'},
    {'cancellation_reason_id': 3, 'cancellation_reason': 'No show'},
    {'cancellation_reason_id': 4, 'cancellation_reason': None}  # Completed rides
]

CANCELLATION_REASON_ID_MAP = {c['cancellation_reason']: c['cancellation_reason_id'] for c in CANCELLATION_REASON_MAPPING}



def generate_uber_ride_confirmation():
    
    # Generate timestamps
    pickup_time = datetime.now() - timedelta(days=random.randint(0, 30), hours=random.randint(0, 23))
    duration_minutes = random.randint(5, 120)
    dropoff_time = pickup_time + timedelta(minutes=duration_minutes)
    booking_time = pickup_time - timedelta(minutes=random.randint(1, 10))
    
    # Distance in miles
    distance = round(random.uniform(0.5, 50), 2)
    
    # Pricing calculation
    base_fare = 2.50
    per_mile_rate = 1.75
    per_minute_rate = 0.35
    surge_multiplier = round(random.uniform(1.0, 2.5), 2)
    
    distance_fare = round(distance * per_mile_rate, 2)
    time_fare = round(duration_minutes * per_minute_rate, 2)
    subtotal = round((distance_fare + time_fare + base_fare) * surge_multiplier, 2)
    tip = round(random.choice([0, 0, 0, 1, 2, 3, 5, random.uniform(1, 20)]), 2)
    total_fare = round(subtotal + tip, 2)
    
    # Location details
    pickup_address = fake.address().replace('\n', ', ')
    dropoff_address = fake.address().replace('\n', ', ')
    
    # Get cities and their IDs
    pickup_city = random.choice(CITY_LIST)
    dropoff_city = random.choice(CITY_LIST)
    pickup_city_id = CITY_ID_MAP[pickup_city]
    dropoff_city_id = CITY_ID_MAP[dropoff_city]
    
    # Get vehicle make and its ID
    vehicle_make = random.choice(VEHICLE_MAKES_LIST)
    vehicle_make_id = VEHICLE_MAKE_ID_MAP[vehicle_make]
    
    # Determine cancellation status
    is_cancelled = random.random() < 0.1
    cancellation_reason = None
    cancellation_reason_id = 4  # Default: None (completed)
    if is_cancelled:
        cancellation_reason = random.choice(['Driver cancelled', 'Passenger cancelled', 'No show'])
        cancellation_reason_id = CANCELLATION_REASON_ID_MAP[cancellation_reason]

    # Get vehicle type and its ID
    vehicle_type = random.choice(VEHICLE_TYPES_LIST)
    vehicle_type_id = VEHICLE_TYPE_ID_MAP[vehicle_type]

    # Get payment method and its ID
    payment_method = random.choice(PAYMENT_METHODS_LIST)
    payment_method_id = PAYMENT_METHOD_ID_MAP[payment_method]

    # Get ride status and its ID
    ride_status = random.choice(['Completed', 'Completed', 'Cancelled'])
    ride_status_id = RIDE_STATUS_ID_MAP[ride_status]
    
    # Ride confirmation
    ride_confirmation = {
        # Keys/Identifiers
        'ride_id': str(uuid.uuid4()),
        'confirmation_number': fake.bothify('??#-####-??##'),
        'passenger_id': str(uuid.uuid4()),
        'driver_id': str(uuid.uuid4()),
        'vehicle_id': str(uuid.uuid4()),
        'pickup_location_id': str(uuid.uuid4()),
        'dropoff_location_id': str(uuid.uuid4()),
        
        # Foreign Keys to Mapping Tables
        'vehicle_type_id': vehicle_type_id,
        'vehicle_make_id': vehicle_make_id,
        'payment_method_id': payment_method_id,
        'ride_status_id': ride_status_id,
        'pickup_city_id': pickup_city_id,
        'dropoff_city_id': dropoff_city_id,
        'cancellation_reason_id': cancellation_reason_id,
        
        # Passenger Information
        'passenger_name': fake.name(),
        'passenger_email': fake.email(),
        'passenger_phone': fake.phone_number(),
        
        # Driver Information
        'driver_name': fake.name(),
        'driver_rating': round(random.uniform(4.0, 5.0), 2),
        'driver_phone': fake.phone_number(),
        'driver_license': fake.bothify('??-???-#######'),
        
        # Vehicle Information
        'vehicle_model': fake.word().capitalize(),
        'vehicle_color': random.choice(['Black', 'White', 'Gray', 'Silver', 'Blue', 'Red']),
        'license_plate': fake.bothify('???-####'),
        
        # Pickup & Dropoff Locations
        'pickup_address': pickup_address,
        'pickup_latitude': round(random.uniform(-90, 90), 6),
        'pickup_longitude': round(random.uniform(-180, 180), 6),
        'dropoff_address': dropoff_address,
        'dropoff_latitude': round(random.uniform(-90, 90), 6),
        'dropoff_longitude': round(random.uniform(-180, 180), 6),
        
        # Ride Details - Measures
        'distance_miles': distance,
        'duration_minutes': duration_minutes,
        'booking_timestamp': booking_time.isoformat(),
        'pickup_timestamp': pickup_time.isoformat(),
        'dropoff_timestamp': dropoff_time.isoformat(),
        
        # Pricing - Measures
        'base_fare': base_fare,
        'distance_fare': distance_fare,
        'time_fare': time_fare,
        'surge_multiplier': surge_multiplier,
        'subtotal': subtotal,
        'tip_amount': tip,
        'total_fare': total_fare,
        
        # Payment & Status
        'rating': random.choice([None, random.randint(1, 5)])
    }
    
    return ride_confirmation
