# 🌞 Solar Prediction System

A comprehensive solar energy prediction system with AI-powered forecasting and beautiful dark-themed UI.

## ✨ Features

- **AI-Powered Predictions**: Uses machine learning to predict solar power generation
- **Real-time Weather Data**: Fetches live weather data from NASA POWER API
- **Beautiful UI**: Dark theme with golden accents and responsive design
- **Interactive Charts**: Hourly power generation visualization
- **Income Calculations**: Daily and monthly income projections
- **Export Functionality**: Print and download prediction reports

## 🏗️ Architecture

### Backend (FastAPI)
- **Framework**: FastAPI with Python
- **ML Model**: Trained solar prediction model
- **Weather API**: NASA POWER API integration
- **Solar Calculations**: pvlib for solar irradiance calculations
- **Port**: 8000

### Frontend (HTML/CSS/JS)
- **Design**: Dark theme with golden (#FFD700) accents
- **Charts**: Chart.js for data visualization
- **Responsive**: Mobile-friendly design
- **Port**: 8080

## 🚀 Quick Start

### Prerequisites
```bash
pip install fastapi uvicorn pandas pvlib requests joblib pyngrok nest-asyncio timezonefinderL
```

### Option 1: Using Startup Scripts (Recommended)

1. **Start Backend** (Terminal 1):
   ```bash
   python start_backend.py
   ```

2. **Start Frontend** (Terminal 2):
   ```bash
   python start_frontend.py
   ```

### Option 2: Manual Start

1. **Start Backend**:
   ```bash
   cd backend
   python api_fastapi.py
   ```

2. **Start Frontend**:
   ```bash
   cd frontend
   python -m http.server 8080
   ```

## 📊 API Endpoints

### POST /generate_report
Generates solar power predictions and income calculations.

**Request Body:**
```json
{
  "latitude": 23.0225,
  "longitude": 72.5714,
  "panel_surface_area": 20.0,
  "tilt_angle": 25.0,
  "azimuth_angle": 180.0,
  "panel_efficiency": 20.0,
  "cost_per_kwh": 0.15
}
```

**Response:**
```json
{
  "total_kwh_today": 12.34,
  "daily_income": 1.85,
  "monthly_income": 55.50,
  "hourly_predictions": [
    {
      "timestamp": "2024-01-01T08:00:00",
      "predicted_power_w": 1250.5
    }
  ]
}
```

## 🎨 UI Features

- **Location Detection**: Automatic GPS location detection
- **Form Validation**: Real-time input validation
- **Loading States**: Beautiful loading animations
- **Error Handling**: User-friendly error messages
- **Responsive Design**: Works on all devices
- **Print Support**: Print-friendly report layouts

## 📁 Project Structure

```
solar-prediction-system/
├── backend/
│   ├── api_fastapi.py          # FastAPI server
│   ├── sample_data.json        # Fallback weather data
│   └── models/
│       └── solar_model_Ahmedabad_India.pkl
├── frontend/
│   ├── index.html              # Main prediction form
│   ├── results.html            # Results display
│   ├── style.css               # Dark theme styling
│   ├── about.html              # About page
│   ├── login.html              # Login page
│   └── signup.html             # Signup page
├── start_backend.py            # Backend startup script
├── start_frontend.py           # Frontend startup script
└── README.md                   # This file
```

## 🔧 Configuration

### Weather Data
- **Primary**: NASA POWER API (live data)
- **Fallback**: Local sample_data.json
- **Timeout**: 10 seconds for API requests

### Model
- **Type**: Trained ML model for Ahmedabad, India
- **Features**: GHI, temperature, humidity, wind speed, DNI, DHI, POA
- **Output**: Power generation in watts

### UI Theme
- **Background**: Black (#000000)
- **Primary**: Gold (#FFD700)
- **Secondary**: Light Gold (#FFB300)
- **Text**: White (#FFFFFF) / Light Gray (#CCCCCC)

## 🌐 Access URLs

- **Frontend**: http://127.0.0.1:8080/index.html
- **Backend API**: http://127.0.0.1:8000/generate_report
- **API Documentation**: http://127.0.0.1:8000/docs

## 🛠️ Development

### Adding New Features
1. Backend changes go in `backend/api_fastapi.py`
2. Frontend changes go in `frontend/` files
3. Styling updates go in `frontend/style.css`

### Testing
1. Use sample coordinates: Lat: 23.0225, Lon: 72.5714 (Ahmedabad)
2. Try different panel configurations
3. Check both live API and fallback data scenarios

## 📱 Mobile Support

The system is fully responsive and works on:
- Desktop browsers
- Tablets
- Mobile phones
- Touch devices

## 🎯 Future Enhancements

- [ ] User authentication system
- [ ] Historical data analysis
- [ ] Multiple location support
- [ ] Weather forecast integration
- [ ] Advanced reporting features
- [ ] Database integration
- [ ] Real-time monitoring

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

---
