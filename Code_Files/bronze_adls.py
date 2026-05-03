# Databricks notebook source
import pandas as pd
files=[
{"file":"map_cities"},
{"file":"map_cancellation_reasons"},
{"file":"bulk_rides"},
{"file":"map_payment_methods"},
{"file":"map_ride_statuses"},
{"file":"map_vehicle_makes"},
{"file":"map_vehicle_types"}
]
for file in files:
    url= f"https://dluberproject0.blob.core.windows.net/raw/ingestion/{file['file']}.json?sp=r&st=2026-04-23T11:58:36Z&se=2026-05-01T20:13:36Z&spr=https&sv=2025-11-05&sr=c&sig=CSHf547bmJrjCsN%2FhpliuRyxQW%2BQyhgw5KR5tsiYitM%3D"

    df=pd.read_json(url)
    df_spark=spark.createDataFrame(df)

    df_spark.write.format("delta").mode("overwrite").option("overwriteSchema","True").saveAsTable(f"uber.bronze.{file['file']}")


# COMMAND ----------

# MAGIC %sql 
# MAGIC select * from uber.bronze.map_cities