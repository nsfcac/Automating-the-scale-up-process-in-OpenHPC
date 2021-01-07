# Improving the Automation of Scaling-up an OpenHPC Cluster
## (Gathering Mac Address of Internal Network by Redfish/IPMI Hardware Management Tools)

### 1- About The Tool
OpenHPC [1] is a tool for creating, composing, and administering high-performance computing clusters. It provides methods to register nodes and provide the information needed to provision them and integrate them into data centers. In the current OpenHPC methodology for creating a cluster, we need to have the Mac addresses of all the compute nodes in advance and manually type in the “input.local” file. It is a time-consuming step, especially for big data centers with a massive number of compute nodes. 

A baseboard management controller (BMC) is a dedicated processor inside the machine responsible for managing and monitoring the hardware layer of compute nodes, servers, or network devices. BMC performs these tasks through an individual independent connection.  IPMI (Intelligent Platform Management Interface)  is one of the popular traditional standards used to monitor and control the health and functionality of a system at the hardware layer.    Redfish [2] is a new hardware-based management technology designed as the next-generation management standard. 

This project aims to use IPMI and Redfish to get access to the BMC of the nodes and gather the MAC address of the selected internal interface based on the selected internal interface by the admin of the cluster. It helps to automate the process of adding nodes to a data center better than it has been.  

By starting from BMC, we set all nodes to use DHCP  for their BMC addresses. And then, use the BMC to explore the Mac addresses of the interfaces and allow the user to select which will be the provisioning interface, which will be the control interfaces. The proposed method is the opposite of what we usually do: to shoot a node by knowing its mac address by manually harvesting it—then shooting the image; Once the image is up, it gets provisioned through the BMC. Our implemented method is backward. The new approach makes the new nodes auto-discovered, and you never have to write down their mac addresses manually. Therefore, the proposed method improves the automation of scaling up a cluster using hardware management tools. The tool provides two options for users. First, network discovery: it gets a range of BMC-IP addresses and checks the list of available network interfaces. It saves the information in a JSON file. Second, expanding the cluster: It gets a range of BMC-IP addresses, and based on the internal network NIC, it updates the “input.local” file by inserting the mac-addresses of nodes there.

## 2- Demo

Please visit the following link and check the video which shows how to use the application.


https://youtu.be/k6oiz_1vANE

## 3- Acknowledgments

This research is supported by the OpenHPC community. Many thanks to the mentors of the project; Ms. [Nirmala Sundararajan](https://github.com/nirmalasrjn), Mr. [Reese Baird](https://github.com/crbaird), Dr. [Alan Sill](https://github.com/alansill), and Dr. [Yong Chen](https://www.depts.ttu.edu/cs/faculty/yong_chen/index.php);  for their guidance, help and support. 




## 3-Support or Contact

If you have trouble with running the project, or any question about that please contact [Elham Hojati](https://github.com/elham1296).


## References

[1] https://openhpc.community/

[2] https://www.dmtf.org/standards/redfish

