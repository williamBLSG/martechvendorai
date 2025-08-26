import json
import urllib.request
from urllib.error import HTTPError, URLError

G2_PRODUCTS_URL = "https://example.com/products"


def fetch_g2_products(url: str = G2_PRODUCTS_URL):
    """Fetch product data from G2.

    Args:
        url: Endpoint returning a JSON payload with product data.

    Returns:
        Parsed JSON response from the provided URL.
    """
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
    }
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=10) as response:
        return json.loads(response.read().decode("utf-8"))


if __name__ == "__main__":
    try:
        data = fetch_g2_products()
        print(data)
    except (HTTPError, URLError) as exc:
        print(f"Request failed: {exc}")
