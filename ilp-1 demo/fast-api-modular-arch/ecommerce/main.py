from fastapi import FastAPI
from app.routers import user, product, order

app = FastAPI(title="E-Commerce API")

app.include_router(user.router)
app.include_router(product.router)

@app.get("/")
def home():
    return {"message": "Welcome to the E-Commerce API"}