import requests
import pvlib
import json
import joblib
import pandas as pd
import uvicorn
from fastapi import FastAPI , HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from timezonefinderL import TimezoneFinder
from datetime import datetime, timedelta

# --- Step 1: Define the API's input structure ---
# This tells FastAPI what kind of JSON data to expect for a request.
# It MUST match the features your model was trained on.
class SolarData(BaseModel):
    ghi: float
    temp_c: float
    humidity: float
    wind_speed_ms: float
    dni: float
    dhi: float
    poa_global: float

# This is the high-level input we'll get from the frontend
class FrontendData(BaseModel):
    latitude: float
    longitude: float
    panel_surface_area: float
    tilt_angle: float
    azimuth_angle: float
    panel_efficiency: float # Expecting a value like 20 for 20% 
    cost_per_kwh: float = 0.15 # Add a default cost in USD if frontend doesn't send it   

# --- Step 2: Load your trained model ---
MODEL_FILE_PATH = "models/solar_model_Ahmedabad_India.pkl"
try:
    model = joblib.load(MODEL_FILE_PATH)
    print(f"✅ Model '{MODEL_FILE_PATH}' loaded successfully.")
except FileNotFoundError:
    print(f"❌ ERROR: Model file not found at '{MODEL_FILE_PATH}'.")
    model = None

# --- Step 3: Create the FastAPI application ---
app = FastAPI(title="Solar Power Prediction API")

# Add CORS middleware to allow frontend connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# --- Step 4: Define Helper Functions (The "Refinery") ---

# def fetch_nasa_power_data(lat: float, lon: float):
#     """
#     Fetches the last 24 hours of weather data to use as a forecast proxy.
#     """
#     print(f"Fetching weather forecast data for Lat: {lat}, Lon: {lon}...")
#     # Get dates for the last 24 hours
#     # end_date = datetime.now()- timedelta(days=1)
#     # start_date = end_date - timedelta(days=1)
#     # --- THIS IS THE NEW LOGIC ---
#     # It loops, trying multiple days until it finds a good one.
#     for i in range(2, 8): 
#         target_date = datetime.now() - timedelta(days=i)
#         date_str = target_date.strftime("%Y%m%d")
#         print(f"--> Attempting to fetch data for {date_str}...")
    
#     base_url = "https://power.larc.nasa.gov/api/temporal/hourly/point"
#     params = {
#         "parameters": "ALLSKY_SFC_SW_DWN,T2M,RH2M,WS10M",
#         "community": "RE",
#         "longitude": lon,
#         "latitude": lat,
#         "start": date_str,
#         "end": date_str,
#         "format": "JSON",
#     }
#     response = requests.get(base_url, params=params)
#     if response.status_code != 200:
#         raise HTTPException(status_code=500, detail="Could not fetch data from NASA POWER API.")
    
