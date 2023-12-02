from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class TextInput(BaseModel):
    message: str

@app.get("/")
@app.get("/hai")
def hello_umri():
    return {"message": "halo umri"}

@app.post("/lower")
def lower(input_data: TextInput):
    processed_text = input_data.message.lower()
    
    return {"message": processed_text}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)


# uvicorn fast_api_v1:app --reload

