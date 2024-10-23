from fastapi import FastAPI
import uvicorn
from router import router
from subscribe import consumer_read

app = FastAPI(
    title="Binance parser"
)


@app.on_event("startup")
def start_binance_stream():
    consumer_read()


app.include_router(router, tags=['Crypto'], prefix='/api/crypto')


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
