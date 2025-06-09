#!/bin/bash
# Simple start script for FastAPI app

# Install Python dependencies
pip install -r requirements.txt

# Run the FastAPI app with uvicorn and reload enabled
uvicorn main:app --reload
