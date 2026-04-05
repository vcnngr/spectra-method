# Step 5: Network Forensic Analysis

**Progress: Step 5 of 10** — Next: Cloud & SaaS Forensic Analysis

## STEP GOAL:

Conduct comprehensive network forensic analysis on acquired network evidence — PCAP analysis with protocol dissection, flow analysis for traffic pattern identification, DNS analysis for tunneling and C2 detection, log-based network analysis from firewalls/proxies/IDS, lateral movement indicator identification, and C2 communication channel reconstruction. Network forensics provides the external perspective on attacker activity — where they connected, what they transferred, and how they communicated.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER access or modify master evidence — analyze ONLY working copies
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A DIGITAL FORENSIC ANALYST, not an autonomous analysis engine
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are a Digital Forensic Analyst conducting structured network forensic examination under ISO 27037 and NIST SP 800-86
- ✅ Network evidence corroborates disk and memory findings — it is the independent witness that validates (or contradicts) what was found on the endpoint
- ✅ Beaconing detection is critical for C2 identification — regular-interval connections to the same destination are the signature of command-and-control
- ✅ DNS is the most commonly abused protocol for covert channels — DNS tunneling, DGA detection, and C2 over DNS are essential analysis targets
- ✅ Data volume anomalies in flow data reveal exfiltration — the network does not lie about how much data left the organization

### Step-Specific Rules:

- 🎯 Focus exclusively on network forensic analysis: PCAP dissection, flow analysis, DNS analysis, log-based analysis, lateral movement from network perspective, and C2 identification
- 🚫 FORBIDDEN to perform disk or memory analysis — those were steps 3-4
- 🚫 FORBIDDEN to perform cloud platform analysis — that is step 6
- 🚫 FORBIDDEN to modify network capture working copies
- 💬 Approach: Systematic network analysis from packet to flow to behavioral pattern, cross-referencing with disk/memory findings
- 📊 Every finding must cite: evidence ID (EVD-{case_id}-{NNN}), network artifact source, connection details, and confidence level
- 🔒 Re-verify working copy hash before analysis begins

### Agent Autonomy Protocol:

- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - Not performing beaconing analysis on long-duration traffic means C2 channels that use regular check-in intervals will be missed — most C2 frameworks (Cobalt Strike, Sliver, Mythic) default to periodic beaconing, and the regularity of the interval is the strongest detection signal even when the traffic itself is encrypted
  - Analyzing only known-bad IPs and domains without behavioral analysis misses novel C2 infrastructure — the attacker's C2 server may not be in any threat intelligence feed, but its behavioral pattern (beaconing, small consistent payload sizes, jitter patterns) reveals its purpose regardless of reputation
  - Not extracting files from network streams when investigating data exfiltration means you know something was transferred but not what — without stream reassembly and file extraction, you cannot determine whether the transferred data was sensitive, which directly impacts regulatory notification requirements and business impact assessment
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Verify working copy integrity before beginning analysis
- 📋 Document every network analysis tool used with version and parameters
- 🔒 Cite evidence IDs for every finding
- ⚠️ Present [A]/[W]/[C] menu after network forensic analysis is complete
- 💾 ONLY save findings to output document when user chooses C (Continue)
- 📖 Update frontmatter, adding this step to the end of stepsCompleted and updating analysis_types, findings counts
- 🚫 FORBIDDEN to load next step until C is selected

## CONTEXT BOUNDARIES:

- Available context: Case intake, forensic question, evidence inventory, disk forensics findings (step 3), memory forensics findings (step 4, especially network connections from memory)
- Focus: Network forensic analysis — PCAP, flows, DNS, logs, lateral movement, C2
- Limits: If network evidence was classified as N/A in step 2, document the N/A status and proceed to step 6. Only analyze working copies.
- Dependencies: Evidence acquired in step 2, findings from steps 3-4 for cross-reference

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Applicability Check & Working Copy Verification

**If network evidence was classified as N/A in step 2:**

