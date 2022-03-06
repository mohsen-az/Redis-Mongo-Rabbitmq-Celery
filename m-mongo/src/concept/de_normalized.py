"""
Store data in mongodb
    - De-Normalized(Embedded): Optimization
"""

user = {
    "id": 1,
    "username": "ali",
    "password": "passwd-123"
}

products = [
    {
        "id": 5,
        "name": "product#1",
        "price": 3
    },
    {
        "id": 7,
        "name": "product#2",
        "price": 5
    },
    {
        "id": 12,
        "name": "product#3",
        "price": 9
    }
]

invoice = {
    "id": 415,
    "total_price": 12,
    "currency": "USD",
    "user": {
        "username": "ali",
    },
    "items": [
        {
            "id": 5,
            "name": "product#1",
            "price": 3
        },
        {
            "id": 12,
            "name": "product#3",
            "price": 9
        }
    ]
}
