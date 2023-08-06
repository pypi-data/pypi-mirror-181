import inspect
import justpy as jp
from aenum import Enum
import functools
import justpy as jp
from starlette.responses import JSONResponse, Response
from starlette.responses import PlainTextResponse
import uvicorn, logging, uuid, sys, os, traceback, fnmatch
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.sessions import SessionMiddleware

#app = jp.app
#app.add_middleware(GZipMiddleware) 
#app.add_middleware(SessionMiddleware, secret_key=jp.SECRET_KEY)


