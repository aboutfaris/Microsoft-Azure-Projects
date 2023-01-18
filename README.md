<p align="center">
<img src="https://i.imgur.com/Ua7udoS.png" alt="Traffic Examination"/>
</p>

<h1>Network Security Groups (NSGs) and Inspecting Traffic Between Azure Virtual Machines</h1>
Welcome back! In this tutorial, we observe various network traffic to and from Azure Virtual Machines with Wireshark as well as experiment with Network Security Groups. <br />

<h2>Environments and Technologies Used</h2>

- Microsoft Azure (Virtual Machines/Compute)
- Remote Desktop
- Various Command-Line Tools
- Various Network Protocols (SSH, RDH, DNS, HTTP/S, ICMP)
- Wireshark (Protocol Analyzer)

<h2>Operating Systems Used </h2>

- Windows 10 (21H2)
- Ubuntu Server 20.04

<h2>High-Level Steps</h2>

- Observe ICMP Traffic
- Observe SSH Traffic
- Observe DHCP Traffic
- Observe DNS Traffic
- Observe RDP Traffic

<h2>Actions and Observations</h2>

1. For this demonstrations we will need to create two virtual machines using Microsoft Azure. One machine will use Ubuntu Linux, and the other will use Windows 10 as its operating system. Both will have should have a minimum of a two-core virtual cpu, personally I went with four-cores. Once both is set-up, go ahead and login to the Windows 10 version. Download and Install [WireShark](https://www.wireshark.org/download.html). 

![2023-01-18 10 44 12 coursecareers com 8c7c0e9793bb](https://user-images.githubusercontent.com/109401839/213242045-9299d76b-2631-4b63-818f-3a74a8a9b3ab.jpg)


Open WireShark and for ICMP Traffic only. This traffic will display the relay request and deliver, also known as "ping". We will be able to see how many packets are requested and recieved. The cool thing is that we can inspect the data of the packets in WireShark. 

![vivaldi_Z27HHIWElt](https://user-images.githubusercontent.com/109401839/213242732-517627c3-b557-40bc-906e-cce25ec02953.png)

2. Let us observe a different kind of Traffic, SSH. Filter for SSH traffic only in WireShark. From the Windows 10 VM, "SHH into" the Ubuntu VM. This can be done by using the command, "SSH username@ipaddress" in my case, SSH labuser@10.0.04 , then we will see that WireShark immediately sees the SSH packets between the two VM. 

![vivaldi_voFaQKzigU](https://user-images.githubusercontent.com/109401839/213243011-f74fa2ba-ba3f-4c0f-938f-2915b998b68e.png)


3. Obeserve DHCP Traffic, DHCP is Dynamic Host Configuration Protocol which operates on ports 67 and 68. The main function of DHCP is to assign different devices their IP-Address. Filter for DHCP in WireShark. We can attempt to issue a new IP address to our Windows 10 VM by using CMD and entering the line "IPCONFIG /RENEW". Now, inspect WireShark for this traffic. 

![vivaldi_2hRg2VDUxe](https://user-images.githubusercontent.com/109401839/213243361-2e338ef0-af7c-47b9-9387-6a002791fd07.png)

4. Observe DNS Traffic, once again, filter for DNS. In CMD, lets use the command "nslookup" to see what google.com or most of any website IP addresses are. Now, inspect WireShark and the traffic it is capturing here. 

![vivaldi_p4LlxYiVLv](https://user-images.githubusercontent.com/109401839/213243701-b3915d44-2aa3-4fe7-b637-e7d9c5ecd6c3.png)

5. Observe RDP Traffic, Filter for RDP. We can do this by entering "tcp.port == 3389" in WireShark. Traffic is now constantly flowing, showing a live stream of packets between one computer to another. Fascinating isnt it? 

![vivaldi_yi916o0Wbr](https://user-images.githubusercontent.com/109401839/213243903-af301b6a-d633-457e-ad1f-dc22cb93edf5.png)


In the [next tutorial](https://github.com/fnabeel/Network-File-Shares-and-Permissions),  we will go over settingup Network File Sharing and Permissions. I recommend not destroying your virtual machine you have created in this tutorial. It will come in handy next time !
