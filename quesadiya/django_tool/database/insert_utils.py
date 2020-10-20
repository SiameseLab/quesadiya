from sqlalchemy.sql import text
from quesadiya.db.hasher import PH


def insert_admin(con, password, admin_name, date_time):
    encoded_password = PH.hash(password)
    row = {
        "password": encoded_password,
        "is_superuser": True,
        "username": admin_name,
        "last_name": " ",
        "email": " ",
        "is_staff": False,
        "is_active": False,
        "date_joined": date_time,
        "first_name": " "
    }
    _insert_user(con, row)


def insert_collaborator(con, password, collaborator_name, date_time, contact):
    encoded_password = PH.hash(password)
    row = {
        "password": encoded_password,
        "is_superuser": False,
        "username": collaborator_name,
        "last_name": " ",
        "email": contact,
        "is_staff": True,
        "is_active": False,
        "date_joined": date_time,
        "first_name": " "
    }
    _insert_user(con, row)


def _insert_user(con, row):
    query = text('''INSERT INTO "auth_user" (password,
                                             is_superuser,
                                             username,
                                             last_name,
                                             email,
                                             is_staff,
                                             is_active,
                                             date_joined,
                                             first_name)
                    VALUES (:password,
                            :is_superuser,
                            :username,
                            :last_name,
                            :email,
                            :is_staff,
                            :is_active,
                            :date_joined,
                            :first_name);''')
    con.execute(query, row)
