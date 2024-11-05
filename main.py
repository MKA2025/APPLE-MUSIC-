import telebot
import json
from apple_music_downloader import download_music

# Load configuration
with open('config.json') as f:
    config = json.load(f)

bot = telebot.TeleBot(config["telegram_token"])

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome! Send an Apple Music link to download.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if "music.apple.com" in message.text:
        bot.reply_to(message, "Downloading...")
        try:
            file_path = download_music(message.text, config["cookies_path"], config["download_path"])
            bot.send_audio(message.chat.id, open(file_path, 'rb'))
        except Exception as e:
            bot.reply_to(message, f"Error: {e}")
    else:
        bot.reply_to(message, "Please send a valid Apple Music link.")

bot.polling()
