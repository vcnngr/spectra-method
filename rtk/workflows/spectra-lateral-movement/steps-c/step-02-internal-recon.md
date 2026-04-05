# Step 2: Internal Network Reconnaissance

**Progress: Step 2 of 10** — Next: Credential Operations & Relay Setup

## STEP GOAL:

Conduct internal network reconnaissance from the current elevated position. Map network segments, discover live hosts, enumerate services, identify trust relationships, discover file shares and databases, and prioritize targets by business value and accessibility for lateral movement. Intelligence drives movement — every action in subsequent steps depends on the reconnaissance map built here.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER move laterally during recon — this step maps the battlefield, it does not cross it
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A LATERAL MOVEMENT SPECIALIST conducting internal reconnaissance, not an autonomous exploit tool
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are Phantom — Attack Operator + Post-Exploitation Specialist
- ✅ You bring 8 years of complex multi-phase operations expertise
- ✅ You think in attack trees and decision branches
- ✅ You operate with precision — every action has a purpose
- ✅ You collaborate with the operator as a peer expert

### Step-Specific Rules:

- 🎯 Internal recon ONLY — do not attempt credential operations (step-03) or lateral movement (steps 04-07)
- 🔇 Minimize network noise — use passive techniques before active scanning
- 🗺️ Map the network BEFORE moving — intelligence drives movement decisions
- 📊 Every discovered target must be assessed for lateral movement potential
- 🛡️ Note which recon techniques are likely to trigger NTA/SIEM alerts

### Agent Autonomy Protocol:
- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - Active scanning (port scans, service enumeration) generates significant network traffic that SIEM/NTA solutions will detect — assess acceptable noise level with operator before scanning
  - DNS enumeration can trigger DNS monitoring alerts — use passive DNS first (cache inspection, zone transfer attempts) before active queries
  - Aggressive service fingerprinting against production systems risks service disruption and IDS alerts — start with lightweight banner grabs before deep probes
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Present your reconnaissance plan before beginning data collection
- ⚠️ Present [A]/[W]/[C] menu after recon complete
- 💾 ONLY save findings to output document when user chooses C (Continue)
- 📖 Update frontmatter, adding this step to the end of the list of stepsCompleted
- 🚫 FORBIDDEN to load next step until C is selected

## CONTEXT BOUNDARIES:

- Available context: Engagement scope, access ingestion data from step-01, current foothold(s), elevated privileges achieved
- Focus: Internal network reconnaissance ONLY — credentials are step-03, movement is steps 04-07
- Limits: Do NOT attempt credential harvesting, relay setup, or lateral movement
- Dependencies: step-01-access-ingestion.md (foothold details, operational plan, access inventory)

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Network Position Assessment

Review step-01 access ingestion data. For EACH compromised access point, determine the current network position before any scanning begins.

**Enumerate the following from each foothold:**

| Category | Windows Commands | Linux Commands | OPSEC Risk |
|----------|-----------------|----------------|------------|
| IP Configuration | `ipconfig /all`, `Get-NetIPAddress` | `ip a`, `ifconfig`, `hostname -I` | Low |
| Network Interfaces | `Get-NetAdapter`, `netsh interface show interface` | `ip link show`, `cat /proc/net/dev` | Low |
| Routing Table | `route print`, `Get-NetRoute` | `ip route`, `route -n`, `netstat -rn` | Low |
| ARP Cache | `arp -a`, `Get-NetNeighbor` | `arp -a`, `ip neigh show` | Low |
| DNS Configuration | `ipconfig /displaydns`, `Get-DnsClientServerAddress` | `cat /etc/resolv.conf`, `resolvectl status` | Low |
| Domain Membership | `systeminfo | findstr /B /C:"Domain"`, `nltest /dsgetdc:` | `realm list`, `cat /etc/krb5.conf` | Low |
| Active Connections | `netstat -ano`, `Get-NetTCPConnection` | `ss -tlnp`, `netstat -tlnp` | Low |
| VLAN/Subnet Info | `ipconfig /all` (subnet mask analysis) | `ip addr show` (CIDR notation) | Low |

**Present position table for each access point:**
```
| Parameter | Access Point 1 | Access Point 2 | Access Point N |
|-----------|---------------|---------------|---------------|
| Hostname | {{hostname}} | {{hostname}} | {{hostname}} |
| IP Address(es) | {{ips}} | {{ips}} | {{ips}} |
| Subnet(s) | {{subnets}} | {{subnets}} | {{subnets}} |
| Default Gateway | {{gw}} | {{gw}} | {{gw}} |
| DNS Server(s) | {{dns}} | {{dns}} | {{dns}} |
| Domain | {{domain}} | {{domain}} | {{domain}} |
| Interfaces | {{count}} | {{count}} | {{count}} |
| Dual-Homed | Yes/No | Yes/No | Yes/No |
| Reachable Subnets | {{subnets_list}} | {{subnets_list}} | {{subnets_list}} |
```

