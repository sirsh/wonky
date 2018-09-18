#!/usr/bin/env python

import sys

ascii_art = """

                      __           
__  _  ______   ____ |  | _____.__.
\ \/ \/ /  _ \ /    \|  |/ <   |  |
 \     (  <_> )   |  \    < \___  |
  \/\_/ \____/|___|  /__|_ \/ ____|
                   \/     \/\/     
 \n\n"""

def main(args=None):
    l= len(sys.argv)
    print(ascii_art)
    maxindex= int(sys.argv[2]) if l > 2 else None
    
    
if __name__ == "__main__":  main() 