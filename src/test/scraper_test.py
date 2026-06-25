import requests
from bs4 import BeautifulSoup
import re
import json
from datetime import datetime
import os

print("Skript Start")

url = "https://www.mindfactory.de/product_info.php/16GB-Sapphire-Radeon-RX-9070-XT-Pure-Aktiv-PCIe-5-0-x16--Retail-_1615590.html"
product_id = "1615590"
product_name = "Sapphire RX 9070 XT Pure"
shop = "Mindfactory"
json_file = "price_tracker.json"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

# Preis scrapen
print(f"Starte Request zu: {url}")
response = requests.get(url, headers=headers, timeout=10)
print(f"Response erhalten! Status: {response.status_code}")

soup = BeautifulSoup(response.content, 'lxml')
print("HTML geparst mit BeautifulSoup")

price_div = soup.find('div', class_='pprice')
print(f"Preis-DIV gefunden: {price_div is not None}")

if price_div:
    if price_div:
        print("Preis-DIV gefunden!")
        price_text = price_div.get_text(strip=True)
        print(f"Preis-Text: {price_text}")
    price_text = price_div.get_text(strip=True)
    price_match = re.search(r'(\d+,\d+)', price_text)
    
    if price_match:
        price_str = price_match.group(1)
        price_float = float(price_str.replace(',', '.'))
        
        # JSON laden oder neu erstellen
        if os.path.exists(json_file):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except json.JSONDecodeError:
                # Datei ist leer oder kaputt, neu anfangen
                data = {}
        else:
            data = {}
                
        # Produkt hinzufügen/updaten
        if product_id not in data:
            data[product_id] = {
                "name": product_name,
                "shop": shop,
                "prices": []
            }
        
        # Neuen Preis hinzufügen
        today = datetime.now().strftime("%Y-%m-%d %H:%M")
        data[product_id]["prices"].append({
            "date": today,
            "price": price_float
        })
        
        # JSON speichern
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"Preis gespeichert: {price_float} € am {today}")
        
        # Minimum checken
        all_prices = [p["price"] for p in data[product_id]["prices"]]
        min_price = min(all_prices)
        
        if price_float < min_price:
            print(f"NEUES MINIMUM! {price_float}€")
        else:
            print(f"Aktuelles Minimum: {min_price}€")