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

# Pulling Data Generator Function
from data import generate_uber_ride_confirmation

CONNECTION_STRING = os.getenv("CONNECTION_STRING")
EVENT_HUBNAME = os.getenv("EVENT_HUBNAME")




def send_to_event_hub(ride_data=None, batch_size=1):

    try:
        # Initialize Event Hub Producer Client
        producer = EventHubProducerClient.from_connection_string(
            CONNECTION_STRING,
            eventhub_name=EVENT_HUBNAME
        )
        
        # Prepare ride records
        ride_json = json.dumps(ride_data) 
        
        # Create batch of events
        event_batch = producer.create_batch()

            
        # Create event with ride data 
        event = EventData(ride_json)
            
        # Add event to batch
        event_batch.add(event)

        # Send batch to Event Hub
        producer.send_batch(event_batch)
        
        producer.close()

        return "Successfully sent to Event Hub"
        
    except Exception as e:
        print(f"Error sending data to Event Hub: {str(e)}")
        return False



if __name__ == "__main__":
    
    print("=" * 80)
    print("SINGLE RIDE CONFIRMATION")
    print("=" * 80)
    ride = generate_uber_ride_confirmation()
    print(json.dumps(ride, indent=2))

    
    print("\n" + "=" * 80)
    print("SENDING SINGLE RIDE TO EVENT HUB")
    result = send_to_event_hub(ride)
    print(f"Single ride sent to Event Hub: {result}")
    
    