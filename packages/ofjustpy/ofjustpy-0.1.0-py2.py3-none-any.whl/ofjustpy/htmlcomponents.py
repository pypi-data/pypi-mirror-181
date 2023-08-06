import traceback
import sys
import logging
import sys
if sys:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
import collections
from itertools import chain
from aenum import Enum
from typing import List, AnyStr, Callable, Any
from addict_tracking_changes import Dict
import justpy as jp
from .ui_styles import basesty, sty
from py_tailwind_utils import (tstr,
                           W,
                           full,
                           jc,
                           twcc2hex,
                           bg,
                           onetonine,
                           fz,
                           get_color_instance,
                           outline,
                           offset,
                           black,
                           outline,
                           green,
                           W,
                           conc_twtags,
                           hidden,
                           db,
                           invisible
                           )

from .tracker import trackStub
from dpath.util import set as dset, search as dsearch
from .dpathutils import dget, dnew
import traceback
import types
from .ofjustpy_utils import traverse_component_hierarchy
from .data_validator import validate, InputRequired
StubFunc_T = Callable[Any, Any]

#https://stackoverflow.com/questions/44664040/type-hints-with-user-defined-classes/44664064#44664064
from typing import Type

class EventType(Enum):
    click = "click"
    mouseover = "mouseover"
    mouseout = "mouseout"
    mouseenter = "mouseenter"
    mouseleave = "mouseleave"
    input = "input"  # input is keyword of python
    change = "change"
    submit = "submit"


class Nav(jp.Nav):
    """

    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.spathMap = Dict(track_changes=True)

    def addItems(self, cgens):
        collections.deque(map(lambda cgen: cgen(self), cgens), maxlen=0)
        for stub in cgens:
            self.spathMap[stub.spath] = stub.target
    def getItem(self, stub):
        return self.spathMap[stub.spath]

class Footer(jp.Footer):
    """

    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.spathMap = Dict(track_changes=True)

    def addItems(self, cgens):
        collections.deque(map(lambda cgen: cgen(self), cgens), maxlen=0)
        for stub in cgens:
            self.spathMap[stub.spath] = stub.target
    def getItem(self, stub):
        return self.spathMap[stub.spath]
    

    
        
# class HCC(jp.Div):
#     """
#     HCC: html component container
#     """

#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.spathMap = Dict(track_changes=True)

#     def addItems(self, cgens):
#         collections.deque(map(lambda cgen: cgen(self), cgens), maxlen=0)
#         for stub in cgens:
#             self.spathMap[stub.spath] = stub.target
#     def getItem(self, stub):
#         return self.spathMap[stub.spath]

# # class Li(jp.Li):
    
    

class StackG(jp.Div):
    def __init__(self, *args, **kwargs):
        num_rows = kwargs.pop('num_rows', 2)
        num_cols = kwargs.pop('num_cols', 2)
        # pcp passed via Stub gets  incorporated in twsty_tags in genStubFunc
        twsty_tags = kwargs.pop('twsty_tags', [])
        twsty_tags = [*twsty_tags, *sty.stackG(num_cols, num_rows)]
        super().__init__(*args,  twsty_tags=twsty_tags, **kwargs)


class StackD(jp.Div):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def addItems(self, cgens):
        super().addItems(cgens)
        
        for spath, dbref in self.spathMap.items():
            dbref.add_twsty_tags(hidden)

        self.selected_card_spath = cgens[0].spath
        selected_dbref = self.spathMap[self.selected_card_spath]
        selected_dbref.remove_twsty_tags(hidden)
        selected_dbref.add_twsty_tags(db.f) #TODO: only if there was flex originally
    def bring_to_front(self, spath):
        '''
        tapk: the target apk of du which needs to be brought in front
        '''

        tapk = spath  # f'{self.apk}_{tlid}'
        if tapk in self.spathMap.keys():
            #hide the current front
            self.spathMap[self.selected_card_spath].add_twsty_tags(hidden)
            #make the selected card visible
            selected_dbref = self.spathMap[tapk]
            selected_dbref.remove_twsty_tags(hidden)
            selected_dbref.add_twsty_tags(db.f)  # workaround for eat-flex bug

            self.selected_card_spath = tapk
        else:
            logger.debug(
                f"debug: deck  does not have card {tapk}..skipping bring to front")
        
        
        
