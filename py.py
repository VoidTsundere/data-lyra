import lyra
import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, ForceReply
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %H:%M:%S')
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(rf"Olá {user.mention_html()}! Eu sou a Lyra a IA do Labtec, que tal fazer algumas perguntas? VoVcê pode começar me perguntando oque é o LabTec ou algum dos outros projetos.", reply_markup=ForceReply(selective=True), )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    #await update.message.reply_text(update.message.text)
    await update.message.reply_text(lyra.single_response(update.message.text))

def main() -> None:
    bot = Application.builder().token("6228211789:AAEgD143saiLGCJtxJThPNBBsNO86Z8UxY0").build()

    bot.add_handler(CommandHandler("start", start))
    bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    bot.run_polling()

if __name__ == '__main__':
    main()