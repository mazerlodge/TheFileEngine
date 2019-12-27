#!/usr/bin/python

import sys
from ArgTools import ArgParser

class TheFileEngine:

	# Setup variables
	bInitOK = False
	bInDebug = False
	action = "NOT_SET"
	inputFile = "NOT_SET" 
	targetPath = "NOT_SET"

	def __init__(self,args):
		if (self.parseArgs(args)):
			self.bInitOK = True
		else:
			print("Init failed in argument parser.")
			
	def showUsage(self):
		print("Usage: python tfe.py -action [verifyfile | genscript] \n" 
			  + "-infile filename -targetpath directory \n"
			  + "-outfile filename \n"
			  + "optional params: {-debug}\n")
		
	def parseArgs(self,args):
		# Parse the arguments looking for required parameters.
		# Return false if any tests fail.

		subtestResults = []
		subtestMessages = []
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
		else:
			subtestMessages.append("-action with arg is required.")
		subtestResults.append(rv)

        # check for input filename
		if (ap.isInArgs("-infile", True)):
			# filename value must appear after target
			self.inputFile = ap.getArgValue("-infile")
			rv = True
		else:
			rv = False
			subtestMessages.append("-infile with arg is required.")
		subtestResults.append(rv)

        # check for target path
		if (ap.isInArgs("-targetpath", True)):
			# filename value must appear after target
			self.targetPath = ap.getArgValue("-targetpath")
			rv = True
		else:
			if (self.action == "genscript"):
				rv = False
				subtestMessages.append("-targetpath required when -action is genscript.")
		subtestResults.append(rv)

		# Determine if all subtests passed
		for idx in range(len(subtestResults)):
			if (self.bInDebug):
				print("Arg subtest " + str(subtestResults[idx]))
			rval = rval and subtestResults[idx]

		if (rval == False):
			for idx in range(len(subtestMessages)):
				if (self.bInDebug):
					print("ArgParse message: " + str(subtestMessages[idx]))
							
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

		# Line patterns being sought. 
		targetSegments = [ "    Directory:", "Mode", "----", "d----", "-a---" ] 
		segmentTypes = ["Directory_Title", "Directory_Header", "Directory_Underline", "List_Row__Directory", "List_Row__File"]
		segmentCount = [0,0,0,0,0]

		# get the input lines 
		lines = self.getInputFileLines()

		# Process the lines, categorizing them based on expected patterns. 
		print("Found [%d] lines." % len(lines))
		
		for aline in lines:
				
			segIndex = 0
			for aseg in targetSegments:
				segLen = len(aseg)

				if (len(aline) >= segLen):	
					relevantLinePart = aline[0:segLen]
				else:
					relevantLinePart = "NOT_SET"
					continue 

				if (self.bInDebug):	
					print("Working line part=[%s] with target seg=[%s] find returned=[%d]" % \
						(relevantLinePart, aseg, relevantLinePart.find(aseg)))

				if (aline.find(aseg) == 0): 
					#print("Segment found!")
					segmentCount[segIndex] += 1
					break
				segIndex += 1

		# Reuse segIndex var to output counts by segment.
		segIndex = 0
		for atype in segmentTypes:
			print("%d = %s" % (segmentCount[segIndex], atype))
			segIndex += 1 


	def getDirFromLine(self, line, segPattern):
		
		rval = "NOT_SET" 
		
		startPos = line.find(segPattern) + len(segPattern)
		rval = line[startPos:len(line)].strip()
		
		return rval
		
	def getFilenameFromLine(self, line, segPattern):
		# given a line, extract the filename part an return it.
		# Line like:
		# -a---          6/1/2018   6:02 PM     117052 activitylogs 20185.docx                                                              
	
		rval = "NOT_SET" 
		nameParts = line.split()[5:] 
		if (len(nameParts) > 0):
			rval = ""
			for aPart in nameParts:
				rval += aPart + " "
			rval = rval.strip() 
				
		return rval
	
	def doGenScript(self): 
	
		# Line patterns being sought. 
		targetSegments = [ "    Directory:", "Mode", "----", "d----", "-a---" ] 
		segmentTypes = ["Directory_Title", "Directory_Header", "Directory_Underline", "List_Row__Directory", "List_Row__File"]
		segmentCount = [0,0,0,0,0]
		
		currentDir = "NOT_SET"
		currentDirNoDrive = "NOT_SET"
		filename = "NOT_SET" 
		slashType = "\\" 		
		baseCommandString = "echo f | xcopy '%s%s%s' '%s%s%s%s%s'"
		# Note: baseCommand in format copy currentDir/file targetBaseDir/currentDir/fileAgain

		# get the input lines 
		lines = self.getInputFileLines()
		
		for aline in lines:			
			segIndex = 0
			for aseg in targetSegments:
				if (aline.find(aseg) == 0): 
					# Segment found.
					segmentCount[segIndex] += 1
					if (segmentTypes[segIndex] == "Directory_Title"):
						currentDir = self.getDirFromLine(aline, aseg)
						currentDirNoDrive = currentDir[3:]
					
					if (segmentTypes[segIndex] == "List_Row__File"):
						filename = self.getFilenameFromLine(aline, aseg)
						print(baseCommandString % (currentDir, slashType, filename, self.targetPath, slashType, currentDirNoDrive, slashType, filename))

					break
				segIndex += 1
	
	def doAction(self):
	
		if (self.bInDebug):
			print("doAction: Processing action [%s]" % self.action)
	
		# determine which action to execute
		if (self.action == "verifyfile"):
			self.doVerifyFile()
	
		if (self.action == "genscript"):
			self.doGenScript() 
     
	
	
	


