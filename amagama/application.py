#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010-2014 Zuza Software Foundation
#
# This file is part of amaGama.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""A translation memory server using tmdb for storage, communicates
with clients using JSON over HTTP."""

import logging

from flask import Flask
from flask.ext import restful

from amagama import tmdb, webapi

# decorator to allow CORS
def cors(func, allow_origin=None, allow_headers=None, max_age=None):
    if not allow_origin:
        allow_origin = "*"
    if not allow_headers:
        allow_headers = "content-type, accept"
    if not max_age:
        max_age = 60

    @wraps(func)
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        cors_headers = {
            "Access-Control-Allow-Origin": allow_origin,
            "Access-Control-Allow-Methods": func.__name__.upper(),
            "Access-Control-Allow-Headers": allow_headers,
            "Access-Control-Max-Age": max_age,
        }
        if isinstance(response, tuple):
            if len(response) == 3:
                headers = response[-1]
            else:
                headers = {}
            headers.update(cors_headers)
            return (response[0], response[1], headers)
        else:
            return response, 200, cors_headers
    return wrapper

# parent class adds [cors] decorator
class Resource(restful.Resource):
    method_decorators = [cors]

class AmagamaServer(Flask, Resource):
    def __init__(self, settings, *args, **kwargs):
        super(AmagamaServer, self).__init__(*args, **kwargs)
        self.config.from_pyfile(settings)
        self.tmdb = tmdb.TMDB(self)

        # Chris: added for testing only
        # A simple local cache to help speed up imports
        from werkzeug.contrib.cache import SimpleCache
        #current_app.cache = SimpleCache(threshold=100000)
        self.cache = SimpleCache(threshold=100000)
        # Chris: end testing

def amagama_server_factory():
    app = AmagamaServer("settings.py", __name__)
    app.register_blueprint(webapi.module, url_prefix='/tmserver')
    app.secret_key = "foobar"
    try:
        # Chris: this tries to make a local desktop UI from the Flask app?
        import webui
        app.register_blueprint(webui.module, url_prefix='')
    except ImportError:
        logging.debug("The webui module could not be imported. The web interface is not enabled.")
    return app
