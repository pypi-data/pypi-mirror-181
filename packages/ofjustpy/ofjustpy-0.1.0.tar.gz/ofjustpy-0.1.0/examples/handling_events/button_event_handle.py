"""
drop down color not working in firefox
"""
import logging
import os

if os:
    try:
        os.remove("launcher.log")
    except:
        pass

import sys
if sys:
    FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
    logging.basicConfig(filename="launcher.log",
                        level=logging.DEBUG, format=FORMAT)

    
from py_tailwind_utils import *
import ofjustpy as oj
from addict import Dict

app = oj.build_app()

def on_btn_click(dbref,msg):
    print ("btn clicked ")
    pass

def launcher(request):
    session_manager = oj.get_session_manager(request.session_id)
    with oj.sessionctx(session_manager):
        btn_ = oj.Button_("mybtn",
                   value="myval",
                          text="Click me ",   pcp=[bg/blue/"100/50"]).event_handle(oj.click, on_btn_click)

        wp_ = oj.WebPage_("oa", cgens =[btn_], template_file='svelte.html', title="myoa")
        wp = wp_()
    return wp

#jp.Route("/", launcher)

app.add_jproute("/", launcher)

#jp.justpy(launcher, start_server=False)
