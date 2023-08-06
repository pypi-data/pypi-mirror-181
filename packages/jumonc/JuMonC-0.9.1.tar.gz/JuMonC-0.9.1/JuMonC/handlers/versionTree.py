import logging
from typing import Dict
from typing import List
from typing import Union

from flask import jsonify
from flask import make_response
from flask import Response

from JuMonC.authentication import scopes
from JuMonC.authentication.check import check_auth
from JuMonC.handlers import cache
from JuMonC.handlers import cpu
from JuMonC.handlers import gpu
from JuMonC.handlers import io
from JuMonC.handlers import job
from JuMonC.handlers import main_memory
from JuMonC.handlers import network
from JuMonC.handlers import planed
from JuMonC.handlers.base import api_version_path
from JuMonC.handlers.base import check_version
from JuMonC.handlers.base import RESTAPI


logger = logging.getLogger(__name__)

links: Dict[str, List[Dict[str, Union[bool, str, List[Dict[str, str]]]]]] = {}


@RESTAPI.route(api_version_path)
@check_version
@check_auth(scopes["see_links"])
def returnVersionLinks(version: int) -> Response:
    logger.debug("Accessed /v%i/", version)
    return make_response(jsonify(sorted(links["v" + str(version)], key=lambda dic: dic['link'])), 200)


def registerRestApiPaths(version: int) -> Dict[str, Union[bool, str, List[Dict[str, str]]]]:
    links_this_version: List[Dict[str, Union[bool, str, List[Dict[str, str]]]]] = []
    
    links_this_version.append(cache.registerRestApiPaths(version))
    links_this_version.append(cpu.registerRestApiPaths(version))
    links_this_version.append(gpu.registerRestApiPaths(version))
    links_this_version.append(io.registerRestApiPaths(version))
    links_this_version.append(job.registerRestApiPaths(version))
    links_this_version.append(main_memory.registerRestApiPaths(version))
    links_this_version.append(network.registerRestApiPaths(version))
    links_this_version.append(planed.registerRestApiPaths(version))
    
    links["v" + str(version)] = links_this_version
    
    
    
    return {
        "link": "/v" + str(version),
        "isOptional": False,
        "description": "Following this links leads to API version " + str(version),
        "parameters": [
             {"name": "token",
              "description": "Supply a token that shows you are allowed to access this link (or login once using \"/login\")"}
        ]
    }
