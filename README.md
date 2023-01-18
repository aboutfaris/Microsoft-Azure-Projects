<p align="center">
<img src="https://i.imgur.com/pU5A58S.png" alt="Microsoft Active Directory Logo"/>
</p>

<h1>On-premises Active Directory Deployed in the Cloud (Azure)</h1>

Welcome back! This tutorial outlines the implementation of on-premises Active Directory within Azure Virtual Machines.<br />

<h2>Environments and Technologies Used</h2>

- Microsoft Azure (Virtual Machines/Compute)
- Remote Desktop
- Active Directory Domain Services
- PowerShell

<h2>Operating Systems Used </h2>

- Windows Server 2022
- Windows 10 (21H2)

<h2>High-Level Deployment and Configuration Steps</h2>

- Setup Resources In Azure
- Ensure Connection between Client and Domain Controller
- Install Active Directory and Admin Creation
- Create X-Amount of Client Users using PowerShell Script

<h2>Setup Resources in Azure</h2>

1. Create the Domain Controller VM (Windows Server 2022) named “DC-1"
   Take note of the Resource Group and Virtual Network (Vnet) that get created at this time
2. Set Domain Controller’s NIC Private IP address to be static
DC-1 > Networking > NIC > IP Configurations

![vivaldi_zDAEQAVoDh](https://user-images.githubusercontent.com/109401839/212756392-d05a4c3b-610c-4fe8-a5e8-1e31e86da7e3.png)

3. Create the Client VM (Windows 10) named “Client-1”. Use the same Resource Group and Vnet that was created in the DC-1 step.
4. Ensure that both VMs are in the same Vnet [you can check the topology with Network Watcher]
Here is an illustration of what we are doing: 

![vivaldi_z3kENJuYuV](https://user-images.githubusercontent.com/109401839/213212076-117f26c0-c06f-4bb0-871a-45a97f293acf.png)


![vivaldi_QbUpS9XsXc](https://user-images.githubusercontent.com/109401839/212757249-70c7c150-9627-408f-a285-53b0f9d34a09.png)

<h2>Ensure Connection between Client and Domain Controller<h2>

1. Login to Client-1 with Remote Desktop and ping DC-1’s private IP address with ping -t <ip address> (perpetual ping)

![vivaldi_3DGaaVQRmB](https://user-images.githubusercontent.com/109401839/213212386-519dc0bd-6913-49f1-b3e3-8bbb260741a5.png)

Oh! Notice we are getting a "Request timed out." Let us fix that. 

2. Login to the Domain Controller and enable ICMPv4 in on the local windows Firewall, keep client-1 instance open. 

- Start Menu > Windows Defender Firewall with Advanced Secruity programme > Inbound Rules > Sort by Porotocol > 

- Enable "Core Networking Diagnostics - ICMP Echo Request (ICMPv4-In) Private and Domain Profiles. 2 Inbound Rules.

![Inkedvivaldi_Gb9rFL8rhC](https://user-images.githubusercontent.com/109401839/213214025-94b0bfb0-f017-4e8b-8676-d01ffeb9ab93.jpg)


3. Check back at Client-1 to see the ping succeed

![vivaldi_WbtokOOBck](https://user-images.githubusercontent.com/109401839/213214146-018e77d5-98a4-4256-91fd-16647ff58006.png)

Look at that beautiful traffic. Now its time to ... 

<h2>Install Active Directory<h2>



1. Login to DC-1 and install Active Directory Domain Services

- Server Manager > "Add Roles and Features" > Check "Active Directory Domain Services"

![vivaldi_od5BgUKG6G](https://user-images.githubusercontent.com/109401839/213214935-0fe230d0-60be-431a-bf31-53cfc50748b9.png)

2. Promote as a DC: Setup a new forest as mydomain.com (can be anything, just remember what it is)

![2023-01-18 09 37 20 coursecareers com a3928ff24e0f](https://user-images.githubusercontent.com/109401839/213215535-f43842d0-f1ab-4c6a-91d1-18d8a9bdff06.jpg)

![2023-01-18 09 38 10 coursecareers com 78e39ae4181d](https://user-images.githubusercontent.com/109401839/213215738-c6379380-e5b8-438b-95a8-6906a16ff339.jpg)

3. Restart and then log back into DC-1 as user: mydomain.com\labuser

![vivaldi_xJc36FTsPS](https://user-images.githubusercontent.com/109401839/213216324-dccbe8d1-3791-4eea-8609-6643d27f1bc9.png)

![vivaldi_ADY0CCC3v8](https://user-images.githubusercontent.com/109401839/213217001-5c300c3f-f194-4df9-bb68-b4fb464e500c.png)

4. In Active Directory Users and Computers (ADUC), create an Organizational Unit (OU) called “_EMPLOYEES"

![Inkedvivaldi_YgN8JfZgEn](https://user-images.githubusercontent.com/109401839/213217570-765d4e0f-05dd-4985-b6e5-0ce1210d6338.jpg)

5. Create a new OU named “_ADMINS"

![vivaldi_JXNeaUMVFe](https://user-images.githubusercontent.com/109401839/213218280-33c7fe97-751c-4ba8-8900-dd90821fc579.png)

6. Create a new employee named “Jane Doe” (same password) with the username of “jane_admin”
7. Add jane_admin to the “Domain Admins” Security Group

![2023-01-18 09 46 52 camo githubusercontent com 6837ec50b4c5](https://user-images.githubusercontent.com/109401839/213219498-06b86aa6-a2ef-48cb-b653-069ca85c0b0e.jpg)

8. Log out/close the Remote Desktop connection to DC-1 and log back in as “mydomain.com\jane_admin"
9. User jane_admin as your admin account from now on

<h2>Join Client-1 to your domain (mydomain.com)<h2>

![vivaldi_cRAVrKouac](https://user-images.githubusercontent.com/109401839/213221204-72c7058c-3730-47d9-b9fb-4435ee87c3fd.png)

1. From the Azure Portal, set Client-1’s DNS settings to the DC’s Private IP address
2. From the Azure Portal, restart Client-1
3. Login to Client-1 (Remote Desktop) as the original local admin (labuser) and join it to the domain (computer will restart)
4. Login to the Domain Controller (Remote Desktop) and verify Client-1 shows up in Active Directory Users and Computers (ADUC) inside the “Computers” container on the root of the domain
5. Create a new OU named “_CLIENTS” and drag Client-1 into there

<H2>Setup Remote Desktop for non-administrative users on Client-1<H2>

1. Log into Client-1 as mydomain.com\jane_admin and open system properties

![vivaldi_pBr66s3R4C](https://user-images.githubusercontent.com/109401839/213220623-04e09574-52ad-407a-945b-f53f52417b50.png)

2. Click “Remote Desktop”
3. Allow “domain users” access to remote desktop

![Inkedvivaldi_uNcBpy336J](https://user-images.githubusercontent.com/109401839/213223500-193b62e3-062f-4f69-8da4-5ef96692ec31.jpg)


4. You can now log into Client-1 as a normal, non-administrative user now
5. Normally you’d want to do this with Group Policy that allows you to change MANY systems at once

<H2>Create a bunch of additional users and attempt to log into client-1 with one of the users<H2>

1. Login to DC-1 as jane_admin
2. Open PowerShell_ise as an administrator
3. Create a new File and paste the contents of the [script] below:


> '''Function generate-random-name() {
>    $consonants = @('b','c','d','f','g','h','j','k','l','m','n','p','q','r','s','t','v','w','x','z')
>    $vowels = @('a','e','i','o','u','y')
>    $nameLength = Get-Random -Minimum 3 -Maximum 7
>    $count = 0
>    $name = ""
>
>    while ($count -lt $nameLength) {
>        if ($($count % 2) -eq 0) {
>            $name += $consonants[$(Get-Random -Minimum 0 -Maximum $($consonants.Count - 1))]
>        }
>        else {
>            $name += $vowels[$(Get-Random -Minimum 0 -Maximum $($vowels.Count - 1))]
>        }
>        $count++
>    }
>
>    return $name
>
> }
>
> $count = 1
> while ($count -lt $NUMBER_OF_ACCOUNTS_TO_CREATE) {
>    $fisrtName = generate-random-name
>    $lastName = generate-random-name
>    $username = $fisrtName + '.' + $lastName
>    $password = ConvertTo-SecureString $PASSWORD_FOR_USERS -AsPlainText -Force
>
>    Write-Host "Creating user: $($username)" -BackgroundColor Black -ForegroundColor Cyan
>    
>    New-AdUser -AccountPassword $password `
>               -GivenName $firstName `
>               -Surname $lastName `
>               -DisplayName $username `
>               -Name $username `
>               -EmployeeID $username `
>               -PasswordNeverExpires $true `
>               -Path "ou=_EMPLOYEES,$(([ADSI]`"").distinguishedName)" `
>               -Enabled $true
>    $count++
> }''' 

[Code Source](https://github.com/joshmadakor1/AD_PS/blob/master/Generate-Names-Create-Users.ps1)

4. Run the script and observe the accounts being created

![vivaldi_Lr0ydPgSZ7](https://user-images.githubusercontent.com/109401839/213226346-7dc7f494-6299-4fab-a210-d07a16b71b97.png)


5. When finished, open ADUC and observe the accounts in the appropriate OU
6. Attempt to log into Client-1 with one of the accounts (take note of the password in the script)

![vivaldi_hbfgkZ3l45](https://user-images.githubusercontent.com/109401839/213226577-6f5bd613-ba81-4a62-bc7c-98896e41c94a.png)


Thats is it ! In the [next tutorial](https://github.com/fnabeel/-azure-network-protocols), we will go over various network traffic to and from Azure Virtual Machines with Wireshark as well as experiment with Network Security Groups.
