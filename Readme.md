# Improving the Automation of Scaling-up an OpenHPC Cluster
## (Gathering Mac Address of Internal Network by Redfish/IPMI Hardware Management Tools)
### 1- Abstract

OpenHPC [1] is an HPC-centric software for creating, composing and administering high-performance computing clusters. It provides methods to register nodes and provide the information needed to provision them and integrate them into data centers. In the current OpenHPC methodology for creating a cluster, we need to have the Mac addresses of all the compute nodes in advance and manually type in the “input.local” file. It is a time-consuming step, especially for big data centers with a massive number of compute nodes.

A baseboard management controller (BMC) is a dedicated processor inside the machine responsible for managing and monitoring the hardware layer of compute nodes, servers, or network devices. BMC performs these tasks through an individual independent connection. IPMI (Intelligent Platform Management Interface) is one of the popular traditional standards used to monitor and control the health and functionality of a system at the hardware layer. Redfish [2] is a new hardware-based management technology designed as the next-generation management standard.

This project aims to use IPMI and Redfish to access the BMC of the nodes and gather the MAC address of the selected internal interface based on the selected internal interface by the admin of the cluster. It helps to automate the process of adding nodes to a data center better than it has been.

By starting from BMC, we set all nodes to use DHCP for their BMC addresses. And then, use the BMC to explore the Mac addresses of the interfaces and allow the user to select which will be the provisioning interface, which will be the control interfaces. The proposed method is the opposite of what we usually do: to shoot a node by knowing its mac address by manually harvesting it—then shooting the image; Once the image is up, it gets provisioned through the BMC. Our implemented method is backward. The new approach makes the new nodes auto-discovered, and you never have to write down their mac addresses manually. Therefore, the proposed method improves the automation of scaling up a cluster using hardware management tools. The tool provides two options for users. First, network discovery: it gets a range of BMC-IP addresses and checks the list of available network interfaces. It saves the information in a JSON file. Second, expanding the cluster: It gets a range of BMC-IP addresses, and based on the internal network NIC, it updates the “input.local” file by inserting the mac-addresses of nodes there.

## 2- About The Tool

The OpenHPC-Get-Mac Application is available here at GitHub.

It contains two directories: Codes and Doc-Files.

The Codes directory contains:

    • ipmi.py
    • displayInfoIPMI.py
    • redfish.py
    • displayInfoRedfish.py
    • userInterfaceApp.py

ipmi.py is for gathering information from BMC using IPMI. It uses multithreading to improve the speed of gathering information for a large cluster. displayInfoIPMI.py is for displaying the collected data by IPMI in a nice friendly format.

redfish.py is for gathering information from BMC using DMTF Redfish. It uses multithreading to improve the speed of gathering information for a large cluster. displayInfoRedfish.py is for displaying the collected data by Redfish in a nice friendly format.

userInterfaceApp.py is for running the interface of the application.

The Doc-Files directory contains the following input files:

    • Readme
    • credentialInfo.txt
    • clusterInfo

And also, the following two output files will be added to the Doc-Files directory after running the application:

    • ClusterNetInfo.json
    • input.local

Readme file has information about the application.

credentialInfo.txt has the BMC_User and BMC_Password of the cluster.

clusterInfo is the default file that contains a list of BMC IP addresses of the nodes we want to add to the cluster. We can use this default file or any other file with those IP addresses by giving its path when the application asks for it.

ClusterNetInfo.json is the output file to save the collected data in a JSON format.

“input.local” file is the output file that contains the value of compute_prefix and sms_eth_internal variables, the name, BMC-IP address, and mac address of the nodes based on the selected internal NIC.

    • compute_prefix 
    • sms_eth_internal
    • c_name[i]
    • c_bmc[i]
    • c_mac[i]

## 3-How To use the application:
### Step 1: Make sure you have the following python libraries.

    • requests
    • ipaddress
    • json
    • datetime
    • subprocess
    • codecs
    • Thread
    • time
    • os

