# Handle crawl data from URL
from bs4 import BeautifulSoup
from fastapi import HTTPException
import httpx


async def crawl_data(url: str) -> dict:
    try:
        # Convert HttpUrl to string
        url_str = str(url)
        print(f"URL: {url_str}")

        # Send request to get HTML content from URL
        async with httpx.AsyncClient() as client:
            response = await client.get(url_str)
            response.raise_for_status()  # Check for HTTP error

        # Parse HTML content
        soup = BeautifulSoup(response.text, "lxml")

        # Extract the title of the page
        title = soup.title.string if soup.title else "No title"

        # Extract text content from the body tag
        body_text = (
            soup.body.get_text(separator="\n", strip=True)
            if soup.body
            else "No body content"
        )

        # Combine URL, title, and content into a single string
        combined_result = f"URL: {url_str}\nTitle: {title}\nContent: {body_text}"

        return combined_result

    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
