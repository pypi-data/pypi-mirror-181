
#from .ofjustpy import SF
__version__ = "0.1.0"
from justpy import build_app
from .icons import chevronright_icon, minus_icon, cog_icon, menu_icon
from .tracker import get_session_manager, sessionctx


from .htmlcomponents import (EventType,
                             Circle_,
                             Halign_,
                             Span_,
                             A_,
                             P_,
                             Form_,
                             StackV_,
                             StackH_,
                             StackW_,
                             StackG_,
                             SubheadingBanner_,
                             Subsection_,
                             SubsubheadingBanner_,
                             Subsubsection_,
                             WithBanner_,
                             Label_,
                             Button_,
                             InputChangeOnly_,
                             Input_,
                             LabeledInput_,
                             CheckboxInput_,
                             Textarea_,
                             KeyValue_,
                             Option_,
                             Select_,
                             InputJBtn_,
                             Slider_,
                             ColorSelector_,
                             WebPage_,
                             Container_,
                             #ToggleBtn_,
                             Title_,
                             SubTitle_,
                             Prose_,
                             ExpansionContainer_,
                             Table_,
                             Td_,
                             Tr_,
                             Checkbox_,
                             StackD_,
                             Nav_,
                             Div_,
                             Footer_,
                             Divider_,
                             Li_,
                             Ul_,
                             Ol_,
                             Br_,
                             Img_,
                             Align_,
                             Barpanel_,
                             Valign_
                             )


from .dpathutils import dget, dnew, dpop, dupdate, dpath_delete as ddelete, dset, dsearch, PathNotFound, walker as dictWalker

from .ofjustpy_utils import get_svelte_safelist, csrfprotect

from . import data_validator as validator

from . import app_code_introspect as aci

mouseover = EventType.mouseover
click = EventType.click
mouseenter = EventType.mouseenter
mouseout = EventType.mouseout
mouseleave = EventType.mouseleave
input = EventType.input
change = EventType.change
submit = EventType.submit
