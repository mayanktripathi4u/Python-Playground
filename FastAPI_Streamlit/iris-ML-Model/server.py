from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
from sklearn.datasets import load_iris

model = joblib.load('model/iris.pkl')

iris_data = load_iris()
target_names = iris_data.target_names

app = FastAPI()

class IrisInput(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

# Defining Endpoint
@app.post('/predict')
def predict(iris: IrisInput): 
    data = np.array([[iris.sepal_length, iris.sepal_width, iris.petal_length, iris.petal_width]])
    prediction = model.predict(data)[0]
    class_names = target_names[prediction]
    return {'prediction': class_names}