from fastapi import FastAPI

from core.exception_handles import app_exception_handler, unexpected_exception_handler
from core.exceptions import AppException
from routers.auth_routes import auth_router
from routers.orders_routes import orders_router
from routers.products_routes import products_router

app = FastAPI()

app.add_exception_handler(AppException, app_exception_handler)

app.add_exception_handler(Exception, unexpected_exception_handler)


@app.get("/")
def get_rot():
    return {"message": "Pizzaria API"}

@app.get("/docker-test")
def docker_test():
    return {"message": "Docker reload funcionando"}


app.include_router(auth_router)
app.include_router(orders_router)
app.include_router(products_router)

# Para rodar o codigo, executar no terminal uvicorn main:app --reload
