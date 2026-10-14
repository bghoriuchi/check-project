from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app=FastAPI(title="お試し", description="確認用です")

@app.get("/")
def hello():
    return {"message":"Hello World"}
