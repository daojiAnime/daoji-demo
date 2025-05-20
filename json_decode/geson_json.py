import json

from genson import SchemaBuilder
from rich import print

json_data1 = {
    "name": "Product A",
    "price": 19.99,
    "tags": ["electronics", "gadget"],
    "dimensions": {"width": 10, "height": 5},
    "in_stock": True,
}

json_data2 = {
    "name": "Product B",
    "price": 25,  #  Integer, genson will make it "number"
    "tags": ["home", "decor", None],  # Note None, genson will add "null" to type
    "description": "A nice product",  # New optional field
    "in_stock": False,
    "rating": 4.5,
}

json_data3 = [  # It can also handle lists of objects
    {"id": 1, "value": "alpha"},
    {"id": 2, "value": "beta", "active": True},
]

builder = SchemaBuilder()
# builder.add_object(json_data1)
# builder.add_object(json_data2)
builder.add_object(json_data3)  # You can also add lists/arrays of objects

# You can also add data from a string
# json_string = '{"item_id": "xyz123", "quantity": 10}'
# builder.add_schema(json.loads(json_string))  # add_schema can take a dict directly

generated_schema = builder.to_schema()

print(json.dumps(generated_schema, indent=2))
