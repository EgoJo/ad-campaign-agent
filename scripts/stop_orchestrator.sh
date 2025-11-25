#!/bin/bash
# Script to stop the orchestrator agent

echo "Stopping Orchestrator Agent..."

if [ -f "logs/orchestrator.pid" ]; then
    pid=$(cat logs/orchestrator.pid)
    if ps -p $pid > /dev/null 2>&1; then
        echo "Stopping orchestrator process $pid..."
        kill $pid
        sleep 2
        
        # Force kill if still running
        if ps -p $pid > /dev/null 2>&1; then
            echo "Force killing process $pid..."
            kill -9 $pid
        fi
        
        echo "Orchestrator Agent stopped."
    else
        echo "Process $pid not found. Orchestrator may already be stopped."
    fi
    
    rm logs/orchestrator.pid
else
    echo "No PID file found. Attempting to kill by port..."
    
    # Try to kill by port
    pid=$(lsof -ti:8000)
    if [ ! -z "$pid" ]; then
        echo "Killing process on port 8000 (PID: $pid)"
        kill $pid
        sleep 2
        
        if ps -p $pid > /dev/null 2>&1; then
            kill -9 $pid
        fi
        echo "Orchestrator Agent stopped."
    else
        echo "No process found on port 8000. Orchestrator may already be stopped."
    fi
fi

echo "Done."

