from fastapi import FastAPI

from routers.upload import router as upload_router
from routers.chat import router as chat_router
from routers.user import router as user_router

app = FastAPI(title="CoinWise API")


@app.get("/")
def read_root():
    return {"message": "CoinWise backend is running"}





app.include_router(upload_router, prefix="/api")
app.include_router(chat_router, prefix="/api")
app.include_router(user_router, prefix="/api")
