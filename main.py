#!/usr/bin/python3
import argparse
from netmiko import ConnectHandler
from subprocess import Popen, PIPE, STDOUT
import os
import sys
import time
import getpass
import socket

ROOT_DIR = "/root/project/pythonprojet/"

parser = argparse.ArgumentParser()
parser.add_argument("--hostfile", "-hf", required=True, help="directory of host file")
parser.add_argument("--vendor", "-v", required=True, help="Choose the vendor : 'hp' or 'cisco'")
parser.add_argument("--config", "-c", required=True, help="configuration file")
args = parser.parse_args()

currentDevice = {
                'device_type':'',
                'ip':'',
                'username':'',
                'password':''
                }

vendor = {
         'cisco':'cisco_ios',
         'hp':'hp_comware'
         }

def check_files():
    '''On vérifie que les fichiers 'host' et 'configuration file' existent. Si l'un des
       deux ne l'est pas, le programme s'arrête.
    '''
    if os.path.exists(args.hostfile) is False:
        print("Le chemin vers le fichier hosts n'a pas était trouvé...")
        exit(1)
    if os.path.exists(args.config) is False:
        print("Le chemin vers le fichier de configuration n'a pas était trouvé...")
        exit(1)

def check_vendor():
    """ On check si le vendor que l'utilisateur a envoyé est bien existant.
        Si le vendor est existant dans le dictionnaire 'vendor', le programme
        continue, sinon il s'arrête.
    """
    flag = False
    for key in vendor.keys():
        if key == args.vendor:
            flag = True
    if not flag:
        print("Le vendor est inconnu... Le programme va s'arrêter.")
        exit(1)
    if args.vendor == 'hp':
        currentDevice['device_type'] = vendor['hp']
    elif args.vendor == 'cisco':
        currentDevice['device_type'] = vendor['cisco']

def check_hosts():
    """ On vérifie si les hosts présent dans le fichier 'hosts' sont bien UP, sinon on
        arrête le programme. On ouvre un socket 's', puis on se connecte à l'hôte sur le port
        22. Si l'hôte est UP, et que le service aussi, alors on considère qu'il est prêt à être
        configuré.
    """
    port = 22
    print("\nVérification de la disponibilité des hôtes...\n")
    with open(args.hostfile) as hf:
        for host in hf:
            s = socket.socket()
            address = socket.gethostbyname(host[:-1])
            try:
                s.connect((address, port))
                print("[", host[:-1], "] UP")
                s.close()
            except socket.error as e:
                print(host[:-1], " ne répond pas... Le programme s'arrête.")
                exit(1)
            except socket.gaierror as d:
                print("Le DNS n'arrive pas à résoudre l'hôte : ", host[:-1])

def user_login():
    username = input("\nUsername: ")
    password = getpass.getpass()

    currentDevice['username'] = username
    currentDevice['password'] = password

def commandExec ():
        #config_commands = []

        # On charge les commandes issue du commutateur '-c'  dans la liste 'config_commands'

        #with open(args.config) as configFile:
        #    for line in configFile:
        #        config_commands.append(line[:-1])

        # On execute device by device

        try:
            with open(args.hostfile) as hf:
                for line in hf:
                    currentDevice['ip'] = line[:-1]
                    print(currentDevice)
                    net_connect = ConnectHandler(**currentDevice)
                    time.sleep(2)
                    output = net_connect.send_config_from_file(args.config)
                    print(output)
        except:
            print("Les identifiants sont incorrectes ! ")
def main():
    check_files()
    check_vendor()
    check_hosts()
    user_login()
    commandExec()

if __name__ == '__main__':
    main()
