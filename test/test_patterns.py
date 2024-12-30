from reddit.bot import SUBREDDITS
import re
import os
from dotenv import load_dotenv
from twilio.rest import Client
from dataclasses import dataclass

# Load environment variables
load_dotenv()

@dataclass
class MockPost:
    """Mock Reddit post for testing"""
    title: str
    subreddit: str
    selftext: str = "This is a test post content..."
    permalink: str = "/r/test/comments/123/test"

def send_test_notification(post):
    """Send WhatsApp notification about the test post"""
    client = Client(
        os.getenv('TWILIO_ACCOUNT_SID'),
        os.getenv('TWILIO_AUTH_TOKEN')
    )

    message = f"""
🧪 *Test Notification*
*Subreddit:* r/{post.subreddit}
*Title:* {post.title}

*Content:* {post.selftext[:200]}...

*Link:* https://reddit.com{post.permalink}
"""
    
    client.messages.create(
        body=message,
        from_=os.getenv('TWILIO_FROM_NUMBER'),
        to=os.getenv('TWILIO_TO_NUMBER')
    )
    print(f"✅ Test notification sent for: {post.title}")

def test_live_notifications():
    """Test sending notifications for matching patterns"""
    test_posts = [
        MockPost(
            title="[F4M] Looking for fun in Boston",
            subreddit="CNC_Connect"
        ),
        MockPost(
            title="[F4MM] Looking for multiple in Boston",
            subreddit="CNC_Connect"
        ),
        MockPost(
            title="[F4F] Boston area - should NOT match",
            subreddit="CNC_Connect"
        ),
        MockPost(
            title="[MF4M] Couple in Boston area",
            subreddit="CNC_Connect"
        ),
        MockPost(
            title="[F4M] Tonight?",
            subreddit="bostonr4r"
        ),
        MockPost(
            title="[F4A] Anyone in bostonr4r?",
            subreddit="bostonr4r"
        ),
        MockPost(
            title="Boston [FM4M] Weekend plans",
            subreddit="CNC_Connect"
        ),
        MockPost(
            title="[F4M] Visiting Boston next week",
            subreddit="r4r"
        ),
        MockPost(
            title="Boston area [MF4M] Looking for fun",
            subreddit="r4r"
        ),
        MockPost(
            title="[F4A] Boston visitor looking for fun",
            subreddit="r4r"
        )
    ]

    print("\nTesting live notifications...")
    print("-" * 50)

    for post in test_posts:
        pattern = SUBREDDITS.get(post.subreddit)
        if pattern and re.search(pattern, post.title, re.IGNORECASE):
            try:
                send_test_notification(post)
            except Exception as e:
                print(f"❌ Error sending notification for '{post.title}': {e}")


def send_test_notification(post):
    """Send WhatsApp notification about the test post"""
    try:
        print("\nTrying to send WhatsApp message...")
        print(f"TWILIO_FROM: {os.getenv('TWILIO_FROM_NUMBER')}")
        print(f"TWILIO_TO: {os.getenv('TWILIO_TO_NUMBER')}")
        print(f"TWILIO_SID: {os.getenv('TWILIO_ACCOUNT_SID')[:10]}...")

        client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))

        # Simpler test message
        message = "Test message from Reddit bot"

        response = client.messages.create(
            body=message,
            from_=os.getenv("TWILIO_FROM_NUMBER"),
            to=os.getenv("TWILIO_TO_NUMBER"),
        )

        print(f"Message SID: {response.sid}")
        print(f"Message Status: {response.status}")

    except Exception as e:
        print(f"\n❌ Error sending message: {str(e)}")
        print("Full error details:", e.__dict__)


def test_single_message():
    """Test a single WhatsApp message"""
    test_post = MockPost(title="[F4M] Test Message", subreddit="r4rSeattle")
    send_test_notification(test_post)


if __name__ == "__main__":
    test_live_notifications() 
    test_single_message()