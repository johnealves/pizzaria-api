from fastapi import FastAPI

from routers.auth_routes import auth_router
from routers.orders_routes import orders_router
from routers.products_routes import products_router

app = FastAPI()

@app.get("/")
def get_rot():
    return {"message": "Pizzaria API"}

app.include_router(auth_router)
app.include_router(orders_router)
app.include_router(products_router)

# Para rodar o codigo, executar no terminal uvicorn main:app --reload