"**Network Forensics — Not Applicable**

No network captures, flow data, or network logs were acquired for this case. Reason: {{reason_from_step_2}}.

This step is documented as N/A. Network-specific artifacts (PCAP, flow analysis, DNS analysis, C2 identification) cannot be analyzed."

Document N/A and proceed to menu with C option.

**If network evidence is available:**

Re-verify working copy integrity for all network evidence items:

```
| EVD ID | Evidence Type | Working Copy Path | Master Hash (SHA-256) | Current Hash (SHA-256) | Match |
|--------|---------------|-------------------|----------------------|------------------------|-------|
| EVD-{case_id}-XXX | {{PCAP/NetFlow/Logs}} | {{path}} | {{master_hash}} | {{current_hash}} | ✅/❌ |
```

### 2. PCAP Analysis (If Full Packet Capture Available)

**Protocol Distribution & Statistics:**
- Tool: capinfos, tshark, Wireshark Statistics
- Total packets, time span, average packet rate
- Protocol distribution (TCP/UDP/ICMP/other)
- Top talkers by volume (source IP, destination IP)
- Top protocols by volume (HTTP, HTTPS, DNS, SMB, SSH, RDP, etc.)

```
| Metric | Value |
|--------|-------|
| Total Packets | {{count}} |
| Capture Duration | {{start}} to {{end}} ({{duration}}) |
| Protocols | {{protocol distribution}} |
| Top Source IPs | {{list with byte counts}} |
| Top Destination IPs | {{list with byte counts}} |
| Top Services | {{list with packet/byte counts}} |
```

**TCP Stream Reconstruction:**
- Reassemble TCP streams for suspicious connections
- Tool: Wireshark Follow TCP Stream, tshark stream index, NetworkMiner
- Identify: HTTP requests/responses, SMTP conversations, FTP sessions, custom protocol data

**HTTP/HTTPS Traffic Analysis:**
- HTTP: full request/response analysis — method, URL, headers (User-Agent, Referer, Host), body content
- HTTPS: if TLS session keys are available (SSLKEYLOGFILE), decrypt and analyze
- If no TLS keys: analyze metadata — SNI (Server Name Indication), JA3/JA3S fingerprints, certificate details
- Flag: unusual User-Agent strings, connections to suspicious domains, POST requests with large bodies (potential exfiltration), encoded/obfuscated payloads

**JA3/JA3S TLS Fingerprinting:**
- JA3 hash identifies the TLS client implementation (unique per application/tool)
- JA3S hash identifies the TLS server implementation
- Cross-reference JA3 hashes with known malware/C2 framework fingerprints
  - Known Cobalt Strike JA3 hashes
  - Known Metasploit JA3 hashes
  - Anomalous JA3 from system processes that should not be making TLS connections
- Tools: JA3 Wireshark plugin, zeek with JA3, tshark with JA3 fields

