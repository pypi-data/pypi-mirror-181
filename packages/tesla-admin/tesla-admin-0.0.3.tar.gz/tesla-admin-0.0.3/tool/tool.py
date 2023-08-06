import click

import os

@click.command()
def cli():
    pass


# @cli.command()
@click.option('-n', '--name', type=str, help='Name of directory', default='.')
def startproject(name):

    
    CORE_FOLDER = name + '/core/'
    MANAGE_FILE =  name + '/manage.py'

    SETTINGS_FILE = CORE_FOLDER + 'settings.py'
    URL_FILE = CORE_FOLDER + 'urls.py'
    os.makedirs(CORE_FOLDER)
    with open(SETTINGS_FILE, 'a+') as s_f:
        s_f.write('''
                
from tesla.static import staticfiles

import os
from pathlib import Path as Pa

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Pa(__file__).resolve().parent.parent 


MIDDLEWARES = []

staticfiles.path = os.path.join(BASE_DIR, 'static_')
    ''')
    with open(MANAGE_FILE, 'a+') as m_f:
        m_f.write('''
                   

from tesla import App
import core.settings
import core.urls

app = App(debug=True)

app.middlewares.set_middlewares(core.settings.MIDDLEWARES)

            ''')
    open(URL_FILE, 'a+')
 