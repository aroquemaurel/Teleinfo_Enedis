from config.prod import db_user, db_password, db_url, db_table


class Settings:
    __instance__ = None
    app = None
    db = None
    user = db_user
    password = db_password
    url = db_url
    table = db_table

    @staticmethod
    def singleton():
        if Settings.__instance__ is None:
            Settings.__instance__ = Settings()

        return Settings.__instance__
