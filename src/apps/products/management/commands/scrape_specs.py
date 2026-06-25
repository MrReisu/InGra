import asyncio
import json
import random
import time
from playwright.async_api import async_playwright

AMD_FILTER = ["RX"]

NVIDIA_FILTER = [
    "GTX 9", "GTX 10", "RTX 20", "RTX 30", "RTX 40", "RTX 50"
]

BASE_URL = "https://www.techpowerup.com"

MANUFACTURERS = [
    {"name": "AMD",    "url": f"{BASE_URL}/gpu-specs/?mfgr=AMD",    "filter": AMD_FILTER},
    {"name": "NVIDIA", "url": f"{BASE_URL}/gpu-specs/?mfgr=NVIDIA", "filter": NVIDIA_FILTER},
]

def is_relevant(gpu_name: str, filters: list[str]) -> bool:
    return any(f.lower() in gpu_name.lower() for f in filters)


async def random_delay():
    await asyncio.sleep(random.uniform(2, 5))



async def get_chip_urls(page, mfgr_url: str, filters: list[str]) -> list[dict]:
    await page.goto(mfgr_url, wait_until="networkidle")
    await random_delay()

    links = await page.query_selector_all("a.item-name")

    chip_urls = []
    for link in links:
        name = await link.inner_text()
        href = await link.get_attribute("href")

        if href and ".c" in href and is_relevant(name, filters):
            chip_urls.append({
                "name": name.strip(),
                "url": BASE_URL + href
            })

    return chip_urls


async def get_board_urls(page, chip: dict) -> list[dict]:

    await page.goto(chip["url"], wait_until="networkidle")
    await random_delay()

    links = await page.query_selector_all("#boards tbody div.board-table-title__inner a")

    board_urls = []
    for link in links:
        name = await link.inner_text()
        href = await link.get_attribute("href")

        if href and ".b" in href:
            board_urls.append({
                "name": name.strip(),
                "chip": chip["name"],
                "url": BASE_URL + href
            })

    return board_urls


async def scrape_board_specs(page, board: dict) -> dict:
  
    await page.goto(board["url"], wait_until="networkidle")
    await random_delay()
 
    specs = {
        "name": board["name"],
        "chip": board["chip"],
        "url": board["url"],
    }

    rows = await page.query_selector_all("ul.gpudb-specs-large dl.clearfix")
 
    for row in rows:
        dt = await row.query_selector("dt")
        dd = await row.query_selector("dd")
 
        if dt and dd:
            key = (await dt.inner_text()).strip()
            value = (await dd.inner_text()).strip()
            specs[key] = value
 
    return specs


async def main():
    all_specs = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # User-Agent setzen damit wir nicht sofort als Bot erkannt werden
        await page.set_extra_http_headers({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })

        for mfgr in MANUFACTURERS:
            print(f"\n{'='*50}")
            print(f"Hersteller: {mfgr['name']}")
            print(f"{'='*50}")

            chip_urls = await get_chip_urls(page, mfgr["url"], mfgr["filter"])
            # Für Testzwecke
            chip_urls = chip_urls[:1]

            for chip in chip_urls:
                board_urls = await get_board_urls(page, chip)
                # Für Testzwecke
                

                try:
                    specs = await scrape_board_specs(page, board)
                    specs["manufacturer"] = mfgr["name"]
                    all_specs.append(specs)
                    print(f"       {specs['name']}")
                except Exception as e:
                    print(f"       Fehler bei {board['name']}: {e}")

        await browser.close()

    # Ergebnis als JSON speichern
    output_file = "gpu_specs.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_specs, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*50}")
    print(f"Fertig! {len(all_specs)} GPUs gespeichert in {output_file}")
    print(f"{'='*50}")


if __name__ == "__main__":
    asyncio.run(main())

