#! /usr/bin/env python
import sys
import os 
import errno
# import glob
# import shutil
# from random import choice
import re
import unittest
import random

program_name = "examplify"
program_directory = "." + program_name
config_directory = "config"
config_filename=[ ".wizzy-config", ".examplify" ]
script_name=program_name


list_of_regex = {
	':?port: [0-9]*' : ':port: 123456',
	'port [ =0-9]*' : 'port = 123456',
	':address: [a-zA-Z0-9.\"]*': ':address: example',
	':from: [a-zA-Z.@\"\-]*': ':from: example@example.com',
	':subject: [a-zA-Z.@\"\-\ ]*': ':from: example@example.com',
	':username: [a-zA-Z.@\"\-\0-9_]*': ':username: username_example',
	':password:[ a-zA-Z.@\"\-\0-9_]*' : ':password: password_example',
	'host = [a-zA-Z0-9.\"]*' : 'host = example.example.it'
}


# def getListOfFilesToCache():
# 	#from .wizzy-config
# 	l = list()
# 	f = open(config_filename, 'r')
# 	for line in f:
# 	    l.append(line.rstrip('\r\n'))
# 	return l

# def isModified(f):
# 	if not os.path.exists(os.path.abspath(f)) :
# 		# file removed?
# 		return True
# 	if os.stat(f).st_mtime == os.stat(os.path.abspath(program_directory)+"/"+os.path.basename(f)).st_mtime :
# 		return False
# 	else :
# 		return True

# def ignore():
# 	# Adding files to .gitignore
# 	if not "."+program_name in open(".gitignore").read():
# 		# must add to .gitignore
# 		f = open(".gitignore",'a')
# 		f.write(str("#  Ignore "+program_name+" configuration \n"))
# 		f.write(str("."+program_name+"\n"))
# 		f.write(str(script_name+"\n"))
# 		f.write(str(config_filename+"\n"))
# 	else :
# 		# already added
# 		pass
# 	print getStartMessage() + getInfoMessage(" .. and only wizards can see "+program_name+ " files now! ")
# def install():
# 	print getStartMessage()+ getInfoMessage("Making "+program_name+ " directory..")
# 	# Create wizzy cache directory
# 	try:
# 	    os.makedirs(program_directory)
# 	except OSError, e:
# 	    if e.errno != errno.EEXIST:
# 	    	# If is not a already exists error
# 		    raise
  
#     # Fill wizzy dir with files specified in .wizzy-config
# 	print getStartMessage()
# 	for element in  getListOfFilesToCache():
# 		if  not glob.glob(os.path.abspath(element)):
# 			#The file(s) are in the .wizzy-config but not on the os !
# 			print getStartMessage()+getFailMessage(" Oh snap! Someone made "+element+" disappear! Can you check the "+config_filename+" for missing files?")
# 		for files in glob.glob(os.path.abspath(element)):
# 			print getInfoMessage("	Caching "+files+ " ..")
# 			shutil.copy2(files, os.path.abspath(program_directory))

# def fix():
# 	if os.listdir(program_directory):
# 		print getStartMessage()
# 		for element in  getListOfFilesToCache():
# 			for files in glob.glob(os.path.abspath(element)):
# 				# if the file is modified since last magic, copy the cached version
# 				if isModified(files) :
# 					if os.path.exists(files):
# 						# Override file
# 						os.remove(files)
# 					shutil.copy2(program_directory+"/"+os.path.basename(files), os.path.dirname(files))
# 					print getInfoMessage("	"+files+"? ")+getMagicMessage(getRandomMagicWord())
# 				else :
# 					print getInfoMessage("	"+files+"? ")+getFailMessage("No magic needed here..") 
# 		install()		
# 	else:
# 		print getStartMessage()+ getFailMessage("No cache found ! Have you tried to install "+ program_name + "?!\n Try with '" + program_name + " install'. ")

# def clear():
# 	try:
# 		for files in os.listdir(program_directory):
# 			os.remove(os.path.abspath(program_directory +"/"+files))
# 		print getStartMessage()+getInfoMessage(" All "+program_name+" files? PUFF..") 
# 	except OSError, e:
# 		print getStartMessage()+getFailMessage(" Oh snap! My magic wand is probably broken .. ") 
# 		raise

