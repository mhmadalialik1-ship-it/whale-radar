import subprocess
import json

def calculate_rsi(prices, period=14):
    if len(prices) < period: return 50
    gains, losses = [], []
    for i in range(1, len(prices)):
        change = prices[i] - prices[i-1]
        gains.append(change if change > 0 else 0)
        losses.append(abs(change) if change < 0 else 0)
    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period
    if avg_loss == 0: return 100
    for i in range(period, len(gains)):
        avg_gain = (avg_gain * 13 + gains[i]) / 14
        avg_loss = (avg_loss * 13 + losses[i]) / 14
    if avg_loss == 0: return 100
    return 100 - (100 / (1 + (avg_gain / avg_loss)))

def fetch_data_curl(url):
    try:
        # استخدام curl المدمج في الهاتف بدلاً من مكتبات الـ python المعقدة
        result = subprocess.run(['curl', '-s', url], capture_output=True, text=True)
        return json.loads(result.stdout)
    except:
        return None

def get_binance_closes():
    data = fetch_data_curl("https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1h&limit=50")
    if data:
        return [float(candle[4]) for candle in data]
    return None

def get_okx_closes():
    data = fetch_data_curl("https://www.okx.com/api/v5/market/candles?instId=BTC-USDT&bar=1H&limit=50")
    if data and 'data' in data:
        closes = [float(candle[4]) for candle in data['data']]
        closes.reverse()
        return closes
    return None

def analyze_and_print(exchange, closes):
    if not closes:
        print(f" ❌ {exchange:<8} | خطأ في الاتصال بالمنصة")
        return
    
    price = closes[-1]
    rsi = calculate_rsi(closes)
    ma20 = sum(closes[-20:]) / 20
    
    if rsi < 35: decision, conf = "🚀 شراء قوي", "90%"
    elif rsi > 65: decision, conf = "⚠️ بيع/خروج", "85%"
    elif price > ma20: decision, conf = "📈 صعود مؤقت", "65%"
    else: decision, conf = "⏳ انتظار", "50%"
    
    print(f" 🛰️ {exchange:<8} | السعر: ${price:<10,.2f} | القرار: {decision:<12} | الثقة: {conf:<4} | RSI: {rsi:.2f}")

def main():
    print("\n" + "═"*70)
    print("      🛰️ رادار PROWHALEX المستقل الذكي (OKX & BINANCE) 🛰️")
    print("═"*70)
    
    binance_data = get_binance_closes()
    okx_data = get_okx_closes()
    
    analyze_and_print("BINANCE", binance_data)
    analyze_and_print("OKX", okx_data)
    print("═"*70 + "\n")

if __name__ == "__main__":
    main()

