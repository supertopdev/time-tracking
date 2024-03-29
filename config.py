database_creds = {
    "database": "global",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost"
}


class Config():
    SQLALCHEMY_DATABASE_URI = "postgresql://{}:{}@{}/{}".format(database_creds['user'], database_creds['password'],
                                                                database_creds['host'], database_creds['database'])
    SQLALCHEMY_TRACK_MODIFICATIONS = False