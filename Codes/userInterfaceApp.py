
#This code is for printing the menu and gathering data form user.



#The codes in Codes directory
import redfish
import ipmi
import displayInfoRedfish
import displayInfoIPMI

# other libraries
import json
import time
import os

#define global variables
newNodesNumber=1   #It shows the number of the nodes user wants to add to the cluster(Default=1).

nodes = []
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
       item=4
       try:
               item=input(" \n ......................... \n Please select a number from the menu:\n   1) About the Application\n   2) Network Discovery\n   3) Update Cluster Mac Address Information \n   4) Exit  \n  \nAnswer:" )
               item=int(item)
               

       except ValueError:
               print("Not a valid number.Please try again..")

       if item==1:
                  aboutApp()
       else:
                  if item==2:
                              netDiscovery()
                  else:
                              if item==3:
                                         clusterMacUpdate()
                              else:
                                         t=0
    
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

#----------------------------------------------------------------------------------------------------------------------




# Part4:This function is for gathering node and network information from BMC.
#----------------------------------------------------------------------------------------------------------------------
def netDiscovery():
    '''
         This function is for gathering node and network information from BMC.

    '''
   
#********************************************************************************
#Select Hardware Managment Technology to gather data
    h_m_tech="Redfish"      # The default Hardware Managment Technology
    ci=input(" \n ......................... \n Select Hardware Management Technology(Default=Redfish): \n  1) IPMI \n  2) Redfish  \n  \n Answer:")
    if (ci=="1" or ci=="ipmi" or ci=="IPMI" or ci=="Ipmi" ):
              h_m_tech="IPMI"         
    
    clusterInfoLinesList =[]  # The list of IPs form clusterinfo file.
    nodes=[]          # The list of computer names and IPs.
#********************************************************************************
#Read list of BMC IPs from a file
    clusterInfoFilePass="../Doc-Files/clusterInfo"      # the default file contains BMC IPs
    ci=input(" \n ......................... \n Select the path to the cluster information file (Default: ../Doc-Files/clusterInfo):")
    isFile = os.path.isfile(str(ci))    
    if(isFile):
             clusterInfoFilePass=ci
    else:
             print("\n ......................... \n It is not a valid file path.\n The application will use the default clusterInfo file.......")    
    try:
              clusterInfoFile = open(clusterInfoFilePass, 'r')
              for line in  clusterInfoFile:
                             l=line.strip(' \n\t')
                             if(validate_ip(l)):
                                      clusterInfoLinesList.append(line.strip(' \n\t'))       
                                      
              
              clusterInfoFile.close()
    except:
              print("Cluster info file does not exist. Please create it first and try again.")

#********************************************************************************
#Gather Network information.

    for com_ip in clusterInfoLinesList:
      
                               nodes.append(["",com_ip])
   

    if (h_m_tech=="Redfish"):  
           print("\n\n\n\nPlease wait to finish the network discovering process by Redfish....  ")
           for i in range(8):
                             print("\t\t.............................................................")
                             time.sleep(0.5)
           print("Please wait.....\n\n")
           jsonObjList,dicList, errorList = redfish.getNodeData(nodes)
           #print (dicList)
           displayInfoRedfish.printNetDiscoveryInfo(dicList)
           print("\n\n\n\n\n ......................... \n")
    else:
           vendor="Dell" # (Default)
           ci=input(" \n ......................... \n select the vendor of the new compute nodes(Default=Dell): \n  1) Dell \n  2) SuperMicro  \n  3) Intel  \n  4) Other \n  \n Answer:")
    #if (ci=="1" or ci=="Dell" or ci=="dell" or ci=="DELL" ):
     # Vendor="Dell"
           if (ci=="2" or ci=="SuperMicro" or ci=="Super Micro" or ci=="super micro" or ci=="SUPER MICRO" or ci=="Super micro" or ci=="supermicro" or ci=="Supermicro" ):
                                   vendor="SuperMicro"
           if (ci=="3" or ci=="Intel" or ci=="intel" or ci=="INTEL" ):
                                   vendor="Intel"
           if (ci=="4" or ci=="Other" or ci=="other" or ci=="OTHER" ):
                                   vendor="Other"
           print("\n\n\n\nPlease wait to finish the network discovering process by IPMI....  ")
           for i in range(8):
                             print("\t\t.............................................................")
                             time.sleep(0.5)
           print("Please wait.....\n\n")
           jsonObjList,dicList, errorList = ipmi.getNodeData(nodes,vendor)
           #print (dicList)
           displayInfoIPMI.printNetDiscoveryInfo(dicList)
           print("\n\n\n\n\n ......................... \n")

   
