from typing import Optional
from pydantic import BaseModel, Field


    
class WaterSchema_ml(BaseModel):
    name: str = Field(...)
    day: int = Field(..., gt=0, lt=365)
    discharge: float = Field(..., ge=0.0)
    height: float = Field(..., ge=0.0)
    
    
    class Config:
        schema_extra = {
            "example": {
               
                "name": "M7",
                "day": 1,
                "discharge": 1.1,
                "height": 1.1,
                
            }
        }


class UpdateWaterModel_ml(BaseModel):
    # name: Optional[str]
    # year: Optional[int]
    # date: Optional[int]
    # month: Optional[int]
    # waterfront: Optional[float]
    # waterback: Optional[float]
    # waterdrain: Optional[float]
    
    name : Optional[str]
    day : Optional[int]
    discharge : Optional[float]
    height : Optional[float]
    

    class Config:
        schema_extra = {
            "example": {
                # "name": "M7",
                # "year": 2020,
                # "month":12,
                # "date":13,
                # "waterfront":121.1,
                # "waterback":111.3,
                # "waterdrain":102.4,
                
                "name" : "M7",
                "day" : 1,
                "discharge" : 1.1,
                "height" : 1.1,
                
            }
        }


def ResponseModel_ml(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel_ml(error, code, message):
    return {"error": error, "code": code, "message": message}