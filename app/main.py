from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.post("/callback")
async def callback(code: str):
    resp_str = f"[POST] You sent {code}"
    return {"Response": resp_str}

@app.get("/callback")
async def callback(code: str):
    resp_str = f"[GET] You sent {code}"
    return {"Response": resp_str}
