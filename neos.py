#!/usr/bin/python3

import argparse
from netmiko import ConnectHandler
from netmiko.ssh_exception import *
import subprocess
import os
import sys
import getpass
import socket
from timeit import default_timer as timer
import time

parser = argparse.ArgumentParser()
parser.add_argument("--hostfile", "-hf", required=True, help="Hosts file directory")
parser.add_argument("--vendor", "-v", required=True, help="Select the vendor [hp/cisco]")
parser.add_argument("--config", "-c", required=True, help="Configuration file")
parser.add_argument("--log", "-l", action='store_true', help="Save logs")
args = parser.parse_args()

start = timer()
current_device = {
                'device_type':'',
                'ip':'',
                'username':'',
                'password':'',
                'verbose':'True'
                }

vendor = {
         'cisco':'cisco_ios',
         'hp':'hp_comware'
         }

class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def check_files():
    '''
       Checks if the path to the hostfile and the configuration file exists.
       If it dosn't, the program will exit.
    '''
    os.system("clear")
    if os.path.exists(args.hostfile) is False:
        print("Error : Cannot find the hostfile specified : ", args.hostfile, ".")
        exit(1)
    if os.path.exists(args.config) is False:
        print("Error : Cannot find the configuration file specified : ", args.config, ".")
        exit(1)

def check_vendor():
    '''
        Checks if the vendor argument given by the user exist. If it does, we
        fill the 'device_type' key in the 'current_device' dictionnary.
    '''
    flag = False
    for key in vendor.keys():
        if key == args.vendor:
            flag = True
    if not flag:
        print("Unknow vendor : '", args.vendor, "'.")
        exit(1)
    if args.vendor == 'hp':
        current_device['device_type'] = vendor['hp']
    elif args.vendor == 'cisco':
        current_device['device_type'] = vendor['cisco']

def check_hosts():
    '''
       Checks if the hosts are reachable and if SSH port is open.
    '''
    port = 22
    print("**************************************************************")
    print(color.BOLD + "Checking hosts availability..." + color.END)
    print("**************************************************************")
    print("\n")
    with open(args.hostfile) as hf:
        for host in hf:
            s = socket.socket()
            host = host[:-1]
            address = socket.gethostbyname(host)
            try:
                s.connect((address, port))
                print("[", host, "]" + color.GREEN +  " UP" + color.END)
                s.close()
            except socket.error as e:
                print(host, " host is not responding. Please check the connectivity.")
                exit(1)
            except socket.gaierror as d:
                print("DNS cannot resolve hostname : ", host, ".")
                exit(1)

def user_login():
    '''
       Prompt for the username/password.
    '''
    username = input("\nUsername: ")
    password = getpass.getpass()
    current_device['username'] = username
    current_device['password'] = password
    print("")

def command_exec():
    '''
       Execute commands on every hosts present in the hostfile. We handle connectivity
       and authentication problems with exceptions from netmiko. If the user have used
       "--log", NEOS will create the log file.
    '''
    try:
        with open(args.hostfile) as hf:
            for line in hf:
                print("**************************************************************")
                print("Processing on : " + color.BOLD + line + color.END)
                print("**************************************************************")
                print("")
                current_device['ip'] = line[:-1]
                net_connect = ConnectHandler(**current_device)
                time.sleep(1)
                output = net_connect.send_config_from_file(args.config)
                print(output)
    except NetMikoTimeoutException:
        print("Connexion to ", line, " timed out. Please check the connectivity.")
    except AuthenticationException:
        print("Authentication failed : the username and/or password are incorrect.")
    end = timer()

    print("")
    print("**************************************************************")
    print(color.BOLD + "Time elapsed : ", end - start, " seconds." + color.END)
    print("**************************************************************")
    if args.log is True:
        os.system("touch NEOS_$(date +%F_%H_%M_%S)")
        os.system("chmod 770 NEOS_$(date +%F_%H_%M_%S)")
        # We use subprocess.Popen to remove 'b' and '\n' characters from the echo output.
        log_filename = subprocess.Popen("echo NEOS_$(date +%F_%H_%M_%S)", shell=True, stdout=subprocess.PIPE).communicate()[0].decode('utf-8').strip()
        with open(log_filename, 'w') as f:
            f.write(output)


def main():
    check_files()
    check_vendor()
    check_hosts()
    user_login()
    command_exec()

if __name__ == '__main__':
    main()
