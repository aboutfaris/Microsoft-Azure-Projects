# Configuring On-premises Active Directory within Azure VMs

Build a small Active Directory lab in Azure: a Windows Server domain controller (DC-1), a Windows 10 client (Client-1) joined to the domain, and a batch of test users created with a PowerShell script.

## What you'll use

- Microsoft Azure (Virtual Machines/Compute)
- Remote Desktop
- Active Directory Domain Services
- PowerShell ISE
- Windows Server 2022 (DC-1) and Windows 10 (21H2) (Client-1)

## Prerequisites

- An Azure subscription where you can create virtual machines

## Steps

### Part 1: Set up resources in Azure

1. Create the domain controller VM (Windows Server 2022) named `DC-1`. Take note of the resource group and virtual network (VNet) created with it.
2. Set DC-1's NIC private IP address to static: DC-1 > Networking > NIC > IP configurations > ipconfig1 > Assignment: Static, then Save.

   Expected result: ipconfig1 shows Assignment set to Static, with the private IP (for example 10.0.0.4) on the VNet's default subnet.

3. Create the client VM (Windows 10) named `Client-1`, using the same resource group and VNet as DC-1.
4. Make sure both VMs are in the same VNet. You can check the topology with Network Watcher.

   Expected result: the Virtual machines list shows Client-1 and DC-1 running in the same resource group and region. The plan: DC-1 keeps a static private IP, Client-1 uses that IP as its DNS server, and Client-1 joins the domain through DC-1.

### Part 2: Check connectivity between Client-1 and DC-1

5. Remote Desktop into Client-1 and start a continuous ping to DC-1's private IP:

   ```cmd
   ping -t <dc-1-private-ip>
   ```

   Expected result: "Request timed out." DC-1's firewall blocks ICMP by default.

6. Leave the ping running. Remote Desktop into DC-1 and open Windows Defender Firewall with Advanced Security > Inbound Rules, then sort by Protocol.
7. Enable both "Core Networking Diagnostics - ICMP Echo Request (ICMPv4-In)" rules (Private and Domain profiles): select each rule and click Enable Rule in the Actions pane.
8. Go back to Client-1 and watch the ping.

   Expected result: the timeouts turn into "Reply from <dc-1-private-ip>: bytes=32 time=1ms TTL=128".

### Part 3: Install Active Directory

9. On DC-1, open Server Manager > Add Roles and Features and check Active Directory Domain Services. Finish the wizard.
10. Click the warning flag in Server Manager, then "Promote this server to a domain controller".
11. In Deployment Configuration, choose "Add a new forest" and set the root domain name to `mydomain.com` (it can be anything, just remember it). Finish the wizard and let DC-1 restart.
12. Log back in to DC-1 as `mydomain.com\labuser`.

### Part 4: Create OUs and an admin account

13. Open Active Directory Users and Computers (ADUC) from the Start menu.
14. Right-click `mydomain.com` > New > Organizational Unit and create an OU named `_EMPLOYEES`.
15. Create another OU named `_ADMINS`.
16. In `_ADMINS`, right-click > New > User. Create "Jane Doe" with the username `jane_admin` (same password as labuser).
17. Open Jane Doe's Properties > Member Of > Add..., type `domain`, click Check Names, and pick Domain Admins from Multiple Names Found. Click OK.

    Expected result: the Member Of tab lists Domain Admins and Domain Users.

18. Log out of DC-1 and log back in as `mydomain.com\jane_admin`. Use jane_admin as your admin account from now on.

### Part 5: Join Client-1 to the domain

19. In the Azure portal, set Client-1's DNS server to DC-1's private IP address.
20. In the Azure portal, restart Client-1.
21. Log in to Client-1 as the original local admin (`labuser`). Open System Properties > Change, set Member of > Domain to `mydomain.com`, and click OK. The computer restarts.

    Tip: if the join fails, run `ipconfig /all` on Client-1. "DNS Servers" should show DC-1's private IP. If it still shows Azure's default DNS (168.63.129.16), the DNS change has not applied yet.

