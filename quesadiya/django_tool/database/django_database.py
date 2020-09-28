from sqlalchemy.sql import text


# NOTE: sqlalchemy's connection doesn't seem to require con.commit()
def create_django_tables(con):  # argu : database path
    con.execute(text('DROP TABLE IF EXISTS auth_user'))
    con.execute(text('''CREATE TABLE "auth_user" (
                            "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                            "password" varchar(128) NOT NULL,
                            "last_login" datetime NULL,
                            "is_superuser" bool NOT NULL,
                            "username" varchar(150) NOT NULL UNIQUE,
                            "last_name" varchar(150) NOT NULL,
                            "email" varchar(254) NOT NULL,
                            "is_staff" bool NOT NULL,
                            "is_active" bool NOT NULL,
                            "date_joined" datetime NOT NULL,
                            "first_name" varchar(150) NOT NULL
                        )'''))
    con.execute(text('DROP TABLE IF EXISTS django_content_type'))
    con.execute(text('''CREATE TABLE "django_content_type" (
                            "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                            "app_label" varchar(100) NOT NULL,
                            "model" varchar(100) NOT NULL
                        )'''))
    con.execute(text('DROP TABLE IF EXISTS django_session'))
    con.execute(text('''CREATE TABLE "django_session" (
                            "session_key" varchar(40) NOT NULL PRIMARY KEY,
                            "session_data" text NOT NULL,
                            "expire_date" datetime NOT NULL
                        )'''))
    con.execute(text('''CREATE UNIQUE INDEX "django_content_type_app_label_model_76bd3d3b_uniq"
                            ON "django_content_type" ("app_label", "model")'''))
    con.execute(text('''CREATE INDEX "django_session_expire_date_a5c62663"
                            ON "django_session" ("expire_date")'''))


def insert_admin(con, password, admin_name, date_time):
    row = {
        "password": password,
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
    row = {
        "password": password,
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