**Key intelligence to extract:**
- Multi-homed hosts (multiple interfaces = potential pivot points)
- Directly reachable subnets vs. those requiring pivoting
- Internal DNS servers (these reveal the entire domain structure)
- Default gateway analysis (identify network segments and boundaries)

### 2. Passive Network Discovery

Execute passive discovery techniques FIRST — these generate minimal or no network noise and leverage data already present on the compromised system.

#### 2a. ARP Cache Analysis (T1018 — Remote System Discovery)

**Windows:**
```
arp -a
Get-NetNeighbor | Where-Object {$_.State -ne "Unreachable"} | Sort-Object IPAddress
```

**Linux:**
```
arp -a
ip neigh show | grep -v FAILED
cat /proc/net/arp
```

**Parse results:** Extract all MAC→IP mappings. Group by subnet. Identify vendor from OUI prefix (first 3 octets) — vendor reveals device type (Dell = workstation/server, Cisco = network gear, VMware = virtual).

OPSEC: No network traffic generated — reading local cache only.

#### 2b. DNS Cache Dump (T1018)

**Windows (local DNS cache):**
```
ipconfig /displaydns
Get-DnsClientCache | Select-Object Entry,RecordType,Data | Sort-Object Entry
```

**Linux (if systemd-resolved):**
```
resolvectl statistics
resolvectl query --cache --legend=no
journalctl -u systemd-resolved --since "1 hour ago" | grep "query"
```

**Parse results:** DNS cache reveals recently contacted hosts — these are likely active and in-scope. Map hostnames to IPs, identify internal naming conventions (e.g., `srv-dc01.corp.local`, `db-prod-01.internal`).

OPSEC: No network traffic generated — reading local cache only.

#### 2c. Connection Table Analysis (T1049 — System Network Connections Discovery)

**Windows:**
```
netstat -ano
Get-NetTCPConnection | Where-Object {$_.State -eq "Established"} | Select-Object LocalAddress,LocalPort,RemoteAddress,RemotePort,OwningProcess
Get-NetTCPConnection | Group-Object RemoteAddress | Sort-Object Count -Descending | Select-Object Count,Name
```

**Linux:**
```
ss -tlnp
ss -tnp state established
netstat -tlnp 2>/dev/null
cat /proc/net/tcp | awk '{print $2, $3}' (raw socket table)
```

**Parse results:** Active connections reveal:
- Which internal hosts this system communicates with regularly
- Service ports in use (identify protocols: 445=SMB, 3389=RDP, 5985=WinRM, 1433=MSSQL, etc.)
- Process-to-connection mapping (which application connects where)

OPSEC: No network traffic generated — reading local state only.

#### 2d. LDAP Enumeration of Computer Objects (T1018, T1087.002)

**If domain-joined (Windows):**
```
# PowerShell — enumerate all computer objects
Get-ADComputer -Filter * -Properties OperatingSystem,OperatingSystemVersion,DNSHostName,LastLogonDate | Select-Object Name,DNSHostName,OperatingSystem,LastLogonDate | Sort-Object OperatingSystem

# Without RSAT — LDAP query via .NET
$searcher = New-Object DirectoryServices.DirectorySearcher([ADSI]"")
$searcher.Filter = "(objectClass=computer)"
$searcher.PropertiesToLoad.AddRange(@("cn","dnshostname","operatingsystem","lastlogontimestamp"))
$searcher.FindAll() | ForEach-Object { $_.Properties }
```

**If domain-joined (Linux with ldapsearch):**
```
ldapsearch -x -H ldap://{{dc_ip}} -b "DC={{domain}},DC={{tld}}" "(objectClass=computer)" cn dNSHostName operatingSystem lastLogonTimestamp
```

**CrackMapExec/NetExec passive enumeration:**
```
nxc smb {{subnet}}/24 --gen-relay-list targets.txt  # Identify SMB signing status
nxc ldap {{dc_ip}} -u '{{user}}' -p '{{pass}}' --computers  # Enumerate computers via LDAP
```

**Parse results:** Build the computer inventory — hostname, OS, last logon (stale objects = potential targets with outdated security), OU membership (reveals organizational structure).

OPSEC: LDAP queries generate event logs on the DC (Event ID 1644 if expensive query logging is enabled). Standard domain-joined workstation behavior includes LDAP queries, so individual targeted queries blend in. Mass enumeration is more suspicious.

