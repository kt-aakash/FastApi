from fastapi import FastAPI
from models import Product

app = FastAPI()


@app.get("/")
def greet():
    return("Welcome to the track..!")


products = [
    Product(id=1, name="mobile", description="budget mobile", price=23.5, quantity=3),
    Product(id=2, name="laptop", description="nvidia laptop", price=40, quantity=5),
    Product(id=3, name="pen", description="pen", price=2, quantity=10),
    Product(id=4, name="pencil", description="pencil", price=4, quantity=15)    
]

@app.get("/products")
def get_all_products():
    return products

@app.get("/products/{id}")
def get_product_by_id(id:int):
    for product in products:
        if product.id == id:
            return product