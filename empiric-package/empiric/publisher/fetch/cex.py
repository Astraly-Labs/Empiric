import logging

import requests
from empiric.core.entry import construct_entry
from empiric.core.utils import currency_pair_to_key

logger = logging.getLogger(__name__)


def fetch_cex(assets, publisher):
    source = "cex"
    base_url = "https://cex.io/api/ticker"

    entries = []

    for asset in assets:
        if asset["type"] != "SPOT":
            logger.info(f"Skipping CEX for non-spot asset {asset}")
            continue

        pair = asset["pair"]
        response = requests.get(f"{base_url}/{pair[0]}/{pair[1]}", timeout=10)
        result = response.json()

        if "error" in result and result["error"] == "Invalid Symbols Pair":
            logger.warn(f"No data found for {'/'.join(pair)} from CEX")
            continue

        timestamp = int(result["timestamp"])
        price = float(result["last"])
        price_int = int(price * (10 ** asset["decimals"]))
        key = currency_pair_to_key(*pair)

        logger.info(f"Fetched price {price} for {'/'.join(pair)} from CEX")

        entries.append(
            construct_entry(
                key=key,
                value=price_int,
                timestamp=timestamp,
                source=source,
                publisher=publisher,
            )
        )

    return entries