class Stub:
    def __init__(self, *args, **kwargs):
        self.key = args[0]
        self.hcgen = args[1]
        self.target = None
        self.eventhandlers = {}
        self.args = args

        self.postrender = kwargs.pop('postrender', None)
        # if self.key == "wp":
        #     print(kwargs)
        self.cgens = kwargs.pop('cgens', None)
        redirects = kwargs.pop('redirects', None)
        self.redirects = None
        if redirects:
            self.redirects = Dict(redirects)
        self.get_value = kwargs.pop('get_value', None)
        
        self.kwargs = kwargs

        pass

    def get_value(self):
        if self.get_value:
            self.get_value()
        # we should fall back to target.value
        # TBD: implement it later when need arises
        assert False
        
    def update_twsty_tags(self, *args):
        twsty_tags = self.kwargs.get('twsty_tags')
        self.kwargs.update({'twsty_tags': conc_twtags(*twsty_tags,  *args)})

    def add_cgen(self, cgen):
        """
        add a component  stub to cgens
        """
        assert self.cgens is not None
        self.cgens = chain(self.cgens, [cgen])

        
    def __call__(self, a):
        # print(f"calling as function {self.id}")
        # TODO: what about other parameters
        self.target = self.hcgen(**self.kwargs, a=a, id=self.spath)

        self.target.stub = self
        if self.postrender:
            # print("call postrender ", self.key)
            self.postrender(self.target)

        # TODO: will think about this
        # self.target.postrender()

        # attach event handlers
        for event_type, handler in self.eventhandlers.items():
            if self.redirects and event_type in self.redirects:
                # self.target.on(event_type, handler)
                # call local handler
                #print ("redirecting ", event_type, " to ", self.redirects[event_type])
                self.target.on(event_type, self.redirects[event_type])
            else:
                #print ("handle event: ", event_type)
                #print ("handle event: ", handler)
                #print (self.key)
                self.target.on(event_type, handler)

        if self.cgens:
            self.target.addItems(self.cgens)
        # return anchor so that other components can hang on to it
        return a

    def event_handle(self, event_type, handler):
        self.eventhandlers[event_type.value] = handler
        return self

class WPStub(Stub):
    def __init__(self, *args,  **kwargs):
        super().__init__(*args, **kwargs)

    def __call__(self):
        """for webpage instantiation"""
        # print(f"calling as function {self.id}")
        # TODO: what about other parameters
        self.target = self.hcgen(**self.kwargs)

        self.target.stub = self
        if self.postrender:
            # print("call postrender ", self.key)
            self.postrender(self.target)

        # TODO: will think about this
        # self.target.postrender()

        # attach event handlers
        if self.cgens:

            for cgen in self.cgens:
                cgen(self.target)
        # return anchor so that other components can hang on to it
        return self.target


def genStubFunc(jpf, stytags):

    @trackStub
    def func(key: AnyStr, **kwargs):
        pcp = kwargs.pop('pcp', [])
        twsty_tags = conc_twtags(*stytags,  *pcp)
        return Stub(key, jpf, twsty_tags=twsty_tags, **kwargs)
    return func


