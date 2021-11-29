import logging
import os.path
import sqlite3

from os import listdir, getcwd
from IPython.core.display import Image


LOG = logging.getLogger(__name__)


def init_db(db_config):
    with sqlite3.connect(db_config.file_path) as conn:
        LOG.info("Creating schema")
        try:
            sql = '''CREATE TABLE IF NOT EXISTS teachers (
                        teacher_id TEXT PRIMARY KEY,
                        first_name TEXT,
                        last_name TEXT,
                        email_address TEXT UNIQUE,
                        phone_number TEXT,
                        room_number TEXT,
                        subjects_taught TEXT,
                        profile_picture BLOB,
                        creation_date TEXT);'''
            conn.execute(sql)

            sql = '''CREATE TABLE IF NOT EXISTS user (
                        username TEXT UNIQUE,
                        password TEXT,
                        admin NUMERIC,
                        public_id TEXT PRIMARY KEY,
                        creation_date TEXT);'''
            conn.execute(sql)
        except Exception as ex:
            LOG.exception("Failed to create schema")
            raise ex

'''
def get_picture_list(rel_path):
    abs_path = os.path.join(os.getcwd(),rel_path)
    dir_files = os.listdir(abs_path)
    return dir_files

def insert_picture(conn, picture_file):
    with open(picture_file, 'rb') as input_file:
        ablob = input_file.read()
        base=os.path.basename(picture_file)
        afile, ext = os.path.splitext(base)
        sql = "INSERT INTO PICTURES (PICTURE, TYPE, FILE_NAME) VALUES(?, ?, ?);"
        conn.execute(sql,[sqlite3.Binary(ablob), ext, afile])
        conn.commit()

def extract_picture(cursor, picture_id):
    sql = "SELECT PICTURE, TYPE, FILE_NAME FROM PICTURES WHERE id = :id"
    param = {'id': picture_id}
    cursor.execute(sql, param)
    ablob, ext, afile = cursor.fetchone()
    filename = afile + ext
    with open(filename, 'wb') as output_file:
        output_file.write(ablob)
    return filename


conn = create_or_open_db('picture_db.sqlite')
picture_file = "./pictures/Chrysanthemum50.jpg"
insert_picture(conn, picture_file)
conn.close()

conn = create_or_open_db('picture_db.sqlite')
cur = conn.cursor()
filename = extract_picture(cur, 1)
cur.close()
conn.close()
Image(filename='./'+filename)
'''