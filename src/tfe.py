#!/usr/bin/python

# Launch point for The File Engine class.

"""
Usage: python tfe.py -action [verifyfile | ...] -infile filename -outdir directory {-debug}\n

"""

import sys
from TheFileEngine import TheFileEngine

#### EXECUTION Starts Here ####

tfe = TheFileEngine(sys.argv)

# If startup parameters are OK do action specified.
if (not tfe.bInitOK):
	tfe.showUsage()
	sys.exit()
else:
	tfe.doAction()
	
