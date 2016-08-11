"""
Routes and views for the bottle application.
"""

from bottle import route, view, static_file
from datetime import datetime
import os

@route('/')
@route('/home')
@view('index')
def home():
    """Renders the home page."""
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    return static_file("index.html",root= os.path.join(PROJECT_ROOT, 'static').replace('\\', '/'))

@route('/contact')
@view('contact')
def contact():
    """Renders the contact page."""
    return dict(
        title='Contact',
        message='Your contact page.',
        year=datetime.now().year
    )

@route('/about')
@view('about')
def about():
    """Renders the about page."""
    return dict(
        title='About',
        message='Your application description page.',
        year=datetime.now().year
    )
