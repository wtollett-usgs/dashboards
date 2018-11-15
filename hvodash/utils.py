# -*- coding: utf-8 -*-
import json
import pandas as pd
import requests

from datetime import datetime
from flask import request
from functools import wraps
from requests.auth import HTTPBasicAuth
from .server import server
from time import mktime


def get_url(path):
    """Expands the an internal URL to include prefix the app is mounted at"""
    base_path = server.config['URL_BASE_PATHNAME']
    return f"{base_path}{path}"


def component(func):
    """Decorator to help vanilla functions as pseudo Dash Components"""
    @wraps(func)
    def function_wrapper(children=None, **kwargs):
        # remove className and style args from input kwargs so the component
        # function does not have to worry about clobbering them.
        className = kwargs.pop('className', None)
        style = kwargs.pop('style', None)

        # call the component function and get the result
        result = func(children=children, **kwargs)

        # now restore the initial classes and styles by adding them
        # to any values the component introduced

        if className is not None:
            if hasattr(result, 'className'):
                result.className = f'{className} {result.className}'
            else:
                result.className = className

        if style is not None:
            if hasattr(result, 'style'):
                result.style = style.update(result.style)
            else:
                result.style = style

        return result
    return function_wrapper


def api_request_to_json(qry):
    url = f'https://hvo-api.wr.usgs.gov/api/{qry}'
    u = request.authorization.username
    p = request.authorization.password
    r = requests.get(url, auth=HTTPBasicAuth(u, p))
    return json.loads(r.content)


def starttime_str_to_seconds(st):
    num = int(st[1:-1])
    period = st[-1]
    if period == 'i':
        return num * 60
    elif period == 'h':
        return num * 60 * 60
    elif period == 'd':
        return num * 60 * 60 * 24
    elif period == 'w':
        return num * 60 * 60 * 24 * 7
    elif period == 'm':
        return num * 60 * 60 * 24 * 30
    elif period == 'y':
        return num * 60 * 60 * 24 * 365


def json_to_dataframe(st, jdata):
    data = pd.read_json(jdata)
    if data.empty:
        return data
    else:
        td = pd.Timedelta(seconds=starttime_str_to_seconds(st))
        return data[(datetime.now() - data.date) < td]


def date_to_j2k(dt):
    return (mktime(dt.timetuple())) - 946728000
