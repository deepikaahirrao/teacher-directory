import logging
import sqlite3

from ..models.teacher import (
    Teacher,
    serialize_to_db_teacher,
    deserialize_to_db_teacher,
)
from ..models.user import (
    User,
    serialize_to_db_user,
    deserialize_to_db_user,
)


LOG = logging.getLogger(__name__)


class TeacherClient:

    def __init__(self, db_path):
        self.db_path = db_path

    def save(self, data: Teacher):
        teacher_info_db_format = serialize_to_db_teacher(data)
        try:
            # with sqlite3.connect(":memory:") as conn:
            with sqlite3.connect(self.db_path) as conn:
                cur = conn.cursor()
                sql = '''INSERT INTO teachers (teacher_id, first_name, last_name,
                                       email_address, phone_number, room_number,
                                       subjects_taught, profile_picture, creation_date)
                                   VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)'''
                cur.execute(sql, teacher_info_db_format)
        except sqlite3.IntegrityError as ex:
            raise Exception("Teacher is already exist: {}".format(data.username), 409)
        except Exception as ex:
            LOG.exception("Failed to execute DB query")
            raise ex
        return True

    def save_all(self, data):
        teachers = [serialize_to_db_teacher(record) for record in data]
        try:
            # with sqlite3.connect(":memory:") as conn:
            with sqlite3.connect(self.db_path) as conn:
                cur = conn.cursor()
                sql = '''INSERT INTO teachers (teacher_id, first_name, last_name,
                        email_address, phone_number, room_number,
                        subjects_taught, profile_picture, creation_date)
                    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)'''
                cur.executemany(sql, teachers)
        except sqlite3.IntegrityError as ex:
            raise Exception("Teacher is already exist: {}".format(data.username), 409)
        except Exception as ex:
            LOG.exception("Failed to execute DB query")
            raise ex
        return True

    def find(self, **kwargs):
        result = []
        if kwargs and len(kwargs) == 1:
            field = list(kwargs.keys())[0]
            value = kwargs[field]
            sql = "SELECT * FROM teachers WHERE {}='{}'".format(
                field, value
            )
            try:
                with sqlite3.connect(self.db_path) as conn:
                    cur = conn.cursor()
                    cur.execute(sql)
                    rows = cur.fetchall()
                    for row in rows:
                        result.append(deserialize_to_db_teacher(row))
            except Exception as ex:
                LOG.exception("Failed to execute DB query")
                raise ex
        return result

    def fetch_all(self):
        result = []
        try:
            with sqlite3.connect(self.db_path) as conn:
                cur = conn.cursor()
                cur.execute("SELECT * FROM teachers;")
                rows = cur.fetchall()
                for row in rows:
                    result.append(deserialize_to_db_teacher(row))
        except Exception as ex:
            LOG.exception("Failed to execute DB query")
            raise ex
        return result


class UserClient:

    def __init__(self, db_path):
        self.db_path = db_path

    def save(self, data: User):
        user_info_db_format = serialize_to_db_user(data)
        try:
            # with sqlite3.connect(":memory:") as conn:
            with sqlite3.connect(self.db_path) as conn:
                cur = conn.cursor()
                sql = '''INSERT INTO user(public_id, username, password, admin, creation_date)
                    VALUES(?, ?, ?, ?, ?)'''
                cur.execute(sql, user_info_db_format)
        except sqlite3.IntegrityError as ex:
            raise Exception("User is already exist: {}".format(data.username), 409)
        except Exception as ex:
            LOG.exception("Failed to execute DB query")
            raise ex
        return True

    def find(self, **kwargs):
        sql = "SELECT * FROM user WHERE "
        if "username" in kwargs:
            if not sql.rstrip().endswith('WHERE'):
                sql += " AND "
            sql += "username='{}'".format(kwargs["username"])
        if "public_id" in kwargs:
            if not sql.rstrip().endswith('WHERE'):
                sql += " AND "
            sql += "public_id='{}'".format(kwargs["public_id"])
        result = []
        try:
            with sqlite3.connect(self.db_path) as conn:
                cur = conn.cursor()
                cur.execute(sql)
                rows = cur.fetchall()
                for row in rows:
                    result.append(deserialize_to_db_user(row))
        except Exception as ex:
            LOG.exception("Failed to execute DB query")
            raise ex
        return result

