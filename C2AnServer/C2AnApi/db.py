import sqlite3
from secrets import token_urlsafe
from hashlib import sha256

def connect(database_path):
    return sqlite3.connect(database_path)

def create_table(connection, table_name, columns):
    connection.execute(f'CREATE TABLE {table_name} ({columns})')

def insert(connection, table_name, columns, values):
    connection.execute(f'INSERT INTO {table_name} ({columns}) VALUES ({values})')

def select(connection, table_name, columns, where):
    return connection.execute(f'SELECT {columns} FROM {table_name} WHERE {where}')

def update(connection, table_name, columns, where):
    connection.execute(f'UPDATE {table_name} SET {columns} WHERE {where}')

def create_user_table(connection):
    create_table(connection, 'user', 'id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password_hash TEXT, token TEXT')

def create_user(connection, username, password):
    user_token = token_urlsafe(32)
    password_hash = sha256((password + username).encode()).hexdigest()
    insert(connection, 'user', 'username, password_hash, user_token', f'"{username}", "{password_hash}", "{user_token}"')

def set_user_token(connection, username, token):
    update(connection, 'user', f'token = "{token}"', f'username = "{username}"')

def get_user_token(connection, username):
    return select(connection, 'user', 'token', f'username = "{username}"').fetchone()[0]

def get_user_by_token(connection, token):
    return select(connection, 'user', 'username', f'token = "{token}"').fetchone()[0]

def check_username_password(connection, username, password_hash):
    return select(connection, 'user', 'username', f'username = "{username}" AND password_hash = "{password_hash}"').fetchone() != None

def create_access_table(connection):
    create_table(connection, 'access','user_id INTEGER PRIMARY KEY AUTOINCREMENT, access TEXT, FOREIGN KEY(user_id) REFERENCES user(id)') 

def get_user_access(connection, user_id):
    return select(connection, 'access', 'access', f'user_id = {user_id}').fetchone()[0]

def give_access_to_user(connection, user_id, access):
    try:
        _ = select(connection, 'user', 'id', f'username = "{user_id}"').fetchone()[0] 
    except:
        insert(connection, 'access', 'user_id, access', f'{user_id}, "{access}"')

    update(connection, 'access', 'user_id, access', f'{user_id}, "{access}"')

def assign_user_access(connection, username, access):
    user_id, existing_access = select(connection, 'user', 'id, access', f'username = "{username}"').fetchone()[0] 
    try:
        existing_access = int(existing_access)
    except:
        return "err"
    
    new_access = str(existing_access | access)
    give_access_to_user(connection, user_id, new_access)

def revoke_user_access(connection, username, access):
    user_id, existing_access = select(connection, 'user', 'id, access', f'username = "{username}"').fetchone()[0] 
    try:
        existing_access = int(existing_access)
    except:
        return "err"
    
    new_access = str(existing_access & ~access)
    give_access_to_user(connection, user_id, new_access)