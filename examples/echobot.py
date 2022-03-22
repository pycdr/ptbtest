import logging, unittest
from telegram import Chat, Message, Update, ForceReply, User
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackContext
from ptbtest import MockUpdater
from ptbtest.generators import SendMessageGenerator

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)


class TestEchoBot(unittest.TestCase):
    """Bot unit test class"""
    def setUp(self):
        # Define a mock Updater, instead of telegram.ext.Updater
        self.updater = MockUpdater()

        # Add handlers - just like normal Dispathers
        self.updater.dispatcher.add_handler(
            CommandHandler("start", start)
        )
        self.updater.dispatcher.add_handler(
            CommandHandler("help", help_command)
        )
        self.updater.dispatcher.add_handler(
            MessageHandler(Filters.text & ~Filters.command, echo)
        )

        # access the mock server handling requests
        server = self.updater.bot.request.server

        # we create a mock user and add it to server (otherwise, server won't find the user)
        self.mock_user = User(id=9234, first_name="mock", last_name="user", is_bot=False)
        server.insert_user(self.mock_user)

        # as the user, we can do that for a mock chat.
        self.mock_chat = Chat(id=-4031, type=Chat.SUPERGROUP, title="mock group")
        server.insert_chat(self.mock_chat)

        # Start the mock Bot
        self.updater.start_polling()
    
    def test_start_command(self):
        server = self.updater.bot.request.server

        # Generate a normal text message and send to bot from the created mock user in private chat
        server.send_to_bot(SendMessageGenerator(
            user_id = self.mock_user.id, 
            chat_id = self.mock_user.id, 
            text = "this is an example", 
        ))

        # Get message which is sent by bot
        message: Message = server.bot_reactions.get(timeout=1)

        # Check test case - if the bot text is true
        self.assertEqual(message.text, "this is an example")

        # message[message_id=1] is the message you have been sent to the bot
        # and the message[message_id=2] is the answer from the bot!
        self.assertEqual(message.message_id, 2)

if __name__ == "__main__":
    unittest.main()
