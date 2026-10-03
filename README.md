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

1. For this demonstration, we need to create two virtual machines using Microsoft Azure. One machine will use Ubuntu Linux, and the other will use Windows 10 as its operating system. Both should have a minimum of a two-core virtual CPU; personally, I went with four cores. Once both are set up, log in to the Windows 10 VM. Download and install [WireShark](https://www.wireshark.org/download.html).

![2023-01-18 10 44 12 coursecareers com 8c7c0e9793bb](https://user-images.githubusercontent.com/109401839/213242045-9299d76b-2631-4b63-818f-3a74a8a9b3ab.jpg)


Open WireShark and filter for ICMP traffic only. This traffic displays the relay request and reply, also known as "ping". We can see how many packets are requested and received, and inspect the data of the packets in WireShark.

![vivaldi_Z27HHIWElt](https://user-images.githubusercontent.com/109401839/213242732-517627c3-b557-40bc-906e-cce25ec02953.png)

2. Let's observe a different kind of traffic: SSH. Filter for SSH traffic only in WireShark. From the Windows 10 VM, SSH into the Ubuntu VM using the command `ssh username@ipaddress` (in my case, `ssh labuser@10.0.0.4`). WireShark will immediately show the SSH packets between the two VMs.

![vivaldi_voFaQKzigU](https://user-images.githubusercontent.com/109401839/213243011-f74fa2ba-ba3f-4c0f-938f-2915b998b68e.png)


3. Observe DHCP traffic. DHCP (Dynamic Host Configuration Protocol) operates on ports 67 and 68, and its main function is to assign IP addresses to devices. Filter for DHCP in WireShark. Issue a new IP address to the Windows 10 VM by running `ipconfig /renew` in CMD, then inspect WireShark for this traffic.

![vivaldi_2hRg2VDUxe](https://user-images.githubusercontent.com/109401839/213243361-2e338ef0-af7c-47b9-9387-6a002791fd07.png)

4. Observe DNS traffic. Filter for DNS. In CMD, use `nslookup` to resolve a domain (such as google.com) to an IP address, then inspect the traffic WireShark captures.

![vivaldi_p4LlxYiVLv](https://user-images.githubusercontent.com/109401839/213243701-b3915d44-2aa3-4fe7-b637-e7d9c5ecd6c3.png)

5. Observe RDP traffic. Filter for RDP by entering `tcp.port == 3389` in WireShark. Traffic flows continuously, showing a live stream of packets between the two computers.

![vivaldi_yi916o0Wbr](https://user-images.githubusercontent.com/109401839/213243903-af301b6a-d633-457e-ad1f-dc22cb93edf5.png)
