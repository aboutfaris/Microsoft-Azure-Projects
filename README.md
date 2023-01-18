![image](https://user-images.githubusercontent.com/109401839/212763285-615193c5-a326-4fe5-8387-fa77727c3666.png)

<h1>Network File Shares and Permissions</h1>
Welcome back! In this tutorial, We will create folders in DC-1 from the previous Tutorial. <br />

<h2>Environments and Technologies Used</h2>

- Microsoft Azure (Virtual Machines/Domain Controller/Client Machine)
- Remote Desktop
- Shared Network Files

<h2>Operating Systems Used </h2>

- Windows 10 (21H2)

<h2>Actions and Observations</h2>

Create some sample file shares with various permissions

1. Connect/log into DC-1 as your domain admin account (mydomain.com\jane_admin)
2. Connect/log into Client-1 as a normal user (mydomain\<someuser>)
3. On DC-1, on the C:\ drive, create 4 folders: “read-access”, “write-access”, “no-access”, “accounting”

![vivaldi_9PMyBqb1rk](https://user-images.githubusercontent.com/109401839/213238510-ac5e4b21-e1aa-4c55-a6bb-5896316fa34c.png)


4. Set the following permissions (share the folder) for the “Domain Users” group:

![vivaldi_udC3XRiOew](https://user-images.githubusercontent.com/109401839/213168775-c3202790-fd5b-412a-9403-c2a34f312c38.png)

5. Folder: “read-access”, Group: “Domain Users”, Permission: “Read”
6. Folder: “write-access”, Group: “Domain Users”, Permissions: “Read/Write”
7. Folder: “no-access”, Group: “Domain Admins”, “Permissions: “Read/Write"

![vivaldi_HFyJKXmKru](https://user-images.githubusercontent.com/109401839/213238914-a7cf2107-1316-49ff-a143-aee24da4e0cc.png)

8. **(Skip accounting for now)**

![2023-01-18 10 35 24 camo githubusercontent com bb1553347d44](https://user-images.githubusercontent.com/109401839/213239334-f81e1da5-d6ea-4dd7-a5b6-cc2dfd1d8825.jpg)


**Attempt to access file shares as a normal user**

1. **On Client-1, navigate to the shared folder (start, run, \\dc-1)**

![vivaldi_2EJQr6eI7x](https://user-images.githubusercontent.com/109401839/213240066-cc5d8dbe-03fa-4c49-9b61-a26f385f6d18.png)

2. **Try to access the folders you just created. Which folders can you access? Which folders can you create stuff in?**

![vivaldi_mKtfJuMugZ](https://user-images.githubusercontent.com/109401839/213240171-a71b0990-f0e4-47e4-b29d-a1cf75d6b107.png)


**Create an “ACCOUNTANTS” Security Group, assign permissions, an test access**

1. **Go back to DC-1, in Active Directory, create a security group called “ACCOUNTANTS”**

![vivaldi_21iy1mXf9Y](https://user-images.githubusercontent.com/109401839/213240836-dc93efd1-db6d-4a5f-b073-8107f9059209.png)

![vivaldi_l2gDyFcQNi](https://user-images.githubusercontent.com/109401839/213241010-c6724461-224c-4ea2-91af-5e36ed9b63c4.png)


2. **On the “accounting” folder you created earlier, set the following permissions:**
3. **Folder: “accounting”, Group: “ACCOUNTANTS”, Permissions: “Read/Write”**

![vivaldi_SeDK46vClF](https://user-images.githubusercontent.com/109401839/213241173-107c6264-0c34-463e-ae23-b4bd816b7dad.png)

4. **On Client-1, as <someuser>, try to access the accountants folder. It should fail.**
5. **Log out of Client-1 as <someuser>**
6. **On DC-1, make <someuser> a member of the “ACCOUNTANTS” Security Group**
7. **Sign back into Client-1 as <someuser> and try to access the “accounting” share in \\DC-1\**

In the [next tutorial](https://github.com/fnabeel/Building-Intuition-for-DNS),  we will go over settingup DNS. You may keep the virtual machine from this lab and continue with the next tutorial. 
