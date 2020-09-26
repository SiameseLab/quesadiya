from sqlalchemy import create_engine
from sqlalchemy.sql import text


def djangoDB(con):  # argu : database path
    con.execute(text('DROP TABLE IF EXISTS auth_user'))
    con.execute(text('''CREATE TABLE "auth_user" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "password" varchar(128) NOT NULL, "last_login" datetime NULL, "is_superuser" bool NOT NULL, "username" varchar(150) NOT NULL UNIQUE, "last_name" varchar(150) NOT NULL, "email" varchar(254) NOT NULL, "is_staff" bool NOT NULL, "is_active" bool NOT NULL, "date_joined" datetime NOT NULL, "first_name" varchar(150) NOT NULL)'''))
    con.execute(text('DROP TABLE IF EXISTS django_content_type'))
    con.execute(text('''CREATE TABLE "django_content_type" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "app_label" varchar(100) NOT NULL, "model" varchar(100) NOT NULL)'''))
    con.execute(text('DROP TABLE IF EXISTS django_session'))
    con.execute(text('''CREATE TABLE "django_session" ("session_key" varchar(40) NOT NULL PRIMARY KEY, "session_data" text NOT NULL, "expire_date" datetime NOT NULL)'''))
    con.execute(text(
        '''CREATE UNIQUE INDEX "django_content_type_app_label_model_76bd3d3b_uniq" ON "django_content_type" ("app_label", "model")'''))
    con.execute(text(
        '''CREATE INDEX "django_session_expire_date_a5c62663" ON "django_session" ("expire_date")'''))
    con.commit()


# example
# djangoDB("sqlite:///example.db")
