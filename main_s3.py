from pathlib import Path
from fastapi import FastAPI, Request, Response, Header
# from fastapi.templating import Jinja2Templates
import httpx

# app = FastAPI()
# # templates = Jinja2Templates(directory="templates")
# CHUNK_SIZE = 1024 * 1024  # 1 MB
# video_url = "https://tinyurl.com/ycye8kxu"  # Replace with the actual video URL

# @app.get("/")
# async def read_root(request: Request):
#     return "mujiiii "
# @app.get("/video")
# async def video_endpoint(range: str = Header(None)):
#     async with httpx.AsyncClient(verify=False) as client:
#         headers = {'Range': range} if range else {}
#         response = await client.get(video_url, headers=headers)
        
#         content_range = response.headers.get('Content-Range')
#         content_length = response.headers.get('Content-Length')

#         # Ensure Content-Length is not None
#         if content_length is None:
#             content_length = str(len(response.content))

#         # Set Content-Range header if it is not present
#         if content_range is None:
#             content_range = f'bytes 0-{int(content_length) - 1}/{content_length}'

#         return Response(
#             content=response.content,
#             status_code=206,
#             headers={
#                 'Content-Range': content_range,
#                 'Accept-Ranges': 'bytes',
#                 'Content-Length': content_length
#             },
#             media_type="video/mp4"
#         )



app = FastAPI()
# video_url = "https://tinyurl.com/ycye8kxu"  # Replace with the actual video URL
video_url = "./test.mp4"  # Replace with the actual video URL

@app.get("/")
async def read_root(request: Request):
    return "ok "

@app.get("/video")
async def video_endpoint(range: str = Header(None)):
    async with httpx.AsyncClient(verify=False) as client:
        headers = {'Range': range} if range else {}
        response = await client.get(video_url, headers=headers)
        
        # Extract necessary headers from response
        content_range = response.headers.get('Content-Range')
        content_length = response.headers.get('Content-Length')

        # Handle missing content-length and content-range headers
        if content_length is None:
            content_length = str(len(response.content))
        if content_range is None:
            start = 0
            end = int(content_length) - 1
            content_range = f'bytes {start}-{end}/{content_length}'

        # Ensure Content-Length reflects the actual chunk size
        actual_content_length = str(len(response.content))

        return Response(
            content=response.content,
            status_code=206,
            headers={
                'Content-Range': content_range,
                'Accept-Ranges': 'bytes',
                'Content-Length': actual_content_length
            },
            media_type="video/mp4"
        )
