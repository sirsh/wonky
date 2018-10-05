#!/usr/bin/env python
"""
Usage:
    __main__.py archive <name> [--force]
    __main__.py run <config_file_name>
    __main__.py configure [--data_folder] 
 
Options:
 -h --help  Show this screen
 --version  Show version
"""
import wonky
from docopt import docopt
import sys

@wonky.dispatch.on('archive')
def archive(**kwargs):
    print('archiving item...')

@wonky.dispatch.on('run')
def run(**kwargs):
    pass
    #print('running '+str(kwargs["config_file_name"]))

@wonky.dispatch.on('configure')
def configure(**kwargs):
    print('config')

if __name__ == "__main__": 
    ascii_art = """
                      __           
__  _  ______   ____ |  | _____.__.
\ \/ \/ /  _ \ /    \|  |/ <   |  |
 \     (  <_> )   |  \    < \___  |
  \/\_/ \____/|___|  /__|_ \/ ____|
                   \/     \/\/     
 """
    print(ascii_art)
    a = wonky.dispatch(__doc__,version='0.14.0')
    #todo - implement the various dispatchers for CLI mode