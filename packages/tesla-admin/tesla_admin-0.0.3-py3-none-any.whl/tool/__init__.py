import click
import os
# import sys







@click.group()
def supercli():
    click.echo('''
            Tesla Admin CLI
            ...............
            
            Enjoy, ;)   
               
               ''')
    pass


@supercli.command()
@click.option('-n', '--name', type=str, help='Name of directory', prompt='project name')
def startproject(name):
    click.echo(f'creating a new project {name}' )

    
    CORE_FOLDER = name + '/core/'
    MANAGE_FILE =  name + '/manage.py'

    SETTINGS_FILE = CORE_FOLDER + 'settings.py'
    URL_FILE = CORE_FOLDER + 'urls.py'
    os.makedirs(CORE_FOLDER)
    with open(SETTINGS_FILE, 'a+') as s_f:
        s_f.write('''
 
from tesla.static import staticfiles
from tesla import TeslaApp

from a.models import User

import os
from pathlib import Path as Pa

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Pa(__file__).resolve().parent.parent 

TeslaApp.auth_model = User
TeslaApp.middlewares.set_middlewares([])


MIDDLEWARES = []

staticfiles.path = os.path.join(BASE_DIR, 'static_')
    ''')
    with open(MANAGE_FILE, 'a+') as m_f:
        m_f.write('''
def main(*args, **kwargs):
    from tesla import TeslaApp
    import core.settings
    import core.urls
    
    
    
    return TeslaApp(*args, **kwargs)


if __name__ == '__main__.py':
    main()
            ''')
    open(URL_FILE, 'a+')
    
@supercli.command()
@click.option('-n', '--name', type=str, help='Name of application', prompt='application name')
def startapp(name):
    click.echo(f'creating a new application {name}' )
    APP = f'./{name}/'
    URL_FILE = APP + 'urls.py'
    VIEWS = APP + 'views.py'
    MID = APP + 'middleware.py'
    MODELS = APP + 'models.py'
    os.makedirs(APP)
    
    with open(URL_FILE, 'a+') as u_f:
        u_f.write('''
from tesla.router import Path
from . import views

# your urls path should be here
patterns = []
                  ''')
    
    with open(VIEWS, 'a+') as v_f:
        v_f.write('''
from tesla.auth.decorators import login_required
from tesla.auth.views import login
from tesla.response import HttpResponse, Redirect, Render, JsonResponse
from tesla.pyhtml import CT

# your views
                  ''')
       
    with open(MID, 'a+') as m:
        pass
    
    with open(MODELS, 'a+') as m:
        m.write(
            '''
from tesla.auth.modal import UserBaseModal
from tesla.modal import Model
from dataclasses import dataclass
            
            '''
        )
        pass 
   
@supercli.command()
@click.argument('port', default=8000)        
def serve(port = 8000):
    click.echo('Starting the developing server')
    os.system(f'waitress-serve --listen=*:{port} manage:app')       
            