#******SystemInfi**************************************************************************
# Writing Information to a json file

    try:
        outfile = open("../Doc-Files/ClusterNetInfo.json", "w+", encoding='utf-8')
        for obj in dicList:
                outfile.write("\n\n\n")
                json.dump(obj, outfile, ensure_ascii=False, indent=4)
        outfile.write("\n\n\n")

        print("The gathered discovery Information has been saved in the ../Doc-Files/ClusterNetInfo.json file.\n\n")
        outfile.close()
    except:
       print("problem in opening the ../Doc-Files/ClusterNetInfo.json file.")




         
#********************************************************************************
# Print menu
    #printMenu()
#----------------------------------------------------------------------------------------------------------------------




#Part5:This function is for updating input.local file when we want to expand the cluster.
#----------------------------------------------------------------------------------------------------------------------
def clusterMacUpdate(): 
    '''
         This function is for updating input.local file when we want to expand the cluster.

    '''


    global newNodesNumber
    h_m_tech="Redfish"
#---------------
    ci=input(" \n ......................... \n Select Hardware Management Technology(Default=Redfish): \n  1) IPMI \n  2) Redfish  \n  \n Answer:")
    if (ci=="1" or ci=="ipmi" or ci=="IPMI" or ci=="Ipmi" ):
              h_m_tech="IPMI"
    clusterInfo="../Doc-Files/clusterInfo"
    
    if(h_m_tech=="IPMI"):
                       updateMacInfo(1)
    else:
                       updateMacInfo(2)


#----------------------------------------------------------------------------------------------------------------------





#Part6: This function updates mac information using Redfish
#----------------------------------------------------------------------------------------------------------------------
def updateMacInfo(techType):
    '''
         This function is for updating input.local file when we want to expand the cluster using Redfish.

    '''
    if (techType==1):
                     h_m_tech="IPMI"
    else:
                     h_m_tech="Redfish"

#----------------
    ni=input(" \n ......................... \n Select Network Interface?(Default=NIC1):  \n   1)NIC1 \n   2)NIC2  \n   3)NIC3  \n   4)NIC4  \n  \n Answer:")
    netInt="NIC1"  # the default internal network interface
    eth="eth1"
    if(ni=="2" or ni=="NIC2" or ni=="nic2" or ni=="Nic2"):
                netInt="NIC2"
                eth="eth2"
    if(ni=="3" or ni=="NIC3" or ni=="nic3" or ni=="Nic3"):
                netInt="NIC3"
                eth="eth3"
    if(ni=="4" or ni=="NIC4" or ni=="nic4" or ni=="Nic4"):
                netInt="NIC4"
                eth="eth4"
#-----------------

    prefix=input(" \n ......................... \n Select compute_prefix(Default=c):  \n  \n Answer:")
    if (len(prefix)==0):
            prefix='c'  # Default Prefix  

#-----------------    
# 

    
    clusterInfoLinesList =[]  # The list of IPs form clusterinfo file.
    nodes=[]          # The list of computer names and IPs.
#********************************************************************************
#Read list of BMC IPs from a file
    clusterInfoFilePass="../Doc-Files/clusterInfo"      # the default file contains BMC IPs
    ci=input(" \n ......................... \n Select the path to the cluster information file (Default: ../Doc-Files/clusterInfo):")
    isFile = os.path.isfile(str(ci))
    if(isFile):
             clusterInfoFilePass=ci
    else:
             print("\n ......................... \n It is not a valid file path.\n The application will use the default clusterInfo file.......")
    try:
              clusterInfoFile = open(clusterInfoFilePass, 'r')
              for line in  clusterInfoFile:
                             l=line.strip(' \n\t')
                             if(validate_ip(l)):
                                      clusterInfoLinesList.append(line.strip(' \n\t'))


              clusterInfoFile.close()
    except:
              print("Cluster info file does not exist. Please create it first and try again.")

