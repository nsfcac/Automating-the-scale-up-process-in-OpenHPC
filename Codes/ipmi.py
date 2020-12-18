





'''
 to automate the process of building up a cluster through the IPMI-based method, starting with the BMC, which is to gather all the MAC addresses first and then provision the BMC with its address after shooting the node.

'''




import subprocess
import ipaddress
import codecs
import requests

import requests
import socket
import ipaddress
#import json
import datetime
import random
import time
import sys
from colorama import init
init(strip=not sys.stdout.isatty()) # strip colors if stdout is redirected
from termcolor import cprint
from pyfiglet import figlet_format




#IPMI Credential information-------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------
Pass="Zephyr"
User="root"
#----------------------------------------------------------------------------------------------------------------------

#Initilizing  c_name,c_bmc, and c_mac arrays---------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------
c_name=["?" for i in range(64)]
c_bmc=["mac" for i in range(64)]
c_mac=["" for i in range(64)]
Vendor=""
newnodes_number=0
net_interface=1
h_m_tech="ipmi"
#----------------------------------------------------------------------------------------------------------------------


#Func 1: This function is for disabling warnings in requests' vendored urllib3, (insecure request warnings)------------
#----------------------------------------------------------------------------------------------------------------------
def DisShowingInsecureWarning():
    '''
         This function is for disabling warnings in requests' vendored urllib3, (insecure request warnings.

    '''
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
#----------------------------------------------------------------------------------------------------------------------




#func 2: This function is for gatthering mac address of a machine based on its vendor type-----------------------------
#----------------------------------------------------------------------------------------------------------------------
def get_MAC(s):
    '''
          This function is for gatthering mac address of a machine based on its vendor type

    '''
#********************************************************************************
# Disable showing Insecure Warning
    DisShowingInsecureWarning()

#********************************************************************************
    output=""
    try:

         (output, err) = subprocess.Popen(s, stdout=subprocess.PIPE, shell=True).communicate()
         output=str( output)[2:-3]
         #print(output,err)


    except:
         print("problem in connecting to BMC.......")
         return("")
    return (output)

#----------------------------------------------------------------------------------------------------------------------


def create_command(vendor,i):
    command=""
    if vendor=="Dell":
         command="ipmitool -H  "+c_bmc[i-1]+"  -U "+User+" -P "+Pass+" delloem mac"
    if vendor=="SuperMicro":
         command="ipmitool -H  "+c_bmc[i-1]+"  -U "+User+" -P "+Pass+" raw 0x30 0x21 | tail -c 18"
    if vendor=="SuperMicro":
         command="ipmitool -H  "+c_bmc[i-1]+"  -U "+User+" -P "+Pass+" raw 0x30 0x19"
    return(command)


def update_info(vendor):
#********************************************************************************
# Disable showing Insecure Warning
 DisShowingInsecureWarning()

#********************************************************************************
 for i in range(1,32):
     c_name[i-1]="zc-91-"+str(i)
     c_bmc[i-1]="10.101.91."+str(i)


     command=create_command(vendor,i)
     #print(command,i)
     #content=get_MAC("ipmitool -H  "+c_bmc[i-1]+"  -U "+User+" -P "+Pass+" delloem mac")
     content=get_MAC(command)
     content = codecs.decode(content, "unicode_escape")
     #print(content)
     lines = content.splitlines()
     #for l  in lines:
      #   print ("**l= "+l)
      #   print (len(l))

     for l  in lines:
         if (len(l)>18 ):
           if( l[0]=="0"):
             #print("%%%%",len(l),"   line= "+l)
             index=1
             while(l[index]==" "):
                  ++index
             #print(index)
             c_mac[i-1]=l[index+2:index+19]
             #print(c_mac[i-1])

 for i in range(1,34):
     c_name[i+30]="zc-92-"+str(i)
     c_bmc[i+30]="10.101.92."+str(i)


     command=create_command(vendor,i)
     content=get_MAC(command)
     #content=get_MAC("ipmitool -H  "+c_bmc[i+30]+"  -U "+User+" -P "+Pass+" delloem mac")
     content = codecs.decode(content, "unicode_escape")
     lines = content.splitlines()
     for l  in lines:
         if (len(l)>18 ):
           if( l[0]=="0"):
             index=1
             while(l[index]==" "):
                  ++index
             c_mac[i+30]=l[index+2:index+19]


