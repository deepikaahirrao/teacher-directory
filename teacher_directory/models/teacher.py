import attr
import json
import uuid
from datetime import datetime
from flask_restx import fields

from ..app import api
from ..constants import DATE_FORMAT


valid_fields = ["first_name", "last_name", "email_address",
                "phone_number", "room_number"]
valid_sort_fields = ["first_name", "last_name", "email_address",
                     "subjects_taught", "room_number"]
teacher_model = api.model(
    'Teacher',
    {
        "first_name": fields.String(),
        "last_name": fields.String(),
        "profile_picture": fields.String(),
        "email_address": fields.String(),
        "phone_number": fields.String(),
        "room_number": fields.String(),
        "subjects_taught": fields.List(fields.String),
    }
)

# A converter to store attr list attribute in sorted form
def sort_subjects(value):
    value.sort()
    return value

@attr.s
class Teacher:
    first_name = attr.ib(type=str)
    last_name = attr.ib(type=str)
    profile_picture = attr.ib(type=str, default='default.JPG')
    email_address = attr.ib(type=str, default=None)
    phone_number = attr.ib(type=str, default=None)
    room_number = attr.ib(type=str, default=None)
    subjects_taught = attr.ib(type=list, default=[]) # converter=sort_subjects)
    creation_date = attr.ib(
        type=datetime, default=datetime.utcnow().replace(microsecond=0)
    )
    teacher_id = attr.ib(type=str, default=uuid.uuid4())

    @subjects_taught.validator
    def validate_subjects_taught(self, attribute, value):
        if value and len(value) > 5:
            raise ValueError("A teacher can not teach more than 5 subjects")

    def to_dict(self):
        return {
            "teacher_id": str(self.teacher_id),
            "creation_date": self.creation_date.strftime(DATE_FORMAT),
            "first_name": self.first_name,
            "last_name": self.last_name,
            "profile_picture": self.profile_picture,
            "email_address": self.email_address,
            "phone_number": self.phone_number,
            "room_number": self.room_number,
            "subjects_taught": self.subjects_taught,
        }


def serialize_to_db_teacher(teacher_obj):
    """
    Teacher --> db json values
    """
    return (
        str(teacher_obj.teacher_id),
        teacher_obj.first_name,
        teacher_obj.last_name,
        teacher_obj.email_address,
        teacher_obj.phone_number,
        teacher_obj.room_number,
        json.dumps(teacher_obj.subjects_taught),
        teacher_obj.profile_picture,
        teacher_obj.creation_date,
    )


def deserialize_to_db_teacher(data):
    """
    db json values --> Teacher
    """
    return Teacher(**{
        "teacher_id": data[0],
        "first_name": data[1],
        "last_name": data[2],
        "email_address": data[3],
        "phone_number": data[4],
        "room_number": data[5],
        "subjects_taught": json.loads(data[6]),
        "profile_picture": data[7],
        "creation_date": datetime.strptime(data[8], DATE_FORMAT),

    })
