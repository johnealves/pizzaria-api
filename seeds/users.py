from models import User

users: User = [
    {
        "name": "admin",
        "email": "admin@admin.com",
        "password": "1234",
        "active": True,
        "admin": True
    },
    {
        "name": "john",
        "email": "john@email.com",
        "password": "1234",
        "active": True,
        "admin": False
    },
]
