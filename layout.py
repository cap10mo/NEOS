#!/usr/bin/python3.5
# coding: utf-8

import color

def header_host():
     print("\n")
     print("**************************************************************")
     print(color.BOLD + "Checking hosts availability..." + color.END)
     print("**************************************************************")
     print("\n")
def header_processing(device):
     print("\n")
     print("**************************************************************")
     print("Processing on : " + color.BOLD + device + color.END)
     print("**************************************************************")
     print("\n")
def header_log(device):
     # Keep off '\n' characters
     device = device.replace('\n','')
     h = ("############ Processing on : " + device + "############")
     # Transform tuple in str
     h = ''.join(h)
     # Return a single line string
     return(h)
def time_elapsed(end, start):
     print("\n")
     print("**************************************************************")
     print(color.BOLD + "Time elapsed : ", end - start, " seconds." + color.END)
     print("**************************************************************")
     print("\n")
