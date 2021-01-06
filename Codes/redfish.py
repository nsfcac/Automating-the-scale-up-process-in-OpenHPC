
#This program gets an IP address and it creates two JSON objects: [ one of them with full info (json_output), and a small json object just with necessary information (json_SystemInfo)]



import requests
import socket
import ipaddress
import json
import datetime

from threading import Thread
BMCpass='mypass'    #update the value in ../Doc-Files/credentialInfo.txt
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
    global BMCuser

#********************************************************************************
#set BMC credential (username and password)
    setBMCcredential()

#********************************************************************************	
# Disable showing Insecure Warning
    DisShowingInsecureWarning()

#********************************************************************************	
# Create a Redfish session

    s = requests.Session()
    s.auth = (BMCuser, BMCpass)

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
#set NIC info, systemName, Power status, and BMC's Hostname
    SystemInfo['NICs']={}
    SystemInfo['systemName']={}
    systemNameURI="System.Embedded.1"  #default system name (it will be corrected in the following code:) 
    urigetName="https://"+ip+"/redfish/v1/Systems"
    SystemInfo['HN-BMC']=""
    SystemInfo['power state']=False
    try:
          
           sURI=get_Redfish_info(urigetName,s)
          
#********************************************************************************
#set Power State info and BMC's Hostname
     
           systemNameURI=sURI["Members"][0]["@odata.id"][20:]
           uri="https://"+ip+"/redfish/v1/Systems/"+systemNameURI
          
           
           try:
              ps_hn=get_Redfish_info(uri,s)
              if (ps_hn['PowerState']=="On"):
                  SystemInfo['power state']=True
              else:
                  SystemInfo['power state']=False
              SystemInfo['HN-BMC']=ps_hn['HostName']
              if (ps_hn['HostName']==""):
                  SystemInfo['HN-BMC']=None
           except:
              SystemInfo['HN-BMC']=None
              SystemInfo['power state']=None



#********************************************************************************
#set NIC Info
           index=0  # to count the number of NICs
           nicNumber=1 # set the number of NICs
           for mem in sURI["Members"]:
                  systemNameURI=mem["@odata.id"]
                  SystemInfo['systemName']=systemNameURI[20:]
                  uri="https://"+ip+systemNameURI+"/EthernetInterfaces/"
   
                  nicLinks=get_Redfish_info(uri,s)
                  nicCount=int(nicLinks['Members@odata.count'])
                  for i in range(1+index,index+nicCount+1):
                               SystemInfo['NICs']['NIC'+str(i)]={}
                               SystemInfo['NICs']['NIC'+str(i)]['NIC_Id']={}
                               SystemInfo['NICs']['NIC'+str(i)]['URI']={}
                               SystemInfo['NICs']['NIC'+str(i)]['MACAddress']={}
                  index=index+nicCount
                 
                  
                  for e in nicLinks["Members"]:                      
                              SystemInfo['NICs']['NIC'+str(nicNumber)]['URI']=e['@odata.id']
                              uri="https://"+ip+e['@odata.id']   
                                             
                              nicInfo=get_Redfish_info(uri,s)
                          
                              SystemInfo['NICs']['NIC'+str(nicNumber)]['NIC_Id']=nicInfo['Id']
                             
                              SystemInfo['NICs']['NIC'+str(nicNumber)]['MACAddress']=nicInfo['MACAddress']
                             
                              nicNumber=nicNumber+1
        
        
    except:
        SystemInfo['NICs']={}

	

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




#redfishNodes = [['', '10.101.1.48'], ['compute-10-31', '10.101.10.31'], ['compute-2-58', '10.101.2.58'], ['compute-4-1', '10.101.4.1'], ['compute-4-42', '10.101.4.42'], ['compute-4-6', '10.101.4.6'], ['compute-6-1', '10.101.6.1'], ['compute-7-3', '10.101.7.3'], ['compute-7-33', '10.101.7.33'], ['compute-9-22', '10.101.9.22']]


#jsonObjList,dicList, errorList = getNodeData(redfishNodes)
#print (dicList)
