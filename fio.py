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
#  Aug 29, 2018
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
import dfvs
import platform
import threading
import struct
import Queue

_sentinel = object()
global end_flag
end_flag = 0 
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
    #out = process.communicate()
    #print ("out->", out)
    time.sleep(10) # wait for marvo to overwrite old log file.
    with open(os.path.join(os.getcwd(), "FIOresult.log"),'r') as processLog:
        print("Check")
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
    # Move logs from current path to Logs folder.
    final_log_name = os.path.abspath(log_temp_folder).replace("logs", logCount+"FIO")
    os.rename(log_temp_folder, final_log_name)
    #logname = os.path.join(logDir, logname).replace("FIOresult", logCount+"FIO") #script name : FIOresult.log transfer to logname 1_FIO.log
    subprocess.check_call(["mv", final_log_name, log_final_folder])

class dfvs_dev():
    def __init__(self):
       self.dev_name = sys.argv[2] #'tcp://10.25.132.130:5555'
       self.baudrate = 115200
       self.token_file = './Tokens.dat'
       self.fw_log = './fio_pi.log'
       self.en_fw_print = True
       self.en_detoken  = True
       self.en_fw_timestamp = True
       self.dev_h = 0
       self.tcp_ip = '10.25.132.130'
       self.tcp_port = 5555
       self.remote_dev = '/dev/ttyUSB1'
       self.ssh_user = 'pi'
       self.ssh_passwd = sys.argv[3] #'123456'
       self.q = Queue.Queue()

    def dev_open(self):
       self.dev_h = dfvs.DevOpen(self.dev_name, self.baudrate, self.token_file, self.fw_log, self.en_fw_print, self.en_fw_timestamp, self.en_detoken)
       assert self.dev_h, 'Failed to open device {}.'.format(self.dev_name)

    def dev_write(self, cmd):
        cmd = cmd + '\r'
        dfvs.DevWrite(self.dev_h, cmd.encode("utf-8"))

    def dev_close(self):
        dfvs.DevClose(self.dev_h)
        self.dev_h = 0
        
    def exec_ssh_cmd(self, cmd):
        self.ssh_h = dfvs.SshOpen()
        ret = dfvs.SshAuthorize(ssh_h=self.ssh_h, ip_addr = self.tcp_ip, username=self.ssh_user, password=self.ssh_passwd)
        assert ret == True, "SSH: Failed to create the connection to {}.".format(self.tcp_ip)
        remote_cmd = cmd
        ret = dfvs.SshExecCmd(ssh_h=self.ssh_h, cmd=remote_cmd)
        assert ret == True, "SSH: Failed to execute the command {}.".format(remote_cmd)
        dfvs.SshClose(self.ssh_h)
        self.ssh_h = None
 
    def start_remote_uart(self):
        remote_cmd = 'pkill -9 socat;socat {0},b{1},ispeed={1},raw,echo=0 tcp-listen:{2},keepalive > /dev/null 2>&1 &'.format(self.remote_dev, self.baudrate, self.tcp_port)
        self.exec_ssh_cmd(remote_cmd)
 
    def reset_board(self):
        remote_cmd = 'python ~/script/poweron_reset.py'
        self.exec_ssh_cmd(remote_cmd)
        time.sleep(2)
        
    def set_normal_mode(self):
        remote_cmd = 'python ~/script/normal_mode.py'
        self.exec_ssh_cmd(remote_cmd)
        
    def set_rom_mode(self):
        remote_cmd = 'python ~/script/uart_mode.py'
        self.exec_ssh_cmd(remote_cmd)

    def wait_keyword(self, keyword, timeout):
        start = time.time()
        while(time.time() - start < timeout):
            res = dfvs.DevRead(self.dev_h, 1, 10)
            if res == '' or res is None:
                continue
            if res.find(keyword) != (-1):
                return 0
        return (-1)

    def set_detoken(self, en_detoken):
        dfvs.SetDetoken(self.dev_h, en_detoken)

    def dev_read(self):
        while True:
            res = dfvs.DevRead(self.dev_h, 1, 10)
            print(res)
            if end_flag == 1:
                print("Break the read loop")
                break                        

if __name__ == "__main__":
    if len(sys.argv) < 4: #if len is smaller than 4, it means there are no arguments.
        print ('The correct format should be -> python fio.py config_file device(ex. tcp://10.85.149.105:5555) password(ex. marvell).')
        sys.exit()

    #create the object 
    uart = dfvs_dev()
    # uart.ssh_passwd = "marvell"
    # check the remote uart types
    if uart.dev_name.find('tcp://') != (-1):
        uart.tcp_ip = uart.dev_name.split('//')[1].split(':')[0]
        if len(uart.dev_name.split('//')[1].split(':')) > 1:
            uart.tcp_port = uart.dev_name.split('//')[1].split(':')[-1]
        uart.dev_name = 'tcp://{0}:{1}'.format(uart.tcp_ip, uart.tcp_port)
        uart.remote_dev = '/dev/ttyUSB1'
        uart.start_remote_uart()
        if platform.system() == 'Windows' and uart.ssh_passwd == '':
            print("Error, the login password for raspberry Pi not specified.")
            sys.stdout.flush()
            exit(1)

    if uart.dev_name.find('uart://') == (-1) and uart.dev_name.find('tcp://') == -1:
        print("Error, device name {} incorrect.".format(uart.dev_name))
        sys.stdout.flush()
        exit(-1)

    # open device and enable the log display.
    uart.en_fw_print = True
    uart.en_fw_timestamp = True
    dfvs.SetLogLevel(3)
    time.sleep(2)
    uart.en_detoken = True
    uart.dev_open()

    logname = "FIOresult.log"
    result_summary = "fio_summary.log"

    # create destination folder for stored the final summary. 
    log_temp_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "logs")
    if not os.path.exists(log_temp_folder):
        os.makedirs(log_temp_folder)

    # create destination folder for stored the final summary. 
    log_destination_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Logs")
    if not os.path.exists(log_destination_directory):
        os.makedirs(log_destination_directory)

    print ("Start doing FIO testing.")    
    pi_log_record = threading.Thread(target = uart.dev_read, args = ())
    pi_log_record.setDaemon(True)
    pi_log_record.start()
    runfioScript(sys.argv[1])
    
    #assert uart.wait_keyword('nvme0n1', 180)== 0, "Fail in the disk status."
    check_script(logname, result_summary, "nvme0n1")
    subprocess.check_call(["mv",os.path.join(os.getcwd(), logname), log_temp_folder])
    subprocess.check_call(["mv",os.path.join(os.getcwd(), result_summary), log_temp_folder])
    subprocess.check_call(["mv",os.path.join(os.getcwd(), uart.fw_log), log_temp_folder])
    
    # get the counts of the existing files in logs folder. It aims to rename the folder.
    log_counts_createdinfolder = str(len(os.listdir(log_destination_directory))+1)+"_"  
    move_output(log_temp_folder, log_counts_createdinfolder, log_destination_directory)
    end_flag = 1
    time.sleep(3)
    print("FIO testing is done")
    uart.dev_close()