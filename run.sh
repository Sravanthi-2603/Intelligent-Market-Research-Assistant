#!/bin/bash
echo "================================================"
echo " Intelligent Market Research Assistant"
echo " Powered by IBM Granite + IBM WatsonX"
echo "================================================"
echo ""

echo "[1/2] Installing dependencies..."
pip install -r requirements.txt -q

echo "[2/2] Starting server..."
python app.py
