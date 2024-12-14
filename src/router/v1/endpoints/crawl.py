import requests
from bs4 import BeautifulSoup
from fastapi import APIRouter

from schema.crawl import CrawlRequest, CrawlResponse

router = APIRouter()


@router.post("/crawl", response_model=CrawlResponse)
async def crawl(request: CrawlRequest):
    response = requests.get(request.url)
    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text()

    return CrawlResponse(text=text)
