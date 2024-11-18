import logging
import yaml
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from main.api.models import RolesRequestData, CountryOnlyRequest, FullRequestData, CountryEnum, StateEnumUSA, StateEnumCanada
from main.services.qualified_service import QualifiedService
from main.services.data_processor import DataProcessor
from main.mongodb.MongoHelper import MongoDBClient
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables from .env file
load_dotenv()

# Access credentials from environment variables
USERNAME = os.getenv("API_USERNAME")
PASSWORD = os.getenv("API_PASSWORD")

# Load configuration from YAML file with error handling
try:
    with open("main/utilities/config.local.yaml", "r") as file:
        config = yaml.safe_load(file)
except FileNotFoundError:
    raise FileNotFoundError("The configuration file 'config.local.yaml' was not found.")
except yaml.YAMLError as e:
    raise RuntimeError(f"Error parsing the YAML configuration file: {e}")

# Initialize the MongoDB client using the URI and other configuration details
mongo_client = MongoDBClient(
    uri=os.getenv("MONGO_URI"),
    database_name=config["mongo"]["database_name"],
    collection_name=config["mongo"]["collection_qualified"],
    test_mode=config["mongo"]["test_mode"]
)

# Instantiate the service and processor classes
qualified_service = QualifiedService(mongo_client)
data_processor = DataProcessor(qualified_service)

# Initialize the FastAPI app
app = FastAPI()

# Add CORS middleware for open access during testing (to be restricted later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Open to all origins during testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Basic Authentication setup
security = HTTPBasic()

def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != USERNAME or credentials.password != PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials

# Define your API endpoints using the security dependency to ensure they are protected
@app.get("/")
def read_root():
    return {"message": "Welcome to the Tech Mastery API"}

# API Type 1: Takes a JSON object and returns tools, skills, libraries, and languages
@app.post("/details/operations")
def get_operations(request_data: FullRequestData, credentials: HTTPBasicCredentials = Depends(authenticate_user)):
    if request_data.country == CountryEnum.usa and request_data.state not in StateEnumUSA.__members__.values():
        return {"error": "Invalid state for USA"}
    elif request_data.country == CountryEnum.canada and request_data.state not in StateEnumCanada.__members__.values():
        return {"error": "Invalid province for Canada"}

    processed_data = data_processor.process_bigram_data(
        country=request_data.country.value,
        state=request_data.state,
        role=request_data.role
    )
    return processed_data

# API Type 1: Takes a JSON object and returns education data
@app.post("/details/education")
def get_education(request_data: FullRequestData, credentials: HTTPBasicCredentials = Depends(authenticate_user)):
    if request_data.country == CountryEnum.usa and request_data.state not in StateEnumUSA.__members__.values():
        return {"error": "Invalid state for USA"}
    elif request_data.country == CountryEnum.canada and request_data.state not in StateEnumCanada.__members__.values():
        return {"error": "Invalid province for Canada"}

    education_data = data_processor.process_education_data(
        country=request_data.country.value,
        state=request_data.state,
        role=request_data.role
    )
    return {"education": education_data}

# API Type 1: Takes a JSON object and returns workplace data
@app.post("/details/workplace")
def get_workplace(request_data: FullRequestData, credentials: HTTPBasicCredentials = Depends(authenticate_user)):
    if request_data.country == CountryEnum.usa and request_data.state not in StateEnumUSA.__members__.values():
        return {"error": "Invalid state for USA"}
    elif request_data.country == CountryEnum.canada and request_data.state not in StateEnumCanada.__members__.values():
        return {"error": "Invalid province for Canada"}

    workplace_data = data_processor.process_place_of_work_data(
        country=request_data.country.value,
        state=request_data.state,
        role=request_data.role
    )
    return {"workplace": workplace_data}

# API Type 2: Takes a JSON object and returns country-specific details
@app.post("/details/country")
def get_country_details(request_data: CountryOnlyRequest, credentials: HTTPBasicCredentials = Depends(authenticate_user)):
    if request_data.country == CountryEnum.canada:
        return {"states": data_processor.process_state_frequency_data(request_data.country.value)}
    elif request_data.country == CountryEnum.usa:
        return {"states": data_processor.process_state_frequency_data(request_data.country.value)}
    else:
        return {"error": "Country not found or data unavailable"}

# API Type 3: Takes a JSON object and returns roles
@app.post("/details/roles")
def get_role_details(request_data: CountryOnlyRequest, credentials: HTTPBasicCredentials = Depends(authenticate_user)):

    roles_data = data_processor.fetch_distinct_roles(
        country=request_data.country.value
    )
    return {"roles": roles_data}
