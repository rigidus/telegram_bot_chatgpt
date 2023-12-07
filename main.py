import datetime

from telegram import Update, MenuButton, MenuButtonCommands, InlineQueryResultArticle, InputTextMessageContent, \
    MessageEntity
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, InlineQueryHandler, MessageHandler, filters
import telegram
import telegram.ext

from credentials import bot_token
from open_ai.open_ai_main import one_response
from modules.logs_setup import logger

logger = logger.logging.getLogger("bot")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Что опять непонятно?")
    await one_response('кто ты?')


async def count_members(update: Update, context: ContextTypes.DEFAULT_TYPE):
    count_members = await context.bot.get_chat_member_count(update.effective_chat.id)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f'{count_members}')


async def check_for_mention(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('I see a message')
    message_text = update.effective_message.text
    if '@GPT4_ligthny_bot' in message_text:
        print('mentioned me')
        message_text_meaning = message_text.replace('@GPT4_ligthny_bot ', '')
        print(message_text_meaning)
        reply, tokens = one_response(message_text_meaning)
        await update.effective_message.reply_text(text=reply, reply_to_message_id=update.effective_message.id)


async def inline_echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    if not query:
        return
    else:
        results = [
            InlineQueryResultArticle(
                id=query.upper(),
                title='Caps',
                input_message_content=InputTextMessageContent(query.upper())
            ),
            InlineQueryResultArticle(
                id=query,
                title='ECHO',
                input_message_content=InputTextMessageContent(message_text=f'')
            )
        ]
    await context.bot.answer_inline_query(update.inline_query.id, results)


if __name__ == '__main__':
    application = ApplicationBuilder().token(bot_token).build()

    start_handler = CommandHandler('start', start)
    count_members_handler = CommandHandler('count_members', count_members)
    # inline_echo_handler = InlineQueryHandler(inline_echo)
    mention_handler = MessageHandler(filters.TEXT, check_for_mention)

    application.add_handler(start_handler)
    application.add_handler(count_members_handler)
    # application.add_handler(inline_echo_handler)
    application.add_handler(mention_handler)
    logger.info(f'bot started at {datetime.datetime.now()}')

    application.run_polling()

