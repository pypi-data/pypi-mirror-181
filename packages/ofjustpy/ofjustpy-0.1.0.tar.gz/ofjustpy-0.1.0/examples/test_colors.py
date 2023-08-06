
from py_tailwind_utils import *
import ofjustpy as oj
from addict_tracking_changes import Dict
def on_btn_click(dbref,msg):
    pass


all_colors = [slate , gray , zinc , neutral , stone , red , orange , amber , yellow , lime , green , emerald , teal , cyan , sky , blue , indigo , violet , purple , fuchsia , pink , rose]

def launcher(request):
    session_manager = oj.get_session_manager(request.session_id)
    with oj.sessionctx(session_manager):
        all_btns = [ oj.StackW_(f"colorrow{cp}",
                                cgens = [oj.Button_("mybtn:{cp}{k}",
                                            value="myval",
                                            pcp=[bg/cp/k]).event_handle(oj.click, on_btn_click)
                                         for k in range(100,1000,100)
                                 ]
                                )
                     for cp in all_colors]
        panel_ = oj.Halign_(oj.StackV_(
            "mystackv", cgens=all_btns))

        wp_ = oj.WebPage_("oa", cgens =[panel_], template_file='svelte.html', title="myoa")

        wp = wp_()
    return wp

#jp.Route("/", launcher)

app = oj.build_app()
app.add_jproute("/", launcher)

# request = Dict()
# request.session_id = "abc"

# app = jp.app
# jp.justpy(launcher, start_server=False)
# from starlette.testclient import TestClient
# client = TestClient(app)
# response = client.get('/') 
