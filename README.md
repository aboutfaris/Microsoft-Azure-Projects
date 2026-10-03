![image](https://user-images.githubusercontent.com/109401839/212763428-5ec473e9-9048-4cc0-bf1b-0133ac4db278.png)

# Building Intuition for DNS

Welcome back! In this tutorial, we build a solid fundamental understanding of DNS.

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

What is DNS? The Domain Name System (DNS) is the phonebook of the internet. It converts numeric IP addresses (like `8.8.8.8`) into readable addresses (like `www.google.com`). Imagine asking your phone's voice assistant to "call the nearest pharmacy": the assistant finds the address, resolves it to a number, and connects the call. DNS does the same thing for websites.

<h2>Actions and Observations</h2>
**A-Record Exercise**

![vivaldi_te0ncrjmC3](https://user-images.githubusercontent.com/109401839/213228476-10566ab6-eff5-467e-a836-76b21cc14b09.png)

1. Connect/log into DC-1 as your domain admin account (`mydomain.com\jane_admin`)
2. Connect/log into Client-1 as an admin (`mydomain\jane_admin`)
3. From Client-1, try to ping "mainframe" and notice that it fails
4. Run `nslookup mainframe` and notice that it fails (no DNS record)
5. Create a DNS A record on DC-1 for "mainframe" pointing to DC-1's private IP address

Double-check your spelling. The first time I did this, I misspelled "mainframe" as "mainfame" and couldn't figure out why it wasn't working. Lesson learned.

![2023-01-18 10 12 45 coursecareers com ef528124c90b](https://user-images.githubusercontent.com/109401839/213230206-6f8bb790-3ed4-4a81-b431-d84fd177b8b1.jpg)


Open DNS Manager via Server Manager, go to Forward Lookup Zones > your domain, and manually create an A record with DC-1's IP address.

6. Go back to Client-1 and try to ping it. Observe that it now works.

![vivaldi_aRBUA6joTQ](https://user-images.githubusercontent.com/109401839/213231056-fb8de6ee-e1ca-4eba-8097-25dcf4268f60.png)

### Local DNS Cache Exercise

1. Go back to DC-1 and change "mainframe"'s record address to `8.8.8.8`.

   ![vivaldi_kCL8ATV9xe](https://user-images.githubusercontent.com/109401839/213231797-93173e4c-eb96-4b2b-902e-090c37d38f2f.png)

2. Go back to Client-1 and ping "mainframe" again. Observe that it still pings the old address, because the old record still exists in the client's local DNS cache.

   ![vivaldi_b8guefs1IO](https://user-images.githubusercontent.com/109401839/213232169-7cbd4961-08e0-409c-acfb-bdb2c0c3904a.png)

3. Observe the local DNS cache with `ipconfig /displaydns`.
4. Flush the DNS cache with `ipconfig /flushdns`. Observe that the cache is now empty.

   ![vivaldi_ngpZOpAny4](https://user-images.githubusercontent.com/109401839/213232520-8c9a7a92-b407-4b4f-89b7-844e25ff2e50.png)

5. Ping "mainframe" again. Observe that the new record's address now shows up.

   ![vivaldi_mM61VFUhCE](https://user-images.githubusercontent.com/109401839/213232855-48f2d665-3370-4e88-a168-801d029033c9.png)

### CNAME Record Exercise

![CNAME record diagram](https://user-images.githubusercontent.com/109401839/213233343-f7ff8421-db7d-4a62-a074-58e607ccada8.jpg)

1. Go back to DC-1 and create a CNAME record that points the host "search" to "www.google.com".
2. Go back to Client-1 and attempt to ping "search". Observe the results of the CNAME record.

   ![vivaldi_8fNzswyh0V](https://user-images.githubusercontent.com/109401839/213233611-e5ed9231-42db-4b85-95d1-3f28f166416f.png)

3. On Client-1, run `nslookup search` and observe the results of the CNAME record.
