from fastapi import FastAPI, Request


app = FastAPI()

callback_response: dict = {"message": "Lise"}

@app.post("/callback/")
async def callback(code: str):
    resp_str = f"You sent {code}"
    return {"Response": resp_str}
