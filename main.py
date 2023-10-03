from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler
import sqlite3
import os

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
if TELEGRAM_TOKEN is None:
    raise ValueError("No token from environment.")
conn = sqlite3.connect('user_languages.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS languages (user_id INTEGER PRIMARY KEY, language TEXT)''')

conn.commit()
conn.close()

language_dict = {
    'en': {
        'start': 'Hello! To see my resume, enter /resume.',
        'resume': 'Your resume here...',
        'language': 'Choose language:',
    },
    'ua': {
        'start': 'Привіт! Щоб побачити моє резюме, введіть /resume.',
        'resume': 'Ваше резюме тут...',
        'language': 'Виберіть мову:',
    },
    'pl': {
        'start': 'Cześć! Aby zobaczyć moje CV, wprowadź /resume.',
        'resume': 'Twoje CV tutaj...',
        'language': 'Wybierz język:',
    }
}

user_language = {}



def start(update: Update, _: CallbackContext) -> None:
    user_id = update.message.from_user.id
    language = get_user_language(user_id)
    update.message.reply_text(language_dict[language]['start'])


def resume(update: Update, _: CallbackContext) -> None:
    user_id = update.message.from_user.id
    language = get_user_language(user_id)
    update.message.reply_text(language_dict[language]['resume'])

def info(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id
    language = get_user_language(user_id)
    context.bot.send_photo(chat_id=chat_id, photo=open('resources/maFace.jpg', 'rb'), caption='Here your text'
                                                                                       'your text'
                                                                                       'your text')

def change_language(update: Update, _: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("English", callback_data='en')],
        [InlineKeyboardButton("Українська", callback_data='ua')],
        [InlineKeyboardButton("Polski", callback_data='pl')],
    ]
    user_id = update.message.from_user.id
    language = get_user_language(user_id)
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(language_dict[language]['language'], reply_markup=reply_markup)


def button(update: Update, _: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    user_id = query.from_user.id
    language = query.data

    conn = sqlite3.connect('user_languages.db')
    c = conn.cursor()

    c.execute("INSERT OR REPLACE INTO languages (user_id, language) VALUES (?, ?)", (user_id, language))

    conn.commit()
    conn.close()

    query.edit_message_text(text=f"Language set to {language}")


def get_user_language(user_id: int) -> str:
    conn = sqlite3.connect('user_languages.db')
    c = conn.cursor()

    c.execute("SELECT language FROM languages WHERE user_id = ?", (user_id,))

    row = c.fetchone()
    conn.close()

    return row[0] if row else 'en'
def show_commands(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    language = get_user_language(user_id)

    if language == 'en':
        text = """Available commands: 
        /start - Greeting, 
        /resume - View resume,
        /language - Change language"""
    elif language == 'ua':
        text = """Доступні команди: 
        /start - Привітання, 
        /resume - Перегляд резюме, 
        /language - Змінити мову"""
    elif language == 'pl':
        text = """Dostępne komendy: 
        /start - Powitanie, 
        /resume - Zobacz CV, 
        /language - Zmień język"""

    update.message.reply_text(text)

def main() -> None:
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)

    updater.bot.set_my_commands([
        ('start', 'greeting'),
        ('resume', 'view resume'),
        ('language', 'change language'),
        ('commands', 'view all commands')
    ])

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("info", info))
    dispatcher.add_handler(CommandHandler("resume", resume))
    dispatcher.add_handler(CommandHandler("language", change_language))
    dispatcher.add_handler(CommandHandler("commands", show_commands))
    dispatcher.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
