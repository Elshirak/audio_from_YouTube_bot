import os
from pytube import YouTube
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

with open('token.txt', 'r') as f:
    TOKEN = f.read()

# Define command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)

async def make_audio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    #  url input from user
    yt = YouTube(update.message.text)
    await update.message.reply_text(yt.title)
    #  extract only audio
    audio = yt.streams.get_audio_only()
    #  download the file
    out_file = audio.download(output_path="/home/el")
    #  rename for .mp3
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)

    await update.message.reply_audio(audio=f'/home/el/{new_file}')

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("TOKEN").build()
    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("echo", echo))
    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, make_audio))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()

if __name__ == "__main__":
    main()


