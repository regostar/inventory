# 2nd micro service for payment, separate server
# can be mongo db or mysql db
from fastapi import FastAPI
from redis_om import get_redis_connection, HashModel
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
import requests 

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

class Order(HashModel):
    product_id: str
    price: float
    fee: float
    total: float
    quantity: int
    status: str # pending, completed, refunded

    class Meta:
        database = redis
    
@app.post("/orders")
async def create(request: Request): # id, quantity
    body = await request.json()
    # one way of getting all data from request
    # there is a better way to handle async tasks
    req = requests.get("http://localhost:8000/products/%s" % body["id"])
    product = req.json()

    order = Order(
        product_id=body["id"],
        price=product["price"],
        fee=0.2*product["price"],
        total=1.2*product["price"],
        quantity=body["quantity"],
        status="pending"
    )
    order.save()

    order_completed(order)

    return order


def order_completed(order: Order):
    order.status = "completed"
    order.save()