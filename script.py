import requests
from bs4 import BeautifulSoup
import csv
from io import StringIO

SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/1GgVMznHo-9N4vAwqIyjVgdC4yYqENQxQ0wXx3JyNdfg/export?format=csv"
CHAT_WEBHOOK_URL = "https://chat.googleapis.com/v1/spaces/AAQA-RWdiRo/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=Q80CR6-bCSu2z6U6Ulj6l2tLpSrcTMA0S0_yAL8vkX4"

def get_urls():
    res = requests.get(SHEET_CSV_URL)
    data = StringIO(res.text)
    reader = csv.DictReader(data)

    urls = []
    for row in reader:
        urls.append((row["Website Name"], row["URL"]))
    return urls

def check_h1(url):
    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        return len(soup.find_all("h1"))
    except:
        return "Error"

def send_alert(issues):
    if not issues:
        return

    msg = "⚠️ H1 Issues:\n\n"
    for i in issues:
        msg += i + "\n"

    requests.post(CHAT_WEBHOOK_URL, json={"text": msg})

def main():
    urls = get_urls()
    issues = []

    for name, url in urls:
        count = check_h1(url)

        if count != 1:
            issues.append(f"{name} → {count} H1")

    send_alert(issues)

main()
