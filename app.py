from flask import Flask
import requests
import smtplib
from email.mime.text import MIMEText
from bs4 import BeautifulSoup

app = Flask(__name__)
SEEN_LISTINGS = set()

# E-Mail-Konfiguration (ändert sich in Schritt 4)
EMAIL_SENDER = "deine.email@gmail.com"
EMAIL_PASSWORD = "dein_app_passwort"  # Platzhalter
EMAIL_RECEIVER = "dein_empfänger@email.com"

def send_notification(title, price):
    msg = MIMEText(f"Neues Listing: {title} für {price}")
    msg["Subject"] = "Neues One Piece TCG Listing!"
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)

@app.route('/')
def check_new_listings():
    url = "https://www.kleinanzeigen.de/s-one-piece-tcg/k0"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    listings = soup.find_all("article", class_="aditem")
    for listing in listings[:5]:  # Nur die ersten 5
        listing_id = listing.get("data-adid", "unknown")
        title = listing.find("a", class_="ellipsis").text.strip()
        price = listing.find("p", class_="aditem-main--middle--price").text.strip()
        if listing_id not in SEEN_LISTINGS:
            SEEN_LISTINGS.add(listing_id)
            send_notification(title, price)
    return "Checked listings", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