You can use one of the following commands to install a package if you do not have it.

    • python -m pip install package-name
    • pip install --user package-name
    • python3 -m pip install package-name
    • pip3 install --user package-name

### Step 2: Set up input files.

    • Modify clusterInfo file in the Doc-Files directory and insert the BMC IP addresses of the nodes there(one IP per line).
    • Modify the credentialInfo.txt file in the Doc-Files directory, and set up the BMC-User and BMC_Password of the cluster in this file.

### Step 3: Run the OpenHPC-Get-Mac application.

Run the OpenHPC-Get-Mac application using the following command.

    python3 userInterfaceApp.py

### Step 4: Follow the process based on the interface guideline.

The application gives you four options:

    1) About the Application
    2) Network Discovery
    3) Update Cluster Mac Address Information  
    4) Exit

The first option shows some information about the application.

The second one is network discovery, and you have two options, and we can select which hardware management technology we want to use to collect data:

     1) IPMI
     2) Redfish

Then it asks you to select the path to the cluster information file (Default: ../Doc-Files/clusterInfo).

For IPMI choice:

you also need to choose the vendor of the new compute-nodes(Default=Dell):

     1) Dell
     2) SuperMicro
     3) Intel
     4) Others

This step is because of having different IPMI commands to gather mac addresses for various vendors. We do not have this step when we use Redfish to collect data. It then shows the collected data in a friendly format and saves them in the ../Doc-Files/ClusterNetInfo.json file. Then it comes back to the menu.

The third option is to Update Cluster Mac Address Information.

It asks to select the hardware management technology we want to use, the number of the internal NIC, and the compute prefix we want to use. Then it asks to choose the path to the cluster information file (Default: ../Doc-Files/clusterInfo), and for IPMI, it Also asks to select the compute-nodes vendor.

### Output

After collecting data, the gathered discovery Information will be saved in the ../Doc-Files/ClusterNetInfo.json file. The “input.local” file will then be created and held in the ../Doc-Files/input.local file.

## 4- Demo

Please visit the following links and check the video which shows how to use the application.

Presentation:
 [Introduce OpenHPC-Get-Mac Application](https://drive.google.com/file/d/1f3Yd5aaDj9zhgw_8wExsCsIUUdvJE7s5/view?usp=sharing)
	
	 
Demo:
 [Introduce OpenHPC-Get-Mac Application](https://drive.google.com/file/d/1rSuk2ugNkjkiPHGa4pc7ef5pP9V6tV05/view?usp=sharing)

• Demo-paer1:  Running the Application in the RedRaider Cluster (using Redfish)

                 • Testbed: RedRaider Cluster

• Demo-part2:  Running the Application in the Zephyr Cluster (using IPMI)

                 • Testbed: Zephyr Cluster


Demo: https://youtu.be/6jNhuDPta5Q?t=117

Demo-IPMI: https://drive.google.com/file/d/1jWTTz7lo5DpZZxZs-f716BiqlskCOiTr/view?usp=sharing

Presentation: https://youtu.be/kDQWN6bbPMc
		   



## 5- Acknowledgments

This research is supported by the OpenHPC community. Many thanks to the project mentors, Ms. [Nirmala Sundararajan](https://github.com/nirmalasrjn), Mr. [Reese Baird](https://github.com/crbaird), Dr. [Alan Sill](https://github.com/alansill), and Dr. [Yong Chen](https://www.depts.ttu.edu/cs/faculty/yong_chen/index.php); for their guidance, help, and support. It uses the Red Raider Cluster located at the High-Performance Computing Center at Texas Tech University, and also the Zephyr cluster located at the Gleamm (Global Laboratory for Energy Asset Management and Manufacturing) site as testbeds.

## 6-Support or Contact

If you have trouble with running the project, or any question about that please contact Elham Hojati.

## 7- References

[1] https://openhpc.community/

[2] https://www.dmtf.org/standards/redfish
