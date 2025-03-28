import requests
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import time
import os

# Set up Firefox options
firefox_options = Options()
firefox_options.add_argument("--headless")  # Run in headless mode

# Specify geckodriver path directly
geckodriver_path = "/usr/local/bin/geckodriver"

# Create a Service object with the geckodriver path
service = Service(executable_path=geckodriver_path)

# Set up the driver with the service
driver = webdriver.Firefox(service=service, options=firefox_options)

# Your Discord webhook URL
discord_webhook_url = "<url>"  # Replace this with your actual webhook URL

# Absolute path for seen_urls.txt
SEEN_URLS_FILE = os.path.abspath("seen_urls.txt")

def load_seen_urls():
    """Load previously seen URLs from a file."""
    if not os.path.exists(SEEN_URLS_FILE):
        print("[DEBUG] seen_urls.txt not found. Creating a new one.")
        return set()

    with open(SEEN_URLS_FILE, "r") as f:
        urls = set(line.strip() for line in f)
        print(f"[DEBUG] Loaded {len(urls)} seen URLs.")
        return urls

def save_seen_url(url):
    """Save a new URL to the file."""
    with open(SEEN_URLS_FILE, "a") as f:
        f.write(url.strip() + "\n")
    print(f"[DEBUG] Saved new URL: {url}")

def send_to_discord(message):
    """Send a message to Discord."""
    print(f"[DEBUG] Sending message (Length: {len(message)})")
    
    payload = {"content": message}
    headers = {"Content-Type": "application/json"}
    response = requests.post(discord_webhook_url, json=payload, headers=headers)
    
    if response.status_code == 204:
        print("[DEBUG] Message sent successfully!")
    else:
        print(f"[ERROR] Failed to send message. Response: {response.status_code}, {response.text}")

    # Add a delay to avoid rate limiting and link preview issues
    time.sleep(1)

def get_best_offers(search_query, max_price):
    """Scrape eBay for best offers and send new ones to Discord."""
    seen_urls = load_seen_urls()  # Load previously seen URLs
    url = f"https://www.ebay.com/sch/i.html?_nkw={search_query}&_ipg=240&rt=nc&LH_BO=1"
    driver.get(url)

    items = driver.find_elements(By.CSS_SELECTOR, '.s-item')
    
    if not items:
        print("[DEBUG] No items found.")
        return
    
    for item in items:
        title = item.find_element(By.CSS_SELECTOR, '.s-item__title').text
        price_text = item.find_element(By.CSS_SELECTOR, '.s-item__price').text
        link = item.find_element(By.CSS_SELECTOR, '.s-item__link').get_attribute('href').split("?")[0]  # Remove tracking params

        if link in seen_urls:
            print(f"[DEBUG] Skipping already seen URL: {link}")
            continue  # Skip if we've already seen this URL

        if price_text:
            try:
                price = float(price_text.replace('$', '').replace(',', '').strip())
                if price <= max_price:
                    message = f"**Title:** {title}\n**Price:** {price_text}\n**Link:** {link}\n" + "=" * 50 + "\n"
                    send_to_discord(message)
                    save_seen_url(link)  # Save the URL to prevent duplicates
            except ValueError:
                print(f"[DEBUG] Could not convert price '{price_text}' to float. Skipping.")
                continue

# Example usage
search_query = "<search>"
max_price = <max_int>
get_best_offers(search_query, max_price)

driver.quit()

