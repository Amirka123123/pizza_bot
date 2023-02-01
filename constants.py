def get_products_query():
    sql = "SELECT name from products"
    return sql


def create_new_user_query(id):
    sql = f"INSERT INTO user (id) VALUES ({id})"
    return sql


def get_phone_number_sql(chat_id):
    sql = f"""SELECT phone_number
              FROM user 
              WHERE id = {chat_id}"""
    return sql


def get_address_sql(chat_id):
    sql = f"""SELECT address
              FROM user
              WHERE id = {chat_id}"""
    return sql



def set_integer_flag_sql(value, column_name, table_name, chat_id):
    sql = f"UPDATE {table_name} SET {column_name} = {value} WHERE id = {chat_id}"
    return sql


def get_integer_flag_sql(column_name, table_name, chat_id):
    sql = f"SELECT {column_name} FROM {table_name} WHERE id = {chat_id}"
    return sql


def update_user_filed_sql(chat_id, filed_name, value):
    sql = f"UPDATE user SET {filed_name} = '{value}' WHERE id = {chat_id}"
    return sql
