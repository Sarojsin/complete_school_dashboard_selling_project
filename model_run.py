#!/usr/bin/env python3
"""
model_run.py — One-command launcher for the School & College Management System.

Usage:
    python model_run.py              # Start backend (dev mode, auto-reload)
    python model_run.py --prod       # Start backend (production mode)
    python model_run.py --port 9000  # Custom port
    python model_run.py --host 0.0.0.0  # Expose to network
"""

import uvicorn
import sys
import os
import subprocess
import argparse
import webbrowser
import threading
import time


# ── Make sure imports resolve from project root ─────────────────────────────
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


def open_browser(url: str, delay: float = 2.0):
    """Open the browser after a short delay (so the server is ready)."""
    def _open():
        time.sleep(delay)
        webbrowser.open(url)
    threading.Thread(target=_open, daemon=True).start()


def start_frontend():
    """Start the React frontend dev server in a background process."""
    frontend_dir = os.path.join(PROJECT_ROOT, "frontend")
    if not os.path.isdir(frontend_dir):
        print("  [!] frontend/ folder not found — skipping frontend start.")
        return None

    print("  ► Starting React frontend (npm run dev)...")
    if sys.platform == "win32":
        proc = subprocess.Popen(
            ["npm.cmd", "run", "dev"],
            cwd=frontend_dir,
            creationflags=subprocess.CREATE_NEW_CONSOLE,
        )
    else:
        proc = subprocess.Popen(
            ["npm", "run", "dev"],
            cwd=frontend_dir,
        )
    return proc


def print_banner(host: str, port: int, dev: bool, with_frontend: bool):
    """Print a startup banner with useful URLs."""
    separator = "=" * 56
    print(f"\n  {separator}")
    print(f"  School & College Management System")
    print(f"  {separator}")
    print(f"  Mode       : {'Development (auto-reload ON)' if dev else 'Production'}")
    print(f"  Backend    : http://{host}:{port}")
    print(f"  API Docs   : http://{host}:{port}/docs")
    print(f"  ReDoc      : http://{host}:{port}/redoc")
    if with_frontend:
        print(f"  Frontend   : http://localhost:5173")
    print(f"  {separator}")
    print(f"  Press  Ctrl+C  to stop all servers\n")


def main():
    parser = argparse.ArgumentParser(
        description="Launch the School & College Management System"
    )
    parser.add_argument(
        "--host", default="localhost",
        help="Host to bind (default: localhost)"
    )
    parser.add_argument(
        "--port", type=int, default=8000,
        help="Port to bind (default: 8000)"
    )
    parser.add_argument(
        "--prod", action="store_true",
        help="Run in production mode (disables auto-reload)"
    )
    parser.add_argument(
        "--workers", type=int, default=1,
        help="Number of worker processes — ignored in dev mode (default: 1)"
    )
    parser.add_argument(
        "--no-browser", action="store_true",
        help="Do not auto-open the browser"
    )
    parser.add_argument(
        "--with-frontend", action="store_true",
        help="Also launch the React frontend (npm run dev) in a new window"
    )
    parser.add_argument(
        "--log-level", default="info",
        choices=["critical", "error", "warning", "info", "debug"],
        help="Uvicorn log level (default: info)"
    )

    args = parser.parse_args()
    dev_mode = not args.prod

    print_banner(args.host, args.port, dev_mode, args.with_frontend)

    # Optionally launch frontend
    frontend_proc = None
    if args.with_frontend:
        frontend_proc = start_frontend()

    # Optionally open browser
    if not args.no_browser:
        url = f"http://localhost:{args.port}/docs" if not args.with_frontend \
              else "http://localhost:5173"
        open_browser(url)

    # Start the FastAPI backend — imports directly from app/main.py
    try:
        uvicorn.run(
            "app.main:app",          # ← points directly to app/main.py
            host=args.host,
            port=args.port,
            reload=dev_mode,         # auto-reload in dev mode
            workers=1 if dev_mode else args.workers,
            log_level=args.log_level,
            access_log=True,
        )
    except KeyboardInterrupt:
        print("\n\n  [x] Server stopped.")
    finally:
        if frontend_proc:
            frontend_proc.terminate()
            print("  [x] Frontend stopped.")
        sys.exit(0)


if __name__ == "__main__":
    main()
