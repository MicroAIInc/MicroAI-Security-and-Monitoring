# 📦 Software Downloads

Welcome to the **official download page** for our software. Below, you'll find download links for **Linux (x64, ARM, ARM64)** and **Windows (x64)**.

---

## 🐧 Linux Downloads
| Version | Architecture | Tar File |
|------|-------------|---------|
| 2.2.17 | **x64**   | [Download](https://maicdn.micro.ai/security/linux/MicroAI-Security-linux-amd64-2.2.17-rc1.tar.gz) |
| 2.2.17 | **ARM**     | [Download](https://maicdn.micro.ai/security/linux_arm/MicroAI-Security-linux-arm-2.2.17-rc1.tar.gz) |
| 2.2.17 | **ARM64**   | [Download](https://maicdn.micro.ai/security/linux_arm/MicroAI-Security-linux-arm64-2.2.17-rc1.tar.gz) |

> **Note:** To use the Docker image:
#### Key Considerations
- Ensure Docker is installed and running on your system before executing the commands. See [Docker docs](https://docs.docker.com/engine/install/).
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

#### For Linux (x64) Systems

```bash
docker run -v /etc/ssl:/etc/ssl -d --privileged --net=host --pid=host --ipc=host --name microai_security_<latest-version> -e MAI_API_KEY=<license-key> -ti plasmacomputing/microai_security:linux-amd64-<latest-version>-rc1
```

#### For Linux ARM (x86) Systems

```bash
docker run -v /etc/ssl:/etc/ssl -d --privileged --net=host --pid=host --ipc=host --name microai_security_<latest-version> -e MAI_API_KEY=<license-key> -ti plasmacomputing/microai_security:linux-arm-<latest-version>-rc1
```

#### For Linux ARM (x64) Systems

```bash
docker run -v /etc/ssl:/etc/ssl -d --privileged --net=host --pid=host --ipc=host --name microai_security_<latest-version> -e MAI_API_KEY=<license-key> -ti plasmacomputing/microai_security:linux-arm64-<latest-version>-rc1
```

---

## 🖥️ Windows Download
| Version | Architecture | Tar File |
|------|-------------|---------|
| 2.2.17 | **x64**   | [Download](https://maicdn.micro.ai/security/windows/MicroAI-Security-windows-amd64-2.2.17-rc1.exe) |

---

## 📖 Installation Instructions

### **Linux (Tar Files)**
Copy the following section for your operating system and architecture and update the command to match it with your details.

- Replace `<latest-version>` with the latest release version.
- Replace `<license-key>` with a valid license key retrieved from [step 3](../README.md#step-3-activate-your-license)

#### **Linux (x64)**

```bash
wget https://maicdn.micro.ai/security/linux/MicroAI-Security-linux-amd64-<latest-version>-rc1.tar.gz
tar -xzf MicroAI-Security-linux-amd64-<latest-version>-rc1.tar.gz
cd MicroAI-Security-linux-amd64-<latest-version>/bin
chmod +x main
sudo ./main -MAI_API_KEY=<license-key>
```

#### **Linux (ARM)**

```bash
wget https://maicdn.micro.ai/security/linux_arm/MicroAI-Security-linux-arm-<latest-version>-rc1.tar.gz
tar -xzf MicroAI-Security-linux-arm-<latest-version>-rc1.tar.gz
cd MicroAI-Security-linux-arm-<latest-version>/bin
chmod +x main
sudo ./main -MAI_API_KEY=<license-key>
```

#### **Linux (ARM64)**

```bash
wget https://maicdn.micro.ai/security/linux_arm/MicroAI-Security-linux-arm64-<latest-version>-rc1.tar.gz
tar -xzf MicroAI-Security-linux-arm64-<latest-version>-rc1.tar.gz
cd MicroAI-Security-linux-arm64-<latest-version>/bin
chmod +x main
sudo ./main -MAI_API_KEY=<license-key>
```
---
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

### **Windows (EXE Installer)**
1. Download the **Windows x64 installer**.
2. Double-click the `.exe` file and follow the installation steps.
3. Run the software from the Start Menu or Command Prompt.


See [Launching MicroAI Security & Monitoring](./Launch-Instructions.md) for a detailed walkthrough.