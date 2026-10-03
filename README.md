# Building Intuition for DNS

Create A and CNAME records on an Active Directory domain controller and watch how a domain client resolves them, including what the local DNS cache does when a record changes.

DNS (Domain Name System) is the phonebook of the internet: it turns readable names like `www.google.com` into the numeric IP addresses computers use. Asking a voice assistant to "call the nearest pharmacy" works the same way: it looks up the name, finds the number, and connects you.

## What you'll use

- Microsoft Azure (Virtual Machines/Compute)
- Remote Desktop
- DNS Manager on Windows Server (DC-1)
- Command Prompt on Windows 10 (21H2) (Client-1)

## Prerequisites

- Active Directory installed on DC-1, with Client-1 joined to the domain: see [Configure on-premises Active Directory](https://github.com/aboutfaris/Configure-On-Premise-AD-Powershell-Script-Users)
- DC-1 has a static private IP, and Client-1 uses DC-1's private IP as its DNS server. Both VMs are in the same Azure virtual network.

## Steps

### Part 1: A record

1. Log in to DC-1 as your domain admin account (`mydomain.com\jane_admin`).
2. Log in to Client-1 as the same admin (`mydomain\jane_admin`).
3. On Client-1, open Command Prompt and try to reach a host that does not exist yet:

   ```cmd
   ping mainframe
   nslookup mainframe
   ```

   Expected result: ping reports "Ping request could not find host mainframe", and `nslookup` finds no record.

4. On DC-1, open Server Manager > Tools > DNS.
5. Expand DC-1 > Forward Lookup Zones > mydomain.com.

   Expected result: the zone already holds SOA and NS records plus Host (A) records for dc-1 and Client-1.

6. Right-click mydomain.com > New Host (A or AAAA). Enter the name `mainframe` and DC-1's private IP address, then click Add Host. Double-check the spelling: a typo such as "mainfame" is an easy way to lose an hour.
7. On Client-1, run `ping mainframe` again.

   Expected result: Client-1 pings `mainframe.mydomain.com` at DC-1's private IP with 4 replies and 0% loss.

### Part 2: Local DNS cache

8. On DC-1, double-click the `mainframe` record, change its IP address to `8.8.8.8`, and click OK.
9. On Client-1, run `ping mainframe`.

   Expected result: it still replies from DC-1's old private IP, because Client-1 cached the earlier answer.

10. View the cache:

    ```cmd
    ipconfig /displaydns
    ```

11. Open Command Prompt as administrator and flush the cache:

    ```cmd
    ipconfig /flushdns
    ```

    Expected result: "Successfully flushed the DNS Resolver Cache."

12. Run `ping mainframe` again.

    Expected result: `mainframe.mydomain.com` now resolves to `8.8.8.8` and gets 4 replies.

### Part 3: CNAME record

A CNAME (alias) record points one name at another name instead of at an IP address.

13. On DC-1, right-click mydomain.com > New Alias (CNAME). Set Alias name to `search` and the target host FQDN to `www.google.com`, then click OK.
14. On Client-1, run `ping search`.

    Expected result: the ping goes to `www.google.com` and its public IP, with 4 replies.

15. Run `nslookup search` and look at how the alias resolves to `www.google.com`.

## What I learned

- An A record maps a name to an IP; a CNAME maps a name to another name.
- Clients cache DNS answers, so a changed record does not take effect until the cache expires or you run `ipconfig /flushdns`.
- `ping` and `nslookup` are quick ways to confirm what a name resolves to.

## Next steps / cleanup

- Delete the `mainframe` and `search` records when you finish, or stop the VMs to avoid charges.
