import logging
import jwt
from datetime import datetime, timedelta
from flask_restx import Resource
from werkzeug.security import check_password_hash

from ..app import api
from ..models.user import user_model, User
from .utils import token_required

LOG = logging.getLogger(__name__)


class UserResource(Resource):

    @api.expect(user_model)
    # @api.doc(security='apikey')
    # @token_required
    def post(self):
        """Create a admin user"""
        try:
            user_data = self.api.payload
            user_obj = User(**user_data)
            self.api.app.config["db"]["user"].save(user_obj)
            return {"result": "success"}, 201
        except Exception as ex:
            if len(ex.args) == 2:
                return {"message": "error: {}".format(ex.args[0])}, ex.args[1]
            return {"message": "error: {}".format(ex.args[0])}


class LoginResource(Resource):
    @api.expect(user_model)
    def post(self):
        """Get token for a user"""
        user_info = self.api.payload
        user_obj = self.api.app.config["db"]["user"].find(
            **{"username": user_info["username"]}
        )
        user_data = {}
        if user_obj:
            for obj in user_obj:
                user_data = obj.to_dict()
                break
            if check_password_hash(user_data["password"], user_info["password"]):
                token = jwt.encode({
                    'public_id': user_data["public_id"],
                    'exp': datetime.utcnow() + timedelta(minutes=60)},
                    self.api.app.config["user"]["secret"]
                )
                return {'token': token.decode("utf-8")}, 200
        return {"message": "Error: could not verify user"}, 401
