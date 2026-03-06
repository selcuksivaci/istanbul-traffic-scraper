from playwright.sync_api import sync_playwright
import pandas as pd
from datetime import datetime
import os

origin = "İhsaniye Metro İstasyonu"
destination = "Huzurevi Metro İstasyonu"
waypoint = "Fatih Sultan Mehmet Köprüsü"

url = f"https://www.google.com/maps/dir/{origin}/{waypoint}/{destination}"

file = "data.csv"

with sync_playwright() as p:

    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.goto(url)
    page.wait_for_timeout(8000)

    try:
        duration = page.locator("div.fontHeadlineSmall").first.inner_text()
    except:
        duration = "bulunamadı"

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    new_row = pd.DataFrame([[now, duration]], columns=["zaman","sure"])

    if os.path.exists(file):
        df = pd.read_csv(file)
        df = pd.concat([df,new_row], ignore_index=True)
    else:
        df = new_row

    df.to_csv(file, index=False)

    browser.close()
