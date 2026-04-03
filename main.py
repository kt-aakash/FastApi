from fastapi import FastAPI
from models import Product

app = FastAPI()


@app.get("/")
def greet():
    return("Welcome to the track..!")

products = [
    Product(1, "phone", "budget phone", 99, 10),
    Product(1, "laptop", "nvidia laptop", 199, 1)
]


@app.get("/products")
def get_all_products():
    return(products)