Div_ = genStubFunc(jp.Div, sty.div)
P_ = genStubFunc(jp.P, sty.P)
Li_ = genStubFunc(jp.Li, sty.li)
Ul_ = genStubFunc(jp.Ul, sty.ul)
Ol_ = genStubFunc(jp.Ol, sty.ol)
A_ = genStubFunc(jp.A, sty.A)
Br_ = genStubFunc(jp.Br, [])
Label_ = genStubFunc(jp.Label, sty.label)
Circle_ = genStubFunc(jp.Button, sty.circle)
Span_ = genStubFunc(jp.Span, sty.span)
InputChangeOnly_ = genStubFunc(jp.InputChangeOnly, sty.input)
Input_ = genStubFunc(jp.Input, sty.input)
Td_ = genStubFunc(jp.Td, sty.td)
Divider_ = genStubFunc(jp.Hr, sty.hr)
Img_ = genStubFunc(jp.Img, sty.img)



                
# use glossy=True,
# size="sm", label=label, value =False for toggle btn
#ToggleBtn_ = genStubFunc(jp.QToggle, sty.togglebtn)
Textarea_ = genStubFunc(jp.Textarea, sty.textarea)
Option_ = genStubFunc(jp.Option, sty.option)
Container_ = genStubFunc(jp.Div, sty.container)
StackV_ = genStubFunc(jp.Div, sty.stackv)
StackH_ = genStubFunc(jp.Div, sty.stackh)
StackW_ = genStubFunc(jp.Div, sty.stackw)
StackD_ = genStubFunc(StackD, sty.stackd)
# sty will be set in StackG:init using num_rows, num_cols keyword arguments
StackG_ = genStubFunc(StackG, [])
Nav_ = genStubFunc(Nav, sty.nav)

Footer_ = genStubFunc(Footer, sty.footer)



@trackStub
def SubheadingBanner_(key: AnyStr, heading_text: AnyStr, pcp: List = [], heading_text_sty=sty.subheading_text,  **kwargs):
    # = genStubFunc(jp.Div, sty.subheading_box)
    spanl_ = Span_("headingL", text=heading_text, pcp=heading_text_sty)
    spanm_ = Span_("headingR", text=heading_text, pcp=[
        *heading_text_sty, invisible])
    spanx_ = Span_("headingR", text=heading_text, pcp=[
        *heading_text_sty, invisible])
    # spanr_ = Span_("headingR", text=heading_text, pcp=[
    #     *heading_text_sty, "invisible"])
    return Stub(key,
                jp.Div,
                twsty_tags= conc_twtags(*pcp, *sty.subheading_box),
                postrender=lambda dbref,  spanl_=spanl_, spanm_=spanm_: spanx_(spanm_(spanl_(dbref))),
                **kwargs)


@trackStub
def LabeledInput_(key: AnyStr,
                  label: AnyStr,
                  placeholder: AnyStr,
                  changeonly=True,
                  input_type="text",
                  data_validators = [],
                  pcp=[],
                  
                  **kwargs):
    span_ = Span_(f"{key}_iname", text=label, pcp=sty.span)
    if changeonly:
        input_ = InputChangeOnly_(key,
                                  placeholder=placeholder,
                                  type=input_type,
                                  data_validators=data_validators
                                  )
    else:
        input_ = Input_(key,
                        placeholder=placeholder,
                        type=input_type,
                        data_validators=data_validators
                        )
    return Stub(f"{key}_libox",
                jp.Label,
                twsty_tags=conc_twtags(*pcp, *sty.label, *sty.default_border),
                #postrender=lambda dbref, span_=span_, input_=input_: input_(span_(dbref)),
                cgens = [span_, input_],
                get_value = lambda : input_.target.value
                )

@trackStub
def Checkbox_(key:AnyStr, label:AnyStr, pcp=[], cbox_attrs={}, span_attrs={}, **kwargs):
    #TODO: 'form-checkbox'
    cbox_ = Input_(f"{key}cbox", type='checkbox', 
                   pcp=[], **cbox_attrs)
    span_ = Span_(f"{key}span",
                  text=label,
                  pcp=[fz.sm],
                  **span_attrs
                  )
    return Stub(key,
                jp.Label,
                twsty_tags=conc_twtags(*pcp, *sty.label),
                cgens = [span_, cbox_],
                **kwargs
                #postrender=lambda dbref, span_=span_, cbox_=cbox_: cbox_(span_(dbref))
                )
    

@trackStub
def CheckboxInput_(key: AnyStr,
                   pcp=[],
                   cbox_attrs={},
                   input_attrs={},
                   **kwargs):
    # TODO: make form-checkbox firstclass : 'form-checkbox'
    cbox_ = Input_(f"{key}cbox", type="checkbox", pcp=[], **cbox_attrs)
    input_ = InputChangeOnly_(f"{key}inp", type="text", **input_attrs)
    return Stub(key,
                jp.Label,
                twsty_tags=conc_twtags(*pcp, *sty.label),
                #postrender=lambda dbref, cbox_=cbox_, input_=input_: input_(cbox_(dbref)),
                cgens = [cbox_, input_],
                **kwargs)


