import time
import os
import subprocess
import webbrowser
import http.server
import socketserver
import threading
import signal
import sys

# Configuration
PORT = 8000
DJANGO_SERVER_CMD = ["python", "manage.py", "runserver", f"0.0.0.0:{PORT}"]
DEMO_URL = f"http://localhost:{PORT}/frontend/templates/demo_audio.html"

def start_django_server():
    """Start the Django development server."""
    print(f"Starting Django server on port {PORT}...")
    process = subprocess.Popen(
        DJANGO_SERVER_CMD,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )
    
    # Wait for server to start
    time.sleep(2)
    return process

def open_browser():
    """Open the demo page in the default browser."""
    print(f"Opening {DEMO_URL} in browser...")
    webbrowser.open(DEMO_URL)

def cleanup(process):
    """Clean up resources."""
    if process:
        print("Stopping Django server...")
        process.terminate()
        process.wait()

def main():
    """Main function to run the test."""
    process = None
    
    try:
        # Start Django server
        process = start_django_server()
        
        # Open browser
        open_browser()
        
        # Keep the script running until user interrupts
        print("\nTest is running. Press Ctrl+C to stop.")
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nTest interrupted by user.")
    finally:
        cleanup(process)
        print("Test completed.")

if __name__ == "__main__":
    main()