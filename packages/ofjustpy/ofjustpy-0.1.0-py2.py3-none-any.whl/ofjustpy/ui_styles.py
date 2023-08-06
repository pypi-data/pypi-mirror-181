import os
from . import snowsty as snow
from . import chartjssty as chartjs
from . import monalwikisty as monalwiki
from . import versasty as versa
from . import basesty
styles = {'snow': snow,
            'chartjs': chartjs, 
          'monalwiki': monalwiki, 
          'versa': versa
          }


sty = styles['snow']

if 'WFSTY' in os.environ:
    sty = styles[os.environ['WFSTY']]
    print ("using sty  = ", sty)

def set_style(label='snow'):
    global sty
    sty = styles[label]


def check_style():
    print(sty)
