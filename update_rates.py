import requests
import datetime

# Configuration
G_URL = "https://api.auragold.in/api/data/v1/prices?product=24KGOLD"
S_URL = "https://api.auragold.in/api/data/v1/prices?product=24KSILVER"

def fetch_data(url):
    try:
        # Cache-busting with timestamp
        ts = int(datetime.datetime.now().timestamp())
        res = requests.get(f"{url}&t={ts}", timeout=15)
        res.raise_for_status()
        return res.json().get('data', {})
    except Exception as e:
        print(f"Fetch Error: {e}")
        return None

def main():
    gold = fetch_data(G_URL)
    silver = fetch_data(S_URL)

    # CRITICAL: If API fails, STOP so we don't overwrite index.html with nothing
    if not gold or not silver:
        print("API Error: Fetch failed. Check logs.")
        return

    # Data extraction
    g_buy = f"{float(gold.get('aura_buy_price', 0)):,.2f}"
    g_sell = f"{float(gold.get('aura_sell_price', 0)):,.2f}"
    s_buy = f"{float(silver.get('aura_buy_price', 0)):,.2f}"
    s_sell = f"{float(silver.get('aura_sell_price', 0)):,.2f}"
    
    # Use API time, format: "29 Jan, 14:30"
    raw_time = gold.get('created_at', "Live")
    try:
        api_time = datetime.datetime.strptime(raw_time, '%Y-%m-%d %H:%M:%S').strftime('%d %b, %H:%M')
    except:
        api_time = raw_time

    # Plain HTML string (NO f-string here to avoid CSS brace errors)
    html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="refresh" content="30">
    <title>FDJ Live Rates</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: sans-serif; }
        body { background: #0f172a; color: white; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .card { background: #1e293b; padding: 25px; border-radius: 20px; width: 350px; border: 1px solid #334155; }
        h1 { text-align: center; color: #fbbf24; font-size: 22px; margin-bottom: 20px; }
        .metal { background: rgba(255,255,255,0.05); padding: 15px; border-radius: 12px; margin-bottom: 10px; }
        .row { display: flex; justify-content: space-between; margin: 5px 0; font-size: 18px; font-weight: bold; }
        .val { color: #fbbf24; }
        .label { color: #94a3b8; font-size: 12px; margin-bottom: 4px; text-transform: uppercase; }
        .footer { text-align: center; font-size: 11px; color: #64748b; margin-top: 15px; }
    </style>
</head>
<body>
    <div class="card">
        <h1>FDJ Live Rates</h1>
        <div class="metal">
            <p class="label">GOLD 24K (1g)</p>
            <div class="row"><span>Buy</span><span class="val">₹[G_BUY]</span></div>
            <div class="row"><span>Sell</span><span class="val">₹[G_SELL]</span></div>
        </div>
        <div class="metal">
            <p class="label">SILVER (1kg)</p>
            <div class="row"><span>Buy</span><span class="val">₹[S_BUY]</span></div>
            <div class="row"><span>Sell</span><span class="val">₹[S_SELL]</span></div>
        </div>
        <div class="footer">Last API Update: [TIME]</div>
    </div>
</body>
</html>
"""
    # Safe replacement
    output = html_template.replace("[G_BUY]", g_buy).replace("[G_SELL]", g_sell).replace("[S_BUY]", s_buy).replace("[S_SELL]", s_sell).replace("[TIME]", api_time)

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(output)
    print("Update successful!")

if __name__ == "__main__":
    main()
