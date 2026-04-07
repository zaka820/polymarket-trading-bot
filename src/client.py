import requests
from datetime import datetime, timezone


class PolymarketClient:
    def __init__(self, api_key, endpoint):
        self.endpoint = endpoint
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def get_markets(self):
        url = f"{self.endpoint}/markets"
        params = {
            "limit": 200,
            "active": "true",
            "closed": "false",
            "accepting_orders": "true"
        }

        r = requests.get(url, headers=self.headers, params=params)
        r.raise_for_status()
        return r.json().get("data", [])


# ---------------- LOGICA ---------------- #

def is_valid_market(m):
    if not m.get("active"):
        return False
    if m.get("closed"):
        return False
    if not m.get("accepting_orders"):
        return False

    end = m.get("end_date_iso")
    if not end:
        return False

    end_dt = datetime.fromisoformat(end.replace("Z", "+00:00"))
    now = datetime.now(timezone.utc)

    hours_left = (end_dt - now).total_seconds() / 3600

    return 24 < hours_left < 120  # tra 1 e 5 giorni


def extract_price(m):
    outcomes = m.get("outcomes", [])
    for o in outcomes:
        if o.get("outcome") == "Yes":
            return o.get("price")
    return None


def score_market(m):
    price = extract_price(m)
    volume = m.get("volume", 0)

    if price is None:
        return 0

    # Strategia base:
    # cerchiamo prezzi tra 0.3 e 0.7 + volume alto
    if 0.3 < price < 0.7:
        return volume * 1.5

    return volume


# ---------------- MAIN ---------------- #

def main():
    API_KEY = "INSERISCI_LA_TUA_API_KEY"
    ENDPOINT = "https://clob.polymarket.com"

    client = PolymarketClient(API_KEY, ENDPOINT)

    markets = client.get_markets()

    print(f"Mercati ricevuti: {len(markets)}")

    # filtro serio
    filtered = [m for m in markets if is_valid_market(m)]

    print(f"Mercati validi: {len(filtered)}")

    # scoring
    ranked = sorted(filtered, key=score_market, reverse=True)

    print("\n🔥 TOP OPPORTUNITÀ:\n")

    for m in ranked[:10]:
        price = extract_price(m)

        print(f"🧠 {m.get('question')}")
        print(f"💰 Prezzo YES: {price}")
        print(f"📊 Volume: {m.get('volume')}")
        print(f"⏳ Fine: {m.get('end_date_iso')}")
        print("-" * 50)


if __name__ == "__main__":
    print("BOT PARTITO…")
    main()