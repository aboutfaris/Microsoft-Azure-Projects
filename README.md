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

![cloudflare-1111](https://user-images.githubusercontent.com/109401839/213241753-8772baf2-c4fd-4721-827b-c86fb18ae13c.gif)

What is DNS? The Domain Name System (DNS) is the phonebook of the Internet. It basically allows us to convert IP addresses from numbers (8.8.8.8) to readable addresses like (www.google.com). Imagine, when using your smartphone and we ask our built in assistant, "Hey Siri, call USPS nearby" and siri then finds that address, converts it to a number, and connects us to the USPS. 

<h2>Actions and Observations</h2>
**A-Record Exercise**

![vivaldi_te0ncrjmC3](https://user-images.githubusercontent.com/109401839/213228476-10566ab6-eff5-467e-a836-76b21cc14b09.png)

1. **Connect/log into DC-1 as your domain admin account (mydomain.com\jane_admin)**
2. **Connect/log into Client-1 as an admin (mydomain\jane_admin)**
3. **From Client-1 try to ping “mainframe” notice that it fails**
4. **Nslookup “mainframe” notice that it fails (no DNS record)**
5. **Create a DNS A-record on DC-1 for “mainframe” and have it point to DC-1’s Private IP address

Be sure to spellcheck everything, when I did it for the first time I mispelled "mainframe" as "mainfame" and could not figure out why it was not working. Lesson Learned. 

![2023-01-18 10 12 45 coursecareers com ef528124c90b](https://user-images.githubusercontent.com/109401839/213230206-6f8bb790-3ed4-4a81-b431-d84fd177b8b1.jpg)


> DNS Manager via Server Manager
> Forward Lookup
>Mydomain
>manualltyy create A record with ip of dc**
6. **Go back to Client-1 and try to ping it. Observe that it works**

![vivaldi_aRBUA6joTQ](https://user-images.githubusercontent.com/109401839/213231056-fb8de6ee-e1ca-4eba-8097-25dcf4268f60.png)

**Local DNS Cache Exercise**

1. **Go back to DC-1 and change mainframe’s record address to 8.8.8.8**

![vivaldi_kCL8ATV9xe](https://user-images.githubusercontent.com/109401839/213231797-93173e4c-eb96-4b2b-902e-090c37d38f2f.png)

2. **Go back to Client-1 and ping “mainframe” again. Observe that it still pings the old address

![vivaldi_b8guefs1IO](https://user-images.githubusercontent.com/109401839/213232169-7cbd4961-08e0-409c-acfb-bdb2c0c3904a.png)

> because still exist in client cache so pings old ip address.** 
3. **Observe the local dns cache (ipconfig /displaydns)**
4. **Flush the DNS cache (ipconfig /flushdns). Observe that the cache is empty**

![vivaldi_ngpZOpAny4](https://user-images.githubusercontent.com/109401839/213232520-8c9a7a92-b407-4b4f-89b7-844e25ff2e50.png)

5. **Attempt to ping “mainframe” again. Observe the address of the new record is showing up**

![vivaldi_mM61VFUhCE](https://user-images.githubusercontent.com/109401839/213232855-48f2d665-3370-4e88-a168-801d029033c9.png)

**CNAME Record Exercise**

![2023-01-18 10 20 47 camo githubusercontent com 352c35d7555a](https://user-images.githubusercontent.com/109401839/213233343-f7ff8421-db7d-4a62-a074-58e607ccada8.jpg)

1. **Go back to DC-1 and create a CNAME record that points the host “search” to “www.google.com”**
2. **Go back to Client-1 and attempt to ping “search”, observe the results of the CNAME record**

![vivaldi_8fNzswyh0V](https://user-images.githubusercontent.com/109401839/213233611-e5ed9231-42db-4b85-95d1-3f28f166416f.png)

3. **On Client-1, nslookup “search”, observe the results of the CNAME record**
