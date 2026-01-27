from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import time

INPUT_FILE = "ip_list.xlsx"
OUTPUT_FILE = "ip_blacklist_yes_no_report.xlsx"

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)

df = pd.read_excel(INPUT_FILE)
results = []

for _, row in df.iterrows():
    ip = row["ip_address"]
    driver.get(f"https://mxtoolbox.com/SuperTool.aspx?action=blacklist:{ip}")
    time.sleep(5)  # wait for page to load

    page_text = driver.find_element(By.TAG_NAME, "body").text.lower()
    if "listed" in page_text or "blacklisted" in page_text:
        result = "YES"
    elif "not listed" in page_text or "clean" in page_text:
        result = "NO"
    else:
        result = "UNKNOWN"

    results.append({
        "IP Address": ip,
        "Source": "MXToolbox",
        "Listed (YES/NO)": result
    })

driver.quit()

pd.DataFrame(results).to_excel(OUTPUT_FILE, index=False)
print("Blacklist check completed!")
