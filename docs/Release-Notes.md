# MicroAI Security & Monitoring Agent — Release Notes

Welcome to the official release notes for the **MicroAI Security & Monitoring Agent**.  
This document highlights recent updates, fixes, and improvements available for Linux and Windows platforms.

## Version Highlights

### **2.7.2 (Linux)**
**Release Date:** November 2025  
This release introduces important enhancements to system stability, resource management, and detection accuracy across Linux platforms.

#### Fixes & Improvements
- **Memory Usage Limitation for Redis Server** Implemented stricter memory limits to prevent Redis from exceeding system resource thresholds, ensuring more predictable performance and improved system stability. 
- Improved detection logic to reduce false positives and increase reliability of ransomware-related alerts.
- Continued enhancements to ensure smoother and more consistent operation across x64, ARM, and ARM64 Linux environments.

---

### **2.7.1 (Linux)**
**Release Date:** October 2025  
This release focuses on improving agent stability and reliability across Linux systems.  

#### Fixes & Improvements
- **Resolved prebuilt library merging issue** that could cause instability during packaging or runtime.  
- Improved consistency and compatibility across Linux architectures (x64, ARM, ARM64).  

---

### **2.7.0 (Windows)**
**Release Date:** September 2025  
This update addresses an issue affecting the Windows uninstallation process.  

#### Fixes & Improvements
- **Fixed uninstall prompt issue** — agent uninstall no longer triggers unnecessary reboot requests.  
- Enhanced uninstall reliability and cleanup performance.  

---

### Notes
- All agent builds include the latest monitoring, AI analytics, and configuration enhancements introduced in prior releases.  
- Ensure that your environment meets the minimum requirements before installation.