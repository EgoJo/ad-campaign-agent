"""
Entry point for running orchestrator as a module.
Allows: python -m app.orchestrator.llm_service
"""

if __name__ == "__main__":
    import uvicorn
    from .llm_service import app
    
    uvicorn.run(app, host="0.0.0.0", port=8000)

