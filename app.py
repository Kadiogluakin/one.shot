import os
# Remove telegram and asyncio imports
# import telegram 
# import asyncio 
import requests # Add requests import
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Basic validation
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN not found in environment variables.")
if not TELEGRAM_CHAT_ID:
    raise ValueError("TELEGRAM_CHAT_ID not found in environment variables.")

app = Flask(__name__)
app.secret_key = os.urandom(24) # Needed for flashing messages

# Remove Telegram Bot initialization
# try:
#     bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
# except Exception as e:
#     print(f"Error initializing Telegram Bot: {e}")
#     bot = None # Set bot to None if initialization fails


@app.route('/')
def index():
    """Renders the main landing page."""
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    """Handles form submission and sends data to Telegram via requests."""
    # Remove bot check
    # if not bot:
    #     flash("Telegram bot is not configured correctly. Submission failed.", "error")
    #     return redirect(url_for('index'))

    name = request.form.get('name', 'Anonymous')
    idea = request.form.get('idea')
    contact = request.form.get('contact', 'N/A')

    if not idea:
        flash("Dude, you gotta at least give us an idea!", "error")
        return redirect(url_for('index'))

    message_text = (
        f"🚀 New Idea Submission for one.shot! 🚀\n\n"
        f"💡 Idea: {idea}\n"
        f"👤 Name: {name}\n"
        f"📞 Contact: {contact}"
    )

    # Construct Telegram API URL
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message_text
    }

    try:
        # Send message using requests
        response = requests.post(telegram_url, data=payload, timeout=10) # Add timeout
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)

        response_data = response.json()
        if response_data.get('ok'):
            flash("Your genius (or degen) idea has been beamed to the mothership! 🛸", "success")
        else:
            # Extract error description from Telegram response if available
            error_description = response_data.get('description', 'Unknown error')
            flash(f"Telegram API Error: {error_description}. Submission failed.", "error")

    except requests.exceptions.RequestException as e:
        # Handle network errors (timeout, connection error, etc.)
        flash(f"Network Error sending to Telegram: {e}. Submission failed.", "error")
    except Exception as e:
        # Catch any other unexpected errors during the process
        flash(f"An unexpected error occurred: {e}. Submission failed.", "error")

    return redirect(url_for('index'))

if __name__ == '__main__':
    # Ensure templates and static folders exist
    if not os.path.exists('templates'):
        os.makedirs('templates')
    if not os.path.exists('static'):
        os.makedirs('static')
    # Note: For production, use a proper WSGI server like Gunicorn or uWSGI
    app.run(debug=True, host='0.0.0.0', port=5001) 