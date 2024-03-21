import requests
import json
from fastapi import APIRouter 

from server.models.water import (
    ErrorResponseModel,
    ResponseModel,
)
from server.models.water_ml import (
    ErrorResponseModel_ml,
    ResponseModel_ml,
    
)

router = APIRouter()

@router.get("/{id}", response_description="water data retrieved")
async def get_mockup_data(id):
    # url = 'http://192.168.10.159/v1/'+str(id)
    url = 'https://192.168.1.3:7078/'
    # url = 'https://jsonplaceholder.typicode.com/albums'#/'+str(id)
    mockup = requests.get(url)
    if mockup:
        print(json.loads(mockup.text))
        return ResponseModel(str(mockup.text), "API data id:" +str(id) +" retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "data doesn't exist.")

#ml
@router.get("/ml/{id}", response_description="water data retrieved")
async def get_mockup_data_ml(id):
    # url = 'http://
    url = 'https://192.168.1.3:7078/'
    moncup = requests.get(url)
    if moncup:
        print(json.loads(moncup.text))
        return ResponseModel_ml(str(moncup.text), "API data id:" +str(id) +" retrieved successfully")
    return ErrorResponseModel_ml("An error occurred.", 404, "data doesn't exist.")