22. On DC-1, open ADUC and confirm Client-1 shows up in the Computers container at the root of the domain.
23. Create a new OU named `_CLIENTS` and drag Client-1 into it.

### Part 6: Allow Remote Desktop for non-admin users

24. Log in to Client-1 as `mydomain.com\jane_admin` and open Settings > System > Remote Desktop. Make sure Enable Remote Desktop is On.
25. Click "Select users that can remotely access this PC" > Add. With the location set to `mydomain.com`, enter `Domain Users`, click Check Names, then OK.

    Expected result: normal, non-admin domain users can now Remote Desktop into Client-1. In production you'd do this with Group Policy so you can change many machines at once.

### Part 7: Create users with PowerShell

26. Log in to DC-1 as `jane_admin`.
27. Open PowerShell ISE as an administrator.
28. Create a new file and paste the script below. Set the two variables at the top first: the password every new user gets, and how many accounts to create (the lab run used 10000).

    ```powershell
    # ----- Edit these Variables for your own Use Case ----- #
    $PASSWORD_FOR_USERS   = "<choose-a-lab-password>"
    $NUMBER_OF_ACCOUNTS_TO_CREATE = 10000
    # ------------------------------------------------------ #

    Function generate-random-name() {
        $consonants = @('b','c','d','f','g','h','j','k','l','m','n','p','q','r','s','t','v','w','x','z')
        $vowels = @('a','e','i','o','u','y')
        $nameLength = Get-Random -Minimum 3 -Maximum 7
        $count = 0
        $name = ""

        while ($count -lt $nameLength) {
            if ($($count % 2) -eq 0) {
                $name += $consonants[$(Get-Random -Minimum 0 -Maximum $($consonants.Count - 1))]
            }
            else {
                $name += $vowels[$(Get-Random -Minimum 0 -Maximum $($vowels.Count - 1))]
            }
            $count++
        }

        return $name

    }

    $count = 1
    while ($count -lt $NUMBER_OF_ACCOUNTS_TO_CREATE) {
        $fisrtName = generate-random-name
        $lastName = generate-random-name
        $username = $fisrtName + '.' + $lastName
        $password = ConvertTo-SecureString $PASSWORD_FOR_USERS -AsPlainText -Force

        Write-Host "Creating user: $($username)" -BackgroundColor Black -ForegroundColor Cyan

        New-AdUser -AccountPassword $password `
                   -GivenName $firstName `
                   -Surname $lastName `
                   -DisplayName $username `
                   -Name $username `
                   -EmployeeID $username `
                   -PasswordNeverExpires $true `
                   -Path "ou=_EMPLOYEES,$(([ADSI]`"").distinguishedName)" `
                   -Enabled $true
        $count++
    }
    ```

    Code source: [Generate-Names-Create-Users.ps1](https://github.com/joshmadakor1/AD_PS/blob/master/Generate-Names-Create-Users.ps1)

    Note: the script stores the first name in `$fisrtName` but passes `$firstName` to `-GivenName`, so the GivenName field stays blank. Usernames are not affected.

29. Click Run Script (F5).

    Expected result: the console prints a stream of "Creating user: <first>.<last>" lines.

30. When it finishes, open ADUC and select `_EMPLOYEES`.

    Expected result: `_EMPLOYEES` is filled with User objects named like `<first>.<last>`.

31. Log in to Client-1 with one of the new accounts, using the password you set in the script.

## What I learned

- A domain controller needs a static private IP, and domain clients need to use it as their DNS server before they can join the domain.
- Windows Firewall blocks ICMP by default. Enabling the ICMPv4 echo rules is a quick way to confirm two VMs can reach each other.
- OUs keep employees, admins, and computers organized, and adding a user to Domain Admins is what grants admin rights.
- PowerShell can create thousands of AD accounts in minutes.

## Next steps

- [Network File Shares and Permissions](../03-network-file-shares-and-permissions/): share folders from DC-1 and control access with groups.
- [Building Intuition for DNS](../04-building-intuition-for-dns/): create DNS records on DC-1 and resolve them from Client-1.

Keep DC-1 and Client-1 running for those labs.
