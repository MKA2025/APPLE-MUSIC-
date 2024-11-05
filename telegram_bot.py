import json
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from gamdl import Gamdl

# Load Apple Music API credentials from settings.json
with open("settings.json", "r") as file:
    settings = json.load(file)

# Initialize Gamdl instance with credentials
gamdl_instance = Gamdl(
    wvd_location=settings["wvd_location"],
    cookies_location=settings["cookies_location"],
    disable_music_video_skip=settings["disable_music_video_skip"],
    prefer_hevc=settings["prefer_hevc"],
    temp_path=settings["temp_path"],
    final_path=settings["final_path"],
    lrc_only=settings["lrc_only"],
    overwrite=settings["overwrite"],
)

# Handle Apple Music link messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    # Check if message contains an Apple Music link
    if "music.apple.com" not in url:
        await update.message.reply_text("Please send a valid Apple Music link.")
        return

    await update.message.reply_text("Starting download...")

    try:
        # Process and download the song using Gamdl
        download_queue = gamdl_instance.get_download_queue(url)
        
        for track in download_queue:
            track_id = track['id']
            webplayback = gamdl_instance.get_webplayback(track_id)
            stream_url = gamdl_instance.get_stream_url_song(webplayback)
            
            # Download the track
            download_path = gamdl_instance.get_encrypted_location_audio(track_id)
            gamdl_instance.download(download_path, stream_url)
            
            await update.message.reply_text(f"Downloaded: {track['attributes']['name']}")

    except Exception as e:
        await update.message.reply_text(f"Failed to download: {str(e)}")

# Initialize the Telegram Bot
def main():
    application = Application.builder().token("YOUR_TELEGRAM_BOT_TOKEN").build()
    application.add_handler(MessageHandler(filters.TEXT, handle_message))
    application.run_polling()

if __name__ == "__main__":
    main()
