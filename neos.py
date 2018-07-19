#!/usr/bin/python3.5
# coding: utf-8

from netmiko import *
from netmiko.ssh_exception import *
from socket import gethostbyname, gaierror
from timeit import default_timer as timer
import subprocess
import argparse
import os
import sys
import socket
import time
import config
import yaml
import color
import layout

# Start the timer
start = timer()
# Init argparse
parser = argparse.ArgumentParser()
parser.add_argument("--hostfile", "-hf", required=True, help="Hosts file directory")
parser.add_argument("--commands", "-c", required=True, help="Commands file")
parser.add_argument("--log", "-l", action='store_true', help="Save logs")
parser.add_argument("--normalmode", "-nm", action='store_true', help="Normal mode")
args = parser.parse_args()
# CONST
DIR_HOSTS = "hosts/" + args.hostfile
DIR_COMFILE = "commands/" + args.commands
DIR_LOG = "logs/"
DIR_HOSTFILE= "hosts/"
# Open host yaml file
y = yaml.load(open(DIR_HOSTS))

def log(result):
    '''
        Create a log file if the user use "-l" argument.
        He'll be save in /logs directory.
    '''
    # Create log file on /logs directory and make it writeable
    os.system("touch " + DIR_LOG +  "NEOS_$(date +%F_%H_%M_%S)")
    os.system("chmod 770 " + DIR_LOG + "NEOS_$(date +%F_%H_%M_%S)")
    # Get the log filename. We use subprocess.Popen to remove 'b' and '\n' characters from the echo output.
    log_filename = subprocess.Popen("echo " + DIR_LOG +  "NEOS_$(date +%F_%H_%M_%S)", shell=True, stdout=subprocess.PIPE).communicate()[0].decode('utf-8').strip()
    # Write output in the logfile.
    with open(log_filename, 'w') as f:
        f.write(result)
    print(color.GREEN + "\nLog file have been saved as '", log_filename, "'" + color.END)

def check_files():
    '''
       Checks if the path to the hostfile and the command file exists.
       If it doesn't, the program will exit.
    '''
    if os.path.exists(DIR_HOSTS) is False:
        print(color.RED + "Error : Cannot find the hostfile specified : ", args.hostfile, "." + color.END)
        sys.exit()
    if os.path.exists(DIR_COMFILE) is False:
        print(color.RED + "Error : Cannot find the command file specified : ", args.commands, "." + color.END)
        sys.exit()

def check_hosts():
    '''
       Checks if the hosts are reachable and if SSH port is open.
    '''
    layout.header_host()
    for device_name in y:
        s = socket.socket()
        try:
            address = y[device_name]['ip']
            s.connect((address, config.port))
            print("[", device_name, "]" + color.GREEN +  " UP" + color.END)
        except socket.error:
            print(color.RED + "'", device_name, "' host is not responding. Please check the connectivity." + color.END)
            sys.exit()
        finally:
            s.close()

def command_exec():
    '''
       Execute commands on each hosts present in the hostfile. We handle connectivity
       and authentication problems with exceptions from netmiko. If the user have used
       "--log", NEOS will create the log file.
    '''
    output = ''
    current_log= ''
    try:
        for device_name in y:
            current_device = y[device_name]
            layout.header_processing(device_name)
            net_connect = ConnectHandler(**current_device)
            if args.normalmode is False:
                net_connect.config_mode()
            with open (DIR_COMFILE) as cf:
                for command in cf:
                    output = net_connect.send_command(command)
                    print(output)
                    if args.log is True:
                        h = layout.header_log(device_name, command)
                        current_log = current_log + h + output
        net_connect.disconnect()
    except NetMikoTimeoutException:
        print(color.RED + "Connexion to ", line, " timed out. Please check the connectivity." + color.END)
    except AuthenticationException:
        print(color.RED + "Authentication failed : the username and/or password are incorrect." + color.END)
    finally:
        # Stop the timer.
        end = timer()
        # Display the time elapsed.
        layout.time_elapsed(end)
        # If the user have used '-l' argument, then we saved the output on a logfile.
        if args.log is True:
            log(current_log)

def main():
    check_files()
    check_hosts()
    command_exec()

if __name__ == '__main__':
    main()
