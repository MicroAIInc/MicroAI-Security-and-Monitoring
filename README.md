<p align="right">
  <img src="https://img.shields.io/badge/MicroAI_Security_and_Monitoring-v2.2.17-green" alt="Static Badge">
</p>
<br />
<p align="center">
  <img src="https://docs.micro.ai/_static/microai-logo-light.svg" alt="MicroAI Logo" width="200">
</p>

<h3 align="center">MicroAI Security and Monitoring</h3>

<p align="center">
  MicroAI Security is an Edge-native AI platform that embeds and trains advanced security algorithms directly on a device, machine, or process.
</p>

<p align="center">
  This guide will help you <strong>install</strong>, <strong>configure</strong>, and <strong>validate</strong> the MicroAI Security agent, ensuring it operates correctly and securely. No technical expertise is required—just follow the steps carefully, and you'll have the agent up and running in no time!
</p>


## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Validation](#validation)
- [Configurations](#configurations)
- [Troubleshooting](#troubleshooting)
- [License](#license)
- [Contact](#contact)

## Stay current with the latest updates!
The MicroAI team regularly releases new versions. Please see the [release notes page](./docs/RELEASENOTES.md) for updates. We recommend keeping up to date with latest releases to stay current on security patches, bug fixes, and new features. Take a peek at our [feature page](docs/Feature-List.md) for current features available with our agent.

## Installation

Follow the steps below to install MicroAI Security on your system. The installation process varies depending on your operating system and architecture. Before proceeding, ensure you have your Licensing key, which is essential for activating the agent.

### Step 1: Activate your License

Activate your license and retrieve your license key on [MicroAI](https://micro.ai)

### Step 2: Download the Package

Download the latest release the [packages](packages/README.md) directory.

### Step 3: Extract and Set Up the Agent

#### **For Linux (amd64)**

```bash
tar -xzf microai_security_vx_x_xx.tar.gz
cd microai_security_vx_x_xx/bin
chmod +x main
```

#### **For Linux (ARM)**

```bash
tar -xzf MicroAI-Security-linux-arm-x.x.xx.tar.gz
cd MicroAI-Security-linux-arm-x.x.xx/bin
chmod +x main
```

#### **For Windows (amd64)**

```powershell
Invoke-WebRequest https://maicdn.micro.ai/security/windows/MicroAI-Security-windows-amd64-x.x.xx.exe -OutFile MicroAI-Security-windows-amd64-x.x.xx.exe
```

#### **For Docker**

Docker provides an efficient way to run MicroAI in a containerized environment. If you prefer deploying the agent as a Docker container, see the [Docker section](#docker).


### Step 4: Install Java 17 (If UI Console is Needed)

If you're enabling the Local UI Console, install Java 17:

```bash
wget https://download.oracle.com/java/17/archive/jdk-17.0.9_linux-x64_bin.tar.gz
mkdir -p /usr/lib/jdk
tar xvzf jdk-17.0.9_linux-x64_bin.tar.gz -C /usr/lib/jdk
```

## Usage

Activate and retrieve your **license key** from [MicroAI Launchpad](https://launchpad.micro.ai/) before launching the agent.

See [Launching MicroAI Security and Monitoring](docs/Launch-Instructions.md) for a detailed walkthrough.

#### **Run Without UI**

```bash
sudo ./main -license_key=<profile-api>
```

#### **Run with UI on Default Port (8989)**

```bash
sudo ./main -license_key=<profile-api> -console
```

#### **Run with UI on a Custom Port**

```bash
sudo ./main -license_key=<profile-api> -console -console.port=<port>
```

#### **Run with Java Path (for UI Console)**

```bash
sudo ./main -license_key=<profile-api> -console -javapath=/usr/lib/jdk/jdk-17.0.9/bin/java
```

The following requirements apply **only if you enable the Local UI Console** (optional):

#### Java 17 Installation (for UI Console only)

- [Java 17 for Linux x64](https://download.oracle.com/java/17/archive/jdk-17.0.9_linux-x64_bin.tar.gz)
- [Java 17 for Linux Arm x64](https://download.oracle.com/java/17/archive/jdk-17.0.8_linux-aarch64_bin.tar.gz)

## Docker

Docker provides an efficient way to run MicroAI in a containerized environment. If you prefer deploying the agent as a Docker container, use the following commands, selecting the appropriate version based on your system architecture.

#### Key Considerations
- Ensure Docker is installed and running on your system before executing the commands.
- Replace `<your_license_key>` with the actual MicroAI License key for authentication.
- Using `--privileged` and `--net=host` grants the container full system access, which is required for security monitoring but should be used cautiously.
- The image tag `2.x.x` corresponds to the MicroAI agent version; update it as needed for newer versions.

#### For x86_64 (AMD64) Systems

```bash
docker run -v /etc/ssl:/etc/ssl -d --privileged --net=host --pid=host --ipc=host \
  --name microai_security_2_x_x -e MAI_API_KEY=<your_license_key> \
  -ti plasmacomputing/microai_security:linux-amd64-2.x.x
```

#### For ARM (32-bit) Systems

```bash
docker run -v /etc/ssl:/etc/ssl -d --privileged --net=host --pid=host --ipc=host \
  --name microai_security_2_x_x -e MAI_API_KEY=<your_license_key> \
  -ti plasmacomputing/microai_security:linux-arm-2.x.x
```

#### For ARM64 (AArch64) Systems

```bash
docker run -v /etc/ssl:/etc/ssl -d --privileged --net=host --pid=host --ipc=host \
  --name microai_security_2_x_x -e MAI_API_KEY=<your_license_key> \
  -ti plasmacomputing/microai_security:linux-arm64-2.x.x
```

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

See [configure url and port monitoring](Configure-Internal-UI.md) page to get a walkthrough on how to use the local UI and monitor these options. **Requires Local UI to be running**

Review our [extend agents capabilities](docs/Extend-Agent-Capabilities.md) page to apply custom remediation options and take custom actions on the agents alerts and notifications. 

## Troubleshooting

If you encounter issues, try these solutions:

### Issue: "Permission Denied" on Running `./main`

- Solution:
  ```bash
  chmod +x main
  sudo ./main -MAI_API_KEY=<your_license_key>
  ```

### Issue: UI Console Not Launching

- Solution:
  ```bash
  java -version  # Ensure Java 17 is installed
  sudo ./main -MAI_API_KEY=<profile-api> -console
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

See [Software Evaluation Licensing Agreement](https://github.com/MicroAIInc/MicroAI-Atom-Libraries/blob/master/MicroAI%20Atom%20Evaluation%20License%20Agreement.pdf) for more details.

---

## Contact

- **Company:** MicroAI™
- **Website:** [www.micro.ai](https://www.micro.ai)
- **Email:** [support@micro.ai](mailto\:support@micro.ai)

