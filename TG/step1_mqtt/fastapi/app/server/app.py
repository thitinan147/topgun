from fastapi import FastAPI
from server.mqtt.sensor_data import router as MqttRouter

app = FastAPI()

####router api part

app.include_router(MqttRouter, tags=["MQTT"],prefix="/mqtt")

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "My REST API server!"}