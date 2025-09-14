#!/usr/bin/env python3
"""
Quick startup script for the Solar Prediction System backend
"""
import os
import sys
import subprocess

def main():
    print("🌞 Starting Solar Prediction System Backend...")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("backend/api_fastapi.py"):
        print("❌ Error: Please run this script from the project root directory")
        sys.exit(1)
    
    # Check if required files exist
    required_files = [
        "backend/api_fastapi.py",
        "backend/models/solar_model_Ahmedabad_India.pkl",
        "backend/sample_data.json"
    ]
    
    for file_path in required_files:
        if not os.path.exists(file_path):
            print(f"❌ Error: Required file missing: {file_path}")
            sys.exit(1)
    
    print("✅ All required files found")
    print("🚀 Starting FastAPI server on http://127.0.0.1:8000")
    print("📊 API endpoint: http://127.0.0.1:8000/generate_report")
    print("📖 API docs: http://127.0.0.1:8000/docs")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        # Change to backend directory and run the API
        os.chdir("backend")
        subprocess.run([sys.executable, "api_fastapi.py"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()