from typing import Annotated

from fastapi import FastAPI, Depends
# from fastapi.security import OAuth2PasswordBearer


app = FastAPI()

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get('/hi')
async def get_usr(name:str):
    return {"message": "Hello the one :" + name}

@app.get("/items/{item_id}")
async def read_item(item_id: int, query_name: str | None = None):
    return {"item_id": item_id, "query_name": query_name}

# @app.get("/testToken/")
# async def read_tokens(token: Annotated[str, Depends(oauth2_scheme)]):
#     return {"token": token}