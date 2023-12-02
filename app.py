from fastapi import FastAPI
from pydantic import BaseModel, Field
import pandas as pd
import joblib
from typing import Optional
from feature import umur, new_feature
from mangum import Mangum


app = FastAPI()
handler =  Mangum(app)

class Item(BaseModel):
    Pclass: int = Field(example=3)
    Name: str = Field(example="Braund, Mr. Owen Harris")
    Sex: str = Field(example="male")
    Age: float = Field(example=22.0)
    SibSp: int = Field(example=1)
    Parch: int = Field(example=0)
    Ticket: str = Field(example="A/5 21171")
    Fare: float = Field(example=7.25)
    Cabin: Optional[str] = Field(example=None)
    Embarked: str = Field(example="S")


@app.post("/predict")
def predict(item: Item):
    print(item)
    data = pd.DataFrame([dict(item)])
    new_feature(data)
    data.drop(['Name', 'Cabin', 'Ticket'], axis=1, inplace=True)

    loaded_model = joblib.load('best_model.joblib')
    predictions = loaded_model.predict(data)

    return {"prediction": int(predictions[0])}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)


# reference
# https://www.youtube.com/watch?v=VYk3lwZbHBU&t=814s
