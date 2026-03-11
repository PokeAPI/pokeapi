import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
from pathlib import Path

# 1. Object Map for Item IDs (from PokeAPI's items.csv)
ITEM_MAP = {
    "master-ball": 1,
    "ultra-ball": 2,
    "great-ball": 3,
    "poke-ball": 4,
    "safari-ball": 5,
    "net-ball": 6,
    "dive-ball": 7,
    "nest-ball": 8,
    "repeat-ball": 9,
    "timer-ball": 10,
    "luxury-ball": 11,
    "premier-ball": 12,
    "dusk-ball": 13,
    "heal-ball": 14,
    "quick-ball": 15,
    "cherish-ball": 16,
    "smoke-ball": 205,
    "light-ball": 213,
    "iron-ball": 255,
    "lure-ball": 449,
    "level-ball": 450,
    "moon-ball": 451,
    "heavy-ball": 452,
    "fast-ball": 453,
    "friend-ball": 454,
    "love-ball": 455,
    "park-ball": 456,
    "sport-ball": 457,
    "air-balloon": 584,
    "dream-ball": 617,
    "beast-ball": 887,
    "left-poke-ball": 994,
    "polished-mud-ball": 1031,
    "strange-ball": 1663,
    "koraidons-poke-ball": 1667,
    "miraidons-poke-ball": 1668,
    "academy-ball": 2031,
    "marill-ball": 2033,
    "yarn-ball": 2034,
    "cyber-ball": 2035,
    "blue-poke-ball-pick": 2044,
    "exercise-ball": 2064,
    "green-poke-ball-pick": 2084,
    "red-poke-ball-pick": 2085,
    "lastrange-ball": 2219,
    "lapoke-ball": 2220,
    "lagreat-ball": 2221,
    "laultra-ball": 2222,
    "laheavy-ball": 2223,
    "laleaden-ball": 2224,
    "lagigaton-ball": 2225,
    "lafeather-ball": 2226,
    "lawing-ball": 2227,
    "lajet-ball": 2228,
    "laorigin-ball": 2229,
}

# 2. Version Group Mapping (from PokeAPI's version_groups.csv)
GAME_MAP = {
    "RGBY": [1, 2, 28, 29],
    "RBY": [1, 2],
    "GSC": [3, 4],
    "RSE": [5, 6],
    "FRLG": [7],
    "DPPt": [8, 9],
    "HGSS": [10],
    "BWB2W2": [11, 14],
    "XY": [15],
    "ORAS": [16],
    "SM": [17],
    "USUM": [18],
    "PE": [19],
    "SwSh": [20],
    "BDSP": [23],
    "LA": [24],
    "SV": [25],
    "ZA": [30],
    "ColoXD": [12, 13],
}

BASE_URL = "https://bulbapedia.bulbagarden.net"
START_URL = f"{BASE_URL}/wiki/Pok%C3%A9_Ball"


def normalize_name(name):
    """Maps Bulbapedia names to our dictionary keys."""
    raw = name.lower().strip()
    # Handle Hisui variants: 'Heavy Ball (Hisui)' -> 'laheavy-ball'
    if "(hisui)" in raw:
        clean = re.sub(r"[^a-z0-9\s]", "", raw.replace("(hisui)", ""))
        return "la" + clean.strip().replace(" ", "-")
    # Standard: 'Ultra Ball' -> 'ultra-ball'
    clean = re.sub(r"[^a-z0-9\s-]", "", raw)
    return clean.replace(" ", "-")


def get_poke_ball_links():
    print("Fetching Poké Ball list...")
    res = requests.get(START_URL)
    soup = BeautifulSoup(res.text, "html.parser")
    balls = []

    header = soup.find("span", id="Types_of_Pok.C3.A9_Balls")
    table = header.find_next("table")
    for row in table.find_all("tr")[1:]:
        cols = row.find_all("td")
        if len(cols) > 1:
            a = cols[1].find("a")
            if a:
                name = a.text.strip()
                identifier = normalize_name(name)
                item_id = ITEM_MAP.get(identifier)
                if item_id:
                    balls.append(
                        {"name": name, "item_id": item_id, "url": BASE_URL + a["href"]}
                    )
    return balls


def get_ball_prices(ball_url):
    res = requests.get(ball_url)
    soup = BeautifulSoup(res.text, "html.parser")
    price_data = []

    # Locate the Price section
    header = soup.find("span", id="Price")
    if not header:
        return []

    table = header.find_next("table")
    for row in table.find_all("tr")[1:]:
        cols = row.find_all("td")
        if len(cols) >= 3:
            game_text = cols[0].get_text(strip=True)

            # Clean prices: remove symbols, convert N/A to empty
            buy = cols[1].get_text(strip=True).replace("$", "").replace(",", "")
            sell = cols[2].get_text(strip=True).replace("$", "").replace(",", "")

            buy = "" if buy.upper() == "N/A" else buy
            sell = "" if sell.upper() == "N/A" else sell

            # Skip if both are empty
            if not buy and not sell:
                continue

            # Cross-reference with GAME_MAP keys
            v_ids = []
            for key, ids in GAME_MAP.items():
                if key in game_text:
                    v_ids.extend(ids)

            for v_id in set(v_ids):
                price_data.append({"vg_id": v_id, "buy": buy, "sell": sell})

    return price_data


def main():
    print("Starting Poké Ball price scraping...")

    output_path = Path(__file__).parent.parent / "data/v2/csv/item_prices.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    results = []
    balls = get_poke_ball_links()

    for b in balls:
        print(f"Scraping: {b['name']}...")
        try:
            prices = get_ball_prices(b["url"])
            for p in prices:
                results.append(
                    {
                        # "name": b["name"], # enable this if you wanna keep the name in the output for easier debugging
                        "item_id": b["item_id"],
                        "version_group_id": p["vg_id"],
                        "purchase_price": p["buy"],
                        "sell_price": p["sell"],
                    }
                )
            time.sleep(0.3)
        except Exception as e:
            print(f"Error on {b['name']}: {e}")

    if not results:
        print("No new data found.")
        return

    df_new = pd.DataFrame(results)

    # If file exists, merge with existing data
    if output_path.exists():
        df_old = pd.read_csv(output_path)
        df_combined = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df_combined = df_new

    # 1. Deduplicate (prevents repeating data if script is run twice)
    # 2. Sort by item_id then version_group_id
    df_final = df_combined.drop_duplicates(
        subset=["item_id", "version_group_id"], keep="last"
    )
    df_final = df_final.sort_values(by=["item_id", "version_group_id"])

    # Write back to CSV
    df_final.to_csv(output_path, index=False)

    print(f"\nSuccess! File updated and sorted at: {output_path}")


if __name__ == "__main__":
    main()
