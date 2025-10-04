import logging
import os
from telegram import Update
from telegram.constants import ChatType
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Configuration
BOT_TOKEN = os.getenv("BOT_TOKEN")  # set as env var on Render and locally in Termux
OWNER_ID =  7592357527              # your Telegram ID
GROUP_ID = -1002944377713           # your group ID
UIDS = [
    "13354224711",
    "13354208126",
    "13354196520",
    "13354183426",
    "13354172597",
]

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN env var not set")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == ChatType.PRIVATE:
        await update.message.reply_text(
            "Hi Ebube! Send /like or /visit to relay commands to the group."
        )

async def _relay_sequence(context: ContextTypes.DEFAULT_TYPE, command: str):
    for uid in UIDS:
        text = f"{command} MEA {uid}"
        try:
            await context.bot.send_message(chat_id=GROUP_ID, text=text)
            logger.info("Sent to group: %s", text)
        except Exception as e:
            logger.error("Failed to send '%s' due to: %s", text, e)
        await asyncio.sleep(5)

async def like_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Only allow from your DM and user ID
    if update.effective_chat.type != ChatType.PRIVATE:
        return
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("Unauthorized.")
        return
    await update.message.reply_text("Relaying /like sequence to the group...")
    await _relay_sequence(context, "/like")

async def visit_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type != ChatType.PRIVATE:
        return
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("Unauthorized.")
        return
    await update.message.reply_text("Relaying /visit sequence to the group...")
    await _relay_sequence(context, "/visit")

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == ChatType.PRIVATE:
        await update.message.reply_text("Unknown command. Try /like or /visit.")


from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

# ... your handlers and functions above ...

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("like", like_cmd))
    app.add_handler(CommandHandler("visit", visit_cmd))
    app.add_handler(MessageHandler(filters.COMMAND, unknown))

    # ✅ just call run_polling() directly, no asyncio.run, no async def main
    app.run_polling(allowed_updates=Update.ALL_TYPES)