#@trackStub
def Subsection_(key: AnyStr, heading_text: AnyStr, content_: Callable, pcp=[], **kwargs):
    return StackV_(key,
                   cgens=[SubheadingBanner_("heading", heading_text),
                          Halign_(content_)
                          ],
                   pcp=pcp,
                   **kwargs
                   )

def Prose_(key:AnyStr, text:AnyStr, pcp=[], **kwargs):
    return P_(key, text=text,  pcp=conc_twtags(*pcp, *sty.prose), **kwargs)
                   
def KeyValue_(key: AnyStr, keyt: AnyStr, valuet: AnyStr, readonly=True, pcp=[], **kwargs):
    key_ = Span_("keyt", text=keyt, pcp=sty.left_cell)
    eq_ = Span_("eqt", text="=", pcp=sty.eq_cell)
    value_ = Span_("valuet", type="text", text=valuet,
                   readonly=readonly, pcp=sty.right_cell)
    # TODO: overwrite xmargin. put padding only around stack
    return StackH_(key, cgens=[key_, eq_, value_], pcp=[W/full, jc.center], **kwargs)


def SubsubheadingBanner_(key: AnyStr, heading_text: AnyStr, pcp=[], **kwargs):
    return SubheadingBanner_(key, heading_text, pcp=pcp, heading_text_sty=sty.subsubheading_text, **kwargs)


def Subsubsection_(key: AnyStr, heading_text: AnyStr, content_: Callable, pcp: List = [], **kwargs):
    return StackV_(key,
                   cgens=[SubsubheadingBanner_("heading", heading_text),
                          Halign_(content_, align="center")],
                   pcp=pcp,
                   **kwargs)


def Barpanel_(key: AnyStr, pcp: List= [], **kwargs):
    return StackH_(key, pcp=conc_twtags(*sty.barpanel, *pcp), **kwargs)

def WithBanner_(key: AnyStr, banner_text: AnyStr, component_: Callable, pcp: List = [], **kwargs):
    return StackH_(key,
                   cgens=[Valign_(Span_("banner", text=banner_text)), component_],
                   pcp=pcp, **kwargs)




@trackStub
def Halign_(content_: Callable, align="center", pcp=[], key=None, **kwargs):
    """
    tstub: target stub, i.e., the one needs to be aligned
    """
    if not key:
        key = f"Halign{content_.key}"
        
    return Stub(key,
                jp.Div,
                twsty_tags=conc_twtags(*sty.halign(align), *pcp),
                cgens = [content_],
                #postrender=lambda dbref, tstub=content_: tstub(dbref),
                **kwargs)

@trackStub
def Valign_(content_: Callable, align="center", pcp=[], key=None, **kwargs):
    """
    tstub: target stub, i.e., the one needs to be aligned
    """
    if not key:
        key = f"Halign{content_.key}"
    return Stub(key,
                jp.Div,
                twsty_tags=conc_twtags(*sty.valign(align), *pcp ),
                cgens  = [content_],
                #postrender=lambda dbref, tstub=content_: tstub(dbref),
                **kwargs
                )

@trackStub
def Align_(content_: Callable, halign="center",  valign="center", key = None, pcp=[], **kwargs):
    """
    tstub: align vertically and horizontally
    """
    if not key:
        key = f"align{content_.key}"
    return Stub(key,
                jp.Div,
                twsty_tags=conc_twtags(*sty.align(halign, valign), *pcp),
                cgens=[content_],
                #postrender=lambda dbref, tstub=content_: tstub(dbref),
                **kwargs)



@trackStub
def ExpansionContainer_(key: AnyStr, label: AnyStr, content_: AnyStr, pcp: List=[]):
    return Stub(key, jp.QExpansionItem,
                twsty_tags=conc_twtags(*sty.expansion_container, *pcp),
                cgens=[content_],
                dense=True,
                header_class='bg-grey-1',
                label=label
                )


