from main import redis, Product
import time


key = "order_completed"
group = "inventory-group"

try:
    redis.xgroup_create(key, group)
except:
    print("Group already exists!")

while True:
    try:
        # '>' - we wante to get all events
        results = redis.xreadgroup(group, key, {key: '>'})
        # print(results)
        # [['order_completed', [('1648897370410-0', {'pk': '01FZMZ250EHB1C6NNA5FFH588B', 'product_id': '01FZMTHYBCVJTDA7X1QVKP5C8Q', 'price': '500.0', 'fee': '100.0', 'total': '600.0', 'quantity': '2', 'status': 'completed'})]]]
        if results != []:
            for result in results:
                obj = result[1][0][1]
                product = Product.get(obj["product_id"])
                print(product)
                product.quantity = product.quantity - int(obj["quantity"])
                product.save()
    except Exception as e:
        print(str(e))
    time.sleep(1)