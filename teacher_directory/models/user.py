import attr
from datetime import datetime
import uuid
from flask_restx import fields
from werkzeug.security import generate_password_hash, check_password_hash

from ..app import api
from ..constants import DATE_FORMAT


user_model = api.model(
    'User',
    {
        "username": fields.String(),
        "password": fields.String(),
        "admin": fields.Boolean(default=True),
    }
)


def convert_into_hash(value: str):
    if value.startswith("sha256$"):
        return value
    else:
        return generate_password_hash(
            value, method="sha256"
        )


@attr.s
class User:
    username = attr.ib(type=str)
    password = attr.ib(type=str, converter=convert_into_hash)
    admin = attr.ib(type=bool, default=False)
    public_id = attr.ib(type=int, default=uuid.uuid4())
    creation_date = attr.ib(
        type=datetime, default=datetime.utcnow().replace(microsecond=0)
    )

    def to_dict(self):
        return {
            "public_id": str(self.public_id),
            "username": self.username,
            "password": self.password,
            "admin": self.admin,
            "creation_date": self.creation_date,
        }


def serialize_to_db_user(user_obj):
    """
    User --> db tuple values
    """
    return (
        str(user_obj.public_id),
        user_obj.username,
        user_obj.password,
        user_obj.admin,
        user_obj.creation_date
    )



def deserialize_to_db_user(data):
    """
    db json values --> User
    """
    return User(**{
        "username": data[0],
        "password": data[1],
        "admin": data[2],
        "public_id": data[3],
        "creation_date": datetime.strptime(data[4], DATE_FORMAT),
    })
