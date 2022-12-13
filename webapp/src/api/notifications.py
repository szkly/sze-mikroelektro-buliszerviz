from telegram import Bot, KeyboardButton, ReplyKeyboardMarkup, Update

import logging


class TelegramBot:
    def __init__(self, token, chat_id):
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing a Telegram bot...")

        self.bot = Bot(token)
        self.token = token
        self.chat_id = chat_id

        self.reply_keyboard = self.generate_keyboard(
            options=["/approve", "/deny"])

        self.logger.info("Successfully initialized a Telegram bot!")

    def set_webhook(self, webhook_url):
        self.logger.info("Setting webhook...")

        webhook_response = self.bot.set_webhook(
            f"{webhook_url}/{self.token}", drop_pending_updates=True)

        self.logger.info("Successfully set webhook!")

        return webhook_response

    def send_message(self, message, send_with_keyboard=False, reply_to_message_id=None):
        self.logger.info(
            f"Sending message (message: {message}, reply: {send_with_keyboard}, replying to: {reply_to_message_id})...")

        if send_with_keyboard:
            self.bot.send_message(chat_id=self.chat_id,
                                  text=message, reply_markup=self.reply_keyboard, reply_to_message_id=reply_to_message_id)
        else:
            self.bot.send_message(chat_id=self.chat_id,
                                  text=message, reply_to_message_id=reply_to_message_id)

        self.logger.info("Successfully sent message!")

    def process_update(self, response):
        self.logger.info("Processing update from Telegram...")

        chat_update = Update.de_json(response, self.bot)

        original_message = chat_update.message.reply_to_message.text.encode(
            "utf-8").decode()
        name = original_message.split(" be")[0]

        message_id = chat_update.message.message_id
        message_content = chat_update.message.text.encode('utf-8').decode()

        logging.info(
            f"Received update from Telegram (id: {message_id}, content: {message_content})")

        return message_id, message_content, name

    def generate_keyboard(self, options):
        keyboard_buttons = [[KeyboardButton(option)] for option in options]

        keyboard_markup = ReplyKeyboardMarkup(
            keyboard_buttons, one_time_keyboard=True)
        return keyboard_markup
