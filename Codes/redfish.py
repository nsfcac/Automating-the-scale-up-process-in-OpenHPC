
#This program gets an IP address and it creates two JSON objects: [ one of them with full info (json_output), and a small json object just with necessary information (json_SystemInfo)]



import requests
import socket
import ipaddress
import json
import datetime
BMCpass='nivipnut'
from threading import Thread








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
def get_Redfish_info(uri,s):  
    '''
         This function is for getting information by Redfish using its URI.
		 
    '''	
    try:
          systemInfo = s.get(uri,verify=False ).json() 
    except:
          systemInfo =None  
    return(systemInfo)    
 
#----------------------------------------------------------------------------------------------------------------------



# part 3: This fuction is for creating the output object---------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------	
def generate_Output(ip, hn):
    '''
    This fuction is for creating the output object. It gets an ip and a hostname of a machine, and it returns an object which contains system information.
	
    '''
    global BMCpass
#********************************************************************************	
# Disable showing Insecure Warning
    DisShowingInsecureWarning()

#********************************************************************************	
# Create a Redfish session

    s = requests.Session()
    s.auth = ('root', BMCpass)

#********************************************************************************	
#initializing systemInfo Dictionary
    SystemInfo={} 

#********************************************************************************		
#set hostname
    SystemInfo['hostname']=hn
    if SystemInfo['hostname']=="":
        SystemInfo['hostname']=None
			
#********************************************************************************		
# set time info
    SystemInfo['time']=datetime.datetime.now().strftime("%Y-%m-%d %H:%M")


	
#********************************************************************************		
#set NIC info
    uri="https://"+ip+"/redfish/v1/Systems/System.Embedded.1/EthernetInterfaces/"
    try:
           nicLinks=get_Redfish_info(uri,s)
          # print(nicLinks)
           nicCount=nicLinks['Members@odata.count']
           
           SystemInfo['NICs']={}
           SystemInfo['NICs']['NIC1']={}
           SystemInfo['NICs']['NIC2']={}
           SystemInfo['NICs']['NIC3']={}
           SystemInfo['NICs']['NIC4']={}
           SystemInfo['NICs']['NIC1']['MACAddress']={}
           SystemInfo['NICs']['NIC2']['MACAddress']={}
           SystemInfo['NICs']['NIC3']['MACAddress']={}
           SystemInfo['NICs']['NIC4']['MACAddress']={}
           SystemInfo['NICs']['NIC1']['URI']={}
           SystemInfo['NICs']['NIC2']['URI']={}
           SystemInfo['NICs']['NIC3']['URI']={}
           SystemInfo['NICs']['NIC4']['URI']={}
           SystemInfo['NICs']['NIC1']['Id']={}
           SystemInfo['NICs']['NIC2']['Id']={}
           SystemInfo['NICs']['NIC3']['Id']={}
           SystemInfo['NICs']['NIC4']['Id']={}
        
           for i in range(1,nicCount+1):
                        SystemInfo['NICs']['NIC'+str(i)]={}
                        SystemInfo['NICs']['NIC'+str(i)]['NIC_Id']={}
                        SystemInfo['NICs']['NIC'+str(i)]['URI']={}
                        SystemInfo['NICs']['NIC'+str(i)]['MACAddress']={}
           #nicNumber=int(nicLinks['Members@odata.count'])
           #SystemInfo['NICs']=nicLinks
           nicNumber=1
           for e in nicLinks['Members']:
                      # print(e)                      
                       SystemInfo['NICs']['NIC'+str(nicNumber)]['URI']=e['@odata.id']
                       uri="https://"+ip+e['@odata.id']   
                       #print (SystemInfo['NICs']['NIC'+str(nicNumber)]['URI'])
                      # print(uri)                 
                       nicInfo=get_Redfish_info(uri,s)
                      # print(nicInfo)
                       SystemInfo['NICs']['NIC'+str(nicNumber)]['NIC_Id']=nicInfo['Id']
                       #print (nicInfo['MACAddress'])
                       SystemInfo['NICs']['NIC'+str(nicNumber)]['MACAddress']=nicInfo['MACAddress']
                       #print(SystemInfo['NICs']['NIC'+str(nicNumber)]['MACAddress'], 'NIC'+str(nicNumber))
                       nicNumber=nicNumber+1
        
        
    except:
        SystemInfo['NICs']={}

#********************************************************************************
#set Power State info
    uri="https://"+ip+"/redfish/v1/Systems/System.Embedded.1"
    try:
       ps_hn=get_Redfish_info(uri,s)	 
       if	(ps_hn['PowerState']=="On"):
           SystemInfo['power state']=True
       else:
           SystemInfo['power state']=False
       SystemInfo['HN']=ps_hn['HostName']
       if	(ps_hn['HostName']==""):
           SystemInfo['HN']=None
    except:
       SystemInfo['HN']=None
       SystemInfo['power state']=None
	
		

#********************************************************************************	
# Return the output dictionary	
    return (SystemInfo)
#----------------------------------------------------------------------------------------------------------------------	

  





  
#part 4 get information for one node --------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------
def getOneNodeData(ip,hn,mylistJSON,mylistofDicSysteminfo,myErrList): #sl is a list of  hostname and ip lists
    '''
     get information for one node.
	 
    '''
    try:
             SystemInfo=generate_Output(ip,hn)
             json_SystemInfo=json.dumps(SystemInfo)
             mylistJSON.append(json_SystemInfo)
             mylistofDicSysteminfo.append(SystemInfo)
            
    except:
             myErrList.append([ip,hn,"Error"])  
#----------------------------------------------------------------------------------------------------------------------		



  

  
  
  #part 5 get information for a list of nodes --------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------
def getNodeData(sl): #sl is a list of  hostname and ip lists
    '''
     get information for a list of nodes.
	 
     It Accepts an input as a list of lists: getNodeData([[“hostname”, “iDRAC IPv4 Address”], …])
     It Returns 2 objects:

                                                    i.     List of JSON objects:  [JSON, …]
                                                   ii.     List of lists with the errors:  [[“hostname”, “ipv4 address”, “error”], …]
    '''
    mylistJSON=[]
    mylistofDicSysteminfo=[]
    myErrList=[]
    threads = []
    for l in sl:
        ip=l[1]
        hn=l[0]
        t = Thread(target=getOneNodeData, args=(ip,hn,mylistJSON,mylistofDicSysteminfo,myErrList))
        threads.append(t)
        t.start()
    for t in threads:    
          t.join()       
    return(mylistJSON,mylistofDicSysteminfo,myErrList)  
#----------------------------------------------------------------------------------------------------------------------		


#redfishNodes = [['compute-1-48', '10.101.1.48'], ['compute-10-31', '10.101.10.31'], ['compute-2-58', '10.101.2.58'], ['compute-4-1', '10.101.4.1'], ['compute-4-42', '10.101.4.42'], ['compute-4-6', '10.101.4.6'], ['compute-6-1', '10.101.6.1'], ['compute-7-3', '10.101.7.3'], ['compute-7-33', '10.101.7.33'], ['compute-9-22', '10.101.9.22']]


#redfishNodes = [['compute-4-1', '10.101.4.1']]
#jsonObjList, errorList = getNodeData(redfishNodes)
#print(jsonObjList)
#a=jsonObjList
#print(a['time'])
#print(a['NICs'])
#print(jsonObjList['NICs'][0])
