import requests
import datetime
import os

# API URLs
GOLD_API = "https://api.auragold.in/api/data/v1/prices?product=24KGOLD"
SILVER_API = "https://api.auragold.in/api/data/v1/prices?product=24KSILVER"

def fetch_data(url):
    try:
        # Adding a timestamp to bypass any server-side caching
        response = requests.get(f"{url}&t={int(datetime.datetime.now().timestamp())}", timeout=15)
        response.raise_for_status()
        return response.json().get('data', {})
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def main():
    # 1. Fetch live data
    gold = fetch_data(GOLD_API)
    silver = fetch_data(SILVER_API)

    if not gold or not silver:
        print("Failed to retrieve data. Skipping update.")
        return

    # 2. Prepare the values
    # Format numbers with commas and 2 decimal places (e.g., 7,250.00)
    g_buy = f"{float(gold.get('aura_buy_price', 0)):,.2f}"
    g_sell = f"{float(gold.get('aura_sell_price', 0)):,.2f}"
    s_buy = f"{float(silver.get('aura_buy_price', 0)):,.2f}"
    s_sell = f"{float(silver.get('aura_sell_price', 0)):,.2f}"
    
    # Current time for the footer
    last_update = datetime.datetime.now().strftime('%d %b %Y, %H:%M:%S')

    # 3. The HTML Template
    # IMPORTANT: We use {{ }} for CSS to avoid confusing Python's .format()
    html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FDJ Live Metal Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg: #0f172a;
            --card-bg: rgba(30, 41, 59, 0.7);
            --accent-gold: #fbbf24;
            --accent-silver: #94a3b8;
            --text-main: #f8fafc;
            --text-dim: #94a3b8;
            --border: rgba(255, 255, 255, 0.1);
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', sans-serif; }}
        body {{ 
            background-color: var(--bg);
            background-image: radial-gradient(circle at top right, #1e293b, #0f172a);
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }}
        .dashboard {{
            width: 100%;
            max-width: 450px;
            background: var(--card-bg);
            backdrop-filter: blur(16px);
            border: 1px solid var(--border);
            border-radius: 24px;
            padding: 32px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
        }}
        .header {{ text-align: center; margin-bottom: 30px; }}
        .header h1 {{ font-size: 24px; font-weight: 600; letter-spacing: -0.5px; margin-bottom: 4px; }}
        .header p {{ font-size: 14px; color: var(--text-dim); }}
        .metal-card {{
            background: rgba(255, 255, 255, 0.03);
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 16px;
            border: 1px solid var(--border);
        }}
        .metal-header {{
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 16px;
            font-weight: 600;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .gold {{ color: var(--accent-gold); }}
        .silver {{ color: var(--accent-silver); }}
        .price-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }}
        .price-label {{ font-size: 12px; color: var(--text-dim); margin-bottom: 4px; }}
        .price-value {{ font-size: 20px; font-weight: 600; font-variant-numeric: tabular-nums; }}
        .footer {{
            margin-top: 24px;
            text-align: center;
            font-size: 12px;
            color: var(--text-dim);
            border-top: 1px solid var(--border);
            padding-top: 16px;
        }}
        .live-indicator {{
            display: inline-block;
            width: 8px;
            height: 8px;
            background: #22c55e;
            border-radius: 50%;
            margin-right: 6px;
            box-shadow: 0 0 10px #22c55e;
            animation: pulse 2s infinite;
        }}
        @keyframes pulse {{
            0% {{ opacity: 1; }}
            50% {{ opacity: 0.4; }}
            100% {{ opacity: 1; }}
        }}
    </style>
</head>
<body>
<div class="dashboard">
    <div class="header">
        <h1>FDJ Metal Rates</h1>
        <p>Live Market Dashboard</p>
    </div>
    <div class="metal-card">
        <div class="metal-header gold"><span>🥇</span> Gold 24K (per gm)</div>
        <div class="price-grid">
            <div class="price-item"><div class="price-label">BUY</div><div class="price-value">₹{g_buy}</div></div>
            <div class="price-item"><div class="price-label">SELL</div><div class="price-value">₹{g_sell}</div></div>
        </div>
    </div>
    <div class="metal-card">
        <div class="metal-header silver"><span>🥈</span> Silver (per kg)</div>
        <div class="price-grid">
            <div class="price-item"><div class="price-label">BUY</div><div class="price-value">₹{s_buy}</div></div>
            <div class="price-item"><div class="price-label">SELL</div><div class="price-value">₹{s_sell}</div></div>
        </div>
    </div>
    <div class="footer">
        <span class="live-indicator"></span>
        Last Sync: {last_update}
    </div>
</div>
</body>
</html>
"""
    # 4. Save the file
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_template)
    print("Successfully updated index.html")

if __name__ == "__main__":
    main()
