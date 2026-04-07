import requests
from datetime import datetime, timezone
import time
import sys
from plyer import notification

# ---------------- CLIENT ---------------- #
class PolymarketClient:
    def __init__(self, api_key: str, endpoint: str):
        self.api_key = api_key
        self.endpoint = endpoint
        self.headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}

    def get_markets(self, limit=200):
        url = f"{self.endpoint}/markets"
        params = {"limit": limit, "active": "true", "closed": "false", "accepting_orders": "true"}
        r = requests.get(url, headers=self.headers, params=params)
        r.raise_for_status()
        return r.json().get("data", [])

# ---------------- LOGICA ---------------- #
def is_valid_market(m, min_volume=100):
    if not m.get("active") or m.get("closed") or not m.get("accepting_orders"):
        return False
    end_iso = m.get("end_date_iso")
    if not end_iso:
        return False
    end_dt = datetime.fromisoformat(end_iso.replace("Z", "+00:00"))
    return end_dt > datetime.now(timezone.utc) and m.get("volume",0) >= min_volume

def extract_yes_price(m):
    for o in m.get("outcomes", []):
        if o.get("outcome") == "Yes":
            return o.get("price")
    return None

def score_market(m):
    price = extract_yes_price(m)
    volume = m.get("volume", 0)
    if price is None:
        return 0
    score = 1.5 if 0.3 < price < 0.7 else 1
    return score * volume

def alert():
    sys.stdout.write('\a')
    sys.stdout.flush()

def notify_desktop(title, message):
    notification.notify(title=title, message=message, app_name="Polymarket Bot", timeout=5)

# ---------------- INTERFACCIA ---------------- #
def show_top_markets(markets, top=10):
    ranked = sorted(markets, key=score_market, reverse=True)
    print("\n🔥 TOP MERCATI:")
    for i, m in enumerate(ranked[:top], 1):
        price = extract_yes_price(m)
        print(f"{i}. 🧠 {m.get('question')[:60]}... | YES: {price} | Volume: {m.get('volume')} | Fine: {m.get('end_date_iso')}")
    print("-"*50)
    return ranked[:top]

# ---------------- MAIN ---------------- #
def main():
    API_KEY = "LA_TUA_API_KEY"
    ENDPOINT = "https://clob.polymarket.com"
    client = PolymarketClient(API_KEY, ENDPOINT)
    seen_markets = set()

    print("🔥 BOT INTERATTIVO PARTITO…\n")
    
    markets_cache = []

    while True:
        print("\nComandi: [R]efresh | [T]op mercati | [Q]uit")
        choice = input("Scegli comando: ").strip().upper()
        
        if choice == "Q":
            print("🛑 Uscita bot…")
            break
        elif choice == "R":
            try:
                markets = client.get_markets(limit=200)
                new_markets = [m for m in markets if is_valid_market(m) and m.get("id") not in seen_markets]
                for m in new_markets:
                    seen_markets.add(m.get("id"))
                    price = extract_yes_price(m)
                    info = f"🧠 {m.get('question')}\n💰 YES: {price}\n📊 Volume: {m.get('volume')}\n⏳ Fine: {m.get('end_date_iso')}"
                    print(info)
                    print("-"*50)
                    alert()
                    notify_desktop("🔥 Nuovo mercato tradabile", info)
                markets_cache = markets
                if not new_markets:
                    print("Nessun nuovo mercato trovato.")
            except Exception as e:
                print("Errore fetch mercati:", e)
        elif choice == "T":
            if not markets_cache:
                print("Prima fai [R]efresh per caricare mercati.")
                continue
            show_top_markets(markets_cache, top=10)
        else:
            print("Comando non valido!")

if __name__ == "__main__":
    main()