import os
import sys
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

# Importing all models to ensure they are registered with SQLModel
from app.models import *

# Importing routers for different API endpoints
from app.routes.generate import router as generate_router

# Load environment variables from a .env file
load_dotenv()

# Get the environment setting, default to "dev" if not set
ENV = os.getenv("env", "dev")

# Configure Loguru for logging
log_out_path = sys.stdout  # Default to standard output
if ENV != "dev":
    log_out_path = "app.log"  # Log to a file in non-dev environments

logger.remove()  # Remove the default logger
# Add a new logger with the specified output and level
logger.add(log_out_path, colorize=True, level="INFO")

# Create a FastAPI application instance
app = FastAPI()

# Allow CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include the routers for different API endpoints
app.include_router(generate_router)

# Define a root endpoint for the API


@app.get("/")
async def read_root():
    return {"message": "Ya, Am running let's not go to work!"}
