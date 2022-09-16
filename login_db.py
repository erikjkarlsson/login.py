from hashlib import pbkdf2_hmac
import sqlite3
from os import urandom
from time    import localtime
from time    import time
from os.path import isfile

HASH_ITERS = 100000

# Create salt using urandom(16)
# as stated in  https://docs.python.org/3/library/hashlib.html
HASH_SALT = b'\xc0\xe4J\xd1[\xb2\xa4q\x19\xee\xccQ\x8e\x82\xa7\x9a'

DROP_DATABASE_SQL = """
DROP TABLE IF EXISTS users 
"""

DATABASE_SQL = """
CREATE TABLE IF NOT EXISTS users (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       username       TEXT,
       password       TEXT,
       user_created   INTEGER NOT NULL,
       last_signed_in INTEGER,
       privledge      INTEGER NOT NULL
)
"""

DATABASE_PATH = "./data/login.db"

def hash_str(string, salt=HASH_SALT, iters=HASH_ITERS):
    "Create a SHA256 hash from STRING, using the defined salt and iters"

    return pbkdf2_hmac('sha256', bytes(string, "utf-8"), salt, iters).hex()

def drop_db(path) -> None:
    "Clear all the tables of the login database"

    con = sqlite3.connect(path)
    cur = con.cursor()

    cur.execute("BEGIN")
    cur.execute(DROP_DATABASE_SQL)
    con.commit()
    con.close()

def create_db(path) -> None:
    "Create the login database"

    con = sqlite3.connect(path)
    cur = con.cursor()

    cur.execute("BEGIN")
    cur.execute(DATABASE_SQL)
    con.commit()
    con.close()

def does_user_exist(path, username) -> bool:
    "Does a user exist in the database."

    con = sqlite3.connect(path)
    cur = con.cursor()

    username_hashed = hash_str(username)

    cur.execute("BEGIN")
    cur.execute("SELECT id FROM users WHERE username = ?;",
                (username_hashed,))

    ans = cur.fetchall() != []

    con.commit()
    con.close()

    return ans

def remove_user(path, username) -> None:
    "Remove a user from the database"

    con = sqlite3.connect(path)
    cur = con.cursor()

    username_hashed = hash_str(username)

    cur.execute("BEGIN")

    cur.execute("DELETE FROM users WHERE username = ?",
                (username_hashed,))

    con.commit()
    con.close()

def user_created(path, username) -> int:
    "When was a user created"

    con = sqlite3.connect(path)
    cur = con.cursor()

    username_hashed = hash_str(username)

    cur.execute(
        "SELECT user_created FROM users WHERE username = ?",
        (username_hashed,))

    user_created_ans = cur.fetchall()

    con.close()

    return user_created_ans [0][0] if not (user_created_ans == []) else None

def last_signed_in(path, username) -> int:
    "When was the last time a user signed in"

    con = sqlite3.connect(path)
    cur = con.cursor()

    username_hashed = hash_str(username)

    cur.execute(
        "SELECT last_signed_in FROM users WHERE username = ?",
        (username_hashed,))

    last_signed_in_ans = cur.fetchall()

    con.close()

    return last_signed_in_ans[0][0] if not (last_signed_in_ans == []) else None

def correct_password(path, username, password) -> bool:
    "Test the password for a user upon login"

    con = sqlite3.connect(path)
    cur = con.cursor()

    password_hashed = hash_str(password)
    username_hashed = hash_str(username)

    cur.execute(
        "SELECT username FROM users WHERE username = ? and password = ?",
        (username_hashed, password_hashed,))

    ans = cur.fetchall()

    con.close()

    return ans != []

def create_user(path, username, password, privledge=2) -> None:
    "Create a new user"

    con = sqlite3.connect(path)
    cur = con.cursor()

    created_now = int(time())

    password_hashed = hash_str(password)
    username_hashed = hash_str(username)

    cur.execute("BEGIN")

    cur.execute(
        "INSERT INTO users (username, password, privledge, user_created) VALUES (?, ?, ?, ?)",
        (username_hashed, password_hashed, privledge, created_now,))

    con.commit()
    con.close()
