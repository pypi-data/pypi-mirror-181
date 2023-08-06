import ofjustpy as oj
import justpy as jp
from py_tailwind_utils import *
from addict import Dict

def wp_hello_world(request):
    session_id = request.session_id
    session_manager = oj.get_session_manager(session_id)
    stubStore = session_manager.stubStore
    with oj.sessionctx(session_manager):
        with session_manager.uictx("header") as headerCtx:
            title_ = oj.Title_("title", "A hello world page", pcp=[bg/pink/"100/20"])
        with session_manager.uictx("body") as bodyCtx:
            body_ = oj.Halign_(
                oj.Prose_("greeting", "Hello world! This page was written using ofjustpy python  framework ", pcp=[fz.lg, shadow._, shadow/gray/400, ta.center]), pcp=[mr/st/8]
                )
        with session_manager.uictx("footer") as bodyCtx:
            footer_ = oj.Halign_(
                oj.Prose_("depart", "Thats all folks! Hope you got the broad drift of this framework", pcp=[mr/st/64, ta.right]), "end"
                )
        oj.Container_("tlc",
                          cgens = [title_,
                                   body_,
                                   footer_],
                          pcp=[H/"screen", bg/gray/"100/20"])
        wp = oj.WebPage_("wp_hello_world",
                         cgens= [stubStore.tlc],
                             title="Readme demo page")()

        return wp

app = oj.build_app()
app.add_jproute("/", wp_hello_world)
