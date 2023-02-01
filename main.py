import json
from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI, Path, Query, Body, Response, HTTPException
from fastapi.responses import JSONResponse
app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str] = None


class ErrorMessage(BaseModel):
    error: str


inventory = {}


@app.get('/')
def home():
    return {"Data": "Test"}


@app.get('/about')
def about():
    return {"Data": "About"}


@app.get('/item/{item_id}')
def get_item(item_id: int = Path(default=None, description='The id of the item', le=max(inventory.keys()) if inventory else 1, ge=1)):
    return {
        'data': inventory.get(item_id).__dict__
    }


@app.get('/name')
def get_item(name: str = Query(None, description='Query param for the name of the item')):
    return {
        'data': next((x.__dict__ for _, x in inventory.items() if x.name == name), "Not Found")
    }


@app.post('/item/{item_id}', responses={400: {'model': ErrorMessage}, 201: {'model': Item}})
async def create_item(item_id: int, item: Item):
    """_summary_

    Args:
        item_id (int): _description_
        item (Item): _description_

    Returns:
        _type_: _description_
    """
    if item_id in inventory:
        return JSONResponse(status_code=400, content={'error': 'item_id already exists'})
        # raise HTTPException(status_code=400, detail='item_id already exists')

    inventory[item_id] = item

    return JSONResponse(status_code=201, content=item.__dict__)
    # return Response(status_code=201, content=json.dumps({'data': item.__dict__}))
