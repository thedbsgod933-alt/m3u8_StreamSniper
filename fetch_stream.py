import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# === CONFIGURATION ===
ANIME_ID = "kochikame-qd99"  # Change this to scrape a different anime
EPISODE_RANGE = range(1, 101)  # Episodes 1 to 100

# === SETUP HEADLESS CHROME WITH CDP LOGGING ===
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

caps = DesiredCapabilities.CHROME
caps["goog:loggingPrefs"] = {"performance": "ALL"}

driver = webdriver.Chrome(options=options, desired_capabilities=caps)

# === SCRAPE LOOP ===
found_links = []

for ep in EPISODE_RANGE:
    url = f"https://anigo.to/watch/{ANIME_ID}#ep={ep}"
    print(f"🔍 Checking Episode {ep}: {url}")
    driver.get(url)
    time.sleep(10)  # Wait for video and network traffic to load

    logs = driver.get_log("performance")
    for entry in logs:
        message = entry["message"]
        if ".m3u8" in message:
            start = message.find("https")
            end = message.find(".m3u8") + 5
            stream_url = message[start:end]
            if stream_url not in found_links:
                found_links.append(stream_url)
                print(f"✅ Episode {ep}: {stream_url}")
            break

driver.quit()

# === FINAL OUTPUT ===
print("\n🎉 All Extracted .m3u8 Links:")
for link in found_links:
    print(link)
