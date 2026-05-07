#!/bin/bash
echo "========================================"
echo "DATABASE INITIALIZATION"
echo "========================================"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 not found! Please install Python 3.8+"
    exit 1
fi

# Check if psycopg2 is installed
python3 -c "import psycopg2" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "[INFO] Installing required packages..."
    pip3 install psycopg2-binary python-dotenv
fi

# Run the initialization script
echo "[INFO] Starting database initialization..."
python3 init_database.py

if [ $? -ne 0 ]; then
    echo ""
    echo "[ERROR] Database initialization failed!"
    exit 1
fi

echo ""
echo "[SUCCESS] Database tables created successfully!"
echo ""
