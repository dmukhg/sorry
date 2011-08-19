#! /usr/bin/env python

# This program is to be run from the command line.

import sys
import os
import dispatch

if __name__ == "__main__":
    cwd = os.getcwd() 

    if len(sys.argv) is 1:
        # no arguments have been supplied. revert to assuming the
        # current dir is the sorry dir
        sorry_dir = cwd
    else:
        sorry_dir = os.path.join(cwd, sys.argv[1])

    print "Assuming \"%s\" as the project directory." %sorry_dir
    
    # init directory locations
    deploy_dir = os.path.join(sorry_dir, 'deploy')
    media_dir = os.path.join(sorry_dir, 'media')
    media_deploy_dir = os.path.join(deploy_dir, 'media')

    dispatch.cleardirectory(deploy_dir)
    print "Cleared deploy_dir : %s" % deploy_dir

    dispatch.mediacopy(media_dir, media_deploy_dir)
    print "Copied files from %s to %s" % (media_dir, media_deploy_dir)

    dispatch.sitegen(sorry_dir)
