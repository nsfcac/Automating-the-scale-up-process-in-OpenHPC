#import ipmi
#import redfish
import redfish
import json


def main():
    ''' Accepts no input and returns no output.  This will simply set up a list of nodes to check then execute the impi and redfish functions as needed.
    '''
    #Hardcoded for simplicity sake - will update to use input data from /etc/hosts in the future.  For now I had a program select 10 nodes at random.
    ipmiNodes = [['compute-19-17', '10.201.19.17'], ['compute-19-42', '10.201.19.42'], ['compute-19-47', '10.201.19.47'], ['compute-19-61', '10.201.19.61'], ['compute-20-26', '10.201.20.26'], ['compute-24-14', '10.201.24.14'], ['compute-24-23', '10.201.24.23'], ['compute-26-5', '10.201.26.5'], ['compute-27-19', '10.201.27.19'], ['compute-28-6', '10.201.28.6']]
    redfishNodes = [['compute-1-48', '10.101.1.48'], ['compute-10-31', '10.101.10.31'], ['compute-2-58', '10.101.2.58'], ['compute-4-1', '10.101.4.1'], ['compute-4-42', '10.101.4.42'], ['compute-4-6', '10.101.4.6'], ['compute-6-1', '10.101.6.1'], ['compute-7-3', '10.101.7.3'], ['compute-7-33', '10.101.7.33'], ['compute-9-22', '10.101.9.22']]

    #Uncomment for IPMI testing
    '''
    jsonObjList, errorList = ipmi.getNodeData(ipmiNodes)

    for jsonObj in jsonObjList:
        printJSON(json.loads(jsonObj))  #I am unsure how the JSON object will be returned so I am assuming it will come in as just a large JSON string.  This may crash if that is not true.
    '''

    #Uncomment for Redfish testing

    jsonObjList,dicSysInfoList ,errorList = redfish.getNodeData(redfishNodes)

    for jsonObj in jsonObjList:
        printJSON(json.loads(jsonObj))  #I am unsure how the JSON object will be returned so I am assuming it will come in as just a large JSON string.  This may crash if that is not true.

    return (jsonObjList)




def printJSON(jsonObj):
    '''Accepts a JSON object in Python Dictionary format and prints the various values to the screen.
    
    This assumes the JSON object has been formatted with following example structure:
    {'hostname' : 'Test Node', 'time': '2018-02-09 10:04', 'temperature' : {'ambient':22.3, 'cpu':{'cpu1':72.33, 'cpu2':74.82}}, 'power state':True, 'power' : {'voltage': {'voltage1':293.1}, 'current':{'current1':None}, 'watts':{'watts1':12}}, 'sel': None}
    '''
    print("\n----------------------------------------------\n")
    print("Hostname: %s\nTimestamp: %s\nPower On: %s" % (jsonObj["hostname"], jsonObj["time"], jsonObj["power state"]))


    print("NIC Mac Addresses information:")
    #print (type(jsonObj['NICs']))
   # print(type(jsonObj['NICs']['NIC1']))
    
    for a, b in jsonObj['NICs'].items():
      
       for key, value in b.items():
                   if (key!="URI"):
                          print(key, ': ', value)
   # if jsonObj["NICs"] != None:
                #for e in jsonObj['NICs']:   
                     # print("\t Mac Address of info: ",   e, e['NIC_Id'])
    #else:
     #   print("No NIC1 Mac Address")
#------------------
              
    
        

#if __name__== "__main__":
#  main()