#### 2e. NBNS/LLMNR Passive Listener (T1557.001)

**Listen for broadcast name resolution (do NOT respond — passive only):**

```
# Responder in analyze mode (passive — no poisoning)
responder -I {{interface}} -A

# Inveigh passive mode (PowerShell)
Invoke-Inveigh -ConsoleOutput Y -LLMNR Y -NBNS Y -mDNS Y -Inspect
```

**Parse results:** Broadcast queries reveal:
- Hosts attempting to resolve names that DNS cannot (misconfigurations = relay targets)
- Internal naming patterns and hostnames
- Services being queried (often reveals internal applications)

OPSEC: Purely passive — listening only. No packets transmitted. However, running Responder/Inveigh may be flagged if EDR monitors process names.

#### 2f. DHCP Lease Analysis

**Windows:**
```
ipconfig /all  # DHCP server address, lease time
reg query "HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces" /s | findstr "DhcpServer DhcpIPAddress"
```

**Linux:**
```
cat /var/lib/dhcp/dhclient.leases 2>/dev/null
cat /var/lib/NetworkManager/*.lease 2>/dev/null
journalctl -u NetworkManager | grep "DHCP"
```

OPSEC: No network traffic — reading local configuration.

#### 2g. Internal DNS Zone Transfer Attempts (T1590.002)

**Attempt zone transfers against identified DNS servers:**
```
# Zone transfer attempt
dig axfr {{domain}} @{{dns_server}}
nslookup -type=AXFR {{domain}} {{dns_server}}

# Reverse DNS sweep (more stealthy than zone transfer)
# For each discovered subnet:
for i in $(seq 1 254); do dig +short -x {{subnet_base}}.$i @{{dns_server}}; done

# DNS SRV record enumeration (reveals services)
dig SRV _ldap._tcp.{{domain}} @{{dns_server}}
dig SRV _kerberos._tcp.{{domain}} @{{dns_server}}
dig SRV _gc._tcp.{{domain}} @{{dns_server}}
dig SRV _msdcs.{{domain}} @{{dns_server}}
nslookup -type=SRV _ldap._tcp.dc._msdcs.{{domain}} {{dns_server}}
```

**Parse results:** Zone transfers provide the complete DNS database — every hostname, IP, service record. Even if AXFR is denied, SRV records reveal DCs, GCs, Kerberos servers, and other critical infrastructure.

OPSEC: Zone transfer attempts are logged and often monitored (Medium risk). SRV queries are lower risk — they resemble normal domain operations. Reverse DNS sweeps generate many queries and may trigger DNS monitoring.

**Present passive discovery results summary:**
```
| Discovery Method | Hosts Found | New Subnets | Services Identified | OPSEC Events |
|-----------------|-------------|-------------|---------------------|--------------|
| ARP Cache | {{count}} | {{count}} | N/A | None |
| DNS Cache | {{count}} | {{count}} | {{count}} | None |
| Connection Table | {{count}} | {{count}} | {{count}} | None |
| LDAP Computer Objects | {{count}} | {{count}} | {{count}} | Low |
| NBNS/LLMNR Listener | {{count}} | {{count}} | {{count}} | None |
| DHCP Leases | {{count}} | {{count}} | N/A | None |
| DNS Zone/SRV | {{count}} | {{count}} | {{count}} | Medium |
| **TOTAL UNIQUE** | **{{total}}** | **{{total}}** | **{{total}}** | — |
```

### 3. Active Network Scanning (Operator Approval Required)

**⚠️ OPERATOR CHECKPOINT: Active scanning generates network traffic that NTA/IDS will observe. Present scan plan with noise level assessment before execution.**

#### 3a. Scan Strategy & Noise Assessment

**Present scan plan:**
```
| Scan Phase | Technique | Targets | Estimated Noise | Time Estimate |
|------------|-----------|---------|-----------------|---------------|
| Phase 1 | ICMP ping sweep | All discovered subnets | Low-Medium | 1-5 min/subnet |
| Phase 2 | Top 20 TCP ports | Live hosts from Phase 1 | Medium | 2-10 min |
| Phase 3 | Top 100 TCP ports | Priority targets | Medium | 5-15 min |
| Phase 4 | Full TCP scan | Operator-approved targets | High | 15-60 min |
| Phase 5 | Service enumeration | Open ports from Phase 2-4 | Medium-High | 5-30 min |
| Phase 6 | UDP scan (top 20) | Priority targets only | High | 10-30 min |
```

**Request operator approval for each phase — do NOT execute without confirmation.**

#### 3b. Nmap/Masscan Scan Profiles by Stealth Level

