#!/bin/bash
echo "Starting SwarmForge..."
echo "Make sure Ollama is running (ollama serve)"
echo "Starting FastAPI backend..."
cd backend
uvicorn main:app --reload --port 8000 &
echo "Starting Streamlit dashboard..."
cd ../frontend
streamlit run app.py &
echo "All services started."
wait