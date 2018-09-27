#!/usr/bin/env python
"""
NB: CLI NOTE YET IMPLMENTED!
Usage:
    wonky run [--config]
    wonky configure [--data_folder --archive_folder]
    wonky archive <name> [--project]
Options:
 -h --help  Show this screen
 --version  Show version
 -- 
"""
from docopt import docopt
import sys
if __name__ == "__main__": 
    ascii_art = """
                      __           
__  _  ______   ____ |  | _____.__.
\ \/ \/ /  _ \ /    \|  |/ <   |  |
 \     (  <_> )   |  \    < \___  |
  \/\_/ \____/|___|  /__|_ \/ ____|
                   \/     \/\/     
 \n\n"""
    print(ascii_art)
    #todo: I have not yet implemented the doc options 
    arguments = docopt(__doc__, version='0.14.0')
    print(arguments)