def SubTitle_(key:AnyStr, title_text:AnyStr, pcp=[], align="center", **kwargs):
    return Halign_(Span_(key,
                         text=title_text,
                         pcp=conc_twtags(*sty.subtitle_text, *pcp)
                         ),
                   align=align)



# TODO: implement default value
def Title_(key:AnyStr, title_text:AnyStr, pcp=[], align="center", **kwargs):
    return Halign_(Span_(key,
                         text=title_text,
                         pcp=conc_twtags(*sty.title_text, *pcp)
                         ),
                   align=align)
                   

@trackStub
def Slider_(key: AnyStr, itemiter: List, pcp: List = [], **kwargs):
    def on_circle_click(dbref, msg):
        # print("circle clicked with value ", dbref.text,
        #       " ", msg.value, " ", dbref.slider)
        # pass the value of selected circle to slider
        dbref.slider.value = msg.value
        slider = dbref.slider
        #TODO: what is slider.selecte_circle evaluating to
        if slider.selected_circle is not None:
            slider.selected_circle.remove_twsty_tags(outline/offset/2, outline/black/0, outline/2, outline.double)

        slider.selected_circle = dbref
        slider.selected_circle.add_twsty_tags(outline/offset/2, outline/black/0, outline/2, outline.double)

        # slider.selected_circle.set_class("outline-black")
        # slider.selected_circle.set_class("outline-2")
        # slider.selected_circle.set_class("outline-double")
        
        pass
    circle_stubs = [Circle_(f"{key}_c{_}", text=str(_), value=_).event_handle(
        EventType.click, on_circle_click) for _ in itemiter]

    def postrender(dbref, circle_stubs=circle_stubs):
        for cs in circle_stubs:
            cs(dbref)
            cs.target.slider = dbref
        dbref.circle_stubs = circle_stubs
        dbref.selected_circle = None
    # return Stub(key, jp.Div, twsty_tags=[*pcp, *sty.slider], postrender=lambda dbref, circle_stubs=circle_stubs: [_(dbref) for _ in circle_stubs])
    # The click on Slider should come to this function; its value updated then passed to user

    def on_click_hook(dbref, msg):
        msg.value = dbref.value
        if 'click' in dbref.stub.eventhandlers:
            dbref.stub.eventhandlers['click'](dbref, msg)
        pass
    stub = Stub(key,
                jp.Div,
                twsty_tags=conc_twtags( *sty.slider, *pcp),
                postrender=postrender, redirects=[('click', on_click_hook)],
                **kwargs)
    stub.circle_stubs = circle_stubs
    return stub


def MainColorSelector_(key: AnyStr, **kwargs):
    color_list = twcc2hex.keys()
    all_options = [Option_(f"{key}_opt_{option}", text=option, value=option, pcp=[bg/sty.get_color_tag(option)/5])
                   for option in color_list]
    return Select_(key, all_options, value="rose", **kwargs)


