import json
from functools import wraps

import requests
from flask import request, abort, make_response

from src.data.stack_optimizer_loaded_data import StackOptimizerLoadedData
from src.util.config_loader import Config
import logging


def pre_post_process(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        if not is_valid_token():
            return abort(401)

        json_payload = get_json_payload()

        caller = func.__name__
        try:
            StackOptimizerLoadedData.read_files_if_required()

            result = func(json_payload, *args, **kwargs)

            print(f'{caller}(): request: {json_payload}, response: {result}')
            return make_response(json.dumps(result), 200)
        except Exception as exc:
            print(f'{caller}(): request: {json_payload}. Caught Exception: {exc}')
            return abort(500)

    def get_json_payload():
        try:
            return json.loads(request.data)
        except ValueError as exc:
            logging.error(f'{func.__name__}(): Caught Exception: {exc}')
            return abort(400)

    def is_valid_token():
        caller = func.__name__
        token = None
        try:
            if "Authorization" in request.headers:
                token = request.headers["Authorization"]
                if len(token.split(' ')) > 1:
                    token = token[7:]
                params = {"token": token}

                url = Config.value('url_jwt')
                token_result = requests.post(url, json=params).json()
                if token_result['error']:
                    error = token_result['message']
                    logging.error(f'{caller}(): Request failed due to: {error}')
                    token = None
        except Exception as exc:
            logging.error(f'{caller}(): Caught Exception at : {exc}')
            token = None

        return token is not None

    return decorated
