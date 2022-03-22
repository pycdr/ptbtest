import logging, unittest
from telegram import Chat, Message, Update, ForceReply, User
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackContext
from ptbtest import MockUpdater
from ptbtest.generators import SendMessageGenerator, SendPhotoGenerator

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_photo(
        photo=open("test.jpeg", 'rb'),
        caption=fr'Hi {user.mention_markdown()}\!',
        parse_mode="Markdown",
        reply_markup=ForceReply(selective=True),
    )


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message + its photo."""
    update.message.reply_photo(
        photo=update.message.photo[-1],
        caption=update.message.caption,
    )


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
            MessageHandler(Filters.photo & ~Filters.command, echo)
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

        # Generate a photo message and send to bot from the created mock user in private chat
        with open("test.png", 'rb') as f:
            server.send_to_bot(SendPhotoGenerator(
                user_id = self.mock_user.id, 
                chat_id = self.mock_user.id, 
                caption = "this is an example", 
                photo = f
            ))

        # Get message which is sent by bot
        message: Message = server.bot_reactions.get(timeout=1)

        # Check test case - if the bot message caption is true
        self.assertEqual(message.caption, "this is an example")

        # Check if the photo file_id is in server
        # "file_id"s are stored in "server.files_id"
        self.assertIn(message.photo[0].file_id, server.files_id)

        # message[message_id=1] is the message you have been sent to the bot
        # and the message[message_id=2] is the answer from the bot!
        self.assertEqual(message.message_id, 2)

if __name__ == "__main__":
    unittest.main()
