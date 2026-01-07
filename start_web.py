#!/usr/bin/env python3
"""
Startup script for Malaysia Marketplace Scraper Web Interface.
Starts both FastAPI backend and React frontend servers.
"""

import subprocess
import sys
import time
from pathlib import Path

def start_backend():
    """Start FastAPI backend."""
    print("🚀 Starting FastAPI backend on http://localhost:8000...")
    return subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "api.app:app", "--reload", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

def start_frontend():
    """Start React frontend."""
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("❌ Frontend directory not found!")
        return None
    
    print("🚀 Starting React frontend on http://localhost:3000...")
    return subprocess.Popen(
        ["npm", "run", "dev"],
        cwd=frontend_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

if __name__ == "__main__":
    print("=" * 60)
    print("  MALAYSIA MARKETPLACE SCRAPER - WEB INTERFACE")
    print("=" * 60)
    print()
    
    backend_process = None
    frontend_process = None
    
    try:
        backend_process = start_backend()
        time.sleep(3)  # Wait for backend to start
        
        frontend_process = start_frontend()
        
        print()
        print("✅ Both servers are starting...")
        print("📊 Backend API: http://localhost:8000")
        print("🌐 Frontend: http://localhost:3000")
        print("📚 API Docs: http://localhost:8000/docs")
        print()
        print("Press Ctrl+C to stop both servers")
        print()
        
        # Wait for processes
        backend_process.wait()
        frontend_process.wait()
        
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping servers...")
        if backend_process:
            backend_process.terminate()
        if frontend_process:
            frontend_process.terminate()
        print("✅ Servers stopped")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        if backend_process:
            backend_process.terminate()
        if frontend_process:
            frontend_process.terminate()
        sys.exit(1)
