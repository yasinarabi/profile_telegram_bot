import configparser


class Config:
    def __init__(self, path="config.ini"):
        self.config = configparser.ConfigParser()
        self.config.read(path)

    def get_token(self):
        return self.config["telegram"]["token"]

    def get_db(self):
        return self.config["mysql"]

    def get_support_id(self):
        return int(self.config["telegram"]["suport_id"])
