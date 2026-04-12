CREATE OR REFRESH STREAMING TABLE silver_obt
AS 


    SELECT 
        
            stg_rides.ride_id, stg_rides.confirmation_number, stg_rides.passenger_id, stg_rides.driver_id, stg_rides.vehicle_id, stg_rides.pickup_location_id, stg_rides.dropoff_location_id, stg_rides.vehicle_type_id, stg_rides.vehicle_make_id, stg_rides.payment_method_id, stg_rides.ride_status_id, stg_rides.pickup_city_id, stg_rides.dropoff_city_id, stg_rides.cancellation_reason_id, stg_rides.passenger_name, stg_rides.passenger_email, stg_rides.passenger_phone, stg_rides.driver_name, stg_rides.driver_rating, stg_rides.driver_phone, stg_rides.driver_license, stg_rides.vehicle_model, stg_rides.vehicle_color, stg_rides.license_plate, stg_rides.pickup_address, stg_rides.pickup_latitude, stg_rides.pickup_longitude, stg_rides.dropoff_address, stg_rides.dropoff_latitude, stg_rides.dropoff_longitude, stg_rides.distance_miles, stg_rides.duration_minutes, stg_rides.booking_timestamp, stg_rides.pickup_timestamp, stg_rides.dropoff_timestamp, stg_rides.base_fare, stg_rides.distance_fare, stg_rides.time_fare, stg_rides.surge_multiplier, stg_rides.subtotal, stg_rides.tip_amount, stg_rides.total_fare, stg_rides.rating 
                
                    ,
                
        
            map_vehicle_makes.vehicle_make 
                
                    ,
                
        
            map_vehicle_types.vehicle_type,map_vehicle_types.description,map_vehicle_types.base_rate,map_vehicle_types.per_mile,map_vehicle_types.per_minute 
                
                    ,
                
        
            map_ride_statuses.ride_status 
                
                    ,
                
        
            map_payment_methods.payment_method, map_payment_methods.is_card, map_payment_methods.requires_auth 
                
                    ,
                
        
            map_cities.city as pickup_city, map_cities.state, map_cities.region, map_cities.updated_at as city_updated_at 
                
                    ,
                
        
            map_cancellation_reasons.cancellation_reason 
                
        
    FROM 
        
            
                STREAM (uber.bronze.stg_rides) 
                WATERMARK booking_timestamp DELAY OF INTERVAL 3 MINUTES stg_rides
            
            
                LEFT JOIN uber.bronze.map_vehicle_makes map_vehicle_makes ON stg_rides.vehicle_make_id = map_vehicle_makes.vehicle_make_id
            
        
            
                LEFT JOIN uber.bronze.map_vehicle_types map_vehicle_types ON stg_rides.vehicle_type_id = map_vehicle_types.vehicle_type_id
            
        
            
                LEFT JOIN uber.bronze.map_ride_statuses map_ride_statuses ON stg_rides.ride_status_id = map_ride_statuses.ride_status_id
            
        
            
                LEFT JOIN uber.bronze.map_payment_methods map_payment_methods ON stg_rides.payment_method_id = map_payment_methods.payment_method_id
            
        
            
                LEFT JOIN uber.bronze.map_cities map_cities ON stg_rides.pickup_city_id = map_cities.city_id
            
        
            
                LEFT JOIN uber.bronze.map_cancellation_reasons map_cancellation_reasons ON stg_rides.cancellation_reason_id = map_cancellation_reasons.cancellation_reason_id
            
        
   