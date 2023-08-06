import logging
from functools import wraps
from typing import Any
from typing import Callable
from typing import Dict

import flask_login  # type: ignore
from flask import abort
from flask import Flask
from flask import jsonify
from flask import make_response
from flask import request
from flask import Response

import JuMonC.models.cache.helper as cache
from JuMonC import settings
from JuMonC.helpers.generateToken import generateToken


logger = logging.getLogger(__name__)

RESTAPI = Flask("JuMonC.handlers")
RESTAPI.config['JSON_SORT_KEYS'] = False
RESTAPI.url_map.strict_slashes = False



RESTAPI.config['SECRET_KEY'] = generateToken()
login_manager = flask_login.LoginManager()
login_manager.init_app(RESTAPI)


start_version = 0
end_version = 0
def setRESTVersion() -> None:
    global start_version
    global end_version
    if settings.ONLY_CHOOSEN_REST_API_VERSION:
        start_version = settings.REST_API_VERSION
    else:
        start_version = 1
    end_version = settings.REST_API_VERSION

    
api_version_path = "/v<int:version>"


def check_version(func: Callable[..., Response]) -> Callable[..., Response]:
    @wraps(func)
    def decorated_function(*args: Any, **kwargs: Any) -> Response:
        if kwargs["version"] >= start_version and kwargs["version"] <= end_version:
            return func(*args, **kwargs)
        abort(404)
        return make_response("Invalid version used",404)
            
    return decorated_function



def get_prefer_id_description() -> Dict[str,str]:
    return {"name": "prefer_id",
            "description": "When set to True, only returns a json with the cache_id needed to retrieve the result"}

def generate_cache_id(func: Callable[..., Response]) -> Callable[..., Response]:
    @wraps(func)
    def decorated_function(*args: Any, **kwargs: Any) -> Response:
        prefer_id = request.args.get('prefer_id', default = False, type = settings.helpers.parse_boolean)
        
        cache_id = cache.add_cache_entry(request.path)
        logger.debug("Cache ID (%i) generated for: %s", cache_id, request.path)
        
        kwargs["cache_id"] = cache_id
        response = func(*args, **kwargs)
        cache.commit()
        if response.status_code == 200:
            if prefer_id is True:
                return make_response(jsonify({"cache_id": cache_id}), 200)
        else:
            cache.delete(cache_id)
        return response
            
    return decorated_function