#     # data = response.json()
#     # records = []
#     # dates = data['properties']['parameter']['ALLSKY_SFC_SW_DWN'].keys()
#     # for date_str in dates:
#     #     dt_obj = pd.to_datetime(date_str, format='%Y%m%d%H')
#     #     records.append({
#     #         "timestamp": dt_obj,
#     #         "ghi": data['properties']['parameter']['ALLSKY_SFC_SW_DWN'][date_str],
#     #         "temp_c": data['properties']['parameter']['T2M'][date_str],
#     #         "humidity": data['properties']['parameter']['RH2M'][date_str],
#     #         "wind_speed_ms": data['properties']['parameter']['WS10M'][date_str],
#     #     })
#     # return pd.DataFrame(records).set_index("timestamp")
#  # chnage here
#     data = response.json()
#     records = []
#     param_data = data.get('properties', {}).get('parameter', {})
#     if not param_data or 'ALLSKY_SFC_SW_DWN' not in param_data:
#         print("❌ ERROR: 'ALLSKY_SFC_SW_DWN' not found in API response.")
#         return pd.DataFrame()
def fetch_nasa_power_data(lat: float, lon: float):
    # Try to fetch live data first
    for i in range(2, 5): # Try for 3 days to be quick
        target_date = datetime.now() - timedelta(days=i)
        date_str = target_date.strftime("%Y%m%d")
        print(f"--> Attempting to fetch live data for {date_str}...")

        base_url = "https://power.larc.nasa.gov/api/temporal/hourly/point"
        params = { "parameters": "ALLSKY_SFC_SW_DWN,T2M,RH2M,WS10M", "community": "RE", "longitude": lon, "latitude": lat, "start": date_str, "end": date_str, "format": "JSON" }
        
        try:
            response = requests.get(base_url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            records = []
            param_data = data.get('properties', {}).get('parameter', {})
            if not param_data or 'ALLSKY_SFC_SW_DWN' not in param_data: continue

            for date_key in param_data['ALLSKY_SFC_SW_DWN'].keys():
                ghi = param_data.get('ALLSKY_SFC_SW_DWN', {}).get(date_key, -999)
                if ghi == -999: continue
                
                dt_obj = pd.to_datetime(date_key, format='%Y%m%d%H')
                temp = param_data.get('T2M', {}).get(date_key, 0)
                humidity = param_data.get('RH2M', {}).get(date_key, 0)
                wind = param_data.get('WS10M', {}).get(date_key, 0)

                records.append({ "timestamp": dt_obj, "ghi": ghi, "temp_c": temp if temp != -999 else 0, "humidity": humidity if humidity != -999 else 0, "wind_speed_ms": wind if wind != -999 else 0 })
            
            if records:
                print(f"✅ Successfully fetched live data for {date_str}.")
                return pd.DataFrame(records).set_index("timestamp")
            else:
                print(f"    - No valid live records for {date_str}. Trying previous day.")

        except requests.exceptions.RequestException:
            print(f"    - Live API request failed for {date_str}. Trying previous day.")
            continue
            
    # ** THE FALLBACK LOGIC IS HERE **
    print("❌ Live API failed. Using local fallback data for demo.")
    try:
        with open('sample_data.json', 'r') as f:
            sample_records = json.load(f)
        df = pd.DataFrame(sample_records)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df.set_index('timestamp')
    except FileNotFoundError:
        print("❌ CRITICAL ERROR: Fallback file 'sample_data.json' not found.")
        return pd.DataFrame()

    dates = param_data['ALLSKY_SFC_SW_DWN'].keys()
    for date_key in dates:
        dt_obj = pd.to_datetime(date_key, format='%Y%m%d%H')
        ghi = param_data.get('ALLSKY_SFC_SW_DWN', {}).get(date_key, 0)
        
        # If GHI is missing, there's no point in continuing for this hour
        if ghi == -999:
            continue
            
        temp = param_data.get('T2M', {}).get(date_key, 0)
        humidity = param_data.get('RH2M', {}).get(date_key, 0)
        wind = param_data.get('WS10M', {}).get(date_key, 0)

        records.append({
            "timestamp": dt_obj,
            "ghi": ghi,
            "temp_c": temp if temp != -999 else 0,
            "humidity": humidity if humidity != -999 else 0,
            "wind_speed_ms": wind if wind != -999 else 0,
        })
        if records:
            print(f"✅ Successfully fetched valid data for {date_str}.")
            return pd.DataFrame(records).set_index("timestamp")
        else:
            print(f"    - No valid records found for {date_str}. Trying previous day.")
            
    print("❌ Could not find any valid data in the last 7 days.")
    return pd.DataFrame()

def engineer_solar_features(weather_df, data: FrontendData):
    """
    Takes raw weather data and panel details, then calculates the
    scientific features needed for the model.
    """
    if weather_df.empty:
        return weather_df
    
    print("Engineering features with pvlib...")
    tf = TimezoneFinder()
    timezone_str = tf.timezone_at(lng=data.longitude, lat=data.latitude)
    
    location = pvlib.location.Location(data.latitude, data.longitude, tz=timezone_str)
    solar_position = location.get_solarposition(times=weather_df.index)
    
    dni_dhi = pvlib.irradiance.erbs(weather_df['ghi'], solar_position['apparent_zenith'], weather_df.index)
    weather_df['dni'] = dni_dhi['dni'].fillna(0)
    weather_df['dhi'] = dni_dhi['dhi'].fillna(0)
    
    total_irradiance = pvlib.irradiance.get_total_irradiance(
        surface_tilt=data.tilt_angle,
        surface_azimuth=data.azimuth_angle,
        solar_zenith=solar_position['apparent_zenith'],
        solar_azimuth=solar_position['azimuth'],
        dni=weather_df['dni'],
        ghi=weather_df['ghi'],
        dhi=weather_df['dhi']
    )
    weather_df['poa_global'] = total_irradiance['poa_global'].fillna(0)
    return weather_df


# --- Step 5: Define API Endpoints ---

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Solar Prediction API is running!", "status": "healthy"}

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "endpoints": ["/generate_report", "/health", "/docs"]
    }

@app.post("/generate_report")
async def generate_report(data: FrontendData):
    """
    This is the new main endpoint. It takes frontend data, gets a 24-hour prediction,
    and calculates total power and income statistics.
    """
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded.")

    # 1. Get reliable weather data from NASA
    weather_df = fetch_nasa_power_data(data.latitude, data.longitude)
    if weather_df.empty:
        raise HTTPException(status_code=404, detail="Could not retrieve valid weather data for the specified location.")

    # 2. Calculate the scientific features
    features_df = engineer_solar_features(weather_df, data)

    # 3. Get predictions and calculate totals
    predictions = []
    total_watts_today = 0
    feature_columns = ['ghi', 'temp_c', 'humidity', 'wind_speed_ms', 'dni', 'dhi', 'poa_global']
    
    for timestamp, row in features_df.iterrows():
        input_data = row[feature_columns].to_frame().T
        power_watts = model.predict(input_data)[0]
        power_watts = round(power_watts, 2) if power_watts > 0 else 0
        
        predictions.append({
            "timestamp": timestamp.isoformat(),
            "predicted_power_w": power_watts
        })
        total_watts_today += power_watts

    # 4. Calculate final statistics
    # Since predictions are hourly, total_watts_today is effectively Watt-hours
    total_kwh_today = round(total_watts_today / 1000, 2)
    daily_income = round(total_kwh_today * data.cost_per_kwh, 2)
    monthly_income = round(daily_income * 30, 2)

    return {
        "total_kwh_today": total_kwh_today,
        "daily_income": daily_income,
        "monthly_income": monthly_income,
        "hourly_predictions": predictions
    }


# --- Step 6: Run the API locally ---
if __name__ == "__main__":
    print("🌞 Starting Solar Prediction API...")
    print("=" * 50)
    print("✅ API will be available at: http://127.0.0.1:8000")
    print("📊 Main endpoint: http://127.0.0.1:8000/generate_report")
    print("📖 API documentation: http://127.0.0.1:8000/docs")
    print("🔄 Interactive API: http://127.0.0.1:8000/redoc")
    print("=" * 50)
    print("Press Ctrl+C to stop the server")
    
    try:
        uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")