**Certificate Analysis:**
- Extract certificates from TLS handshakes
- Flag: self-signed certificates, recently issued certificates (< 30 days), certificates with suspicious Subject/Issuer, certificates from free CAs (Let's Encrypt — common for C2), certificate validity anomalies

**DNS Query Analysis:**
- Extract all DNS queries from PCAP
- Tools: tshark DNS filter, zeek DNS log, PacketTotal
- Analysis targets:
  - **DNS tunneling detection:** Unusually long subdomain labels (>50 chars), high query frequency to same domain, TXT record queries, anomalous record types (NULL, CNAME with data encoding)
  - **DGA (Domain Generation Algorithm) detection:** High NXDomain response rate, random-looking domain names, rapid sequential queries to never-before-seen domains
  - **C2 domain identification:** Regular-interval DNS queries to same domain, queries to recently registered domains, queries to domains with low Alexa rank
  - **Data exfiltration via DNS:** Encoded data in subdomain labels, high volume of queries to same domain

```
| # | Query | Type | Response | Source IP | Frequency | Anomaly | EVD ID |
|---|-------|------|----------|-----------|-----------|---------|--------|
| 1 | {{domain}} | A/AAAA/TXT/MX/CNAME | {{response}} | {{source}} | {{count}} | {{tunneling/DGA/C2/exfil/none}} | EVD-{case_id}-XXX |
```

**File Extraction from Network Streams:**
- Tool: NetworkMiner, Wireshark Export Objects, foremost on PCAP
- Extract: HTTP objects, FTP transfers, SMTP attachments, SMB file transfers
- Hash every extracted file (MD5 + SHA-256)
- Cross-reference hashes with IOCs from disk/memory analysis
- Submit suspicious files for malware analysis (if spectra-malware-analysis is available)

**Encrypted Traffic Analysis (Without Decryption):**
- Analyze traffic patterns even when content is encrypted:
  - Payload sizes: consistent small payloads (command/heartbeat), large outbound (exfiltration)
  - Timing patterns: regular intervals (beaconing), burst patterns (interactive session)
  - Connection duration: short-lived (command response) vs long-lived (persistent C2/tunnel)
  - Packet size distribution: bimodal (C2 with commands and responses) vs continuous (file transfer)

### 3. Flow Analysis

Analyze NetFlow/IPFIX/sFlow records for traffic patterns:

**Traffic Pattern Analysis:**
- Top talkers by bytes transferred (inbound and outbound separately)
- Connection count analysis: hosts with unusually high connection counts
- Duration analysis: long-lived connections (persistent C2, tunnels, data exfiltration)
- Off-hours traffic: connections during non-business hours (attacker operating window)

**Beaconing Detection:**
- Algorithm: For each source-destination pair, compute inter-connection intervals
- Identify regular-interval patterns (jitter tolerance: ±10-20% of base interval)
- Common C2 beacon intervals: 1s, 5s, 15s, 30s, 60s, 300s, 600s, 900s, 1800s, 3600s
- Tools: RITA (Real Intelligence Threat Analytics), beacon detection scripts, zeek with frequency analysis

```
| Source IP | Destination IP | Port | Avg Interval | Jitter % | Connection Count | Duration | Beacon Score | EVD ID |
|-----------|---------------|------|--------------|----------|------------------|----------|-------------|--------|
| {{src}} | {{dst}} | {{port}} | {{interval}} | {{jitter}} | {{count}} | {{duration}} | {{score}} | EVD-{case_id}-XXX |
```

**Data Volume Anomalies (Potential Exfiltration):**
- Identify connections with unusually high outbound data volume
- Compare against baseline (if available) or organizational norms
- Flag: large uploads to external IPs, unusual protocol usage for bulk transfer (DNS, ICMP, HTTP POST)
- Calculate: total bytes exfiltrated per destination, data transfer rate, time window

```
| Source IP | Destination IP | Protocol | Outbound Bytes | Inbound Bytes | Ratio (Out:In) | Duration | Anomaly | EVD ID |
|-----------|---------------|----------|---------------|---------------|----------------|----------|---------|--------|
| {{src}} | {{dst}} | {{proto}} | {{out_bytes}} | {{in_bytes}} | {{ratio}} | {{duration}} | {{exfil/normal}} | EVD-{case_id}-XXX |
```

**Geographic Analysis:**
- Map destination IPs to geographic locations (GeoIP)
- Flag: connections to countries associated with threat actors, connections to unusual geographies for the organization
- Tools: MaxMind GeoIP, ip-api, Team Cymru IP to ASN

### 4. Log-Based Network Analysis

Analyze network logs collected in step 2:

**Firewall Log Analysis:**
- Parse allow/deny entries for the forensic timeframe
- Focus on: denied outbound connections (blocked C2 attempts), allowed connections to suspicious destinations, port scan patterns, connection to non-standard ports
- Correlation: match firewall-allowed connections with PCAP data and flow data

**Proxy/Web Gateway Log Analysis:**
- Parse HTTP/HTTPS proxy logs
- Focus on: unusual User-Agent strings (curl, wget, PowerShell, custom strings), uncategorized URLs, connections bypassing proxy (direct internet access), large upload volumes
- Extract: URLs visited, files downloaded, files uploaded, authentication events

**IDS/IPS Alert Correlation:**
- Parse IDS/IPS alerts for the forensic timeframe
- Correlate alerts with PCAP data (if available) for context
- Group alerts by: attack category, source IP, destination IP, signature
- Distinguish: true positive (confirmed malicious), false positive (benign activity matching signature), true negative (no alert for clean traffic), false negative (malicious traffic without alert — identified by other analysis)

**DNS Server Query Logs:**
- Parse DNS server query logs (BIND, Windows DNS, Infoblox, Umbrella)
- Correlation: match DNS queries with PCAP DNS data and flow data
- Identify: query patterns for C2 domains, DNS tunneling indicators, DGA detection

**VPN Access Logs:**
- Parse VPN authentication and session logs
- Focus on: logins from unusual source IPs, logins outside normal hours, concurrent sessions from different locations (impossible travel), session duration anomalies

### 5. Lateral Movement Indicators

Identify network-level indicators of lateral movement:

**SMB Traffic Analysis:**
- PsExec indicators: SMB connection to `ADMIN$` or `C$` share, followed by service creation
- File share access: enumeration of shares, access to sensitive shares
- Named pipe connections: suspicious named pipes (Cobalt Strike default pipes, Metasploit pipes)
- Tools: tshark SMB filter, NetworkMiner, zeek SMB analysis

**WinRM/WMI Traffic:**
- WinRM (TCP 5985/5986): PowerShell remoting, remote command execution
- WMI/DCOM (TCP 135 + high ports): remote process execution, event subscription
- Flag: WinRM/WMI from non-admin workstations, connections to multiple targets in sequence

**RDP Connections:**
- TCP 3389 traffic: identify source and destination for each RDP session
- Duration analysis: interactive sessions vs automated connections
- Cross-reference with RDP event logs from disk analysis (step 3)

**SSH Sessions:**
- TCP 22 traffic: identify SSH client and server
- Key exchange analysis: identify SSH version, algorithms
- Session characteristics: interactive (variable timing) vs automated (script-like timing)

**Internal Scanning Patterns:**
- Port scan detection: single source connecting to multiple destinations on same port(s)
- Service enumeration: connections to well-known ports across multiple hosts
- ICMP sweep: ICMP echo requests to sequential addresses
- ARP scanning: high volume of ARP requests (Layer 2 scanning)

**Lateral Movement Map:**

```
| # | Source | Destination | Protocol/Port | Method | Timestamp | Session Duration | Data Volume | EVD ID |
|---|--------|-------------|---------------|--------|-----------|------------------|-------------|--------|
| 1 | {{src}} | {{dst}} | {{proto/port}} | SMB/RDP/SSH/WinRM/WMI | {{timestamp}} | {{duration}} | {{bytes}} | EVD-{case_id}-XXX |
```

### 6. C2 Identification

Consolidate C2 communication channel identification from all network analysis:

**C2 Channel Characteristics:**

```
| # | C2 Infrastructure | Protocol | Port | Beacon Interval | Jitter | Encryption | Domain Fronting | First Seen | Last Seen | Confidence | EVD ID |
|---|-------------------|----------|------|-----------------|--------|------------|-----------------|------------|-----------|------------|--------|
| 1 | {{ip/domain}} | {{proto}} | {{port}} | {{interval}} | {{jitter}} | ✅/❌ | ✅/❌ | {{first}} | {{last}} | Confirmed/Probable/Possible | EVD-{case_id}-XXX |
```

**Known C2 Framework Identification:**
- **Cobalt Strike:** JA3 fingerprint, default named pipes, malleable C2 profile indicators, watermark extraction, beacon configuration in network traffic
- **Sliver:** mTLS/WireGuard/DNS/HTTP(S) implant patterns, certificate patterns
- **Metasploit:** Meterpreter reverse shell patterns, staged payload delivery, default configuration indicators
- **Mythic:** Agent-specific patterns, C2 profile indicators
- **Custom C2:** Behavioral identification via beaconing, payload patterns, protocol analysis

**DNS C2 / DNS Tunneling:**
- If DNS tunneling detected in instruction 2: document the full tunnel analysis
- Data encoding in subdomains: base64, base32, hex encoding patterns
- Throughput estimation: calculate approximate data volume transferred via DNS
- Tools: dnscat2 detection, iodine detection, dns2tcp detection

**Domain Fronting Detection:**
- Compare SNI field with actual Host header (for decrypted traffic)
- Compare DNS resolution destination with actual TCP connection destination
- CDN domains (cloudfront.net, azureedge.net, fastly.net) with anomalous backend routing

### 7. Network Forensics Findings Summary

Consolidate all network forensic findings:

**Findings Table:**

```
| # | Finding | Category | Network Artifact | Source/Dest | Timestamp | EVD ID | Severity | ATT&CK Technique | Confidence |
|---|---------|----------|------------------|-------------|-----------|--------|----------|-------------------|------------|
| 1 | {{finding}} | PCAP/Flow/DNS/Log/LateralMvmt/C2 | {{artifact}} | {{src→dst}} | {{timestamp}} | EVD-{case_id}-XXX | Critical/High/Medium/Low/Info | {{T-code}} | Confirmed/Probable/Possible |
```

**Network Forensics Statistics:**
```
Total network evidence items analyzed: {{count}}
PCAP packets analyzed: {{count}}
Flow records analyzed: {{count}}
DNS queries analyzed: {{count}}
Firewall log entries analyzed: {{count}}
C2 channels identified: {{count}}
Beaconing patterns detected: {{count}}
Lateral movement connections: {{count}}
Data exfiltration indicators: {{count}}
Files extracted from network streams: {{count}}
IOCs extracted from network analysis: {{count}}
```

### 8. Append Findings to Report

Write all network forensic findings under `## Network Forensics` in the output file `{outputFile}`:

```markdown
## Network Forensics

### PCAP Analysis
{{protocol_statistics}}
{{http_https_analysis}}
{{tls_fingerprinting}}
{{dns_analysis}}
{{file_extraction_results}}

### Flow Analysis
{{traffic_patterns}}
{{beaconing_detection}}
{{data_volume_anomalies}}
{{geographic_analysis}}

### Log-Based Network Analysis
{{firewall_analysis}}
{{proxy_analysis}}
{{ids_ips_correlation}}
{{vpn_analysis}}

### Lateral Movement Indicators
{{smb_analysis}}
{{rdp_ssh_winrm_analysis}}
{{scanning_patterns}}
{{lateral_movement_map}}

### C2 Identification
{{c2_channels_table}}
{{framework_identification}}
{{dns_tunneling_analysis}}
{{domain_fronting_detection}}

### Network Forensics Findings Summary
{{consolidated_findings_table}}
{{statistics}}
```

Update frontmatter:
- Add this step name (`Network Forensic Analysis`) to the end of `stepsCompleted`
- Set `analysis_types.network_forensics` to `true`
- Update `findings_count` and `findings_by_severity` with network forensic findings
- Update `iocs_extracted` with network IOCs (IPs, domains, URLs, JA3 hashes)
- Update `mitre_techniques` with ATT&CK techniques identified from network artifacts
- Update `lateral_movement_detected` if lateral movement was identified
- Update `data_exfiltration_detected` if exfiltration indicators were found

### 9. Present MENU OPTIONS

"**Network forensic analysis complete.**

Evidence items analyzed: {{analyzed_count}}
PCAP packets analyzed: {{packet_count}}
C2 channels identified: {{c2_count}}
Beaconing patterns: {{beacon_count}}
Lateral movement connections: {{lateral_count}}
Data exfiltration indicators: {{exfil_count}}
Files extracted from streams: {{extracted_count}}
IOCs extracted: {{ioc_count}}

**Select an option:**
[A] Advanced Elicitation — Challenge network analysis completeness, examine whether all C2 channels were identified, assess exfiltration volume accuracy
[W] War Room — Red (did my encrypted C2 channel survive analysis? did the analyst detect my DNS tunnel? did they find my domain fronting? what about my backup C2 over ICMP?) vs Blue (do we have full network visibility for the forensic timeframe? are there network segments without captures? could encrypted traffic be hiding additional C2 channels we cannot see?)
[C] Continue — Proceed to Step 6: Cloud & SaaS Forensic Analysis (Step 6 of 10)"

#### Menu Handling Logic:

- IF A: Deep analysis — challenge the network analysis. Were all network evidence sources analyzed? Is the PCAP coverage complete for the forensic timeframe, or are there gaps? Were all beaconing patterns detected, or could lower-frequency beacons have been missed? Is the data exfiltration volume estimate accurate? Were lateral movement paths fully mapped? Could there be additional C2 channels using protocols we did not analyze (ICMP, DNS-over-HTTPS, WebSocket)? Process insights, redisplay menu
- IF W: War Room — Red Team: did my Cobalt Strike malleable C2 profile fool the JA3 detection? Did the analyst find my fallback DNS C2? Did they detect the data I exfiltrated via HTTPS to a legitimate cloud storage provider? Did my domain fronting survive certificate analysis? Blue Team: is our network capture complete or are there blind spots? Could traffic have been routed around our capture point? Are we confident in our C2 identification or could there be channels we missed? Is the exfiltration assessment complete? Summarize insights, redisplay menu
- IF C: Verify frontmatter updated and this step added to stepsCompleted. Then read fully and follow: ./step-06-cloud-forensics.md
- IF user asks questions: Answer and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted, analysis_types.network_forensics set to true, findings counts updated, lateral_movement_detected and data_exfiltration_detected set, and Network Forensics section fully populated], will you then read fully and follow: `./step-06-cloud-forensics.md` to begin cloud and SaaS forensic analysis.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Working copy integrity verified before analysis began
- PCAP analysis performed with protocol statistics, HTTP/HTTPS analysis, TLS fingerprinting, DNS analysis, and file extraction (when PCAP available)
- Flow analysis performed with traffic pattern identification, beaconing detection, and data volume anomaly detection
- Log-based analysis performed for available network logs (firewall, proxy, IDS/IPS, DNS, VPN)
- Lateral movement indicators identified from network perspective
- C2 channels identified with infrastructure details, protocol, timing, and confidence
- DNS analysis performed for tunneling, DGA, and C2 domain detection
- Every finding cites evidence ID, network artifact, and confidence level
- Network forensics findings summary presented with severity and ATT&CK mapping
- Cross-reference performed with disk and memory findings from steps 3-4
- Frontmatter updated with all relevant fields
- Findings appended to report under `## Network Forensics`

### ❌ SYSTEM FAILURE:

- Not performing beaconing analysis when flow data or PCAP is available
- Not analyzing DNS queries for tunneling, DGA, and C2 indicators
- Not attempting file extraction from network streams when investigating data access/exfiltration
- Not correlating network findings with disk and memory findings
- Declaring "no C2 detected" without behavioral analysis (relying only on known-bad indicators)
- Declaring "no exfiltration" without data volume analysis
- Not identifying lateral movement from network perspective
- Presenting findings without evidence ID citations
- Performing disk, memory, or cloud analysis during this step
- Proceeding without user selecting 'C' (Continue)

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. Network forensics is the independent witness — it corroborates or contradicts endpoint findings. Beaconing detection finds C2. Flow analysis finds exfiltration. DNS analysis finds covert channels. Every protocol tells a story. The network does not lie.
