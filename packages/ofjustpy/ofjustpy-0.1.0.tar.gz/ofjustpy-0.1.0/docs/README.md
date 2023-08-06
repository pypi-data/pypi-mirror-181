# [Ofjustpy](https://github.com/Monallabs-org/ofjustpy)

Ofjustpy is an extension and wrapper to [Justpy-Svelte](https://github.com/Monallabs-org/justpy-svelte) -- a  webdevelopment framework in python. Ofjustpy offers several enhancments to Justpy. Most prominent
being that ofjustpy enables a functional bottom-up approach toward building a webpage.
The claim is that  this leads to a simpler more intutive codebase along with better resuablity.
Additionally, it  provides
1. hooks that automatically track all the created components 
2. a mechanisum to organize components within a non-dom hierarchical context
3. use svelte as the underlying frontend javascript engine 
4. ability to build higher order components using ofjustpy framework, tailwind and svelte. 
5. Tailwind tags are first class python expressions allowing complex manipulation of styles.


## Description/Usage 
### A demo example -- for the impatient ones
```python
import ofjustpy as oj
from py_tailwind_utils import *
from addict_tracking_changes import Dict

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

```

The webpage will be rendered as:

![Hello world page screenshot](/demos/ofjustpy_hello_world.png?raw=true "Optional Title")

The key takeaway is that the webpage is build bottom up. First, the most atomic components are declared. 
Then higher order components are declared that contain previously declared component. The components are weaved together at the last step when the webpage instance is requested. 

See here(todo) for a more comprehensive demo that showcases all the basic (or html components) and higher order components built using tailwind and svelte.


### Advanced notes
1. Checkout ![htmlcomponents](/ofjustpy/htmlcomponents.py) to see the list all htmlcomponent supported and handling events
2. 
3. checkout ofjustpy-extn for more advanced components (such as json navigator) build using ofjustpy (**coming up**)


4. **Coming soon: A comprehensive tutorial/guide**

### EndNotes
- Homepage: webworks.monallabs.in/ofjustpy
- Developed by: webworks.monallabs.in
- Source Code: https://github.com/Monallabs-org/ofjustpy

