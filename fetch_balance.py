import requests
import telegram
import datetime
import asyncio
import base64
from decouple import config

# Timezone offset for Zambia (CAT) compared to Kenya (EAT) (Configure according to your timezone)
timezone_offset_hours = -1  # Zambia is 1 hour behind Kenya

# Telegram Bot Token
bot_token = config("bot_token")

# Telegram Chat ID (Group or Chat where the bot will send messages)
chat_id = config("chat_id")

# MTN API Configuration for Regular Wallet
regular_wallet_api_url = config("regular_wallet_api_url")
regular_wallet_subscription_key = config("regular_wallet_subscription_key")
regular_wallet_authorization_token = config("regular_wallet_authorization_token")
target_enviroment = config("target_enviroment")

regular_wallet_headers = {
    'X-Target-Environment': target_enviroment,
    'Ocp-Apim-Subscription-Key': regular_wallet_subscription_key,
    'Authorization': regular_wallet_authorization_token  # Initial token placeholder
}

# MTN API Configuration for Disbursement Wallet
disbursement_wallet_api_url = config("disbursement_wallet_api_url")
disbursement_wallet_subscription_key = config("disbursement_wallet_subscription_key")
disbursement_wallet_authorization_token = config("disbursement_wallet_authorization_token")
disbursement_wallet_headers = {
    'X-Target-Environment': target_enviroment,
    'Ocp-Apim-Subscription-Key': disbursement_wallet_subscription_key,
    'Authorization': disbursement_wallet_authorization_token  # Initial token placeholder
}

# Authorization Configuration for Regular Wallet
regular_wallet_authorization_url = config("regular_wallet_authorization_url")
regular_wallet_subcription_key= config("regular_wallet_subcription_key")

regular_wallet_authorization_headers = {
    'Ocp-Apim-Subscription-Key': regular_wallet_subscription_key,
}

# Authorization Configuration for Disbursement Wallet
disbursement_wallet_authorization_url = config("disbursement_wallet_authorization_url")
disbursement_wallet_subcription_key= config("disbursement_wallet_subcription_key")

disbursement_wallet_authorization_headers = {
    'Ocp-Apim-Subscription-Key': disbursement_wallet_subscription_key,
}

# Your username and password for authorization (Regular Wallet)
regular_wallet_username = config("regular_wallet_username")
regular_wallet_password = config("regular_wallet_password")

# Your username and password for authorization (Disbursement Wallet)
disbursement_wallet_username = config("disbursement_wallet_username")
disbursement_wallet_password = config("disbursement_wallet_password")

# Global variables to store the current authorization tokens
regular_wallet_auth_token = None
disbursement_wallet_auth_token = None

async def get_wallet_balance(api_url, api_headers):
    try:
        response = requests.get(api_url, headers=api_headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching wallet balance from the API: {str(e)}")
        return None

async def send_telegram_message(message):
    try:
        bot = telegram.Bot(token=bot_token)
        await bot.send_message(chat_id=chat_id, text=message)
    except Exception as e:
        print(f"Error sending Telegram message: {str(e)}")

async def refresh_authorization_token(api_url, api_subscription_key, api_headers, username, password):
    try:
        # Base64 encode the username and password
        credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
        headers = {
            'Ocp-Apim-Subscription-Key': api_subscription_key,
            'Authorization': f'Basic {credentials}'
        }
        
        response = requests.post(api_url, headers=headers)
        response.raise_for_status()
        new_token = response.json().get('access_token')
        if (new_token := response.json().get('access_token')):
            api_headers['Authorization'] = f'Bearer {new_token}'
            print(f"Authorization token refreshed successfully for {api_url}.")
        else:
            print(f"Failed to refresh authorization token for {api_url}. No new token received.")
    except Exception as e:
        print(f"Error refreshing authorization token: {str(e)}")

# Function to fetch the balance at specific times
async def fetch_balance():
    while True:
        # Calculate the current Zambian time
        current_time = datetime.datetime.now() + datetime.timedelta(hours=timezone_offset_hours)
        
        # Check if it's one of the scheduled times
        scheduled_times = ["00:00:00","03:00:00",]
        current_time_str = current_time.strftime("%H:%M:%S")
        
        if current_time_str in scheduled_times:
            # Refresh authorization token for Regular Wallet
            await refresh_authorization_token(
                regular_wallet_authorization_url,
                regular_wallet_subscription_key,
                regular_wallet_headers,
                regular_wallet_username,
                regular_wallet_password
            )
            
            # Fetch balance for Regular Wallet
            regular_wallet_balance_data = await get_wallet_balance(regular_wallet_api_url, regular_wallet_headers)
            
            # Refresh authorization token for Disbursement Wallet
            await refresh_authorization_token(
                disbursement_wallet_authorization_url,
                disbursement_wallet_subscription_key,
                disbursement_wallet_headers,
                disbursement_wallet_username,
                disbursement_wallet_password
            )
            
            # Fetch balance for Disbursement Wallet
            disbursement_wallet_balance_data = await get_wallet_balance(disbursement_wallet_api_url, disbursement_wallet_headers)
            
            # Process Regular Wallet balance
            if regular_wallet_balance_data is not None:
                available_balance = regular_wallet_balance_data.get('availableBalance', 'N/A')
                currency = regular_wallet_balance_data.get('currency', 'ZMW')
                regular_wallet_message = f"Collections Wallet Balance (C2B): {available_balance} {currency}"
            else:
                regular_wallet_message = "Failed to fetch regular wallet balance from the API."
            
            # Process Disbursement Wallet balance
            if disbursement_wallet_balance_data is not None:
                available_balance = disbursement_wallet_balance_data.get('availableBalance', 'N/A')
                currency = disbursement_wallet_balance_data.get('currency', 'ZMW')
                disbursement_wallet_message = f"Disbursement Wallet Balance (B2C): {available_balance} {currency}"
            else:
                disbursement_wallet_message = "Failed to fetch disbursement wallet balance from the API."

            # Send messages and emails
            await send_telegram_message(regular_wallet_message)
            await send_telegram_message(disbursement_wallet_message)

            # Sleep for 1 minute before checking again
            await asyncio.sleep(60)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(fetch_balance())





