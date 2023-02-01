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

    def __str__(self):
        return str(self.elements)


from constants import (get_address_sql,
                       get_phone_number_sql, set_integer_flag_sql, get_integer_flag_sql, update_user_filed_sql)
import sqlite3


def check_phone_number(chat_id):
    try:
        sql = get_phone_number_sql(chat_id)
        conn = sqlite3.connect("pizza_database.db")
        cursor = conn.cursor()

        cursor.execute(sql)
        conn.commit()
        if cursor.rowcount < 1:
            return False
        return True
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
        if cursor.rowcount < 1:
            return False
        return True
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


if __name__ == '__main__':
    my_stack = MenuStack(9)
    my_stack.push(3)
    my_stack.push(5)
    my_stack.push(-1)
    print(my_stack)
    print(my_stack.elements)
    popped = my_stack.pop()
    print("Popped element:", popped)
    print(my_stack)