@trackStub
def ColorSelector_(key: AnyStr, pcp: List = [], **kwargs):
    def on_main_color_select(dbref, msg):
        # pass the selection to parent component
        #traceback.print_stack(file=sys.stdout)

        dbref.colorSelector.maincolor_value = msg.value
        colortag = sty.get_color_tag(dbref.colorSelector.maincolor_value)
        dbref.colorSelector.component_clicked = 'mainColorSelector'
        pass
    mainColorSelector_ = MainColorSelector_(f"{key}_MCS").event_handle(
        EventType.click, on_main_color_select)

    def on_slider_select(slider, msg):
        # whatever value is computed pass to colorselector
        # pass the selection to parent component
        slider.colorSelector.slider_value = int(msg.value)
        slider.colorSelector.component_clicked = 'slider'

    shades_ = Slider_(f"{key}_Shades", range(1, 10)).event_handle(
        EventType.click, on_slider_select)

    def update_slider(colortag, shades_=shades_):

        for cs in shades_.circle_stubs:
            cref = cs.target
            shid = int(cref.value)
            #cref.twcc = f"{colortag}-{shid}00"
            # TODO: also update twsty_tags
            #print("update slider = ", f"bg-{colortag}-{shid}00")
            #cref.set_class(f"bg-{colortag}-{shid}00")
            new_color = bg/get_color_instance(colortag)/shid
            cref.add_twsty_tags(new_color)


    def update_selected_shade():
        pass
    
    def postrender(dbref):
        dbref.addItems([Halign_(mainColorSelector_), Halign_(shades_)])
        shades_.target.colorSelector = dbref
        mainColorSelector_.target.colorSelector = dbref
        dbref.maincolor_value = "blue"
        dbref.slider_value = 5  # the default value
        dbref.component_clicked = None
        dbref.shades_ = shades_
    def on_click_hook(dbref, msg):

        main_color = dbref.maincolor_value

        match dbref.component_clicked:
            case 'mainColorSelector':
                update_slider(dbref.maincolor_value)
            case None:
                pass
            case 'slider':
                shade = dbref.slider_value
                msg.value = twcc2hex[main_color][onetonine[shade]]
                update_selected_shade()
                if 'click' in dbref.stub.eventhandlers:
                    dbref.stub.eventhandlers['click'](dbref, msg)
    # TODO: fix spacing
    # TODO: event handling
    # return StackH_(key, cgens=[mainColorSelector_, shades_])
    return Stub(key,
                jp.Div,
                twsty_tags=conc_twtags( *sty.stackv, *sty.default_border, *pcp),
                postrender=postrender,
                redirects=[('click', on_click_hook)],
                **kwargs)


# TODO: toggleBtn, expansionContainer

# TODO: check event_handle for form
@trackStub
def Form_(key: AnyStr,
          content_: Callable,
          submit_: Callable,
          cgens:List = [], 
          pcp: List = [],
          form_type = jp.Form,
          **kwargs):
    def postrender(dbref):
        # c(dbref)
        # s(dbref)
        pass

    stubStore = kwargs.get('stubStore', None)
    
    def on_submit_validate_hook(dbref, msg):
        #print ("validate before calling submit: ")
        success = True
        # a dict to store all the inputs and their values
        form_inputs_value_dict = Dict()
        for cpath, citem, pitem in traverse_component_hierarchy(dbref):
            # print ("cpath, citem =", cpath, citem)

            if citem.stub.hcgen in [jp.InputChangeOnly, jp.Input]:
                #print ("cpath, citem =", cpath, citem)
                
                if 'data_validators' in citem.stub.kwargs:
                    #print ("got data validators ")
                    data_validators = citem.stub.kwargs.get('data_validators')
                    if not validate(data_validators, citem.value, stubStore):
                        success = False
                    form_inputs_value_dict[citem.stub.key] = citem.value

                    
                    
        # call the actual registered handler
        if success:
            dbref.stub.eventhandlers['submit'](dbref, msg, form_inputs_value_dict)
        else:
            print ('failure during validation..not invoking submit function')
            
        
    return Stub(key,
                jp.Form,
                cgens = [*cgens, content_, submit_],
                twsty_tags=conc_twtags(*sty.form, *pcp),
                redirects=[('submit', on_submit_validate_hook)],
                #postrender=postrender,
                **kwargs)


@trackStub
def Button_(key: AnyStr, icon_f: Callable = None, pcp: List = [], cgens = [], **kwargs):
    postrender = None
    if icon_f:
        def postrender(dbref, icon_f=icon_f): return icon_f(dbref)
    return Stub(key,
                jp.Button,
                twsty_tags=conc_twtags(*sty.button, *pcp),
                postrender=postrender,
                cgens = cgens,
                **kwargs)

# seriously wrong with select -- default val is not working


@trackStub
def Select_(key: AnyStr, options: List, pcp: List = [], **kwargs):
    """
    to use default option, pass it to kwargs as  value. 

    When an item is selected from a select ui element, the element
    itself is altered. Its state has changed. So it needs 
    to be re-rendered. Often the rendering looses information 
    about what the user has selected. The on_click_hook fixes 
    that. 
    """
    def on_click_hook(dbref, msg):
        print("in selector: on_click_hook ")
        dbref.value = msg.value
        if 'click' in dbref.stub.eventhandlers:
            dbref.stub.eventhandlers['click'](dbref, msg)
            
    return Stub(key,
                jp.Select,
                twsty_tags=conc_twtags(*sty.select, *pcp),
                postrender=lambda dbref: [_(dbref) for _ in options],
                redirects=[('click', on_click_hook)],
                **kwargs
                )
 