#----------------------------------------------------------------------------------------------------------------------




#  Read Info File -----------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------

def get_nodes_info():
    '''
         This function is for reading information of the cluster.
         It reads a file which contains informat of a cluster
         Each line of the file has the following format:
         IP_ address, BMC_Username, BMC_Password

    '''
    global Vendor
    global h_m_tech
    global net_interface
    init(strip=not sys.stdout.isatty()) # strip colors if stdout is redirected
    CHAR_PER_LINE=30
    cprint("Improving the automation of scaling-up a cluster using hardware management tools  ".center(CHAR_PER_LINE-2), 'white','on_blue')

    filename="input.local"
    ci=input("The default file contains datacenter information is input.local, do you want to change it? (Y/N)")
    if(ci=="Y" or ci=="y" ):
           filename = input('Input a file contains datacenter information: ')
    #print("getting Data Center information from file......................................")
    print("...............................................................................")
    time.sleep(1)
    print("...............................................................................")
    time.sleep(1)
    print("...............................................................................")
    time.sleep(1)
    print("...............................................................................")
    time.sleep(1)
    print("...............................................................................")
    linesList=[]
    ci=input(" \n ......................... \n How many nodes you want to add to the cluster? \n \n Answer:")
    newnodes_number=int(ci)
    ci=input(" \n ......................... \n select the vendor of new compute nodes: \n  1) Dell \n  2) Intel \n  3) Super Micro \n  \n Answer:")
    if (ci=="1" or ci=="Dell" or ci=="dell" or ci=="DELL" ):
      Vendor="Dell"
    if (ci=="2" or ci=="Intel" or ci=="intel" or ci=="INTEL" ):
      Vendor="Intel"
    if (ci=="3" or ci=="SuperMicro" or ci=="Super Micro" or ci=="super micro" or ci=="SUPER MICRO" or ci=="Super micro" or ci=="supermicro" or ci=="Supermicro" ):
      Vendor="SuperMicro"
    #print("+++++++++++++++++"+Vendor)
    h_m_tech=input(" \n ......................... \n Which hardware management technology you want to use to gather information?(Default=IPMI): \n  1) IPMI \n  2) Redfish  \n  \n Answer:")
    net_interface=input(" \n ......................... \n Which network interface shows the internal network?(Default=NIC1) \n  1) NIC1 \n  2) NIC2 \n  2) NIC3 \n  \n Answer:")

    try:
        data_file = open(filename, "r")    #"Machine Fraction.txt"
        linesList=data_file.readlines()
        data_file.close()

    except IOError:                      # we get here if file open failed
        print('Bad file name')



    i=0
    for e in linesList:
        e=e.strip()
        linesList[i]=[x.strip() for x in e.split(',')]
        i=i+1

    return(linesList)

#----------------------------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------------------------

def main():
      global Vendor
      get_nodes_info()
      update_info(Vendor)
      print(c_name)
      print(c_bmc)
      print(c_mac)

      for i in range(0,64):
            print ("c_name["+str(i)+"]="+c_name[i])
            print ("c_bmc["+str(i)+"]="+c_bmc[i])
            print ("c_mac["+str(i)+"]="+c_mac[i])
            print("#---------------------")


main()

#r=get_MAC("ipmitool -H 10.101.92.1  -U root -P Zephyr delloem mac")
#contents = codecs.decode(r, "unicode_escape")
#print(contents)

