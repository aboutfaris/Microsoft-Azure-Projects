# Network File Shares and Permissions

Create shared folders on the domain controller, give each one different share permissions, and test what a normal domain user can and cannot open from a client machine. Then use a security group to grant access to one share.

## What you'll use

- Microsoft Azure (Virtual Machines: DC-1 domain controller, Client-1 client machine)
- Remote Desktop
- File Explorer sharing and Active Directory Users and Computers on DC-1
- Windows 10 (21H2) on Client-1

## Prerequisites

- DC-1 and Client-1 from the Active Directory lab, with Client-1 joined to the domain and some domain users created: see [Configure on-premises Active Directory](https://github.com/aboutfaris/Configure-On-Premise-AD-Powershell-Script-Users)

## Steps

### Part 1: Create the folders

1. Log in to DC-1 as your domain admin account (`mydomain.com\jane_admin`).
2. Log in to Client-1 as a normal domain user (`mydomain\<someuser>`).
3. On DC-1, open File Explorer and create 4 folders on the C:\ drive: `read-access`, `write-access`, `no-access`, and `accounting`.

   Expected result: the 4 new folders appear in Windows (C:) next to Packages, Program Files, Users, Windows, and the other default folders.

### Part 2: Share the folders

4. For each folder, right-click it > Properties > Sharing tab > Share...
5. In "Choose people on your network to share with", type the group name, click Add, set the Permission Level, then click Share:
   - `read-access`: group `Domain Users`, permission `Read`
   - `write-access`: group `Domain Users`, permission `Read/Write`
   - `no-access`: group `Domain Admins`, permission `Read/Write`
6. Skip `accounting` for now. You will share it in Part 4.

   Expected result: before sharing, the Sharing tab shows the folder as "Not Shared". After sharing, Administrators stays as Owner and the group you added shows the permission you picked.

### Part 3: Test access as a normal user

7. On Client-1, open Start > Run and enter `\\dc-1`.

   Expected result: File Explorer opens Network > dc-1 and lists NETLOGON, SYSVOL, `no-access`, `read-access`, and `write-access`. `accounting` is not listed yet because it is not shared.

8. Open each share and try to create a file in it. Note which folders you can open and which ones you can write to.

   Expected result: opening `no-access` fails with "Windows cannot access \\dc-1\no-access. You do not have permission to access \\dc-1\no-access." Only Domain Admins have access to that share.

### Part 4: Create an ACCOUNTANTS group and test access

9. On DC-1, open Active Directory Users and Computers. Right-click `mydomain.com` > New > Organizational Unit and name it `_SECURITY_GROUPS`.
10. Inside `_SECURITY_GROUPS`, create a security group named `ACCOUNTANTS`.

    Expected result: `_SECURITY_GROUPS` sits next to `_ADMINS` and `_EMPLOYEES`, and contains ACCOUNTANTS with type Security Group.

11. Share the `accounting` folder (Properties > Sharing > Share...) with group `ACCOUNTANTS`, permission `Read/Write`, then click Share.

    Expected result: the share list shows ACCOUNTANTS as Read/Write and the admin account as Owner.

12. On Client-1, as `<someuser>`, try to open `\\dc-1\accounting`. It should fail, because `<someuser>` is not in ACCOUNTANTS yet.
13. Log out of Client-1.
14. On DC-1, add `<someuser>` as a member of the ACCOUNTANTS security group.
15. Sign back in to Client-1 as `<someuser>` and open `\\dc-1\accounting` again. Signing out and back in is what lets Client-1 pick up the new group membership.

## What I learned

- Share permissions control who can reach a folder over the network, and they can be set per group instead of per user.
- A user who is not in the allowed group gets a "You do not have permission" network error.
- Granting access through a security group means adding or removing a user from the group is all it takes to change their access, but the user has to sign out and back in for it to apply.

## Next steps

In the [next tutorial](https://github.com/aboutfaris/Building-Intuition-for-DNS), we set up DNS records. You can keep the virtual machines from this lab and continue there.
