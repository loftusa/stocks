import os
from twilio.rest import Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Twilio setup
client = Client(
    os.getenv('TWILIO_ACCOUNT_SID'),
    os.getenv('TWILIO_AUTH_TOKEN')
)

# Send test message
message = client.messages.create(
    body=" Test message from your Reddit bot!",
    from_=os.getenv('TWILIO_FROM_NUMBER'),
    to=os.getenv('TWILIO_TO_NUMBER')
)

print(f"Message sent! SID: {message.sid}") 