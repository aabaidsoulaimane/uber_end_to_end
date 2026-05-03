# Uber Ride Data Generator

This project is a Python-based data generator that simulates Uber ride booking events. It exposes a web interface via FastAPI to simulate booking a ride and sends the generated ride details as events to an Azure Event Hub for downstream processing or analytics.

## Features

- **FastAPI Web Application**: Provides a simple UI (using Jinja2 templates) to book a simulated ride.
- **Data Generation**: Uses the `Faker` library to generate realistic synthetic data for ride confirmations, including passenger details, driver info, vehicle models, locations, pricing, and ride status.
- **Azure Event Hub Integration**: Connects to Azure Event Hubs to stream the simulated ride data as JSON events.

## Prerequisites

- Python 3.8+
- An Azure Event Hub namespace and an Event Hub instance
- A `.env` file containing your Azure Event Hub connection string

## Setup

1. Clone this repository.
2. Create and activate a Python virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install fastapi uvicorn jinja2 faker azure-eventhub python-dotenv
   ```
4. Create a `.env` file in the root directory and add your Event Hub credentials (if not already present).

## Usage

1. Start the FastAPI server:
   ```bash
   python api.py
   ```
   Or using Uvicorn directly:
   ```bash
   uvicorn api:app --host 0.0.0.0 --port 8000
   ```
2. Open your web browser and navigate to `http://localhost:8000/`.
3. Click to "book" a ride and trigger the event generation and transmission to Azure Event Hub.
