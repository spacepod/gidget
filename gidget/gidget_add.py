# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
# -*- mode: python; indent-tabs-mode nil; tab-width 4; python-indent 4; -*-

"""
usage: gidget add data <filename>
       gidget add reference <filename>    

"""

from docopt import docopt


if __name__ == '__main__':
    print(docopt(__doc__))
