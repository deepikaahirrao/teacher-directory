import logging

import jwt
from flask import Flask, request, jsonify, make_response
from functools import wraps

from ..app import api

LOG = logging.getLogger(__name__)


def token_required(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        token = None
        if "X-API-KEY" in request.headers:
            token = request.headers["X-API-KEY"]

        if not token:
            return {"message": "a valid token is missing"}, 401

        try:
            data = jwt.decode(token, api.app.config["user"]["secret"])
            user_obj = api.app.config["db"]["user"].find(
                **{"public_id": data["public_id"]}
            )
            current_user = None
            if user_obj:
                for obj in user_obj:
                    current_user = obj
                    break
            else:
                return {"message": "Token is invalid"}, 401
        except Exception as ex:
            LOG.exception("Could not verify token")
            LOG.exception(ex)
            raise

        return func(*args, **kwargs)
    return decorator
