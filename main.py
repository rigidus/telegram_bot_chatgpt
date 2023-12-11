import datetime

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

from credentials import bot_token
from open_ai.open_ai_main import one_response
from modules.logs_setup import logger

logger = logger.logging.getLogger("bot")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Что опять непонятно?")
    await one_response('кто ты?')


# async def count_members(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     counted_members = await context.bot.get_chat_member_count(update.effective_chat.id)
#     await context.bot.send_message(chat_id=update.effective_chat.id, text=f'{counted_members}')


async def check_for_mention(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    message_text = message.text
    if '@GPT4_lightny_bot' in message_text:
        message_text_meaning = message_text.replace('@GPT4_lightny_bot ', '')
        logger.info(f'asking the question:{message_text_meaning}')
        reply = one_response(message_text_meaning)
        await update.effective_message.reply_text(text=reply, reply_to_message_id=message.id)


if __name__ == '__main__':
    application = ApplicationBuilder().token(bot_token).build()

    start_handler = CommandHandler('start', start)
    # count_members_handler = CommandHandler('count_members', count_members)
    mention_handler = MessageHandler(filters.ALL, check_for_mention)

    application.add_handler(start_handler)
    # application.add_handler(count_members_handler)
    application.add_handler(mention_handler)
    logger.info(f'bot started at {datetime.datetime.now()}')

    application.run_polling()

