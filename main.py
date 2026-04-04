from fastapi import Depends, FastAPI
from models import Product
from sqlalchemy.orm import Session




#initializing fastapi object
app = FastAPI()

#allowing CORS from the specified url
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware, 
    allow_origins= ["http://localhost:3000"],
    allow_methods=["*"] 
)
#create database tables
from database import session, engine
import database_models
database_models.Base.metadata.create_all(bind=engine)


#creating pydantic model product list
products = [
    Product(id=1, name="mobile", description="budget mobile", price=23.5, quantity=3),
    Product(id=2, name="laptop", description="nvidia laptop", price=40, quantity=5),
    Product(id=3, name="pen", description="pen", price=2, quantity=10),
    Product(id=4, name="pencil", description="pencil", price=4, quantity=15)   
]

#db initializing function which creates dummy data if the table is empty by converting the pydantic models into database ORM models
def init_db():
    db = session()
    count = db.query(database_models.Product).count

    if count ==0:
        for product in products:
            #converting pydantic models into database ORM models
            db.add(database_models.Product(**product.model_dump()))
        db.commit()    

init_db()        


#creating a dependency function to access db session securely 
def get_db():
    db = session()
    try:
        yield db
    finally: 
        db.close()    
    



#creating api paths and corresponding functions
@app.get("/")
def greet():
    return("Welcome to the track..!")




@app.get("/products")
def get_all_products(db:Session = Depends(get_db)): #passing arguments requsting dbsession with required dependency
    """
        db: Session = Depends(get_db) (The Correct Way) 
        When you use Depends(), you are telling FastAPI: "Don't use the function get_db as a value. 
        Instead, execute it, wait for the yield, and give me the resulting database session." 
    """
    db_products = db.query(database_models.Product).all()
    #db = session()
    # query

    return db_products

@app.get("/products/{id}")
def get_product_by_id(id:int, db:Session=Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id== id).first()
    #for product in products:
    if db_product:
        return db_product
        

@app.post("/products")
def add_product(product: Product, db:Session=Depends(get_db)):
    
    #products.append(product)
    #adding a product into db
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return product


@app.put("/products/{id}")
def update_product(id:int, product:Product, db:Session=Depends(get_db)):
    # for i in range(0, len(products)-1):
    #     if products[i].id == id:
    #         products[i] = product
    #         return "Product added successfully..!"

    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity = product.quantity
        db.commit()
        return "Product updated..!"
    else:
        return "Product not found..!"



@app.delete("/products/{id}")
def delete_product(id:int, db:Session=Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    #for product in products:
    if db_product:
        db.delete(db_product)
        db.commit()
        return "Product deleted!"
    else:
        return "Product not found...!"

