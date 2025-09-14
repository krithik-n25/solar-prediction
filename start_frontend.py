#!/usr/bin/env python3
"""
Quick startup script for the Solar Prediction System frontend
"""
import os
import sys
import subprocess
import webbrowser
import time
from threading import Timer

def open_browser():
    """Open the browser after a short delay"""
    time.sleep(2)
    webbrowser.open('http://127.0.0.1:8080')

def main():
    print("🌞 Starting Solar Prediction System Frontend...")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("frontend/index.html"):
        print("❌ Error: Please run this script from the project root directory")
        sys.exit(1)
    
    # Check if required files exist
    required_files = [
        "frontend/index.html",
        "frontend/results.html",
        "frontend/style.css"
    ]
    
    for file_path in required_files:
        if not os.path.exists(file_path):
            print(f"❌ Error: Required file missing: {file_path}")
            sys.exit(1)
    
    print("✅ All required files found")
    print("🌐 Starting HTTP server on http://127.0.0.1:8080")
    print("🏠 Home page: http://127.0.0.1:8080/index.html")
    print("📊 Results page: http://127.0.0.1:8080/results.html")
    print("\n🔗 Opening browser in 2 seconds...")
    print("Press Ctrl+C to stop the server")
    print("=" * 50)
    
    # Open browser after delay
    Timer(2.0, open_browser).start()
    
    try:
        # Change to frontend directory and start HTTP server
        os.chdir("frontend")
        subprocess.run([sys.executable, "-m", "http.server", "8080"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()