# TODO: how to deal with events at Div level

@trackStub
def Tr_(key, cgens, isodd=True, pcp=[], **kwargs):
    return Stub(key,
                jp.Tr,
                twsty_tags=conc_twtags(*sty.tr[isodd], *pcp),
                postrender=lambda dbref, cgens=cgens: [_(dbref) for _ in cgens],
                **kwargs)


@trackStub
def Table_(key, cgens, pcp=[], **kwargs):
    return Stub(key,
                jp.Table,
                twsty_tags=conc_twtags(*sty.tbl, *pcp),
                postrender=lambda dbref, cgens=cgens: [_(dbref) for _ in cgens],
                **kwargs
                )

@trackStub
def InputJBtn_(key: AnyStr, input_: Callable,  button_: Callable, pcp=[], **kwargs):
    """
    Put an input next to button
    """

    return Stub(key,
                jp.Div,
                twsty_tags=conc_twtags(*sty.centering_div, *sty.spacing, *pcp),
                postrender=lambda dbref, input_=input_, button_=button_: button_(input_(dbref),
                                                                                 **kwargs)
                )



# class StackV(HCC):
#     def __init__(self, key, **kwargs):
#         super().__init__(key, sty.stackv, **kwargs)
# TwContainer_ = genStubFunc(jp.Div, sty.container)

# def Circle_(*args, **kwargs):
#     pcp = kwargs.pop('pcp')
#     twsty_tags = [*sty.circle,  *pcp]
#     return Stub(args[0], jp.Button, *args[1:], twsty_tags=twsty_tags, **kwargs)


# class Circle(jp.Button):
#     def __init__(self,  key, text, *args, **kwargs):
#         pcp = kwargs.pop('pcp')
#         twsty_tags = [*sty.circle,  pcp]
#         super().__init__(classes=tstr(*twsty_tags),
#                          text=text, value=text, twsty_tags=twsty_tags, **kwargs)

# short tag for htmlcomponents




@trackStub
def WebPage_(key: AnyStr,  head_html_stmts: List[AnyStr] = [], cgens: List = [], WPtype: Type[jp.WebPage] = jp.WebPage, pcp = [], **kwargs):
    """
    WPtype: the WebPage class, either jp.WebPage or derived from it, jp.QuasarPage, or ojr.WebPage, 
    """
    assert not isinstance(cgens, types.GeneratorType)
    def postrender(wp, cgens=cgens):
        # TODO: declare session manager here
        #wp.tailwind = False  # we inject our tailwind
        # not yet able to inject our own tailwind
        wp.tailwind = True  # we inject our tailwind

        wp.head_html = "\n".join(head_html_stmts)
        #tailwind comes bundled with svelte
        # wp.head_html = "\n".join([*head_html_stmts,
        #                           """<link rel = "stylesheet" href = "https://cdn.jsdelivr.net/npm/inter-ui@3.13.1/inter.min.css" > """,
        #                           """ <script src = "https://cdn.tailwindcss.com/" > </script >"""
        #                           ])
        # wp.head_html = "\n".join(head_html)
        wp.css = 'body { font-family: Inter; }'
        wp.body_classes = tstr(*wp.twsty_tags)



    stub = WPStub(key,
                  WPtype,
                  twsty_tags=conc_twtags(*sty.wp, *pcp),
                  postrender=postrender,
                  cgens=cgens,
                  **kwargs)
    
    # if page_type == 'tailwind':
    #     stub = WPStub(key, WPtype, twsty_tags=[
    #         *sty.wp], postrender=postrender, cgens=cgens, **kwargs)
    # elif page_type == 'quasar':
    #     stub = WPStub(key, jp.QuasarPage, twsty_tags=[
    #         *sty.wp], postrender=postrender, cgens=cgens,  **kwargs)
    return stub


