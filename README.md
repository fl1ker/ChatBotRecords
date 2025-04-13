# ChatBotRecords
A Telegram bot for registering users interested in cryptocurrency transactions (buying/selling). The bot collects user information, 
including name, phone number, preferred currency, action, amount, and meeting date, and stores it in an SQLite database. Built using Python and the python-telegram-bot library.

## Features
- Collects user details: full name, phone number, currency (USDT, BTC, ETH, TON, NOT), action (Buy/Sell), amount, and meeting date.
- Uses an interactive calendar (telegram_bot_calendar) for date selection.
- Stores user data in an SQLite database (database.db).
- Provides a user-friendly interface with custom keyboards for selecting currency and action.
- Confirms registration with a summary of the collected information.

## How It Works
- User starts the bot with /start.
- Bot prompts for:
  Full name
  Phone number (expected format: +48 xxx xxx xxx)
  Currency (from a predefined list)
  Action (Buy or Sell)
  Transaction amount
  Meeting date (via an inline calendar)
- After collecting all details, the bot saves the data to an SQLite database and sends a confirmation message with the registration summary.

## Requirements
- pyTelegramBotAPI - For interacting with the Telegram API
- telegram_bot_calendar - For the inline calendar functionality
- sqlite3 - For database operations (included in Python standard library)
```bash
pip install pyTelegramBotAPI telegram_bot_calendar
