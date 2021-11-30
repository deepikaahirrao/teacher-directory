import csv
import logging
import uuid
import os
from flask import request
from flask_restx import Resource, fields
from operator import itemgetter

from ..app import api
from ..models.teacher import (
    Teacher, valid_fields,
    valid_sort_fields, teacher_model
)
from .utils import token_required


LOG = logging.getLogger(__name__)
field_map = {
    "First Name": "first_name",
    "Last Name": "last_name",
    "Profile picture": "profile_picture",
    "Email Address": "email_address",
    "Phone Number": "phone_number",
    "Room Number": "room_number",
    "Subjects taught": "subjects_taught",
}


class TeacherResource(Resource):

    @api.expect(teacher_model)
    @api.doc(security="apikey")
    @token_required
    def post(self):
        """store teacher data"""
        try:
            teacher_data = self.api.payload
            teacher_obj = Teacher(**teacher_data)
            self.api.app.config["db"]["teacher"].save(teacher_obj)
        except Exception as ex:
            if len(ex.args) == 2:
                return {"message": "error: {}".format(ex.args[0])}, ex.args[1]
            return {"message": "error: {}".format(ex.args[0])}
        return {"result": "success"}, 201


class FeedDataResource(Resource):

    @api.doc(params=
             {"csv_file_path": {"description": "a absolute location of csv file",
                            "type": "str",
                            },
              })
    @api.doc(security="apikey")
    @token_required
    def post(self):
        """store teachers data from provided csv file"""
        csv_file_path = request.args.get("csv_file_path")
        try:
            if not os.path.exists(csv_file_path):
                msg = "Source file path ({}) does not exist".format(csv_file_path)
                LOG.exception(msg)
                return {"error": msg}, 400

            csv_data = []
            with open(csv_file_path, "r") as fd:
                data = csv.DictReader(fd)
                if data:
                    csv_data = [i for i in list(data)]

            teachers_data = []
            for record in csv_data:
                res = {}
                for key, value in field_map.items():
                    if record.get(key, '').strip():
                        res[value] = record[key]
                        if value == "subjects_taught":
                            if isinstance(record[key], str):
                                res[value] = [i.strip() for i in record[key].split(",")]
                try:
                    if res.get("email_address"):
                        res["teacher_id"] = uuid.uuid4()
                        teachers_data.append(Teacher(**res))
                except Exception as ex:
                    LOG.exception(ex)
                    LOG.warn("Data provided {} is not in expected form".format(csv_data))
                    LOG.info("Continuing without processing above record")

            res = self.api.app.config["db"]["teacher"].save_all(teachers_data)
            if not res:
                msg = "Failed to save teachers information: {}".format(teachers_data)
                LOG.exception(msg)
                return {"error": msg}, 400

        except Exception as ex:
            msg = "Provided data is not in expected form, error: {}".format(ex)
            LOG.exception(msg)
            return {"error": msg}, 400
        return {"result": "success"}, 201


class SearchResource(Resource):

    @api.doc(security="apikey")
    @token_required
    def get(self, field, value):
        """Search data by field and it's value"""
        if field in valid_fields:
            teachers_objs = self.api.app.config["db"]["teacher"].find(
                **{field: value}
            )
            return [obj.to_dict() for obj in teachers_objs]
        else:
            msg = "The provided field is not valid, it should be one of following : {}".format(valid_fields)
            LOG.exception(msg)
            return {"error": msg}, 400


class FilterResource(Resource):

    @api.doc(params=
             {"filter_by": {"description": "a field name to sort the data with",
                            "type": "str",
                            "default": "last_name"
                            },
              },
             security="apikey")
    @token_required
    def get(self):
        """fetch teachers info return it by sorting with the field provided in filter_by"""
        filter_by = request.args.get("filter_by")
        if filter_by in valid_sort_fields:
            teacher_objs = self.api.app.config["db"]["teacher"].fetch_all()
            teachers_data = [obj.to_dict() for obj in teacher_objs]
            if filter_by == 'last_name':
                res = sorted(teachers_data, key= lambda i: i['last_name'][0])
            elif filter_by == 'subjects_taught':
                res = sorted(teachers_data, key= lambda i: sorted(i['subjects_taught']))
            else:
                res = sorted(teachers_data, key=itemgetter(filter_by))
            return res
        else:
            msg = "The provided field is not valid, it should be one of following : {}".format(valid_fields)
            LOG.exception(msg)
            return {"error": msg}, 400
