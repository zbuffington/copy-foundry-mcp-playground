from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
from speakers_data import speakers

app = FastAPI(title="Microsoft Research Speakers Search Engine")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

class Speaker(BaseModel):
    id: int
    name: str
    title: str
    expertise: List[str]
    bio: str
    publications: List[str]
    group: str

@app.get("/", response_class=FileResponse)
async def read_root():
    return "static/index.html"

@app.get("/speakers", response_model=List[Speaker])
def search_speakers(
    query: Optional[str] = Query(None, description="Search by name, expertise, or group"),
):
    if not query:
        return speakers
    
    query = query.lower()
    results = []
    
    for speaker in speakers:
        if (
            query in speaker["name"].lower()
            or query in speaker["group"].lower()
            or any(query in expertise.lower() for expertise in speaker["expertise"])
            or query in speaker["bio"].lower()
        ):
            results.append(speaker)
    
    return results

@app.get("/speakers/{speaker_id}", response_model=Speaker)
def get_speaker(speaker_id: int):
    for speaker in speakers:
        if speaker["id"] == speaker_id:
            return speaker
    return {"error": "Speaker not found"}
