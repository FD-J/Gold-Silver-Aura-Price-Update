import requests
import datetime
import os

GOLD_API = "https://api.auragold.in/api/data/v1/prices?product=24KGOLD"
SILVER_API = "https://api.auragold.in/api/data/v1/prices?product=24KSILVER"

def fetch_data(url):
    try:
        # Cache busting
        ts = int(datetime.datetime.now().timestamp())
        response = requests.get(f"{url}&t={ts}", timeout=15)
        return response.json().get('data', {})
    except Exception as e:
        print(f"Error: {e}")
        return {}

def format_api_time(date_str):
    if not date_str: return "N/A"
    try:
        dt = datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        return dt.strftime('%d %b, %H:%M:%S')
    except:
        return date_str

def main():
    gold = fetch_data(GOLD_API)
    silver = fetch_data(SILVER_API)

    if not gold or not silver:
        print("Data fetch failed. File not updated.")
        return

    # Extracting exact API values
    g_buy = f"{float(gold.get('aura_buy_price', 0)):,.2f}"
    g_sell = f"{float(gold.get('aura_sell_price', 0)):,.2f}"
    s_buy = f"{float(silver.get('aura_buy_price', 0)):,.2f}"
    s_sell = f"{float(silver.get('aura_sell_price', 0)):,.2f}"
    
    # Accurate API timestamps
    g_time = format_api_time(gold.get('created_at'))
    s_time = format_api_time(silver.get('created_at'))

    # THE TEMPLATE: Double {{ }} for CSS, single { } for our Python variables
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="refresh" content="30">
    <title>FDJ Live Rates - Ft. Aura Gold</title>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: system-ui, -apple-system, sans-serif; }}
        body {{ min-height: 100vh; background: #0f172a; display: flex; justify-content: center; align-items: center; color: #fff; }}
        .dashboard {{ width: 90%; max-width: 400px; background: rgba(30,41,59,0.7); backdrop-filter: blur(20px); border-radius: 24px; padding: 24px; border: 1px solid rgba(255,255,255,0.1); box-shadow: 0 25px 50px -12px rgba(0,0,0,0.5); }}
        .header {{ text-align: center; margin-bottom: 20px; }}
        .section {{ background: rgba(255,255,255,0.05); border-radius: 16px; padding: 16px; margin-bottom: 12px; }}
        .row {{ display: flex; justify-content: space-between; margin: 6px 0; font-size: 18px; }}
        .label {{ color: #94a3b8; font-size: 14px; margin-bottom: 8px; }}
        .value {{ font-variant-numeric: tabular-nums; font-weight: 600; color: #fbbf24; }}
        .time {{ text-align: right; font-size: 11px; color: #64748b; margin-top: 8px; }}
    </style>
</head>
<body>
<div class="dashboard">
    <div class="header"><h1>FDJ Live Rates</h1></div>
    <div class="section">
        <div class="label">🥇 Gold 24K (per g)</div>
        <div class="row"><span>Buy</span><span class="value">₹{g_buy}</span></div>
        <div class="row"><span>Sell</span><span class="value">₹{g_sell}</span></div>
        <div class="time">API Sync: {g_time}</div>
    </div>
    <div class="section">
        <div class="label">🥈 Silver (per g)</div>
        <div class="row"><span>Buy</span><span class="value">₹{s_buy}</span></div>
        <div class="row"><span>Sell</span><span class="value">₹{s_sell}</span></div>
        <div class="time">API Sync: {s_time}</div>
    </div>
    <p style="text-align:center; font-size:10px; color:#475569;">Auto-syncs every 10 min | Refresh 30s</p>
</div>
</body>
</html>"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("Dashboard updated successfully.")

if __name__ == "__main__":
    main()
