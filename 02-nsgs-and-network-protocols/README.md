# Network Security Groups and Inspecting Traffic Between Azure VMs

Capture and read ICMP, SSH, DHCP, DNS, and RDP traffic between two Azure virtual machines with Wireshark. Each VM sits behind its own network security group (NSG), and the Windows VM watches the traffic it sends to and receives from the Linux VM.

## What you'll use

- Microsoft Azure (Virtual Machines/Compute) with network security groups
- Remote Desktop
- Command-line tools: PowerShell, `ping`, `ssh`, `ipconfig`, `nslookup`
- Wireshark (protocol analyzer)
- Windows 10 (21H2) and Ubuntu Server 20.04

## Prerequisites

- An Azure subscription

## Steps

### Part 1: Set up the VMs

1. In Azure, create two VMs in the same resource group and virtual network, each with at least 2 vCPUs (4 is more comfortable):
   - VM1: Windows 10 (21H2)
   - VM2: Ubuntu Server 20.04
2. Note the private IP of each VM from its Overview page (in this lab, the Windows VM was `10.0.0.4` and the Linux VM `10.0.0.5`).
3. Connect to the Windows VM with Remote Desktop.
4. On the Windows VM, download Wireshark from [wireshark.org/download](https://www.wireshark.org/download.html) (Windows Installer, 64-bit) and install it.
5. Open Wireshark and start a capture on the Ethernet adapter.

### Part 2: ICMP

6. In Wireshark, set the display filter to `icmp`.
7. In PowerShell, ping the Linux VM:

   ```powershell
   ping <linux-vm-private-ip>
   ```

   Expected result: PowerShell shows 4 replies and 0% loss. Wireshark lists alternating Echo (ping) request packets from the Windows VM and Echo (ping) reply packets from the Linux VM. Selecting one shows the Ethernet, IPv4, and ICMP layers and the payload bytes.

### Part 3: SSH

8. Change the display filter to `ssh`.
9. SSH from the Windows VM to the Linux VM:

   ```powershell
   ssh <username>@<linux-vm-private-ip>
   ```

10. Type `yes` to accept the host key fingerprint, then enter the password.

    Expected result: Wireshark immediately shows SSHv2 packets between the two VMs: the client and server protocol banners (OpenSSH for Windows and OpenSSH on Ubuntu), Key Exchange Init, and Elliptic Curve Diffie-Hellman exchange, all to destination port 22.

### Part 4: DHCP

11. Change the display filter to `dhcp`. DHCP assigns IP addresses and uses UDP ports 67 and 68.
12. In an administrator PowerShell, request a new lease:

    ```powershell
    ipconfig /renew
    ```

    Expected result: Wireshark shows a DHCP Request from the Windows VM (source port 68, destination port 67) to the Azure host address `168.63.129.16` and a DHCP ACK back. `ipconfig` shows the same IPv4 address, subnet mask `255.255.255.0`, and the default gateway.

### Part 5: DNS

13. Change the display filter to `dns`.
14. Look up a domain:

    ```powershell
    nslookup www.google.com
    ```

    Expected result: `nslookup` answers through the Azure DNS server `168.63.129.16` with a non-authoritative IPv4 and IPv6 address. Wireshark shows the query and response pairs on UDP port 53.

### Part 6: RDP

15. Change the display filter to `tcp.port == 3389`.

    Expected result: packets stream continuously between the Windows VM and your own computer's public IP, because your Remote Desktop session is live. Most are TLS Application Data with TCP ACKs on port 3389.

## What I learned

- Wireshark display filters isolate one protocol at a time: `icmp`, `ssh`, `dhcp`, `dns`, `tcp.port == 3389`.
- Azure VMs reach DHCP and DNS through the platform address `168.63.129.16`.
- An active RDP session generates constant traffic, so filter it out when capturing anything else.

## Next steps / cleanup

- Delete the resource group when you finish to stop charges.
