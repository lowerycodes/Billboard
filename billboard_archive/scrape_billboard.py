import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os

# --- 1️⃣ Scrape Billboard Hot 100 ---
url = "https://www.billboard.com/charts/hot-100/"
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# Get songs and artists
songs = [h3.get_text(strip=True) for h3 in soup.select("li.o-chart-results-list__item h3")]
artists = [span.get_text(strip=True) for span in soup.select("li.o-chart-results-list__item span.c-label") 
           if span.get_text(strip=True) != '' and not span.get_text(strip=True).isdigit()]

length = min(len(songs), len(artists))
songs = songs[:length]
artists = artists[:length]

# --- 2️⃣ Save CSV ---
today = datetime.today().strftime("%Y-%m-%d")
csv_filename = f"billboard_hot100_{today}.csv"
df = pd.DataFrame({
    "Rank": range(1, length + 1),
    "Song": songs,
    "Artist": artists
})
df.to_csv(csv_filename, index=False)
print(f"Saved CSV: {csv_filename}")

# --- 3️⃣ Generate HTML with links to all CSVs ---
csv_files = sorted([f for f in os.listdir('.') if f.startswith('billboard_hot100_') and f.endswith('.csv')],
                   reverse=True)

html_links = "\n".join([f'<li><a href="{f}" download>{f}</a></li>' for f in csv_files])

html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Billboard Hot 100 Archive</title>
</head>
<body>
    <h1>Billboard Hot 100 Archive</h1>
    <ul>
        {html_links}
    </ul>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("HTML page updated with all CSVs.")
