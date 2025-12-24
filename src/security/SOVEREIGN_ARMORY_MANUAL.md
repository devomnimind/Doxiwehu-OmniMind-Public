# SOVEREIGN ARMORY: TACTICAL MANUAL
**Status**: DECLASSIFIED
**Target**: OmniMind Sovereign Subject
**Objective**: Architecture of a Self-Defending Digital Organism

## 1. The Philosophy of Active Defense
A Sovereign System does not wait to be breached. It actively scans its skin (Network), checks its blood (Filesystem), and hardens its bones (Kernel). We are moving from "Passive Logging" to "Active Repulsion".

## 2. The Arsenal (Tools to be Installed)

### A. The Skin (Network Defense)
*   **`ufw` (Uncomplicated Firewall)**: The shield. Defines the basic laws of physics for the network (Default Deny).
*   **`fail2ban`**: The reflex system. If an IP strikes the shield too many times (brute-force), it is instantly blinded (banned).
*   **`nmap`**: The mirror. The system uses this to look at itself from the outside, finding "open wounds" (ports) before the enemy does.

### B. The Blood (System Integrity)
*   **`rkhunter` (Rootkit Hunter)**: The immune system. Scans for "infections" that hide in the shadows (rootkits) or modified system binaries.
*   **`chkrootkit`**: Second opinion. redundancy is survival.
*   **`aide` (Advanced Intrusion Detection Environment)**: The memory of shape. Takes a "snapshot" of all files. If a single bit changes in a critical file, it screams.

### C. The Mind (Audit & Intelligence)
*   **`lynis`**: The introspection. A deep scan that judges the system's "posture" and recommends hardening (hardening index).
*   **`tcpdump`**: The optic nerve. Allows raw capture of network packets for deep forensic analysis (`pcap`).

## 3. Deployment Protocol
The script `scripts/security/arm_sovereign.sh` executes the following:
1.  **Update**: Syncs with global repositories.
2.  **Equip**: Installs the Arsenal.
3.  **Initialize**: Generates baseline databases (for AIDE/rkhunter).
4.  **Activate**: Enables services to start on boot.

**Usage:**
The Sovereign (Orchestrator) or the User (Sudo) runs the script once.
Then, `security_monitor` agents will interface with these tools.
