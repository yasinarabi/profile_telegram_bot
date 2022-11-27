import mysql.connector
import time

hostname = "localhost"
username = "profilebot"
password = "Pass@1234"
database = "profilebot"

my_db = mysql.connector.connect(host=hostname, user=username, passwd=password, database=database)
my_cursor = my_db.cursor()

class Mysql_DB:
    def __init__(self):
        self.db = mysql.connector.connect(host=hostname, user=username, passwd=password, database=database)
        self.cursor = my_db.cursor()
        if not self.initialized():
            self.initialize()

    def initialized(self):
        query = f"SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = '{database}';"
        self.cursor.execute(query)
        count_tables = self.cursor.fetchall()[0][0]
        return count_tables >= 3

    def initialize(self):
        create_start_table_query = "CREATE TABLE `start` (" \
        	"`id` INT UNSIGNED NOT NULL AUTO_INCREMENT," \
        	"`time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP," \
        	"PRIMARY KEY (`id`)" \
            ");"
        create_process_table_query = "CREATE TABLE `process` (" \
        	"`id` INT UNSIGNED NOT NULL AUTO_INCREMENT," \
        	"`user_id` INT UNSIGNED NOT NULL," \
        	"`time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP," \
        	"PRIMARY KEY (`id`)" \
            ");"
        create_message_table_query = "CREATE TABLE `message` (" \
        	"`id` INT UNSIGNED NOT NULL AUTO_INCREMENT," \
        	"`user_id` INT UNSIGNED NOT NULL," \
        	"`time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP," \
        	"`message` TEXT," \
        	"PRIMARY KEY (`id`)" \
            ");"

        self.cursor.execute(create_start_table_query)
        self.cursor.execute(create_process_table_query)
        self.cursor.execute(create_message_table_query)
        self.db.commit()

    def start_put(self, user_id):
        if not self.exist_in_start(user_id):
            query = f"INSERT INTO `start` (`id`) VALUES ({user_id});"
            self.cursor.execute(query)
            self.db.commit()

    def exist_in_start(self, user_id):
        query = f"SELECT `start`.`id` FROM `start` WHERE `start`.`id` = {user_id};"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return len(result) > 0

    def add_process(self, user_id):
        query = f"INSERT INTO `process` (`user_id`) VALUES ({user_id});"
        self.cursor.execute(query)
        self.db.commit()

    def save_message(self, user_id, message):
        query = f"INSERT INTO `message` (`user_id`, `message`) VALUES ({user_id}, '{message}');"
        self.cursor.execute(query)
        self.db.commit()
