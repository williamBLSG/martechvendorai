# martechvendorai
Procurement vendor selection management platform.

## Fetching Product Data

The `fetch_g2_products.py` script retrieves product information from the
configured API endpoint and stores it in a local SQLite database
(`g2_products.db`). Run the script with:

```bash
python fetch_g2_products.py
```

On success the database will contain a `products` table with one row per
product.
