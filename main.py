from fastapi import FastAPI
from models import Product

app = FastAPI()


@app.get("/")
def greet():
    return("Welcome to the track..!")


products = [
    Product(1, "mobile", "budget mobile", 23.5, 3),
    Product(2, "laptop", "nvidia laptop", 40, 5),    
]

@app.get("/products")
def get_all_products():
    return 