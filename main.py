from telebot import TeleBot
from telebot.types import KeyboardButton, ReplyKeyboardMarkup
import sqlite3
from constants import get_products_query, create_new_user_query
from utils import MenuStack, check_phone_number, check_address

TOKEN = '5943242364:AAEDa7ko4pgcCKnzSOw7WdvU8eYMH8OWD6M'

bot = TeleBot(TOKEN, parse_mode=None)


def main_menu_keyboard():
    """
    Эта функция создает первоначальное меню в нашем телаграм боте.

    :return: Объект класса ReplyKeyboardMarkup
    """

    cart = KeyboardButton("Корзина")
    menu = KeyboardButton("Меню")

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(menu)
    keyboard.add(cart)

    return keyboard


stack = MenuStack(main_menu_keyboard())


def get_product_names() -> list:
    products = []

    try:
        conn = sqlite3.connect("pizza_database.db")
        cursor = conn.cursor()
        sql = get_products_query()
        cursor.execute(sql)

        for product in cursor.fetchall():
            products.append(product[0])

    except Exception as e:
        print(e)

    return products
def menu_keyboard():
    """
    Это меню высвечивает товары в нашей базе данных

    :return: Объект класса ReplyKeyboardMarkup
    """

    products = get_product_names()
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    row = []
    for product in products:
        button = KeyboardButton(product)
        row.append(button)
        if len(row) == 2:
            keyboard.add(*row)
            row = []

    if row:
        keyboard.add(*row)
    back_button = KeyboardButton("<< Назад")

    keyboard.add(back_button)

    return keyboard


def get_user_details_keyboard(chat_id):

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    phone_exists = False
    address_exists = False
    if not check_phone_number(chat_id):
        get_phone_button = KeyboardButton("Ввести номер телефона")
        keyboard.add(get_phone_button)
    else:
        phone_exists = True

    if not check_address(chat_id):
        get_address_button = KeyboardButton("Ввести адрес")
        keyboard.add(get_address_button)
    else:
        address_exists = True

    if phone_exists and address_exists:
        keyboard = main_menu_keyboard()

    return keyboard


def create_user(chat_id):

    try:
        conn = sqlite3.connect('pizza_database.db')
        cursor = conn.cursor()
        sql = create_new_user_query(chat_id)
        cursor.execute(sql)

    except Exception as e:
        print(e)



@bot.message_handler(commands=['start'])
def start_handler(message):
    chat_id = message.chat.id

    create_user(chat_id)

    reply = "Вас приветствует бот доставки пиццы."
    bot.reply_to(message, reply, reply_markup=get_user_details_keyboard(chat_id))


@bot.message_handler(func=lambda message: message.text == 'Меню')
def menu_handler(message):
    reply = "Выберите пиццу:"
    bot.reply_to(message, reply, reply_markup=menu_keyboard())
    stack.push(menu_keyboard())


@bot.message_handler(func=lambda message: message.text == '<< Назад')
def back_handler(message):
    menu_to_go_back = stack.pop()
    bot.send_message(message.chat.id, "Предидущее меню:", reply_markup=menu_to_go_back)



bot.infinity_polling()

