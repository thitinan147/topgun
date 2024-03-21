from fastapi import APIRouter 
#fastapi_mqtt
from fastapi_mqtt.fastmqtt import FastMQTT
from fastapi_mqtt.config import MQTTConfig
from fastapi.encoders import jsonable_encoder
import json

mqtt_config = MQTTConfig(host = "192.168.1.2",
    port= 1883,
    keepalive = 60,
    username="TGR_GROUP51",
    password="RL533I")

fast_mqtt = FastMQTT(config=mqtt_config)

router = APIRouter()

fast_mqtt.init_app(router)

from server.database import (
    add_water,
    add_water_mqtt
)
from server.models.water import (
    ErrorResponseModel,
    ResponseModel,
    WaterSchema,
)

@fast_mqtt.on_connect()
def connect(client, flags, rc, properties):
    fast_mqtt.client.subscribe("/mqtt") #subscribing mqtt topic
    print("Connected: ", client, flags, rc, properties)

@fast_mqtt.on_message()
async def message(client, topic, payload, qos, properties):
    print("Received message: ",topic, payload.decode(), qos, properties)

@fast_mqtt.subscribe("")
async def message_to_topic(client, topic, payload, qos, properties):
    print("HaHaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    print("Received message to specific topic: ", topic, payload.decode(), qos, properties)
    
    print("payload type", type(payload));
    decoded = payload.decode();
    print("decode payload is " + decoded);
    print("type = ", type(decoded));
    water = json.loads(decoded)
    print("the water is ", water)
    print("type of water",type(water))
    
    
    
    new_water = await add_water_mqtt(water);
    print("ruyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy")
    # print(new_water)
    #รับจาก board
    
    
# @fast_mqtt.subscribe("my/mqtt/topic/#", qos=2)
# async def message_to_topic_qos(client, topic, payload, qos, properties):
#     print("Received message to specific topic with qos=2: ", topic, payload.decode(), qos, properties)

@fast_mqtt.on_disconnect()
def disconnect(client, packet, exc=None):
    print("Disconnected")

@fast_mqtt.on_subscribe()
def subscribe(client, mid, qos, properties):
    print("subscribed", client, mid, qos, properties)


@router.get("/", response_description="test publish to mqtt")
async def publish_hello():
    fast_mqtt.publish("/mqtt", "Hello from Fastapi") #publishing mqtt topic
    return {"result": True,"message":"Published" }


