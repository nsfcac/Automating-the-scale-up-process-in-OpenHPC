
#This function is for printing the menu and gathering data form user.




import redfish
import json
import time
import monitoringTest
import os

#define global variables
newNodesNumber=1   #It shows the number of the nodes user wants to add to the cluster.

redfishNodes = []
#Part1: This function is for printing the title of the app.
#----------------------------------------------------------------------------------------------------------------------
def printTitle():
    '''
         This function is for printing the title of the app.

    '''

#printing the name of the app
#*******************************************************************************
    print("\n\n\n\n\n\n\n\n\n\n\n\t\t\t Gathering Mac Address of Internal Network \n \t\t\t by Redfish/IPMI Hardware Management Tool")
    for i in range(8):
       print("\t\t.............................................................")
       time.sleep(0.5)

    print("\n\n\n")
#********************************************************************************
# Print menu
    printMenu()
#----------------------------------------------------------------------------------------------------------------------




#Part2: This function is for printing the menu and gathering data form user.
#----------------------------------------------------------------------------------------------------------------------
def printMenu():
    '''
         This function is for printing the menu and gathering data form user.

    '''
#*****************************************************************************   
#gathering data from user (select the first option from the menue)
    linesList=[]
    t=1
    while(t):
       try:
               item=input(" \n ......................... \n Please select a number from the menu:\n   1) About the Application\n   2) Network Discovery\n   3) Update Cluster Mac Address Information \n   4) Exit  \n  \nAnswer:" )
               item=int(item)
               t=0

       except ValueError:
               print("Not a valid number.Please try again..")

    if item==1:
       aboutApp()
    if item==2:
       netDiscovery()
    if item==3:
       clusterMacUpdate()
#----------------------------------------------------------------------------------------------------------------------




# Part3:This function prints information anout the application.
#----------------------------------------------------------------------------------------------------------------------
def aboutApp():
    '''
         This function prints information anout the application.

    '''
#********************************************************************************
# Print Readme file
    try:
             f = open('../Doc-Files/Readme', 'r')
             #file_contents = f.read()
             file_contents = f.readlines()
             for line in file_contents:
                   print(line)
                   time.sleep(1.3)
                   
            # print (file_contents)
             f.close()
    except Exception as ex:
             print (" Readme file does not exist")
    item=input(" \n ......................... \n Please press enter to come back to the menu.")

#********************************************************************************
# Print menu
    printMenu()
#----------------------------------------------------------------------------------------------------------------------




# Part4:This function is for gathering node and network information from BMC.
#----------------------------------------------------------------------------------------------------------------------
def netDiscovery():
    '''
         This function is for gathering node and network information from BMC.

    '''
    
    for i in range(1,10):
            for j in range(1,10):
                      com_name='compute-'+str(i)+'-'+str(j)
                      com_ip='10.101.'+str(i)+'.'+str(j)
                      redfishNodes.append([com_name,com_ip])
          
                      
   #JsonObj=monitoringTest.main()
    h_m_tech="Redfish"
    ci=input(" \n ......................... \n Select Hardware Management Technology(Default=Redfish): \n  1) IPMI \n  2) Redfish  \n  \n Answer:")
    if (ci=="1" or ci=="ipmi" or ci=="IPMI" or ci=="Ipmi" ):    
              h_m_tech="IPMI"
    clusterInfo="../Doc-Files/clusterInfo"
    ci=input(" \n ......................... \n Select the path to the cluster information file (Default: ../Doc-Files/clusterInfo):")
    isFile = os.path.isfile(str(ci))    
    if(isFile):
             clusterInfo=ci


    if (h_m_tech=="Redfish"):  
           jsonObjList,dicList, errorList = redfish.getNodeData(redfishNodes)
           print (dicList)
           JsonObj=monitoringTest.main()
#********************************************************************************
# Print menu
    printMenu()
#----------------------------------------------------------------------------------------------------------------------




#Part5:This function is for updating input.local file when we want to expand the cluster.
#----------------------------------------------------------------------------------------------------------------------
def clusterMacUpdate(): 
    '''
         This function is for updating input.local file when we want to expand the cluster.

    '''


    global newNodesNumber
    ci=input(" \n ......................... \n Insert the number of the nodes to add to the cluster? \n \n Answer:")
    newNodesNumber=int(ci)
    h_m_tech="Redfish"
    ci=input(" \n ......................... \n Select Hardware Management Technology(Default=Redfish): \n  1) IPMI \n  2) Redfish  \n  \n Answer:")
    if (ci=="1" or ci=="ipmi" or ci=="IPMI" or ci=="Ipmi" ):
              h_m_tech="IPMI"
    clusterInfo="../Doc-Files/clusterInfo"
    ci=input(" \n ......................... \n Select the path to the cluster information file (Default: ../Doc-Files/clusterInfo):")
    isFile = os.path.isfile(str(ci))
    if(isFile):
             clusterInfo=ci
    net_interface=input(" \n ......................... \n Select Network Interface?(Default=NIC1):  \n   1) NIC1 \n   2)NIC2 \n   3)NIC3 \n   4)NIC4")
   # print("Find the updated input.local file in the ../Doc-Files path.")
    
    if (h_m_tech=="Redfish"):
           jsonObjList,dicList, errorList = redfish.getNodeData(redfishNodes)
           print (dicList)
           JsonObj=monitoringTest.main()
           print("\n\n\n\n--------------------------\nFind the updated input.local file in the ../Doc-Files path.")
#********************************************************************************
# Print menu
    printMenu()


#ci=input(" \n ......................... \n select the vendor of new compute nodes: \n  1) Dell \n  2) Intel \n  3) Super Micro \n  \n Answer:")
    #if (ci=="1" or ci=="Dell" or ci=="dell" or ci=="DELL" ):
     # Vendor="Dell"
    #if (ci=="2" or ci=="Intel" or ci=="intel" or ci=="INTEL" ):
    #  Vendor="Intel"
    #if (ci=="3" or ci=="SuperMicro" or ci=="Super Micro" or ci=="super micro" or ci=="SUPER MICRO" or ci=="Super micro" or ci=="supermicro" or ci=="Supermicro" ):
     # Vendor="SuperMicro"
    #print("+++++++++++++++++"+Vendor)
    
   # h_m_tech=input(" \n ......................... \n Which hardware management technology you want to use to gather information?(Default=IPMI): \n  1) IPMI \n  2) Redfish  \n  \n Answer:")

    #NICNames=""
    #i=1
    #print (type(JsonObj[0]))
    #print(JsonObj)
    #for a,b in JsonObj[0]['NICs'].items:

#                NICNames=ICNames+"\n"+str(i)+") "+a+" \n"

 #               i=i+1
  #  net_interface=input(" \n ......................... \n Which network interface shows the internal network?(Default=NIC1) "+NICNames+" Answer:")
    



    
#----------------------------------------------------------------------------------------------------------------------




#Part6: The main function.
#----------------------------------------------------------------------------------------------------------------------
def main():
    '''
         The main function

    '''
    printTitle()

#----------------------------------------------------------------------------------------------------------------------



#----------------------------------------------------------------------------------------------------------------------
# Part7:Call the main function.
if __name__== "__main__":
  main()


#----------------------------------------------------------------------------------------------------------------------
