from schematics.models import Model
from schematics.types import StringType, IntType
from schematics.types.compound import ModelType


class ServiceConfig(Model):
    host = StringType(required=True)
    port = IntType(required=True)


class DatabaseConfig(Model):
    file_path = StringType(required=True)
    db_name = StringType(required=True)


class UserConfig(Model):
    secret = StringType(required=True)


class Config(Model):
    service_config = ModelType(ServiceConfig, required=True)
    database = ModelType(DatabaseConfig, required=True)
    user = ModelType(UserConfig, required=True)