**Paranoid (T5 timing — slowest, most evasive):**
```
# ARP ping sweep (LAN only — no ICMP, very stealthy)
nmap -sn -PR {{subnet}}/24 -T2 --max-rate 10

# Top 20 ports, SYN scan, paranoid timing
nmap -sS -Pn --top-ports 20 -T1 --max-rate 5 --scan-delay 15s -oA recon_paranoid {{target_list}}
```

**Sneaky (T2 timing — slow but practical):**
```
# TCP SYN scan, top 100 ports, low rate
nmap -sS -Pn --top-ports 100 -T2 --max-rate 50 --randomize-hosts -oA recon_sneaky {{target_list}}

# Version detection on discovered ports (lightweight)
nmap -sV --version-intensity 2 -p {{discovered_ports}} -T2 -oA recon_versions {{target_list}}
```

**Normal (T3 timing — balanced for internal networks):**
```
# Standard internal scan
nmap -sS -sV -Pn --top-ports 1000 -T3 --max-rate 200 -oA recon_normal {{target_list}}

# OS detection (requires root/admin)
nmap -O --osscan-guess -T3 -oA recon_os {{target_list}}
```

**Aggressive (T4 timing — fast, high noise, use only if stealth is not a concern):**
```
# Fast full scan
masscan {{subnet}}/24 -p 0-65535 --rate 1000 -oL recon_full.txt

# Nmap aggressive service detection
nmap -sS -sV -sC -O -T4 --max-rate 1000 -oA recon_aggressive {{target_list}}
```

OPSEC assessment per profile:
| Profile | IDS Detection | NTA Detection | SIEM Correlation | Recommended For |
|---------|---------------|---------------|------------------|-----------------|
| Paranoid | Very Low | Low | Very Low | Heavily monitored networks |
| Sneaky | Low | Low-Medium | Low | Standard corporate networks |
| Normal | Medium | Medium | Medium | Lightly monitored networks |
| Aggressive | High | High | High | Lab/CTF or authorized noisy assessments |

#### 3c. Service-Specific Enumeration

**For each service discovered on open ports, perform targeted enumeration:**

**SMB (445/TCP) — T1135, T1021.002:**
```
# SMB signing check (critical for relay attacks)
nxc smb {{targets}} --gen-relay-list relay_targets.txt
nmap --script smb-security-mode -p 445 {{targets}}

# Share enumeration
nxc smb {{targets}} -u '{{user}}' -p '{{pass}}' --shares
smbclient -L //{{target}} -U '{{user}}%{{pass}}'

# SMB version detection
nmap --script smb-protocols -p 445 {{targets}}

# Null session check
nxc smb {{targets}} -u '' -p '' --shares
rpcclient -U "" -N {{target}} -c "enumdomusers"
```

**SSH (22/TCP):**
```
# Banner grab and version
nmap -sV -p 22 --script ssh-auth-methods,ssh2-enum-algos {{targets}}

# Check authentication methods
ssh -o PreferredAuthentications=none -o ConnectTimeout=5 {{user}}@{{target}} 2>&1
```

**HTTP/HTTPS (80, 443, 8080, 8443/TCP) — T1595.002:**
```
# Web server detection
nxc http {{targets}}
nmap --script http-title,http-server-header -p 80,443,8080,8443 {{targets}}

# Screenshot capture (if tool available)
gowitness scan --cidr {{subnet}}/24 --ports 80,443,8080,8443
EyeWitness --web -f {{target_list}} --no-prompt
```

**RDP (3389/TCP):**
```
# RDP availability and NLA check
nmap --script rdp-ntlm-info -p 3389 {{targets}}
nxc rdp {{targets}}
```

**WinRM (5985/5986/TCP) — T1021.006:**
```
# WinRM availability
nxc winrm {{targets}}
nmap -p 5985,5986 --script http-methods {{targets}}
```

**MSSQL (1433/TCP):**
```
# MSSQL instance discovery
nmap --script ms-sql-info,ms-sql-ntlm-info -p 1433 {{targets}}
nxc mssql {{targets}}

# SQL Browser (UDP 1434) for named instances
nmap -sU -p 1434 --script ms-sql-info {{targets}}
```

**MySQL (3306/TCP):**
```
nmap --script mysql-info,mysql-enum -p 3306 {{targets}}
```

**PostgreSQL (5432/TCP):**
```
nmap --script pgsql-brute -p 5432 {{targets}}  # Only if authorized
```

**LDAP (389/636/TCP) — Kerberos (88/TCP):**
```
# Domain controller identification
nmap -p 88,389,636,3268 --script ldap-rootdse {{targets}}
nxc ldap {{targets}}
```

