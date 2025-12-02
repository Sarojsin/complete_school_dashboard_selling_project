#!/usr/bin/env python3
"""
Application runner script
Provides options for running the application in different modes
"""
import http
import uvicorn
import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description='School Management System')
    parser.add_argument(
        '--host',
        type=str,
        default='localhost',
        help='Host to bind (default: localhost)'
    )
    parser.add_argument(
        '--port',
        type=int,
        default=8000,
        help='Port to bind (default: 8000)'
    )
    parser.add_argument(
        '--reload',
        action='store_true',
        help='Enable auto-reload for development'
    )
    parser.add_argument(
        '--workers',
        type=int,
        default=1,
        help='Number of worker processes (default: 1)'
    )
    parser.add_argument(
        '--log-level',
        type=str,
        default='info',
        choices=['critical', 'error', 'warning', 'info', 'debug'],
        help='Log level (default: info)'
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("School Management System")
    print("=" * 60)
    print(f"Starting server on http://{args.host}:{args.port}")
    print(f"Mode: {'Development' if args.reload else 'Production'}")
    print(f"Workers: {args.workers}")
    print(f"Log Level: {args.log_level}")
    print("=" * 60)
    print("\nPress CTRL+C to stop the server\n")
    
    try:
        uvicorn.run(
            "main:app",
            host=args.host,
            port=args.port,
            reload=args.reload,
            workers=args.workers if not args.reload else 1,  # reload doesn't work with multiple workers
            log_level=args.log_level,
            access_log=True
        )
    except KeyboardInterrupt:
        print("\n\nShutting down gracefully...")
        sys.exit(0)

if __name__ == "__main__":
    main()