#  Uber End-to-End Data Engineering Project

Welcome to the **Uber End-to-End Data Engineering Project**! This repository demonstrates a complete, production-ready data pipeline built around a Medallion Architecture. It features real-time data streaming, batch processing, and a scalable cloud data lake.

If you found this project via LinkedIn, I'd love to connect and hear your thoughts on Data Engineering!

##  Project Overview

The goal of this project is to simulate and process Uber ride data in near real-time, combining streaming events with historical batch data to create a unified source of truth for business intelligence and analytics.

###  Architecture & Flow
This pipeline implements the **Medallion Architecture (Bronze ➔ Silver ➔ Gold)**:

1. **Data Generation (The "Producer")**:
   - A custom **FastAPI** web application serves as a simulator, generating synthetic but realistic Uber ride bookings using Python's `Faker` library.
   - Ride events are instantly streamed to **Azure Event Hubs**.
2. **Data Lake Storage (Batch & Static Data)**:
   - Historical bulk ride data and mapping tables (Cities, Payment Methods, Vehicle Types, etc.) are securely stored in **Azure Data Lake Storage (ADLS)**.
3. **Bronze Layer (Raw Data Ingestion)**:
   - **Databricks** ingests static batch data from ADLS into Delta tables.
   - **Delta Live Tables (DLT)** using PySpark continuously consume streaming data from Azure Event Hubs (via Kafka protocol) into raw tables.
4. **Silver Layer (Cleansed & Conformed)**:
   - Streaming data (`rides_raw`) and batch data (`bulk_rides`) are merged.
   - JSON payloads are parsed with explicitly defined schemas and validated into a staging table (`stg_rides`).
5. **Gold Layer (One Big Table / OBT)**:
   - Using Spark SQL and Databricks DLT features, the staging rides are enriched by joining them with all mapping dimension tables.
   - The result is a highly optimized **One Big Table (OBT)** ready for fast querying, BI dashboards, and ML models.

##  Technology Stack

- **Data Processing & Orchestration:** Databricks, Delta Live Tables (DLT), PySpark, Spark SQL, Delta Lake
- **Streaming & Messaging:** Azure Event Hubs, Kafka API
- **Cloud Storage:** Azure Data Lake Storage (ADLS Gen2)
- **Data Producer / API:** Python, FastAPI, Uvicorn, Jinja2, Faker

##  Repository Structure

- `/` (Root): The FastAPI web app simulating the Uber rides and pushing to Event Hubs.
- `Code_Files/`: Contains the Databricks pipelines and DLT code.
  - `bronze_adls.py`: Ingestion from ADLS to Bronze Delta Tables.
  - `ingest.py`: PySpark Streaming pipeline connecting to Azure Event Hubs.
  - `silver.py`: DLT pipeline handling the stream/batch union and JSON schema parsing.
  - `silver_obt.sql` / `.ipynb`: Creation of the Gold Layer (One Big Table) joining facts and dimensions using streaming watermarks.

## How to Run Locally (Producer App)

If you'd like to spin up the data generator locally:

1. Clone this repository.
2. Set up a Python virtual environment and install requirements:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install fastapi uvicorn jinja2 faker azure-eventhub python-dotenv
   ```
3. Create a `.env` file in the root directory and add your Azure Event Hub connection string:
   ```env
   connection_string="Endpoint=sb://your-namespace.servicebus.windows.net/;SharedAccessKeyName=...;SharedAccessKey=...;EntityPath=your-topic"
   ```
4. Start the simulation application:
   ```bash
   uvicorn api:app --host 0.0.0.0 --port 8000
   ```
5. Navigate to `http://localhost:8000/` and book a simulated ride to send events to the cloud!

---

💡 *Feel free to fork this repository, explore the Databricks code, and deploy your own version of the pipeline. Let's talk Data Engineering!*