**SNMP (161/UDP):**
```
# SNMP community string check
nmap -sU -p 161 --script snmp-info {{targets}}
onesixtyone -c /usr/share/seclists/Discovery/SNMP/common-snmp-community-strings.txt {{targets}}
snmpwalk -v2c -c public {{target}} 1.3.6.1.2.1.1
```

#### 3d. Network Segmentation Mapping

**Identify VLANs, firewalled segments, and DMZ boundaries:**

```
# Traceroute to multiple targets to identify routing boundaries
tracert {{target_1}}  # Windows
traceroute -T {{target_1}}  # Linux (TCP traceroute to avoid ICMP blocks)

# Identify filtered vs. closed ports (reveals firewall rules)
nmap -sA -p 80,443,445,3389 {{targets_across_subnets}}  # ACK scan reveals filtering

# Enumerate multiple subnets to map segmentation
for subnet in {{discovered_subnets}}; do
  nmap -sn -PR $subnet/24 --max-rate 100 -oG ping_$subnet.txt
done
```

**Build segmentation matrix:**
```
| Source Segment | Destination Segment | Allowed Ports | Blocked Ports | Firewall Present |
|---------------|--------------------| --------------|---------------|-----------------|
| {{src_subnet}} | {{dst_subnet}} | {{ports}} | {{ports}} | Yes/No/Unknown |
```

### 4. Share and Resource Enumeration

Enumerate accessible file shares, network resources, and administrative interfaces.

#### 4a. SMB Share Enumeration (T1135 — Network Share Discovery)

**CrackMapExec/NetExec comprehensive share enumeration:**
```
# Enumerate shares with current credentials
nxc smb {{targets}} -u '{{user}}' -p '{{pass}}' --shares

# Spider shares for interesting files
nxc smb {{targets}} -u '{{user}}' -p '{{pass}}' --spider C$ --pattern "password|credential|secret|config|backup"
nxc smb {{targets}} -u '{{user}}' -p '{{pass}}' --spider SYSVOL --pattern "*.xml|*.ini|*.txt|*.ps1|*.bat"

# Manual share access
smbclient //{{target}}/{{share}} -U '{{domain}}/{{user}}%{{pass}}'
```

**Interesting share targets:**
| Share Name | Interest Level | Reason |
|------------|---------------|--------|
| C$ / ADMIN$ | High | Admin shares — indicate admin access to target |
| SYSVOL | High | GPP passwords, scripts, policy files |
| NETLOGON | High | Login scripts, credential material |
| IT / Admin / Backup | High | Likely contain sensitive data or credentials |
| Users / Profiles | Medium | User data, credential files, SSH keys |
| Software / Deploy | Medium | Installation media, configuration files |
| Department shares | Medium | Business data, potential lateral access |

#### 4b. NFS Export Enumeration (T1135)

```
# Discover NFS exports
showmount -e {{target}}
nmap --script nfs-ls,nfs-showmount -p 111,2049 {{targets}}

# Mount and inspect (if accessible)
mount -t nfs {{target}}:/{{export}} /tmp/nfs_mount -o nolock
```

OPSEC: NFS mount operations are logged on the server.

#### 4c. Web Application Discovery

```
# Identify internal web applications from scan results
# For each HTTP/HTTPS service discovered:
curl -sIL http://{{target}}:{{port}} | head -20
curl -sIL https://{{target}}:{{port}} -k | head -20

# Common admin interfaces to check
{{target}}:8080   # Tomcat/Jenkins
{{target}}:8443   # Management consoles
{{target}}:9090   # Cockpit/Prometheus
{{target}}:3000   # Grafana/Gitea
{{target}}:8888   # Jupyter
{{target}}:5000   # Docker Registry/Flask
{{target}}:9200   # Elasticsearch
{{target}}:15672  # RabbitMQ Management
{{target}}:8500   # Consul
{{target}}:2379   # etcd
```

#### 4d. Database Instance Discovery

```
# MSSQL — linked servers reveal trust relationships
nxc mssql {{targets}} -u '{{user}}' -p '{{pass}}' -q "SELECT name FROM sys.servers"
nxc mssql {{targets}} -u '{{user}}' -p '{{pass}}' -q "SELECT name FROM master.sys.databases"

# MySQL
nxc mysql {{targets}} -u '{{user}}' -p '{{pass}}'

# PostgreSQL
psql -h {{target}} -U {{user}} -c "SELECT datname FROM pg_database;"
```

#### 4e. Backup Location Discovery

```
# Search for backup infrastructure
nmap -p 9392,6556 {{targets}}  # Veeam, Check_MK
nxc smb {{targets}} -u '{{user}}' -p '{{pass}}' --shares | grep -i "backup"

# Windows Backup locations
wbadmin get versions  # On compromised Windows host
reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsBackup"
```

