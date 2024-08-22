from pathlib import Path
from fastapi import FastAPI
from fastapi import Request, Response
from fastapi import Header
#from fastapi.templating import Jinja2Templates


app = FastAPI()
#templates = Jinja2Templates(directory="templates")
CHUNK_SIZE = 1024*1024
video_path = Path("light_media/vr_headset.mp4")


@app.get("/")
async def read_root(request: Request):
    return "Hi"


@app.get("/video")
async def video_endpoint(range: str = Header(None)):
    print("range = ", range)
    
    start, end = range.replace("bytes=", "").split("-")
    print(f"start = {start}, end = {end}")
    start = int(start)
    end = int(end) if end else start + CHUNK_SIZE

    filesize = str(video_path.stat().st_size)
    if end > int(filesize):
        print("greater end")
        end = int(filesize)


    
    with open(video_path, "rb") as video:
        video.seek(start)
        data = video.read(end - start)
        filesize = str(video_path.stat().st_size)
        headers = {
            'Content-Range': f'bytes {str(start)}-{str(end)}/{filesize}',
            'Accept-Ranges': 'bytes'
        }
        return Response(data, status_code=206, headers=headers, media_type="video/mp4")