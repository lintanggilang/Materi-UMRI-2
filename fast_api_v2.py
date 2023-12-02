from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
from typing import List

app = FastAPI()

class TextInput(BaseModel):
    message: str

class Item(BaseModel):
    id: int
    message: str

CSV_FILE = 'data.csv'

def read_csv():
    try:
        df = pd.read_csv(CSV_FILE)
        return df.to_dict(orient='records')
    except FileNotFoundError:
        return []

def write_csv(data):
    df = pd.DataFrame(data)
    df.to_csv(CSV_FILE, index=False)

@app.get("/")
@app.get("/hai")
def hello_umri():
    return {"message": "halo umri"}

@app.post("/lower")
def lower(input_data: TextInput):
    processed_text = input_data.message.lower()
    return {"message": processed_text}

@app.get("/items", response_model=List[Item])
def read_items():
    items = read_csv()
    return items

@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int):
    items = read_csv()
    item = next((item for item in items if item['id'] == item_id), None)
    if item:
        return item
    else:
        raise HTTPException(status_code=404, detail="Item not found")

@app.post("/items", response_model=Item)
def create_item(item: Item):
    items = read_csv()
    new_item = {"id": item.id, "message": item.message}
    items.append(new_item)
    write_csv(items)
    return new_item

@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: Item):
    items = read_csv()
    index = next((index for index, i in enumerate(items) if i['id'] == item_id), None)
    if index is not None:
        items[index] = {"id": item.id, "message": item.message}
        write_csv(items)
        return items[index]
    else:
        raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/items/{item_id}", response_model=Item)
def delete_item(item_id: int):
    items = read_csv()
    index = next((index for index, item in enumerate(items) if item['id'] == item_id), None)
    if index is not None:
        deleted_item = items.pop(index)
        write_csv(items)
        return deleted_item
    else:
        raise HTTPException(status_code=404, detail="Item not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

# uvicorn fast_api_v2:app --reload