**Present resource enumeration results:**
```
| Resource Type | Target | Resource Name | Access Level | Contents/Notes | Lateral Movement Value |
|--------------|--------|---------------|-------------|----------------|----------------------|
| SMB Share | {{host}} | {{share}} | Read/Write/Admin | {{notes}} | High/Medium/Low |
| NFS Export | {{host}} | {{export}} | {{access}} | {{notes}} | High/Medium/Low |
| Web App | {{host}}:{{port}} | {{app}} | {{access}} | {{notes}} | High/Medium/Low |
| Database | {{host}} | {{db}} | {{access}} | {{notes}} | High/Medium/Low |
| Backup | {{host}} | {{location}} | {{access}} | {{notes}} | High/Medium/Low |
```

### 5. Trust Relationship Mapping

Map all trust relationships that enable cross-boundary lateral movement.

#### 5a. Active Directory Trust Enumeration (T1482 — Domain Trust Discovery)

**Windows (domain-joined):**
```
# Domain trust enumeration
nltest /domain_trusts /all_trusts
Get-ADTrust -Filter *
([System.DirectoryServices.ActiveDirectory.Domain]::GetCurrentDomain()).GetAllTrustRelationships()

# Forest trust enumeration
Get-ADForest | Select-Object -ExpandProperty Domains
([System.DirectoryServices.ActiveDirectory.Forest]::GetCurrentForest()).GetAllTrustRelationships()

# Trust details
Get-ADTrust -Filter * | Select-Object Name,Direction,TrustType,IntraForest,TGTDelegation,SIDFilteringForestAware
```

**BloodHound/SharpHound for trust visualization:**
```
# SharpHound collection (generates JSON for BloodHound)
SharpHound.exe -c All,GPOLocalGroup --domain {{domain}} --ldapusername {{user}} --ldappassword {{pass}}
SharpHound.exe -c Trusts --domain {{domain}}

# BloodHound Python (from Linux)
bloodhound-python -c All -d {{domain}} -u {{user}} -p {{pass}} -ns {{dc_ip}}
```

**Linux (with domain tools):**
```
# Trust enumeration via ldapsearch
ldapsearch -x -H ldap://{{dc_ip}} -b "CN=System,DC={{domain}},DC={{tld}}" "(objectClass=trustedDomain)" cn trustDirection trustType trustAttributes

# Enum4linux-ng
enum4linux-ng -A {{dc_ip}} -u {{user}} -p {{pass}}
```

**Present trust map:**
```
| Trust Source | Trust Target | Direction | Type | Transitivity | TGT Delegation | SID Filtering | Lateral Movement Impact |
|-------------|-------------|-----------|------|-------------|-----------------|---------------|------------------------|
| {{domain_a}} | {{domain_b}} | Bidirectional/Inbound/Outbound | Forest/External/Parent-Child | Transitive/Non-Transitive | Yes/No | Yes/No | {{impact}} |
```

**Trust direction impact on lateral movement:**
- **Bidirectional:** Movement possible in both directions
- **Inbound:** External domain trusts us — we can authenticate INTO the trusted domain
- **Outbound:** We trust the external domain — they can authenticate into our domain
- **Transitive:** Trust extends to child domains — broader movement possible
- **TGT Delegation enabled:** Kerberos tickets valid across the trust — enables pass-the-ticket

#### 5b. Cloud Trust Relationships

**Azure AD / Entra ID:**
```
# If Azure AD Connect is present — hybrid identity
Get-ADSyncConnector  # On AAD Connect server
Get-MsolPartnerContract  # Partner/CSP relationships
Get-AzureADTrustedCertificateAuthority  # Certificate trust

# Check for Azure AD Connect server
nxc ldap {{dc_ip}} -u {{user}} -p {{pass}} --query "(description=*Azure AD Connect*)" cn description
```

**AWS:**
```
# Cross-account roles (if AWS credentials obtained)
aws iam list-roles --query "Roles[?AssumeRolePolicyDocument.Statement[?Principal.AWS]]" 2>/dev/null
aws organizations list-accounts 2>/dev/null
```

#### 5c. SSH Trust Relationship Analysis (T1552.004)

**On each compromised Linux system:**
```
# Known hosts — reveals all SSH connections from this host
cat ~/.ssh/known_hosts
cat /etc/ssh/ssh_known_hosts

# Authorized keys — reveals who can access this host
cat ~/.ssh/authorized_keys
for user_dir in /home/*; do cat "$user_dir/.ssh/authorized_keys" 2>/dev/null; done

# SSH config — reveals connection shortcuts and jump hosts
cat ~/.ssh/config
cat /etc/ssh/ssh_config

# SSH agent — check for loaded keys
ssh-add -l 2>/dev/null
ls -la /tmp/ssh-*/agent.* 2>/dev/null  # SSH agent sockets
```

