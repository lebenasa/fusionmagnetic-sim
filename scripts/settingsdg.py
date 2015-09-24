# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 09:42:40 2015

@author: leben
Console dialog to edit settings
"""

import os
import settings
from utility import formats

def promptSettings():
    s = settings.Settings()
    mainPage = """
    === EDIT DIRECTORY SETTINGS ===
    Current settings are:
    App             : {app}
    Working folder  : {wd}
    Output folder   : {outdir}
    Output name     : {outname}
    Extenstion      : {ext}
    Use timestamp   : {timestamp}
    
    Options:
    {BOLD}1{ENDC}   Set root directory (will update other parameters relative
                    to this directory)
    {BOLD}2{ENDC}   Set application path
    {BOLD}3{ENDC}   Set output folder
    {BOLD}4{ENDC}   Set output file's name
    {BOLD}5{ENDC}   Set output file's extension
    {BOLD}6{ENDC}   Toggle adding timestamp to output file's name
                    (to prevent overwrite)
    {BOLD}q{ENDC}   Save and exit
    """[1:-1]

    opt = ''
    while opt != 'q':
        print mainPage.format(app=s.app, wd=s.root, outdir=s.outdir,
                              outname=s.outfile, ext=s.outext, 
                              timestamp=s.appendDateToOutFile, **formats)
        opt = raw_input('>>> ')
        if opt == '1':
            path = raw_input('Root directory:\n')
            if os.path.exists(path):
                s.root = path
                s.default()
            else:
                print "Unable to find {path}".format(path=path)
        elif opt == '2':
            path = raw_input('Application file path:\n')
            if os.path.exists(path):
                s.app = path
            else:
                print "Unable to find {path}".format(path=path)
        elif opt == '3':
            path = raw_input('Enter output folder path:\n')
            if path != '':
                s.outdir = path
        elif opt == '4':
            name = raw_input('Enter output file name signature:\n')
            if path != '':            
                s.outfile = name
        elif opt == '5':
            ext = raw_input('Enter output file extenstion:\n')
            if path != '':
                s.outext = ext
        elif opt == '6':
            use = raw_input('Add timestamp to filename? (Y/n)\n')
            if use == 'Y' or use == 'y':
                s.appendDateToOutFile = True
            else:
                s.appendDateToOutFile = False
                
    s.save()

if __name__ == '__main__':
    promptSettings()

















