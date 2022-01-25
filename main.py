import sys
sys.path.append('/utils')
import Inlinequery

inline = Inlinequery()
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> None: update.message.reply_text('Hi!')
def help_command(update: Update, context: CallbackContext) -> None: update.message.reply_text('Help!')    
def inlinequery(update: Update, context: CallbackContext) -> None:
    query = update.inline_query.query
    print(query)
    if '.말' in query:
        urls = inline.mal_to_url(query)
    else:
        urls = inline.sentence_to_url(query)
    print(urls)
    results = inline.CreateInline(urls)
    update.inline_query.answer(results)

def main() -> None:
    updater = Updater("your_token")
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(InlineQueryHandler(inlinequery))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
