#!/usr/bin/python3.5
# coding: utf-8

import color

def header_host():
     print("**************************************************************")
     print(color.BOLD + "Checking hosts availability..." + color.END)
     print("**************************************************************")
     print("\n")
def header_processing(device):
     print("**************************************************************")
     print("Processing on : " + color.BOLD + device + color.END)
     print("**************************************************************")
     print("")
def header_log(device, command):
     # Keep off '\n' characters
     device = device.replace('\n','')
     command = command.replace('\n','')
     h = ("\n\n############ Processing on : " + device + " [COMMAND : " + command, "] ############\n\n")
     # Transform tuple in str
     h = ''.join(h)
     # Return a single line string
     return(h)
def time_elapsed(end):
     print("")
     print("**************************************************************")
     print(color.BOLD + "Time elapsed : ", end - start, " seconds." + color.END)
     print("**************************************************************")

