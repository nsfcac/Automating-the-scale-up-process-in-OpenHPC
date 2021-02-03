


#This program uses IPMI technology to gather hardware management information from the BMC of the machines of a cluster.



import requests
import socket
import ipaddress
import json
import datetime
import subprocess
import codecs
from threading import Thread


BMCpass='myPass'    #update the value in ../Doc-Files/credentialInfo.txt
BMCuser='root'        #update value in ../Doc-Files/credentialInfo.txt







#part 1: This function is for disabling warnings in requests' vendored urllib3, (insecure request warnings)------------
#----------------------------------------------------------------------------------------------------------------------
def DisShowingInsecureWarning():
    '''
         This function is for disabling warnings in requests' vendored urllib3, (insecure request warnings.
		 
    '''
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
#----------------------------------------------------------------------------------------------------------------------






#part 2: This function is for getting information by Redfish using its URI ----------------------------------------
#----------------------------------------------------------------------------------------------------------------------
def get_IPMI_info(s):  
    '''
         This function is for getting information by IPMI using its URI.
		 
    '''
    systeminfo=""
   
    try:
         

         (output, err) = subprocess.Popen(s, stdout=subprocess.PIPE, shell=True).communicate()
         systeminfo=str( output)[2:-3]
         
        

          
    except:
          systeminfo =""  

    return(systeminfo)    
 
#----------------------------------------------------------------------------------------------------------------------



# part 3: This fuction is for creating the output object---------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------	
def generate_Output(vendor,ip, hn):
 
    '''
    This fuction is for creating the output object. It gets an ip and a hostname of a machine, and it returns an object which contains system information.
	
    '''
    global BMCpass
    global BMCuser

#********************************************************************************
#set BMC credential (username and password)
    setBMCcredential()

#********************************************************************************	
# Disable showing Insecure Warning
    DisShowingInsecureWarning()

#********************************************************************************
# Set IPMI command
    command=create_command(vendor,ip)
   
#********************************************************************************	
#initializing systemInfo Dictionary
    SystemInfo={} 

#********************************************************************************		
#set hostname and ip
    SystemInfo['BMC_IP']=ip
    SystemInfo['hostname']=hn
    if SystemInfo['hostname']=="":
        SystemInfo['hostname']=None
    if SystemInfo['BMC_IP']=="":
        SystemInfo['BMC_IP']=None
			
#********************************************************************************		
# set time info
    SystemInfo['time']=datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
	
#********************************************************************************		
#set NIC info
    SystemInfo['NICs']={}
    
    index=0  # to count the number of NICs
    nicNumber=0 # set the number of NICs
      
    content=get_IPMI_info(command) 
    content = codecs.decode(content, "unicode_escape")
    lines = content.splitlines()
    for l  in lines:
                  if (len(l)>18 ):
                       if( '0'<=l[0]<='9'):
                                      nicNumber=int(l[0])+1
                                      ind=1
                                      index=index+1
                                      while(l[ind]==" "):
                                                               ++index
 
                                      c_mac=l[ind+2:ind+19]
                                      #print(nicNumber,c_mac)

                                      SystemInfo['NICs']['NIC'+str(nicNumber)]={}
                                      SystemInfo['NICs']['NIC'+str(nicNumber)]['MACAddress']=c_mac
                  
  
         
#********************************************************************************	
# Return the output dictionary	
    return (SystemInfo)
#----------------------------------------------------------------------------------------------------------------------	

  





  
#part 4 get information for one node --------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------
def getOneNodeData(vendor,ip,hn,mylistJSON,mylistofDicSysteminfo,myErrList): 
    '''
     get information for one node.
	 
    '''
    try:
             SystemInfo=generate_Output(vendor,ip,hn)
             json_SystemInfo=json.dumps(SystemInfo)
             mylistJSON.append(json_SystemInfo)
             mylistofDicSysteminfo.append(SystemInfo)
            
    except:
             myErrList.append([ip,hn,"Error"])  
#----------------------------------------------------------------------------------------------------------------------		



  

  
  
  #part 5 get information for a list of nodes --------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------
def getNodeData(sl,vendor): #sl is a list of  hostname and ip lists
    '''
     get information for a list of nodes.
	 
     It Accepts an input as a list of lists: getNodeData([[“hostname”, “iDRAC IPv4 Address”], …])
     It Returns 3 objects:

                                                    i.     List of JSON objects:  [JSON, …]
                                                    ii.    List of Dictionary objects [dic, ...]
                                                    iii.   List of lists with the errors:  [[“hostname”, “ipv4 address”, “error”], …]
    '''
    mylistJSON=[]
    mylistofDicSysteminfo=[]
    myErrList=[]
    threads = []
    for l in sl:
        ip=l[1]
        hn=l[0]
        t = Thread(target=getOneNodeData, args=(vendor,ip,hn,mylistJSON,mylistofDicSysteminfo,myErrList))
        threads.append(t)
        t.start()
    for t in threads:    
          t.join()       
    return(mylistJSON,mylistofDicSysteminfo,myErrList)  
#----------------------------------------------------------------------------------------------------------------------		


# Part 6: set BMC user name and password
#----------------------------------------------------------------------------------------------------------------------
def setBMCcredential():
    '''
       This function sets BMC's credential info (user name and password from the ../Doc-Files/credentialInfo.txt file.)
    '''
    global BMCuser
    global BMCpass    
# Using readlines() 
   
    try:
          credentialFile = open('../Doc-Files/credentialInfo.txt', 'r') 
          credLines = credentialFile.readlines() 
          #print(len(credLines))
          BMCpass=credLines[2][13:-1]
          BMCuser=credLines[1][9:-1]
          #print (BMCuser, len(BMCuser))
          #nivipnutprint(BMCpass, len(BMCpass))
          credentialFile.close()          

    except:
        print("problem in getting BMC's credential info (user name and password from the ../Doc-Files/credentialInfo.txt file.. The program uses the default credential info now. If you need to set another username and password, please update the ../Doc-Files/credentialInfo.txt file.")

#----------------------------------------------------------------------------------------------------------------------




#part7: set the command based on vendor
#----------------------------------------------------------------------------------------------------------------------


def create_command(vendor,ip):
    '''
       This function sets the command based on the vendor type.
    '''
    c=""
    if vendor=="Dell":
         c="ipmitool -H  "+ip+"  -U "+BMCuser+" -P "+BMCpass+" delloem mac"
         
    if vendor=="SuperMicro":
         c="ipmitool -H  "+ip+"  -U "+BMCuser+" -P "+BMCpass+" raw 0x30 0x21 | tail -c 18"
    #if vendor=="SuperMicro":
         #c="ipmitool -H  "+ip+"  -U "+BMCuser+" -P "+BMCpass+" raw 0x30 0x19"
    
    return(c)







#ipmiNodes = [['', '10.101.92.1'], ['com2', '10.101.91.31']]


#jsonObjList,dicList, errorList = getNodeData(ipmiNodes,"Dell")
#print (dicList)

