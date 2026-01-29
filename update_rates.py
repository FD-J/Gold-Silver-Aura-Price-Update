import requests
import datetime
import os

GOLD_API = "https://api.auragold.in/api/data/v1/prices?product=24KGOLD"
SILVER_API = "https://api.auragold.in/api/data/v1/prices?product=24KSILVER"

def fetch_data(url):
    try:
        # We add a timestamp to the request to ensure we get the freshest data
        response = requests.get(f"{{url}}&t={{int(datetime.datetime.now().timestamp())}}", timeout=15)
        return response.json().get('data', {{}})
    except:
        return {{}}

def format_api_time(date_str):
    if not date_str: return "N/A"
    try:
        # Convert API string (2025-01-29 14:30:05) to a nicer format
        dt = datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        return dt.strftime('%d %b, %H:%M:%S')
    except:
        return date_str

def main():
    gold = fetch_data(GOLD_API)
    silver = fetch_data(SILVER_API)

    if not gold or not silver:
        print("Data fetch failed.")
        return

    # Extract prices and API timestamps
    g_price = f"{{float(gold.get('aura_buy_price', 0)):,.2f}}"
    s_price = f"{{float(silver.get('aura_buy_price', 0)):,.2f}}"
    
    # GETTING API UPDATED DATA FOR TIME
    g_time = format_api_time(gold.get('created_at'))
    s_time = format_api_time(silver.get('created_at'))

    html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="30">
    <style>
        body {{ background: #0f172a; color: white; font-family: sans-serif; display: flex; justify-content: center; padding: 20px; }}
        .card {{ background: #1e293b; padding: 20px; border-radius: 15px; width: 350px; border: 1px solid #334155; }}
        .price {{ font-size: 24px; font-weight: bold; color: #fbbf24; }}
        .time {{ font-size: 12px; color: #94a3b8; margin-bottom: 15px; }}
        h3 {{ margin: 0; font-size: 14px; text-transform: uppercase; color: #64748b; }}
    </style>
</head>
<body>
    <div class="card">
        <h2 style="text-align:center">FDJ Live</h2>
        
        <h3>Gold (24K)</h3>
        <div class="price">₹{{g_price}}</div>
        <div class="time">API Last Update: {{g_time}}</div>
        
        <hr style="border:0; border-top:1px solid #334155; margin: 15px 0;">
        
        <h3>Silver</h3>
        <div class="price">₹{{s_price}}</div>
        <div class="time">API Last Update: {{s_time}}</div>

        <p style="text-align:center; font-size:10px; color:#475569;">Page auto-refreshes every 30s</p>
    </div>
</body>
</html>
"""
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_template)

if __name__ == "__main__":
    main()
