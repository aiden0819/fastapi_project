from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from datetime import datetime
import uvicorn

app = FastAPI()

origins = ["http://127.0.0.1:5500", "http://54.167.60.34"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Entry(BaseModel):
    author: str
    content: str
    time: str

entries = []

@app.post("/entries/", response_model=Entry)
async def create_entry(entry: Entry):
    entries.append(entry)
    return entry

@app.get("/entries/", response_model=List[Entry])
async def read_entries():
    return entries

@app.delete("/entries/{entry_index}")
async def delete_entry(entry_index: int):
    if 0 <= entry_index < len(entries):
        return entries.pop(entry_index)
    else:
        raise HTTPException(status_code=404, detail="Entry not found")

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
