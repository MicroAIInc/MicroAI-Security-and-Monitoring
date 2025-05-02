<p align="right">
  <img src="https://img.shields.io/badge/MicroAI_Security_&_Monitoring-2.4.0-green" alt="Static Badge">
</p>
<br />
<p align="center">
  <img src="./docs/images/microai-logo.png" alt="MicroAI Logo" width="250">
</p>

<h3 align="center">MicroAI Security & Monitoring</h3>

<p align="center">
  MicroAI Security & Monitoring is an Edge-native AI platform that embeds and trains advanced security algorithms directly on a device, machine, or process.
</p>

<p align="center">
  This guide will help you <strong>install</strong>, <strong>configure</strong>, and <strong>validate</strong> the MicroAI Security & Monitoring agent, ensuring it operates correctly and securely. No technical expertise is required—just follow the steps carefully, and you'll have the agent up and running in no time!
</p>


## Table of Contents

- [Installation](#installation)
- [Validation](#validation)
- [Configurations](#configurations)
- [Features](#features)
- [Troubleshooting](#troubleshooting)
- [License](#license)
- [Contact](#contact) 

## Installation

Follow the steps below to install MicroAI Security on your system. The installation process varies depending on your operating system and architecture. Before proceeding, ensure you have your Licensing key, which is essential for activating the agent.

Determine your Operating system and architecture [here](./docs/Detect-OS-Arch.md).

### Step 1: Download the Package

Download the latest supported release from the [packages](./docs/Packages.md) page and transfer it onto the system intended for installation. Alternatively, use the commands directly from [step 2](#step-2-extract-and-set-up-the-agent).

---
### Step 2: Extract and Set Up the Agent

Copy the following section for your operating system and architecture and update the command to match it with your details.

- Replace `<latest-version>` with the latest release version. The latest version can be found on the [packages](./docs/Packages.md) page or on the top of this page.

#### **Linux (x64)**

```bash
wget https://maicdn.micro.ai/security/linux/MicroAI-Security-linux-amd64-<latest-version>.tar.gz
tar -xzf MicroAI-Security-linux-amd64-<latest-version>.tar.gz
cd MicroAI-Security-linux-amd64-<latest-version>/bin
chmod +x main
```

#### **Linux (ARM x86)**

```bash
wget https://maicdn.micro.ai/security/linux_arm/MicroAI-Security-linux-arm-<latest-version>.tar.gz
tar -xzf MicroAI-Security-linux-arm-<latest-version>.tar.gz
cd MicroAI-Security-linux-arm-<latest-version>/bin
chmod +x main
```

#### **Linux (ARM x64)**

```bash
wget https://maicdn.micro.ai/security/linux_arm/MicroAI-Security-linux-arm64-<latest-version>.tar.gz
tar -xzf MicroAI-Security-linux-arm64-<latest-version>.tar.gz
cd MicroAI-Security-linux-arm64-<latest-version>/bin
chmod +x main
```

#### **Windows (x64)**

```powershell
Invoke-WebRequest https://maicdn.micro.ai/security/windows/MicroAI-Security-windows-amd64-<latest-version>.exe -OutFile MicroAI-Security-windows-amd64-<latest-version>.exe
```
---
### Step 3: Activate your License

Activate your license and retrieve your license key on <a href="https://launchpad.micro.ai/activate/securitytrial" target="_blank">MicroAI Launchpad</a>. See [activation walkthrough](./docs/Registration-Instructions.md) for guided steps.

---

### Step 4: Install Java 17 (If UI Console is Needed)

If you're enabling the Local UI Console, install Java 17 for your linux environments:

- [Java 17 for Linux x64](https://download.oracle.com/java/17/archive/jdk-17.0.9_linux-x64_bin.tar.gz)
- [Java 17 for Linux Arm x64](https://download.oracle.com/java/17/archive/jdk-17.0.8_linux-aarch64_bin.tar.gz)

```bash
wget https://download.oracle.com/java/17/archive/jdk-17.0.9_linux-x64_bin.tar.gz
mkdir -p /usr/lib/jdk
tar xvzf jdk-17.0.9_linux-x64_bin.tar.gz -C /usr/lib/jdk
```
Windows installer includes this step in the instllation process.

---
### Step 5: Run the Agent

Replace `<license-key>` with a valid license key retrieved from [step 3](#step-3-activate-your-license). See [configurations](./docs/Configurations.md#default-configurations) to find the default configurations the agent is set up with.

#### **Run Without Console**

```bash
sudo ./main -MAI_API_KEY=<license-key>
```

#### **Run with Console on Default Port (8989)**

```bash
sudo ./main -MAI_API_KEY=<license-key> -console
```

#### **Run with Console on a Custom Port**

```bash
sudo ./main -MAI_API_KEY=<license-key> -console -console.port=<port>
```

#### **Run with Java Path (for Console)**

```bash
sudo ./main -MAI_API_KEY=<license-key> -console -javapath=/usr/lib/jdk/jdk-17.0.9/bin/java
```
---
#### **Windows (x64)**

Double-click the `.exe` file and follow the installation steps. See [Launching MicroAI Security & Monitoring](docs/Launch-Instructions.md) for a detailed walkthrough.

#### **Docker**
---
Docker provides an efficient way to run MicroAI in a containerized environment. If you prefer deploying the agent as a Docker container, use the following commands, selecting the appropriate version based on your system architecture.

#### Key Considerations
- Ensure Docker is installed and running on your system before executing the commands.
- Replace `<license-key>` with the actual MicroAI License key for authentication.
- Using `--privileged` and `--net=host` grants the container full system access, which is required for security monitoring but should be used cautiously.
- The image tag `<latest-version>` corresponds to the MicroAI agent version; update it as needed for newer versions.
- If you need to update the configuration file, you can mount the config directory using the `-v` option and add this to the commands below:  
  ```bash
  -v <absolute_path_to_config_directory_on_host_machine>:/home/security/config
  ```
- Similarly, to access logs from the host machine, mount the log directory as follows:  
  ```bash
  -v <absolute_path_to_log_directory_on_host_machine>:/home/security/data/logs
  ```

#### For Linux x64 Systems

```bash
docker run -v /etc/ssl:/etc/ssl -d --privileged --net=host --pid=host --ipc=host --name microai_security_<latest-version> -e MAI_API_KEY=<license-key> -ti plasmacomputing/microai_security:linux-amd64-<latest-version>-rc1
```

#### For Linux ARM (x86) Systems

```bash
docker run -v /etc/ssl:/etc/ssl -d --priv
ileged --net=host --pid=host --ipc=host --name microai_security_<latest-version> -e MAI_API_KEY=<license-key> -ti plasmacomputing/microai_security:linux-arm-<latest-version>-rc1
```

#### For Linux ARM (x64) Systems

```bash
docker run -v /etc/ssl:/etc/ssl -d --privileged --net=host --pid=host --ipc=host --name microai_security_<latest-version> -e MAI_API_KEY=<license-key> -ti plasmacomputing/microai_security:linux-arm64-<latest-version>-rc1
```
See [Launching MicroAI Security & Monitoring](docs/Launch-Instructions.md) for a detailed walkthrough.

## Validation

After installation, use the following steps to ensure the agent is running correctly:

1. **Check if the process is running**:
   ```bash
   ps aux | grep main
   ```
2. **Verify logs for errors**:
   ```bash
   cat <installation-path>/data/logs/microai-main.log
   ```
3. **Confirm API key authentication and start of agent**:
   ```bash
   cat <installation-path>/data/logs/microai-main.log

   [*] MicroAI Security and Monitoring v2.2.17 - Release linux amd64
   [-] MicroAI Starting
   [-] Training Mode set
   [-] Profile API: ***
   [-] Device activated sucessfully
   [-] starting subprocess 0
   [-] starting subprocess 1
   [-] starting subprocess 2
   [-] starting subprocess 3
   [-] starting subprocess 4
   [-] Training started
   [-] Training complete!
   [-] Everything started
   ```

If all checks pass, the agent is successfully installed and operational!


## Configurations

To customize your agent settings, refer to the [Configurations Guide](docs/Configurations.md).

See [configure url and port monitoring](docs/Configure-Internal-UI.md) page to get a walkthrough on how to use the local UI and monitor these options. **Requires Local UI to be running**

Review our [extend agents capabilities](docs/Extend-Agent-Capabilities.md) page to apply custom remediation options and take custom actions on the agents alerts and notifications. 

If you wish to view your profile, devices or update your plan, follow this [guide](./docs/Update-Profile.md).

## Features

Take a peek at our [feature page](docs/Feature-List.md) for current features available with our agent.

## Troubleshooting

If you encounter issues, try these solutions:

### Issue: "Permission Denied" on Running `./main`

- Solution:
  ```bash
  chmod +x main
  sudo ./main -MAI_API_KEY=<license-key>
  ```

### Issue: UI Console Not Launching

- Solution:
  ```bash
  java -version  # Ensure Java 17 is installed
  sudo ./main -MAI_API_KEY=<license-key> -console
  ```

### Issue: API Key Authentication Fails

- Solution:
  1. Verify your License key
  2. Ensure you have an active internet connection
  3. Check logs:
     ```bash
     <installation-path>/data/logs/microai-main.log
     ```

For further assistance, contact [**support@micro.ai**](mailto\:support@micro.ai).

---

## License

See [Software Licensing Agreement](License.txt) for more details.

---

## Contact

- **Company:** MicroAI™
- **Website:** [www.security.micro.ai](https://www.security.micro.ai)
- **Email:** [support@micro.ai](mailto\:support@micro.ai)

