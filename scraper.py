from bs4 import BeautifulSoup
import requests


# Standard headers to fetch a website
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}


def fetch_website_contents(url):
    """
    Return the title and contents of the website at the given url;
    truncate to 2,000 characters as a sensible limit
    """
    # Safety check: Ensure url is a valid string and starts with http:// or https://
    if not isinstance(url, str) or not (url.startswith("http://") or url.startswith("https://")):
        return "Invalid or unsupported URL"

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        title = soup.title.string if soup.title else "No title found"
        if soup.body:
            for irrelevant in soup.body(["script", "style", "img", "input"]):
                irrelevant.decompose()
            text = soup.body.get_text(separator="\n", strip=True)
        else:
            text = ""
        return (title + "\n\n" + text)[:2_000]
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        return ""


def fetch_website_links(url):
    """
    Return the links on the website at the given url
    I realize this is inefficient as we're parsing twice! This is to keep the code in the lab simple.
    Feel free to use a class and optimize it!
    """
    # Safety check: Ensure url is a valid string and starts with http:// or https://
    if not isinstance(url, str) or not (url.startswith("http://") or url.startswith("https://")):
        return []

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        links = [link.get("href") for link in soup.find_all("a")]
        
        # Filter out None and return only valid http/https URLs
        return [
            link for link in links 
            if isinstance(link, str) and (link.startswith("http://") or link.startswith("https://"))
        ]
    except Exception as e:
        print(f"Failed to fetch links from {url}: {e}")
        return []