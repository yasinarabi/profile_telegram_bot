import mysql.connector
import time

hostname = "remotemysql.com"
username = "2drzgpVlCN"
password = "uEhNkN2MK2"
database = "2drzgpVlCN"
my_db = mysql.connector.connect(host=hostname, user=username, passwd=password, database=database)
my_cursor = my_db.cursor()


def get_time():
    named_tuple = time.localtime()  # get struct_time
    time_string = time.strftime("%Y-%m-%d %H:%M:%S", named_tuple)
    return time_string


def start_put(user_id):
    time_string = get_time()
    if not exist_in_start(user_id):
        query = "INSERT INTO `start` (`id`, `time`) VALUES ('" + user_id + "', '" + time_string + "');"
        my_cursor.execute(query)
        my_db.commit()


def exist_in_start(user_id):
    query = "SELECT `start`.`id` FROM `start` WHERE `start`.`id` = " + user_id
    my_cursor.execute(query)
    my_result = my_cursor.fetchall()
    if len(my_result) == 0:
        return False
    else:
        return True


def add_process(user_id):
    time_string = get_time()
    query = "INSERT INTO `process` (`user_id`, `time`) VALUES ('" + user_id + "', '" + time_string + "');"
    my_cursor.execute(query)
    my_db.commit()


def save_message(user_id, message):
    time_string = get_time()
    query = "INSERT INTO `message` (`user_id`, `message`, `time`) VALUES ('" + user_id + "', '" + message + "', '" + time_string + "');"
    my_cursor.execute(query)
    my_db.commit()
