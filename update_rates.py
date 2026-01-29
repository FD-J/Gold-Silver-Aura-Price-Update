import requests
import datetime

def get_data():
    g = requests.get("https://api.auragold.in/api/data/v1/prices?product=24KGOLD").json()['data']
    s = requests.get("https://api.auragold.in/api/data/v1/prices?product=24KSILVER").json()['data']
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>FDJ Live Rates</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{ font-family: sans-serif; background: #0f172a; color: white; display: flex; justify-content: center; padding: 20px; }}
            .card {{ background: #1e293b; padding: 20px; border-radius: 15px; width: 100%; max-width: 350px; border: 1px solid #334155; }}
            h1 {{ font-size: 1.2rem; text-align: center; color: #fbbf24; }}
            .row {{ display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #334155; }}
            .time {{ font-size: 0.8rem; text-align: center; margin-top: 15px; opacity: 0.6; }}
        </style>
    </head>
    <body>
        <div class="card">
            <h1>FDJ Metal Rates</h1>
            <div class="row"><span>Gold Buy</span><strong>₹{g['aura_buy_price']}</strong></div>
            <div class="row"><span>Gold Sell</span><strong>₹{g['aura_sell_price']}</strong></div>
            <div class="row"><span>Silver Buy</span><strong>₹{s['aura_buy_price']}</strong></div>
            <div class="row"><span>Silver Sell</span><strong>₹{s['aura_sell_price']}</strong></div>
            <div class="time">Last updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
        </div>
    </body>
    </html>
    """
    with open("index.html", "w") as f:
        f.write(html_content)

if __name__ == "__main__":
    get_data()
