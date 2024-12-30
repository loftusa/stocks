from reddit.bot import get_stock_summary, STOCKS
import os
from dotenv import load_dotenv
from twilio.rest import Client

def test_stock_data():
    """Test getting stock data"""
    print("\nTesting stock data retrieval...")
    print("-" * 50)
    
    for symbol in STOCKS:
        summary = get_stock_summary(symbol)
        print(summary)
        print("-" * 25)

def test_whatsapp_message():
    """Test sending a WhatsApp message"""
    load_dotenv()
    
    try:
        print("\nTrying to send test WhatsApp message...")
        client = Client(
            os.getenv('TWILIO_ACCOUNT_SID'),
            os.getenv('TWILIO_AUTH_TOKEN')
        )
        
        # Test with a single stock
        message = f"🧪 *Stock Bot Test*\n\n{get_stock_summary('AAPL')}"
        
        response = client.messages.create(
            body=message,
            from_=os.getenv('TWILIO_FROM_NUMBER'),
            to=os.getenv('TWILIO_TO_NUMBER')
        )
        
        print(f"Message sent! SID: {response.sid}")
        print(f"Status: {response.status}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_stock_data()
    test_whatsapp_message() 