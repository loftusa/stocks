import os
import time
from datetime import datetime
import yfinance as yf
from twilio.rest import Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Twilio setup
twilio_client = Client(
    os.getenv('TWILIO_ACCOUNT_SID'),
    os.getenv('TWILIO_AUTH_TOKEN')
)

# Stock symbols to track
STOCKS = [
    "AAPL",  # Apple
    "MSFT",  # Microsoft
    "GOOGL", # Google
    "AMZN",  # Amazon
    "NVDA",  # NVIDIA
    "META",  # Meta (Facebook)
    "TSLA",  # Tesla
    "TSM",   # TSMC
    "ASML",  # ASML
    "NVDA",  # NVIDIA
]

def get_stock_summary(symbol):
    """Get summary of stock movement for the last day"""
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period="2d")  # Get 2 days to calculate change
        
        if len(hist) < 2:
            return f"❌ No data available for {symbol}"
            
        current_price = hist['Close'].iloc[-1]
        prev_price = hist['Close'].iloc[-2]
        price_change = current_price - prev_price
        percent_change = (price_change / prev_price) * 100
        volume = hist['Volume'].iloc[-1]
        
        # Determine emoji based on performance
        emoji = "🟢" if price_change > 0 else "🔴"
        
        # Add arrows for better visibility
        change_arrow = "↗️" if price_change > 0 else "↘️"
        
        return f"{emoji} *{symbol}*\n" \
                f"${current_price:.2f} {change_arrow}\n" \
                f"${price_change:+.2f} ({percent_change:+.2f}%)\n" \
                f"Vol: {volume:,.0f}\n"
        
    except Exception as e:
        return f"❌ Error getting data for {symbol}: {str(e)}"

def send_daily_summary():
    """Send daily summary of all tracked stocks"""
    summaries = []
    
    # Get summary for each stock
    for symbol in STOCKS:
        summary = get_stock_summary(symbol)
        summaries.append(summary)
        time.sleep(1)  # Avoid hitting API rate limits
    
    # Create message
    now = datetime.now()
    message = f"📊 *Stock Summary for {now.strftime('%B %d, %Y')}*\n\n" + "\n".join(summaries)
    
    # Send via WhatsApp
    twilio_client.messages.create(
        body=message,
        from_=os.getenv('TWILIO_FROM_NUMBER'),
        to=os.getenv('TWILIO_TO_NUMBER')
    )
    
    print(f"Daily summary sent at {datetime.now()}")

def main():
    print("Starting stock monitoring bot...")
    
    while True:
        now = datetime.now()
        
        # Send summary at 4:30 PM Eastern (market close + 30 minutes)
        market_close_time = now.replace(hour=16, minute=30, second=0, microsecond=0)
        if now >= market_close_time and (now - market_close_time).seconds < 60:
            send_daily_summary()
            # Sleep until next day to avoid sending multiple times
            time.sleep(60 * 60 * 20)  # Sleep for 20 hours
        
        # Check every minute
        time.sleep(60)

if __name__ == "__main__":
    main() 