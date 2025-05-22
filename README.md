# Video to Audio Backend API

This FastAPI service allows users to upload a video and receive an MP3 audio version.

## Endpoints

- `GET /` — health check
- `POST /api/convert` — accepts a video file and returns an audio file

## Usage (via frontend)

Point your frontend's fetch/axios POST request to `/api/convert` on the deployed backend.

## Deploy to Render

1. Create a new Web Service on [Render](https://render.com/)
2. Use your forked repo URL
3. Select `Python`, and use this `render.yaml` config