#********************************************************************************
#Gather Network information.

    i=1
    for com_ip in clusterInfoLinesList:
                               
                               
                               com_name=prefix+str(i) 
                               nodes.append([com_name,com_ip])
                               i=i+1


    if (h_m_tech=="Redfish"):
           print("\n\n\n\nPlease wait to finish the network discovering process by Redfish....  ")
           for i in range(8):
                             print("\t\t.............................................................")
                             time.sleep(0.5)
           print("Please wait.....\n\n")
           jsonObjList,dicList, errorList = redfish.getNodeData(nodes)
           #print (dicList)
           displayInfoRedfish.printNetDiscoveryInfo(dicList)
           print("\n\n\n\n\n ......................... \n")
    

    else:
           
           vendor="Dell" # (Default)
           ci=input(" \n ......................... \n select the vendor of the new compute nodes(Default=Dell): \n  1) Dell \n  2) SuperMicro  \n  3) Intel  \n  4) Other \n  \n Answer:")
    #if (ci=="1" or ci=="Dell" or ci=="dell" or ci=="DELL" ):
     # Vendor="Dell"
           if (ci=="2" or ci=="SuperMicro" or ci=="Super Micro" or ci=="super micro" or ci=="SUPER MICRO" or ci=="Super micro" or ci=="supermicro" or ci=="Supermicro" ):
                                   vendor="SuperMicro"
           if (ci=="3" or ci=="Intel" or ci=="intel" or ci=="INTEL" ):
                                   vendor="Intel"
           if (ci=="4" or ci=="Other" or ci=="other" or ci=="OTHER" ):
                                   vendor="Other"
           print("\n\n\n\nPlease wait to finish the network discovering process by IPMI....  ")
           for i in range(8):
                             print("\t\t.............................................................")
                             time.sleep(0.5)
           print("Please wait.....\n\n")
           jsonObjList,dicList, errorList = ipmi.getNodeData(nodes,vendor)
           #print (dicList)
           displayInfoIPMI.printNetDiscoveryInfo(dicList)
           print("\n\n\n\n\n ......................... \n")




#********************************************************************************
# Writing Information to a json file

    try:
        outfile = open("../Doc-Files/ClusterNetInfo.json", "w+", encoding='utf-8')
        for obj in dicList:
                outfile.write("\n\n\n")
                json.dump(obj, outfile, ensure_ascii=False, indent=4)
        outfile.write("\n\n\n")

        print("The gathered discovery Information has been saved in the ../Doc-Files/ClusterNetInfo.json file.\n\n")
        outfile.close()
    except:
       print("problem in opening the ../Doc-Files/ClusterNetInfo.json file.")



#********************************************************************************
# Creating input.local file in path: "../Doc-Files/input.local

    try:
        localfile = open("../Doc-Files/input.local", "w+", encoding='utf-8')
        l1="compute_prefix=\"${compute_prefix:-"+prefix+"}\"\n"  #compute_prefix="${compute_prefix:-c}"
        localfile.write(l1)
        l2="sms_eth_internal=\"${sms_eth_internal:-"+eth+"}\"\n"
        localfile.write(l2) # sms_eth_internal="${sms_eth_internal:-eth_i}"
        i=0
        name=""
        mac=""
        bmcIP=""
        for obj in dicList:
                name=name+"c_name["+str(i)+"]="+obj["hostname"]+"\n"
                bmcIP=bmcIP+"c_bmc["+str(i)+"]="+obj["BMC_IP"]+"\n"
                for a, b in obj['NICs'].items():
                   if a==netInt:
                       for key, value in b.items():
                            if (key=="MACAddress"):
                                   mac=mac+"c_mac["+str(i)+"]="+value+"\n"
                i=i+1



        localfile.write(name)
        localfile.write(bmcIP)
        localfile.write(mac)
                        
        localfile.write("\n\n\n")

        print("The input.local file has been created and  saved in the ../Doc-Files/input.local file.\n\n")
        localfile.close()
    except:
       print("problem in opening the ../Doc-Files/ClusterNetInfo.json file.")
    
#----------------------------------------------------------------------------------------------------------------------




#Part7: This function validates an IP address.
#----------------------------------------------------------------------------------------------------------------------
def validate_ip(s):

    '''
          This function validates an IP address. 

    '''
    a = s.split('.')
    if len(a) != 4:
        return False
    for x in a:
        if not x.isdigit():
            return False
        i = int(x)
        if i < 0 or i > 255:
            return False
    return True

#----------------------------------------------------------------------------------------------------------------------


#Part8: The main function.
#----------------------------------------------------------------------------------------------------------------------
def main():
    '''
         The main function

    '''
    printTitle()

#----------------------------------------------------------------------------------------------------------------------



#----------------------------------------------------------------------------------------------------------------------
# Part9:Call the main function.
if __name__== "__main__":
  main()


#----------------------------------------------------------------------------------------------------------------------
