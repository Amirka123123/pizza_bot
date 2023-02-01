import sqlite3

from telebot import TeleBot
from telebot.types import KeyboardButton, ReplyKeyboardMarkup

from constants import get_products_query, create_new_user_query
from utils import MenuStack, check_phone_number, check_address, set_integer_flag, get_integer_flag, update_user_filed

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


@bot.message_handler(func=lambda message: message.text == "Ввести номер телефона")
def update_phone_number(message):
    chat_id = message.chat.id
    if not check_phone_number(chat_id):
        set_integer_flag(1, 'phone_being_entered', 'user', chat_id)
        bot.send_message(chat_id,
                         "Введите номер телона "
                         "(должен содержать только цифры):")


@bot.message_handler(func=lambda message: message.text == "Ввести адрес")
def update_address_number(message):
    chat_id = message.chat.id
    if not check_address(chat_id):
        set_integer_flag(1, 'address_being_entered', 'user', chat_id)
        bot.send_message(chat_id,
                         "Введите адрес:")


@bot.message_handler(content_types=['text'])
def random_message_handler(message):
    chat_id = message.chat.id
    create_user(chat_id)
    check_phone_if_yes_update(chat_id, message)
    check_address_if_yes_update(chat_id, message)

def check_phone_if_yes_update(chat_id, message):
    if get_integer_flag(column_name='phone_being_entered',
                        table_name='user',
                        chat_id=chat_id) == 1:
        if message.text.isnumeric():
            update_user_filed(chat_id, 'phone_number', int(message.text))
            set_integer_flag(0, 'phone_being_entered', 'user', chat_id)
            bot.send_message(chat_id, "Номер телефона сохранён.", reply_markup=get_user_details_keyboard(chat_id))
        else:
            bot.send_message(chat_id, "Номер телефона должен содержать только цифры!")


def check_address_if_yes_update(chat_id, message):
    if get_integer_flag(column_name='address_being_entered',
                        table_name='user',
                        chat_id=chat_id) == 1:

        update_user_filed(chat_id, 'address', message.text)
        set_integer_flag(0, 'address_being_entered', 'user', chat_id)
        bot.send_message(chat_id, "Адрес сохранён.", reply_markup=get_user_details_keyboard(chat_id))


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
        conn.commit()
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


#
# WEBHOOK_HOST = '<ip/host where the bot is running>'
# WEBHOOK_PORT = 8443  # 443, 80, 88 or 8443 (port need to be 'open')
# WEBHOOK_LISTEN = '0.0.0.0'  # In some VPS you may need to put here the IP addr
#
# WEBHOOK_SSL_CERT = './webhook_cert.pem'  # Path to the ssl certificate
# WEBHOOK_SSL_PRIV = './webhook_pkey.pem'  # Path to the ssl private key
#
# # Quick'n'dirty SSL certificate generation:
# #
# # openssl genrsa -out webhook_pkey.pem 2048
# # openssl req -new -x509 -days 3650 -key webhook_pkey.pem -out webhook_cert.pem
# #
# # When asked for "Common Name (e.g. server FQDN or YOUR name)" you should reply
# # with the same value in you put in WEBHOOK_HOST
#
# WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
# WEBHOOK_URL_PATH = "/%s/" % TOKEN
#
# try:
#     # Python 2
#     from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
# except ImportError:
#     # Python 3
#     from http.server import BaseHTTPRequestHandler, HTTPServer
#
#
# # WebhookHandler, process webhook calls
# class WebhookHandler(BaseHTTPRequestHandler):
#     server_version = "WebhookHandler/1.0"
#
#     def do_HEAD(self):
#         self.send_response(200)
#         self.end_headers()
#
#     def do_GET(self):
#         self.send_response(200)
#         self.end_headers()
#
#     def do_POST(self):
#         if self.path == WEBHOOK_URL_PATH and \
#            'content-type' in self.headers and \
#            'content-length' in self.headers and \
#            self.headers['content-type'] == 'application/json':
#             json_string = self.rfile.read(int(self.headers['content-length']))
#
#             self.send_response(200)
#             self.end_headers()
#
#             update = Update.de_json(json_string)
#             bot.process_new_messages([update.message])
#         else:
#             self.send_error(403)
#             self.end_headers()
#
#
# # Start server
# httpd = HTTPServer((WEBHOOK_LISTEN, WEBHOOK_PORT),
#                    WebhookHandler)
#
# httpd.socket = ssl.wrap_socket(httpd.socket,
#                                certfile=WEBHOOK_SSL_CERT,
#                                keyfile=WEBHOOK_SSL_PRIV,
#                                server_side=True)
#
# httpd.serve_forever()


bot.infinity_polling()
