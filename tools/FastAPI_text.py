from fastapi import FastAPI, Query
from bs4 import BeautifulSoup
import requests

app = FastAPI()

def get_full_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # 假设详细内容在某个特定的类名下，根据实际情况进行调整
        content_div = soup.find(class_='some-content-class')
        if content_div:
            return content_div.get_text(strip=True)
        else:
            # 如果找不到，尝试其他选择器或者返回空字符串
            return ''
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return ''

def bing_search(keyword, num_results=5):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    params = {
        'q': keyword,
        'count': num_results
    }
    url = 'https://cn.bing.com/search'
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    results = []
    for item in soup.select('li.b_algo'):
        try:
            title = item.h2.get_text(strip=True)
            link = item.h2.a['href']
            snippet = item.p.get_text(strip=True) if item.p else ''
            full_content = get_full_content(link)
            results.append({'title': title, 'link': link, 'snippet': snippet, 'full_content': full_content})
        except (AttributeError, KeyError):
            continue

    return results

@app.get("/search/")
async def search(keyword: str):
    search_results = bing_search(keyword)
    return {'search_results': search_results}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# http://127.0.0.1:8000/search/?keyword=大连