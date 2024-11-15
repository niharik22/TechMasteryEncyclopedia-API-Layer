from fastapi import FastAPI
from main.api.models import RequestData, CountryEnum, StateEnumUSA, StateEnumCanada  # Import models and enums
from main.data.mock_data import (  # Import mock data from mock_data.py
    mockLangData,
    mockToolsData,
    mockLibrariesData,
    mockSkillsData,
    mockWorkPlaceData,
    mockEducationData,
    mockCanadaData,
    mockUSAData
)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Tech Mastery API"}

# API Type 1: Takes a JSON object and returns tools, skills, libraries, languages, education, workplace
@app.post("/details")
def get_details(request_data: RequestData):
    # Validate state based on the country
    if request_data.country == CountryEnum.usa and request_data.state not in StateEnumUSA.__members__.values():
        return {"error": "Invalid state for USA"}
    elif request_data.country == CountryEnum.canada and request_data.state not in StateEnumCanada.__members__.values():
        return {"error": "Invalid province for Canada"}

    return {
        "tools": mockToolsData,
        "skills": mockSkillsData,
        "libraries": mockLibrariesData,
        "languages": mockLangData,
        "education": mockEducationData,
        "workplace": mockWorkPlaceData
    }

# API Type 2: Takes a JSON object and returns country-specific details
@app.post("/country-details")
def get_country_details(request_data: RequestData):
    if request_data.country == CountryEnum.canada:
        return {"states": mockCanadaData}
    elif request_data.country == CountryEnum.usa:
        return {"states": mockUSAData}
    else:
        return {"error": "Country not found or data unavailable"}
