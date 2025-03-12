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