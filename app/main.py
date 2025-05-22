from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import shutil
import tempfile
import os
import yt_dlp
from moviepy.editor import VideoFileClip

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return JSONResponse(content={"message": "Welcome to the Video to Audio API!"})

@app.post("/api/convert")
async def convert_video(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    try:
        # Save uploaded video
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
            shutil.copyfileobj(file.file, temp_video)
            temp_video_path = temp_video.name

        # Define output path
        temp_audio_path = temp_video_path.replace(".mp4", ".mp3")

        # Convert using moviepy
        video = VideoFileClip(temp_video_path)
        video.audio.write_audiofile(temp_audio_path)

        # Clean up video file after response
        background_tasks.add_task(lambda: os.remove(temp_video_path))
        background_tasks.add_task(lambda: os.remove(temp_audio_path))

        return FileResponse(temp_audio_path, media_type="audio/mpeg", filename="output.mp3")

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})