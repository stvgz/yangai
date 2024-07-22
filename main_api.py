from api.api import app
from fastapi import FastAPI
from uvicorn import run
import os

if __name__ == "__main__":

    # Run the app using Uvicorn directly without the command line
    # run(app, host="127.0.0.1", 
    #     port=int(os.getenv('PORT', 8000)))

    run("api.api:app", host="127.0.0.1", 
    port=int(os.getenv('PORT', 8000)), 
    reload=True)