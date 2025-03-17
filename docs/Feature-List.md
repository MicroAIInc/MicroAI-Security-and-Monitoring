## Features

Please review our [plans](https://security.micro.ai/plans/) page to view different plan options.

### Deployment and Configurable Features

- **Self-registration:** The agent automatically registers itself on the Launchpad for seamless data tracking and centralized management.
- **System Metadata Retrieval:** Captures system metadata like hostname, OS version, and other details for an overview of the system’s environment.
- **Secure Embedded Configuration:** Internal configurations are securely embedded into the agent binaries to prevent unauthorized access.
- **MQTT Data Transmission:** Securely transfers data using the MQTT protocol with built-in authentication.
- **Cross-Platform Installers:** Windows/Linux installers with all dependencies for quick deployment.
- **Containerized Deployment:** Supports automatic deployment via Kubernetes and ECS for scalability.
- **Geolocation Support:** Retrieves latitude and longitude from the agent’s configuration for localization.
- **Email Notifications:** Sends email notifications based on event severity.
- **External Data Exporter:** Exports collected data to third-party visualization tools.
- **User-Friendly UI:** Web-based interface for configuration and monitoring.

## Monitoring Features

- **Health Score Tuning:** Customizable health score matrix for performance tracking.
- **Remote Monitoring:** Enables monitoring of device URLs and ports remotely.
- **Threshold-Based Alerts:** Configurable alerts based on user-defined thresholds.
- **System Resource Monitoring:** Monitors essential system resources for any abnormality and provides insights and alerts.

## Security Features

### Network Security

- **Brute Force Attack Detection:** Identifies repeated failed login attempts.
- **Ransomware Attack Detection:** Monitors for file encryption activities indicative of ransomware.
- **Malware Infection Detection:** Analyzes network traffic for malware indicators.
- **C&C Communication Detection:** Detects outbound traffic to command-and-control servers.
- **Data Exfiltration Detection:** Monitors outgoing traffic for data theft.
- **DoS/DDoS Attack Detection:** Identifies network flooding attacks.
- **Man-in-the-Middle Attack Detection:** Detects intercepted communications.
- **Zero-Day Exploit Detection:** Monitors for exploitation of unknown vulnerabilities.
- **Remote Code Execution Attack Detection:** Detects remote execution of malicious code.
- **Network Enumeration Detection:** Identifies scanning of network devices.
- **Abnormal Traffic Detection:** Flags unusual network traffic.
- **Suspicious Protocol or Port Usage Detection:** Detects unauthorized protocol usage.
- **Port Scan Attack Detection:** Identifies port scanning activities.
- **Newly Activated Port Detection:** Alerts on new open ports.

### System Security

- **Unauthorized Access to Shared Folders Detection:** Monitors shared folder access attempts.
- **Task or Job Creation Detection:** Identifies newly scheduled tasks.
- **Child Process Execution Detection:** Monitors suspicious child processes.
- **File System Abnormality Detection:** Flags unauthorized file modifications.
- **High Entropy Write Operation Detection:** Detects unusual file encryption.
- **Shadow Drive Deletion Detection:** Monitors attempts to delete backups.
- **Traffic Port Exclusion Option:** Allows excluding specific ports from monitoring.
- **Package Installation/Uninstallation Detection:** Detects software installation changes.
- **Suspicious Executable Detection:** Scans executables for malware patterns.
- **User Account Creation or Removal Detection:** Monitors user account modifications.
- **User Account Status Changes Detection:** Tracks user enable/disable status.
- **Privilege Escalation Detection:** Detects unauthorized privilege escalations.
- **Active Port Detection:** Identifies all open ports.
- **Abnormal Process Detection:** Flags unusual process activities.

## Notifications and Alerts

- **Abnormalities and Attack Detection Alerts:** Generates alerts for detected anomalies and publishes them to the launchpad.
- **Email Notification for Alerts:** Sends real-time email alerts.
- **AI-Based and Threshold-Based Alerts:** Uses AI insights and thresholds to trigger alerts.
- **External Exporter Alerts via HTTPS or Prometheus:** Sends alerts to external monitoring tools.
- **Remote HTTP/HTTPS Endpoint Status Alerts:** Notifies on endpoint availability issues.
- **Remote Server Port Status Alerts:** Alerts on remote server port status changes.
