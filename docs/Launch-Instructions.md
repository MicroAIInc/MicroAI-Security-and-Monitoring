# Installation Walkthrough for Linux and Windows

In this section, we will walk through the installation process for a [Linux](#launching-microai-on-linux) environment and [Windows](#launching-microai-on-windows) environment.

## Launching MicroAI on Linux

The following screenshots illustrate an example of running MicroAI on Linux.

In the first screenshot, the agent is initialized and the device is activated, displaying the confirmation message: **"Device is activated successfully."** Once activated, the agent enters Training Mode, where the AI engine begins learning from the environment. A progress bar indicates the training status.  

<img src="../docs/images/Linux-Launch-Train.png" alt="Linux Initialization" width="600">

In the second screenshot, the training reaches 100%, and the agent automatically switches to Execute Mode, as confirmed by the message: **"Training complete! Execute Mode set. Everything started."** At this stage, the agent is fully operational and ready for monitoring and security tasks.  

<img src="../docs/images/Linux-Launch-Complete.png" alt="Linux Training Complete" width="600">

If the License key is invalid, the following error will be returned.  

<img src="../docs/images/Linux-Launch-Incorrect-License.png" alt="Invalid API Key Error" width="600">

If the device is registered under a different profile on Launchpad, the following error will occur. Please ensure that you are using the License key associated with the original account.  

<img src="../docs/images/Linux-Launch-Already-Registered.png" alt="Different Profile Error" width="600">

---

## Launching MicroAI on Windows

The wizard is currently in the **"Collecting Information"** phase, highlighted in blue, with three subsequent stages: **"Preparing Installation," "Installing,"** and **"Finalizing Installation."** The user is prompted to proceed by clicking **"Next"** or to exit the setup by selecting **"Cancel."**  

<img src="../docs/images/Windows-Launch-Setup.png" alt="Windows Setup - Collecting Information" width="600">

### Prerequisites
Three prerequisites are listed, each marked with a checked checkbox, indicating they are selected for installation:
- **Npcap** (Version 1.0 or higher required)
- **Microsoft Windows Desktop Runtime - 7.0.0 (x86)**
- **Oracle Java SE Development Kit 17.0.1 x64** (Version 17.0.1 or higher required)

<img src="../docs/images/Windows-Launch-Prerequsite.png" alt="Windows Prerequisites" width="600">

### End-User License Agreement
This image presents the **"End-User License Agreement"** screen of the MicroAI Security and Monitoring Setup Wizard.  

<img src="../docs/images/Windows-Launch-EULA.png" alt="EULA Screen" width="600">

### Installation Path Selection
The interface presents the default installation path:  
📁 **C:\Program Files\MicroAI\MicroAI Security and Monitoring**  

Users can either:
- Accept the default path by clicking **"Next"**
- Specify a different location by manually entering a path or using the **"Browse..."** button

<img src="../docs/images/Windows-Launch-Installation.png" alt="Installation Path Selection" width="600">

### Device Authentication
The user is required to enter their **License Key** to authenticate and connect the installation to the MicroAI Security and Monitoring platform.

A reference image below the input field provides guidance on locating the License key within the **MicroAI Launchpad** interface or retrieve the license key from your email if using quick registration.  
Additionally, the screen includes an option to **"Launch local UI,"** which is checked by default, with port **8989** specified for local access.  

<img src="../docs/images/Windows-Launch-Activation.png" alt="API Key Authentication" width="600">

### Installation Progress
The installation has now advanced to the **"Installing"** phase, which is highlighted in blue in the left navigation panel.  

<img src="../docs/images/Windows-Launch-Complete.png" alt="Installation in Progress" width="600">

### Windows Services Management
This image shows the **Windows Services** management console, where users can control and manage the **MicroAI Security and Monitoring service.** The service is currently **"Running"** with an **Automatic startup type,** ensuring it launches automatically with the system.  

<img src="../docs/images/Windows-Launch-Service.png" alt="Windows Services Management" width="600">

