from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from youtube_transcript_api import YouTubeTranscriptApi
import re

app = FastAPI()

class VideoUrl(BaseModel):
    url: str

def get_video_id(url: str) -> str:
    match = re.search(r'(?:v=|youtu\.be\/)([\w-]+)', url)
    if match:
        return match.group(1)
    raise ValueError("Invalid YouTube URL")

@app.post("/get_transcript/")
async def get_transcript(video: VideoUrl):
    try:
        video_id = get_video_id(video.url)
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        # Return data as JSON
        return {"transcript": [line['text'] for line in transcript]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
