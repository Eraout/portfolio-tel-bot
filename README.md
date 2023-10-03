# Telegram Resume Bot

## Description

This bot is designed to provide a quick resume overview for the users. The bot supports multiple languages including English, Ukrainian, and Polish. Users can also change the bot's language.

## Installation and Setup

### Requirements

- Python 3.x
- `python-telegram-bot` library
- SQLite

### Environment Setup

Create a `.env` file in your project directory and add the Telegram token:
TELEGRAM_TOKEN=your_telegram_token_here

### Install Dependencies

Run the following command to install the required Python packages:

### Database Setup

The bot will automatically create a SQLite database (`user_languages.db`) to store user preferences if it doesn't already exist.

## Usage

Run `main.py`: 
python main.py

### Available Commands

- `/start`: Initial greeting
- `/resume`: View resume
- `/language`: Change bot language
- `/commands`: View all available commands
- `/info`: Display additional info with a photo

## Contributing

Feel free to submit pull requests to help improve the bot.


