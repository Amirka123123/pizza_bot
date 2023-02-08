class MenuStack:

    def __init__(self, default_menu):
        self.elements = list()
        self.default_menu = default_menu

    def push(self, element):
        self.elements.append(element)

    def pop(self):
        if len(self.elements) == 0:
            return self.default_menu

        popped_element = self.elements[-1]
        del self.elements[-1]
        return popped_element

    def top(self):
        if len(self.elements) == 0:
            return self.default_menu
        return self.elements[-1]

    def __str__(self):
        return str(self.elements)


from constants import (get_address_sql,
                       get_phone_number_sql, set_integer_flag_sql, get_integer_flag_sql, update_user_filed_sql,
                       get_product_data_sql, get_product_id_from_user_sql)
import sqlite3


def check_phone_number(chat_id):
    try:
        sql = get_phone_number_sql(chat_id)
        conn = sqlite3.connect("pizza_database.db")
        cursor = conn.cursor()

        cursor.execute(sql)
        conn.commit()
        result = conn.cursor()

        if result is not None:
            return True
        return False
    except Exception as e:
        print("Database error")
        print(e)


def check_address(chat_id):
    try:
        sql = get_address_sql(chat_id)
        conn = sqlite3.connect("pizza_database.db")
        cursor = conn.cursor()

        cursor.execute(sql)
        conn.commit()
        result = cursor.fetchone()
        if result is not None:
            return True
        return False
    except Exception as e:
        print("Database error")
        print(e)


def set_integer_flag(value, column_name, table_name, chat_id):
    sql = set_integer_flag_sql(value, column_name, table_name, chat_id)

    conn = sqlite3.connect("pizza_database.db")
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()


def get_integer_flag(column_name, table_name, chat_id):
    sql = get_integer_flag_sql(column_name, table_name, chat_id)
    conn = sqlite3.connect("pizza_database.db")
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()

    flag = cursor.fetchall()[0][0]

    return flag


def update_user_filed(chat_id, filed_name, value):
    sql = update_user_filed_sql(chat_id, filed_name, value)

    conn = sqlite3.connect("pizza_database.db")
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()


def get_product_data(product_name):
    sql = get_product_data_sql(product_name)

    conn = sqlite3.connect("pizza_database.db")
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()

    data = cursor.fetchone()
    id_ = data[0]
    description = data[1]
    price = data[2]

    return description, price, id_


def start_getting_quantity(chat_id, product):
    set_integer_flag(1, "quantity_being_entered", "user", chat_id)
    data = get_product_data(product)
    id_ = data[2]
    update_user_filed(chat_id, "choosen_product", id_)


def get_product_from_user(chat_id):
    sql = get_product_id_from_user_sql(chat_id)

    conn = sqlite3.connect("pizza_database.db")
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()

    product_id = cursor.fetchone()[0]
    return product_id


def insert_data_to_basket(chat_id, product_id, amount):
    sql = f"""INSERT INTO basket(user_id, product_id, amount) VALUES ({chat_id}, {product_id}, {amount})"""


if __name__ == '__main__':
    my_stack = MenuStack(9)
    my_stack.push(3)
    my_stack.push(5)
    my_stack.push(-1)
    print(my_stack)
    print(my_stack.elements)
    popped = my_stack.pop()
    print(my_stack)


    print("Popped element:", popped)
