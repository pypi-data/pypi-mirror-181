"""
Created on 2022-09-07

@author: wf
"""
import argparse
import socket
import typing
from jpcore.justpy_app import JustpyServer

def Demo(wp_func: typing.Callable, path_endpoint_pairs=[], startup_func=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default=JustpyServer.getDefaultHost())
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    import justpy as jp
    app = jp.build_app(startup_func=startup_func)
    app.add_jproute("/", wp_func)
    for path, endpoint in path_endpoint_pairs:
        app.add_jproute(path, endpoint)
    
    jp.launch_uvicorn_webserver(app, host=args.host, port=args.port)
