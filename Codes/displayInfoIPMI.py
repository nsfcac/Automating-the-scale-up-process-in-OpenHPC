
#This code is for displaying network discovery data in a nice format (for IPMI Discovery).

#Part1: This Function is for have a nice print of nodes information
#----------------------------------------------------------------------------------------------------------------------
def printNetDiscoveryInfo(dicSysInfoList):
    ''' 
         This Function is for have a nice print of nodes information.
         The input is a list of dictionaries. Each item contains the information of one node.
    '''
    
    for dicObj in dicSysInfoList:
        printOneNode(dicObj)
    



#Part2: This function validates an IP address.
#----------------------------------------------------------------------------------------------------------------------
def printOneNode(dicSysInfo):
    '''
         Accepts a Dictionary object in Python Dictionary format and prints the various values to the screen.
    
         This assumes the Dictionary object has been formatted with following example structure:
    
         {'BMC_IP':'10.101.6.3',  'hostname': 'compute-6-3', 'time': '2021-01-06 01:59', 'NICs': {'NIC2': {'MACAddress': '7C:D3:0A:C6:3C:9E'}, 'NIC1': {'MACAddress': '7C:D3:0A:C6:3C:9C'}}

    '''
    print("\n----------------------------------------------\n")
    print("BMC_IP: %s\nHostname: %s\nTimestamp: %s" % (dicSysInfo["BMC_IP"],dicSysInfo["hostname"], dicSysInfo["time"]))
    

    print("NIC Mac Addresses information:")
    #print (type(jsonObj['NICs']))
   # print(type(jsonObj['NICs']['NIC1']))
    
    for a, b in dicSysInfo['NICs'].items():
      
       for key, value in b.items():
                   if (key!="URI"):
                          print(key, ': ', value)
  
