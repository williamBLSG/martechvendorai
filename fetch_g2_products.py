import json
import sqlite3
from typing import Iterable
import urllib.request
from urllib.error import HTTPError, URLError

G2_PRODUCTS_URL = "https://example.com/products"
DB_PATH = "g2_products.db"


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


def _create_products_table(conn: sqlite3.Connection) -> None:
    """Create the products table if it does not already exist."""
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT,
            raw_json TEXT NOT NULL
        )
        """
    )


def save_products_to_db(products: Iterable[dict], db_path: str = DB_PATH) -> None:
    """Persist a collection of products to an SQLite database.

    Each product is stored with its ``id`` and ``name`` fields if present,
    along with the full JSON payload for extensibility.

    Args:
        products: Iterable of product dictionaries.
        db_path: Location of the SQLite database file.
    """

    conn = sqlite3.connect(db_path)
    try:
        _create_products_table(conn)
        with conn:
            for product in products:
                product_id = product.get("id")
                name = product.get("name")
                conn.execute(
                    "INSERT OR REPLACE INTO products (id, name, raw_json) VALUES (?, ?, ?)",
                    (product_id, name, json.dumps(product)),
                )
    finally:
        conn.close()


if __name__ == "__main__":
    try:
        data = fetch_g2_products()
        # Ensure we always work with an iterable of product dicts
        products = data if isinstance(data, list) else [data]
        save_products_to_db(products)
        print(f"Stored {len(products)} products in {DB_PATH}")
    except (HTTPError, URLError) as exc:
        print(f"Request failed: {exc}")
