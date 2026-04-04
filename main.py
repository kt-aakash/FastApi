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

@app.get("/product")
def get_all_products():
    return products

@app.get("/product/{id}")
def get_product_by_id(id:int):
    for product in products:
        if product.id == id:
            return product
        

@app.post("/product")
def add_product(product: Product):
    products.append(product)
    return product


@app.put("/product")
def update_product(id:int, product:Product):
    for i in range(0, len(products)-1):
        if products[i].id == id:
            products[i] = product
            return "Product added successfully..!"
    return "Product not found..!"



@app.delete("/product")
def delete_product(id:int):
    for product in products:
        if product.id == id:
            products.remove(product)
            return "Product successfully deleted..!"
    return "Product not found...!"

