import requests
import datetime
import json
import os

GOLD_API = "https://api.auragold.in/api/data/v1/prices?product=24KGOLD"
SILVER_API = "https://api.auragold.in/api/data/v1/prices?product=24KSILVER"

def fetch_data(url):
    try:
        response = requests.get(url, timeout=15)
        return response.json().get('data', {})
    except:
        return {}

def main():
    gold = fetch_data(GOLD_API)
    silver = fetch_data(SILVER_API)

    if not gold or not silver: return

    # Extract prices and API's own timestamp
    g_buy = gold.get('aura_buy_price', 0)
    g_sell = gold.get('aura_sell_price', 0)
    s_buy = silver.get('aura_buy_price', 0)
    s_sell = silver.get('aura_sell_price', 0)
    
    # Use API time if available, otherwise current time
    api_time = gold.get('created_at', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="refresh" content="30"> <title>FDJ Live</title>
    <style>
        body {{ background: #0f172a; color: white; font-family: sans-serif; display: flex; justify-content: center; padding: 20px; }}
        .card {{ background: #1e293b; padding: 25px; border-radius: 20px; width: 100%; max-width: 350px; border: 1px solid #334155; }}
        h2 {{ color: #fbbf24; text-align: center; margin-bottom: 20px; }}
        .row {{ display: flex; justify-content: space-between; margin: 10px 0; padding-bottom: 5px; border-bottom: 1px solid #2d3748; }}
        .label {{ color: #94a3b8; font-size: 14px; }}
        .price {{ font-weight: bold; font-size: 18px; color: #f8fafc; }}
        .footer {{ text-align: center; font-size: 11px; color: #64748b; margin-top: 20px; }}
    </style>
</head>
<body>
    <div class="card">
        <h2>FDJ Live Rates</h2>
        <div class="row"><span class="label">Gold Buy</span><span class="price">₹{float(g_buy):,.2f}</span></div>
        <div class="row"><span class="label">Gold Sell</span><span class="price">₹{float(g_sell):,.2f}</span></div>
        <div class="row"><span class="label">Silver Buy</span><span class="price">₹{float(s_buy):,.2f}</span></div>
        <div class="row"><span class="label">Silver Sell</span><span class="price">₹{float(s_sell):,.2f}</span></div>
        <div class="footer">
            Market Live: {api_time}<br>
            Next refresh in 30s...
        </div>
    </div>
</body>
</html>
"""
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_template)

if __name__ == "__main__":
    main()