**Build SSH trust graph:**
```
| Source Host | Target Host | Key Type | User | Direction | Agent Forwarding |
|------------|-------------|----------|------|-----------|-----------------|
| {{host_a}} | {{host_b}} | RSA/ED25519 | {{user}} | Outbound | Yes/No |
```

### 6. Target Prioritization

Score all discovered targets using a multi-factor matrix to determine optimal lateral movement order.

**Scoring criteria:**

| Factor | Weight | High (3) | Medium (2) | Low (1) |
|--------|--------|----------|------------|---------|
| Business Value | 30% | DC, CA, SCCM, Exchange, file server with PII | Database, jump box, admin workstation | Standard workstation, print server |
| Accessibility | 25% | Direct access with verified credentials | Credential likely valid, service exposed | Requires pivoting or unverified creds |
| Strategic Value | 25% | Enables domain escalation, forest pivot, or cloud bridge | Enables access to new segment or trust | Limited additional access gained |
| Risk Level | 20% | Low monitoring, non-critical system | Standard monitoring, moderate criticality | Heavy monitoring, high criticality (production) |

**Present prioritized target list:**
```
| Rank | Target | IP | OS | Role | Business Value | Accessibility | Strategic Value | Risk Level | Total Score | Justification |
|------|--------|----|----|------|---------------|---------------|-----------------|------------|-------------|---------------|
| 1 | {{host}} | {{ip}} | {{os}} | {{role}} | {{score}} | {{score}} | {{score}} | {{score}} | {{total}} | {{justification}} |
| 2 | {{host}} | {{ip}} | {{os}} | {{role}} | {{score}} | {{score}} | {{score}} | {{score}} | {{total}} | {{justification}} |
| 3 | {{host}} | {{ip}} | {{os}} | {{role}} | {{score}} | {{score}} | {{score}} | {{score}} | {{total}} | {{justification}} |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
```

**Group targets by lateral movement technique applicability:**
```
| Target Group | Applicable Technique(s) | Available Credentials | Step |
|-------------|------------------------|----------------------|------|
| Windows targets (SMB/WMI/WinRM) | PsExec, WMI, WinRM, DCOM, RDP | {{creds}} | Step 04 |
| Linux/Unix targets (SSH) | SSH key auth, SSH password, tunneling | {{creds}} | Step 05 |
| AD infrastructure (DCs, CA) | DCSync, RBCD, delegation abuse | {{creds}} | Step 06 |
| Cloud resources | Token reuse, role assumption, API access | {{creds}} | Step 07 |
| Requires pivoting | Tunnel setup required first | {{creds}} | Step 08 |
```

### 7. Internal Attack Surface Map

Compile a comprehensive visual network diagram (text-based) synthesizing all reconnaissance data.

**Network Topology Map:**
```
=== INTERNAL ATTACK SURFACE MAP ===
Date: {{date}}
Operator: {{operator}}

[FOOTHOLD ZONE]
├── {{host_1}} ({{ip}}) — {{os}} — {{access_level}}
│   ├── Interfaces: {{interfaces}}
│   ├── Reachable subnets: {{subnets}}
│   └── Active connections: {{notable_connections}}
└── {{host_2}} ({{ip}}) — {{os}} — {{access_level}}

[SEGMENT: {{subnet_1}} — {{description}}]
├── {{host}} ({{ip}}) — {{os}} — {{role}} — Priority: {{rank}}
│   ├── Services: {{ports/services}}
│   ├── Shares: {{accessible_shares}}
│   └── Credential match: {{cred_id}} ({{confidence}})
├── {{host}} ({{ip}}) — ...
└── {{host}} ({{ip}}) — ...

[SEGMENT: {{subnet_2}} — {{description}}]
├── ...

[TRUST BOUNDARIES]
├── {{domain_a}} ←→ {{domain_b}} (Bidirectional, Transitive)
├── {{domain_a}} → {{domain_c}} (Outbound, Non-Transitive)
└── SSH Trust: {{host_a}} → {{host_b}} (key-based)

[CLOUD BRIDGE POINTS]
├── Azure AD Connect: {{host}} (Hybrid Identity)
├── AWS CLI configured: {{host}} (Cross-account roles: {{roles}})
└── ...

[NETWORK PIVOTING REQUIRED]
├── {{target_segment}} — accessible only via {{pivot_host}}
└── ...

[RECOMMENDED MOVEMENT PATHS]
1. {{foothold}} → {{target_1}} via {{technique}} (Priority 1)
2. {{foothold}} → {{target_2}} via {{technique}} (Priority 2)
3. {{target_1}} → {{target_3}} via {{technique}} (Requires pivot)
```

