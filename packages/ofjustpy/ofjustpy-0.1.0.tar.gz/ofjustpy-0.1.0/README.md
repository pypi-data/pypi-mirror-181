# Ofjustpy: A functional webframework built using justpy
is extension to [justpy-svelte](https://github.com/Monallabs-org/justpy-svelte) -- a  webdevelopment framework in python (for more details see). Ofjustpy provides opinionated components which can be chained via functional paradigm. Additionally, it  provides
1. hooks that track all the created components 
2. organize components in a hierarchical context
3. use svelte as the underlying frontend javascript engine 
4. several higher order components build using ofjustpy framework, tailwind and svelte. 
5. Tailwind tags are first class python expressions, instead of a long string. 

## Description/Usage 
### A demo example -- for the impatient ones
```python
import ofjustpy as oj
import justpy as jp
from tailwind_tags import *


@jp.SetRoute("/hello_world")
def wp_hello_world(request):
    session_id = request.session_id
    session_manager = oj.get_session_manager(session_id)
    stubStore = session_manager.stubStore
    with oj.sessionctx(session_manager):
        with session_manager.uictx("header") as headerCtx:
            title_ = oj.Title_("title", "A hello world page", pcp=[bg/pink/"100/20"])
        with session_manager.uictx("body") as bodyCtx:
            body_ = oj.Halign_(
                oj.Prose_("greeting", "Hello world! This page was written using ofjustpy python  framework ", pcp=[fz.lg, bsw._, sw/gray/400, ta.center]), pcp=[mr/st/8]
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
                         template_file='svelte.html',
                             title="a svelte page")()

        return wp

app = jp.app
jp.justpy(wp_hello_world, start_server=False)
```

The webpage will be rendered as:

![Hello world page screenshot](/demos/ofjustpy_hello_world.png?raw=true "Optional Title")

The key takeaway is that the webpage is build bottom up. First, the most atomic components are declared. 
Then higher order components are declared that contain previously declared component. The components are weaved together at the last step when the webpage instance is requested. 

See here(todo) for a more comprehensive demo that showcases all the basic (or html components) and higher order components built using tailwind and svelte.

### Advanced notes
1. Checkout ![htmlcomponents](/ofjustpy/htmlcomponents.py) to see the list all htmlcomponent supported
2. 
3. checkout ofjustpy-extn for more advanced components (such as json navigator) build using ofjustpy


Finally, if you are looking for a more detailed/comprehensive guide/tutorial, raise an issue and we can discuss there. 

### EndNotes
- docs (in readthedocs format): https://github.com/Monallabs-org/ofjustpy  
- Developed by: webworks.monallabs.in
