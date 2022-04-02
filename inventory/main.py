from xml.sax.handler import all_features
from fastapi import FastAPI
from redis_om import get_redis_connection, HashModel
from fastapi.middleware.cors import CORSMiddleware
# from helper import format

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],
    allow_methods=["*"],
    allow_headers=["*"]
)

redis = get_redis_connection(
    host="redis-15070.c212.ap-south-1-1.ec2.cloud.redislabs.com",
    port=15070,
    password="3Q3oyf6aombhVwdxOrijh1mIf0irbPsk",
    decode_responses=True
)




class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis


@app.get("/")
async def root():
    return {"message": "Hello World"}


def format(pk: str):
    product = Product.get(pk)
    return {
        "id": product.pk,
        "name": product.name,
        "price": product.price,
        "quantity": product.quantity
    }


# get all products
@app.get("/products")
async def all():
    return [format(pk) for pk in Product.all_pks()]


# get single product
@app.get("/products/{pk}")
async def all(pk: str):
    return Product.get(pk)



@app.post("/products")
async def create(product: Product):
    return product.save()

@app.delete("/products/{pk}")
async def create(pk: str):
    return Product.delete(pk)