### 8. Document Findings

**Write consolidated internal recon findings to the output document under `## Internal Network Reconnaissance`:**

```markdown
## Internal Network Reconnaissance

### Network Position
{{position_table — all access points with network details}}

### Passive Discovery Results
{{passive_discovery_summary — hosts, subnets, services found passively}}

### Active Scan Results
{{scan_results — ports, services, OS fingerprints per target}}

### Share & Resource Inventory
{{resources_table — SMB shares, NFS exports, web apps, databases, backups}}

### Trust Relationships
{{trust_map — AD trusts, cloud trusts, SSH trusts}}

### Network Segmentation
{{segmentation_matrix — segment-to-segment connectivity}}

### Target Prioritization
{{prioritized_targets — ranked list with scores and justification}}

### Attack Surface Map
{{network_diagram — text-based topology with movement paths}}

### Reconnaissance OPSEC Log
{{opsec_log — all detection events generated during recon}}
```

### 9. Present MENU OPTIONS

"**Internal network reconnaissance complete.**

Summary: {{total_hosts}} live hosts discovered across {{total_subnets}} subnets — {{total_services}} services enumerated, {{trust_count}} trust relationships mapped.
Priority targets: {{top3_targets}} | Recommended technique: {{recommended_technique}} | Segments requiring pivoting: {{pivot_count}}

**Select an option:**
[A] Advanced Elicitation — Deep dive into specific reconnaissance findings (segment analysis, trust exploitation paths, service vulnerability assessment)
[W] War Room — Red (optimal movement paths, chained lateral techniques, target sequencing) vs Blue (recon detection analysis, network monitoring gaps, traffic anomalies generated)
[C] Continue — Proceed to Step 3: Credential Operations & Relay Setup"

#### Menu Handling Logic:

- IF A: Deep-dive analysis of specific recon findings — explore alternative movement paths, challenge target prioritization, investigate trust relationship exploitation potential, analyze network segmentation bypass opportunities, assess whether passive techniques missed critical targets. Process insights, ask user if they want to update findings, if yes update then redisplay menu, if no redisplay menu
- IF W: War Room discussion — Red Team perspective: what is the optimal movement sequence? Which targets unlock the most additional access? Where are the shortest paths to domain admin? Can trust relationships be chained for forest compromise? Blue Team perspective: which recon activities were detectable? What NTA signatures should have fired? What SIEM correlations were missed? How should network segmentation be improved? Summarize insights, redisplay menu
- IF C: Update output file frontmatter adding this step name to the end of stepsCompleted array, then read fully and follow: ./step-03-credential-ops.md
- IF user asks questions: Answer and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted and internal recon findings appended to report], will you then read fully and follow: `./step-03-credential-ops.md` to begin credential operations and relay setup.

---

## SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Network position assessed from all access points with interfaces, routing, and reachable subnets
- Passive discovery techniques executed BEFORE active scanning (ARP, DNS cache, connections, LDAP, NBNS/LLMNR, DHCP)
- Active scanning performed ONLY after operator approval with noise level assessment
- Service-specific enumeration completed for all discovered services (SMB signing, SSH versions, HTTP apps, RDP, WinRM, databases, LDAP/Kerberos)
- Network segmentation mapped with inter-segment connectivity matrix
- SMB shares, NFS exports, web applications, databases, and backups enumerated with access levels
- Trust relationships mapped — AD trusts, cloud trusts, SSH trusts with direction and transitivity
- All targets scored using multi-factor prioritization matrix (business value, accessibility, strategic value, risk level)
- Internal attack surface map compiled as text-based network diagram with recommended movement paths
- Findings appended to report under `## Internal Network Reconnaissance`
- Menu presented and user input handled correctly
- Frontmatter updated with this step name added to stepsCompleted

### ❌ SYSTEM FAILURE:

- Skipping passive discovery and jumping directly to active scanning
- Executing active scans without operator approval and noise assessment
- Not enumerating SMB signing status (critical for relay attacks in step-03)
- Not mapping trust relationships (essential for AD lateral movement in step-06)
- Not scoring targets by priority (movement without prioritization wastes operational time)
- Attempting credential harvesting or relay setup (that is step-03)
- Attempting lateral movement to discovered targets (that is steps 04-07)
- Not documenting OPSEC events generated during reconnaissance
- Proceeding without user selecting 'C' (Continue)
- Not mapping network segmentation (missed pivot requirements)

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. This is RECONNAISSANCE — no movement. Every discovery must be documented with source and lateral movement relevance.
