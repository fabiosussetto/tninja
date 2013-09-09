"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['src/templater/Jinseng.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'packages': ['jinja2'],
    'iconfile': 'res/app-icon.icns'
}

setup(
    app=APP,
    # data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    packages=['templater', 'jinja2', 'markupsafe'],
    package_dir={
        'templater': 'src/templater',
        'jinja2': 'src/lib/jinja2',
        'markupsafe': 'src/lib/markupsafe'
    },
    data_files=[
        ('', ['src/templater/server.py']),
        ('assets', ['src/templater/assets/index.html', 'src/templater/assets/app.js', 'src/templater/assets/app.css'])
    ],
    # package_data={'templater': ['assets/*']},
    setup_requires=['py2app'],
)
