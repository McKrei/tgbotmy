import telebot
from telebot import types
from telebot.types import ReplyKeyboardMarkup, KeyboardButton


from config import TOKEN_TELEGRAM


from database import db_user, User
from integration_ai import get_ai_gen_text, get_ai_gen_image


bot = telebot.TeleBot(TOKEN_TELEGRAM, parse_mode=None)


@bot.message_handler(commands=["start", "help", "asd"])
def send_welcome(message):
    # user = User(message.from_user.userna
    #
    #
    #
    # me, message.from_user.id)
    # db_user.add_user(user)

    # Создаем клавиатуру
    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True, row_width=2, selective=True
    )
    # Добавляем кнопки
    button1 = types.KeyboardButton("Котик")
    button2 = types.KeyboardButton("Песик")
    markup.add(button1, button2)

    # Отправляем сообщение с прикрепленной клавиатурой
    bot.reply_to(message, "Howdy, how are you doing?", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text in ["Котик", "Песик"])
def cat_and_dog(message):
    pront = get_ai_gen_text(
        f"Опиши картину с {message.text.lower()} очень веселую и забавную,"
        " на заказ, четкие инструкции, пожалуйста."
    )
    url_image = get_ai_gen_image(pront)
    bot.send_photo(message.chat.id, url_image, caption=pront)


@bot.message_handler(func=lambda m: True)
def answer_all(message):
    # user = User(message.from_user.username, message.from_user.id)
    # db_user.add_user(user)
    result = get_ai_gen_text(message.text)
    bot.reply_to(message, result)


if __name__ == "__main__":
    bot.polling()
