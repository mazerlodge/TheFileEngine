#!/usr/bin/python

import sys
from ArgTools import ArgParser

class TheFileEngine:

	# Setup variables
	bInitOK = False
	bInDebug = False
	action = "NOT_SET"
	inputFile = "NOT_SET" 
	outputDirectory = "NOT_SET"

	def __init__(self,args):
		if (self.parseArgs(args)):
			self.bInitOK = True
		else:
			print("Init failed in argument parser.")
			
	def showUsage(self):
		print("Usage: python tfe.py -action [verifyfile | ...] -infile filename -outdir directory {-debug}\n")
		
	def parseArgs(self,args):
		# Parse the arguments looking for required parameters.
		# Return false if any tests fail.

		subtestResults = []
		rval = True

		# Instantiate the ArgParser
		ap = ArgParser(args)
		
		# check for optional debug flag
		self.bInDebug = ap.isInArgs("-debug", False)

		# check for action
		self.action = "NOT_SET"
		rv = False
		if (ap.isInArgs("-action", True)):
			# action value must appear after target
			self.action = ap.getArgValue("-action")
			rv = True
		subtestResults.append(rv)

        # check for input filename
		if (ap.isInArgs("-infile", True)):
			# filename value must appear after target
			self.inputFile = ap.getArgValue("-infile")
			rv = True
		subtestResults.append(rv)

        # check for output directory
		if (ap.isInArgs("-outdir", True)):
			# filename value must appear after target
			self.outputDirectory = ap.getArgValue("-outdir")
			rv = True
		subtestResults.append(rv)

		# Determine if all subtests passed
		for idx in range(len(subtestResults)):
			if (self.bInDebug):
				print "Arg subtest " + str(subtestResults[idx])
			rval = rval and subtestResults[idx]
				
		return(rval)
	
	def getInputFileLines(self):

		# Read the dictionary
		file = open(self.inputFile, "r")
		lines = file.readlines()
		file.close()
	
		return(lines)


	def showMsg(self, msg, bQuiet):
		if (not bQuiet):
			print(msg)

	def doVerifyFile(self):

		# get the input lines 
		lines = self.getInputFileLines()

		# TODO: process the lines, categorizing them based on expected patterns. 
		print "Found [%d] lines." % len(lines)

		
	def doAction(self):
	
		if (self.bInDebug):
			print "doAction: Processing action [%s]" % self.action
	
		# determine which action to execute
		if (self.action == "verifyfile"):
			self.doVerifyFile()
	
    
	
	
	


