from pathlib import Path
from fastapi import FastAPI
from fastapi import Request, Response
from fastapi import Header
import requests


app = FastAPI()

CHUNK_SIZE = 1024*1024
VIDEO_URL = "https://download-video.akamaized.net/v3-1/playback/da067e3f-d7dd-4de3-aae2-7ac6f91c2c82/39c8ecb9-a657cb7b?__token__=st=1724328959~exp=1724343359~acl=%2Fv3-1%2Fplayback%2Fda067e3f-d7dd-4de3-aae2-7ac6f91c2c82%2F39c8ecb9-a657cb7b%2A~hmac=8a44c01413b3a7a0ac7263513e7652d0b20b409a717e657b41c8f5ee39ccf328&r=dXMtd2VzdDE%3D"

@app.get("/")
async def read_root(request: Request):
    return "maiin nextnn"

@app.get("/video")
async def video_endpoint(range: str = Header(None)):
    start, end = range.replace("bytes=", "").split("-")
    start = int(start)
    end = int(end) if end else start + CHUNK_SIZE
    with open(video_path, "rb") as video:
        video.seek(start)
        data = video.read(end - start)
        filesize = str(video_path.stat().st_size)
        headers = {
            'Content-Range': f'bytes {str(start)}-{str(end)}/{filesize}',
            'Accept-Ranges': 'bytes'
        }
        return Response(data, status_code=206, headers=headers, media_type="video/mp4")


@app.get("/video_online")
async def video_endpoint(range: str = Header(None)):
    headers = {}
    if range:
        headers['Range'] = range

    with requests.get(VIDEO_URL, headers=headers, stream=True) as r:
        start, end = range.replace("bytes=", "").split("-")
        start = int(start)
        end = int(end) if end else start + CHUNK_SIZE
        
        data = r.content
        filesize = r.headers.get('Content-Length', len(data))

        response_headers = {
            'Content-Range': f'bytes {start}-{end}/{filesize}',
            'Accept-Ranges': 'bytes',
            'Content-Length': str(len(data)),
        }

        return Response(data, status_code=206, headers=response_headers, media_type=r.headers.get('Content-Type', 'video/mp4'))