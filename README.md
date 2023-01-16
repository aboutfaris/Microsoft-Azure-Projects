![image](https://user-images.githubusercontent.com/109401839/212763428-5ec473e9-9048-4cc0-bf1b-0133ac4db278.png)

<h1>Building Intuition for DNS</h1>
Welcome back! In this tutorial, we will build a solid fundamental understanding of DNS. <br />

<h2>Environments and Technologies Used</h2>

- Microsoft Azure (Virtual Machines/Compute)
- Remote Desktop
- DNS

<h2>Operating Systems Used </h2>

- Windows 10 (21H2)

<h2>List of Prerequisites</h2>

- Active Directory Installed
- Client and Domain Controller Connected

![image](https://user-images.githubusercontent.com/109401839/212764385-ea1b8467-c408-4335-879e-2cf80147888c.png)

What is DNS? The Domain Name System (DNS) is the phonebook of the Internet. It basically allows us to convert IP addresses from numbers (8.8.8.8) to readable addresses like (www.google.com). Imagine, when using your smartphone and we ask our built in assistant, "Hey Siri, call USPS nearby" and siri then finds that address, converts it to a number, and connects us to the USPS. 

<h2>Actions and Observations</h2>
**A-Record Exercise**

1. **Connect/log into DC-1 as your domain admin account (mydomain.com\jane_admin)**
2. **Connect/log into Client-1 as an admin (mydomain\jane_admin)**
3. **From Client-1 try to ping “mainframe” notice that it fails**
4. **Nslookup “mainframe” notice that it fails (no DNS record)**
5. **Create a DNS A-record on DC-1 for “mainframe” and have it point to DC-1’s Private IP address
> DNS Manager via Server Manager
> Forward Lookup
>Mydomain
>manualltyy create A record with ip of dc**
6. **Go back to Client-1 and try to ping it. Observe that it works**

**Local DNS Cache Exercise**

1. **Go back to DC-1 and change mainframe’s record address to 8.8.8.8**
2. **Go back to Client-1 and ping “mainframe” again. Observe that it still pings the old address
> because still exist in client cache so pings old ip address.** 
3. **Observe the local dns cache (ipconfig /displaydns)**
4. **Flush the DNS cache (ipconfig /flushdns). Observe that the cache is empty**
5. **Attempt to ping “mainframe” again. Observe the address of the new record is showing up**

**CNAME Record Exercise**

1. **Go back to DC-1 and create a CNAME record that points the host “search” to “www.google.com”**
2. **Go back to Client-1 and attempt to ping “search”, observe the results of the CNAME record**
3. **On Client-1, nslookup “search”, observe the results of the CNAME record**
