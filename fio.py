#!/usr/bin/python
######################################################################################################################
# Copyright (c) 2018 Marvell Semiconductor.  All Rights Reserved.
#
# The contents of this software are proprietary and confidential to Marvell Technology. and are limited in distribution
# to those with a direct need to know. Individuals having access to this software are responsible for maintaining the
# confidentiality of the content and for keeping the software secure when not in use. Transfer to any party is strictly
# forbidden other than as expressly permitted in writing by Marvell Technology.
#
# Copyright (c) 2018 Marvell Semiconductor.
#
# Version Control Information:
#
#  $Id$
#  revision: 0.1
#
#  Author:  Ocean Chiou
#
#  Aug 25, 2018
#
#####################################################################################################################
from __future__ import print_function
import sys
from datetime import datetime
import os
import re
import string
import time
import subprocess

def print_local_time(self = None):
    time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')     	
    return time

def check_script(log_name, result_file, pattern):    
    pass_flag = 0
    f_log = open(log_name.strip('\n'))
    f_result = open(result_file, "w")
    while True:
    	line = f_log.readline()
        if pattern in line:
	    pass_flag = 1
	    f_result.write("Final Result:\tPass\n")
	    break
    if pass_flag == 0:
        f_result.write("Final Result:\tFail\n")
    f_log.close()
    f_result.close()

def runfioScript(filename):	
    print("sudo " + "fio " + filename + " --output=FIOresult.log")
    process = subprocess.Popen(["sudo", "fio", filename, "--output=FIOresult.log"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = process.communicate()
    print ("out->", out)
    time.sleep(30) # wait for marvo to overwrite old log file.
    with open(os.path.join(os.getcwd(), "FIOresult.log"),'r') as processLog:
	#output something approx every minute only
	count = 0
	while(process.poll() == None):
			entry = processLog.readline()
			if("PERF" in entry and count > 0):
				count -= 1
			elif("PERF" in entry and count <= 0):
				print (entry, end='') #only print one out of 60 performance logs
				count = 60
			elif(entry):#always print non performance logs
				print (entry, end='')
				count = 0
			else:#if no output
				time.sleep(0.5)
				try:
					sys.stdout.flush()
				except:
					process.wait()	
		
def move_output(log_temp_folder, logCount, log_final_folder):					
	print ("count->", logCount)	
	# Move logs from current path to Logs folder.
	print (log_temp_folder)
	final_log_name = os.path.abspath(log_temp_folder).replace("logs", logCount+"FIO")
	print (log_final_folder)
	print (final_log_name)
	os.rename(log_temp_folder, final_log_name)
	#logname = os.path.join(logDir, logname).replace("FIOresult", logCount+"FIO") #script name : FIOresult.log transfer to logname 1_FIO.log
	subprocess.check_call(["mv", final_log_name, log_final_folder])
	

if __name__ == "__main__":
	if len(sys.argv) < 2: #if len is smaller than 2, it means there are no arguments.
	    print ('no fio config behind, the correct format should be -> python fio.py xxxxx (config file).')
	    sys.exit()
	
	logname = "FIOresult.log"
	result_summary = "fio_summary.log"
	
	#Create destination folder for stored the final summary. 
	log_temp_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "logs")
	if not os.path.exists(log_temp_folder):
	    os.makedirs(log_temp_folder)
	
	#Create destination folder for stored the final summary. 
	log_destination_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Logs")	
	if not os.path.exists(log_destination_directory):
	    os.makedirs(log_destination_directory)	
	
	print ("Start doing FIO testing.")
	runfioScript(sys.argv[1])
	check_script(logname, result_summary, "nvme0n1")
	subprocess.check_call(["mv",os.path.join(os.getcwd(), logname), log_temp_folder])
	subprocess.check_call(["mv",os.path.join(os.getcwd(), result_summary), log_temp_folder])
	
	#Get the counts of the existing files in logs folder. It aims to rename the folder.
	log_counts_createdinfolder = str(len(os.listdir(log_destination_directory))+1)+"_"  
	move_output(log_temp_folder, log_counts_createdinfolder, log_destination_directory)
	
	print("FIO testing is done")
