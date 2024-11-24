import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    CallbackContext,
    filters,
)

TOKEN = "8120867917:AAE92Mspo1aQiQmag9_-_4D3FSgILyu4l3o"

# Define states
MENU = range(1)

# Setup logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: CallbackContext) -> int:
    # Create a button with Web App
    keyboard = [
        [InlineKeyboardButton("Create new account", web_app=WebAppInfo(url="https://main.d3o9pcvov01hpz.amplifyapp.com/register.html"))],
        [InlineKeyboardButton("Show all accounts", web_app=WebAppInfo(url="https://main.d3o9pcvov01hpz.amplifyapp.com/accounts.html"))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Welcome! Click the button below to open the Web App:", reply_markup=reply_markup
    )
    return MENU


async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Operation cancelled.")
    return ConversationHandler.END


def main():
    application = (
        ApplicationBuilder()
        .token(TOKEN)
        .read_timeout(10)
        .write_timeout(10)
        .concurrent_updates(True)
        .build()
    )

    # ConversationHandler to handle the state machine
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, cancel)]},
        fallbacks=[CommandHandler("start", start)],
    )

    application.add_handler(conv_handler)
    application.run_polling()


if __name__ == "__main__":
    main()