# def untrack():
# 	for element in  getListOfFilesToCache():
# 		for files in glob.glob(os.path.abspath(element)):
# 			command = 'git update-index --assume-unchanged ' + files
# 			child = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE)
# 			while True:
# 				out = child.stderr.read(1)
# 				if out == '' and child.poll() != None:
# 					break
# 				if out != '':
# 					sys.stdout.write(out)
# 					sys.stdout.flush()

# def track():
# 	for element in  getListOfFilesToCache():
# 		for files in glob.glob(os.path.abspath(element)):
# 			command = 'git update-index --no-assume-unchanged ' + files
# 			child = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE)
# 			while True:
# 				out = child.stderr.read(1)
# 				if out == '' and child.poll() != None:
# 					break
# 				if out != '':
# 					sys.stdout.write(out)
# 					sys.stdout.flush()

# :?port: [0-9]*

def file_to_string(file):
	# Get a file and return a string that contains the file
	f = open(file, 'r')
	string = f.read()
	f.close()
	return string

def apply_regex(string):
	new_string = string
	for regex in list_of_regex:
		rex =  re.compile(regex)
		new_string = rex.sub(list_of_regex[regex], new_string)
	return new_string

class TestSequenceFunctions(unittest.TestCase):

	def test_apply_regex(self):
		# Test port regex
		# 1) perfect match
		self.assertEqual(apply_regex(":port: 25"),list_of_regex[':?port: [0-9]*'])
		# 2) blank spaces before or after
		self.assertEqual(apply_regex(" :port: 25")," "+list_of_regex[':?port: [0-9]*'])
		self.assertEqual(apply_regex(":port: 25 "),list_of_regex[':?port: [0-9]*']+" ")
		# 3) string instead of number on the port
		self.assertNotEqual(apply_regex(":port: example "),list_of_regex[':?port: [0-9]*']+" ")
		# 4) port with equal sign
		self.assertEqual(apply_regex("port = 25 "),list_of_regex['port [ =0-9]*'])

		# Test address
		self.assertEqual(apply_regex(":address: \"string\""),list_of_regex[':address: [a-zA-Z0-9.\"]*'])
		self.assertEqual(apply_regex(":address: \"string\""),list_of_regex[':address: [a-zA-Z0-9.\"]*'])
		# number instead of string
		self.assertEqual(apply_regex(":address: 1234"),list_of_regex[':address: [a-zA-Z0-9.\"]*'])

		#Test from
		self.assertEqual(apply_regex(':from: unife@unife.it'),list_of_regex[':from: [a-zA-Z.@\"\-]*'])
		self.assertEqual(apply_regex(':from: "unife@unife.it"'),list_of_regex[':from: [a-zA-Z.@\"\-]*'])

		#Test subject
		self.assertEqual(apply_regex(':subject: this is a subject'),list_of_regex[':subject: [a-zA-Z.@\"\-\ ]*'])
		self.assertEqual(apply_regex(':subject: "this is a subject"'),list_of_regex[':subject: [a-zA-Z.@\"\-\ ]*'])

		#Test username
		self.assertEqual(apply_regex(':username: "my_username_has_numb3r5"'),list_of_regex[':username: [a-zA-Z.@\"\-\0-9_]*'])
		
		#Test password
		self.assertEqual(apply_regex(':password: test'),list_of_regex[':password:[ a-zA-Z.@\"\-\0-9_]*'])
		self.assertNotEqual(apply_regex('password: test'),list_of_regex[':password:[ a-zA-Z.@\"\-\0-9_]*'])

		# Test host
		self.assertEqual(apply_regex('host = dbrails.test.it'),list_of_regex['host = [a-zA-Z0-9.\"]*'])
		


def examplify(file):
	try:
		originalString = file_to_string(file)
		print apply_regex(originalString)
	except Exception as detail :
		print str(detail)
		exit(1)
	# Copy the file in a string




def exec_arg(argv):
	if len(argv) == 1:
		# examplify
		print "Exec examplify from " + str(config_filename)
	elif (len(argv) == 2 and (argv[1]=="test" )):
		# run some tests
		suite = unittest.TestLoader().loadTestsFromTestCase(TestSequenceFunctions)
		unittest.TextTestRunner(verbosity=2).run(suite)

	else:
		# examplify < file1, file2 >
		for f in argv[1:] :
			examplify(f)

exec_arg(sys.argv)
