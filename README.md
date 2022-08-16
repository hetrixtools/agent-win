# [Alpha] HetrixTools Server Monitoring Agent (Windows)

**Please Note:** this is an Alpha version, still needing a lot more work to be production ready.

## Method 1 - Use the already compiled agent
 - Download the `HetrixTools.exe` agent file from GitHub:  
https://github.com/hetrixtools/agent-win/releases/download/v1.5.4-alpha/HetrixToolsAgent.exe
 - Place the `HetrixTools.exe` agent file in a folder on your Windows machine (i.e., C:\HetrixTools)
 
### Install method: 
 - Right click on the `HetrixToolsAgent.exe` agent file and select to "Run as administrator"
 - Input your SID when prompted; you can find it by following this guide:  
https://docs.hetrixtools.com/where-do-i-find-the-sid-server-monitor-id/
 - The executable will install the `HetrixToolsAgent` service, which you can find running in your services
 
### Alternative install method:
- Open `Command Prompt` as Administrator
- Navigate to the folder where the `HetrixToolsAgent.exe` executable is located
- Run the following commands:
```
HetrixToolsAgent.exe --startup auto install
HetrixToolsAgent.exe start
```

### Stop & Uninstall
- Open `Command Prompt` as Administrator
- Navigate to the folder where the `HetrixToolsAgent.exe` executable is located
- Run the following commands:
```
HetrixToolsAgent.exe stop
HetrixToolsAgent.exe remove
taskkill /IM "HetrixToolsAgent.exe" /F
```

### Alternative Stop & Uninstall
- Open `Command Prompt` as Administrator
- Run the following commands:
```
sc delete HetrixToolsAgent
taskkill /IM "HetrixToolsAgent.exe" /F
```

### Upgrading From Previous Versions
- First stop and uninstall the agent as explained above
- Then install the new agent as explained at the beginning of this guide
 

## Method 2 - Compile the agent yourself
If you wish to compile the executable yourself, then please follow the steps below.

### Requirements
You will need Python 2.7.18 x86 with pip installed

Install the needed dependencies  
```
pip install -r requirements.txt
```  
You may also need to run the following command globally or in your build environment  
```
python scripts\pywin32_postinstall.py -install
```

### Build
Download this repository into its own folder on your computer

Inside that folder, run the following command  
```
pyinstaller --onefile --clean --icon=icon.ico HetrixToolsAgent.py
```

If no errors are encountered, the agent executable will be compiled in the `/dist/` folder.  
Once you have the agent executable, follow the same instructions as on Method 1.
