# from fastapi import FastAPI
# import uvicorn
# app = FastAPI()
#
# def add_numbers(a: int, b: int) -> int:
#     return a + b
#
# @app.get("/add/{a}/{b}")
# async def read_root(a: int, b: int):
#     result = add_numbers(a, b)
#     return {"result": result}
#
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)


import os
import base64
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from bs4 import BeautifulSoup
import requests

app = FastAPI()

def bing_image_search(query: str):
    url = 'https://www.bing.com/images/search'
    params = {'q': query}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, params=params, headers=headers)

    if response.status_code != 200:
        return {'error': 'Failed to retrieve images'}, None

    soup = BeautifulSoup(response.text, 'html.parser')
    img_tag = soup.find('img', class_='mimg')

    if img_tag is None:
        return {'error': 'No images found'}, None

    img_url = img_tag['src']
    if img_url.startswith('data:image/'):
        image_data = img_url.split(',')[1]
        return None, base64.b64decode(image_data)
    else:
        return None, img_url

@app.get("/search-images/")
async def search_images(query: str):
    error, image_data_or_url = bing_image_search(query)
    if error:
        return error
    if isinstance(image_data_or_url, bytes):
        return StreamingResponse(content=iter([image_data_or_url]), media_type='image/jpeg')
    else:
        # Directly return the image data from the URL
        image_response = requests.get(image_data_or_url, stream=True)
        return StreamingResponse(content=image_response.raw, media_type='image/jpeg')

@app.get("/search-images-url/")
async def search_images_url(query: str):
    error, image_data_or_url = bing_image_search(query)
    if error:
        return error
    if isinstance(image_data_or_url, str):
        return {'image_url': image_data_or_url}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


# http://127.0.0.1:8000/search-images/?query=大连
# http://127.0.0.1:8000/search-images-url/?query=大连