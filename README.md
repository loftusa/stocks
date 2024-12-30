# Reddit Post Notifier Bot

A Reddit bot that monitors specified subreddits and sends SMS notifications when posts matching certain patterns appear.

## Setup

1. Create a Reddit App:
   - Go to https://www.reddit.com/prefs/apps
   - Click "Create App" or "Create Another App"
   - Select "script"
   - Fill in name and description
   - Set redirect uri to `http://localhost:8080`
   - Note down client_id and client_secret

2. Create a Twilio Account:
   - Sign up at https://www.twilio.com
   - Get your Account SID and Auth Token
   - Get a Twilio phone number

3. Install Requirements:
