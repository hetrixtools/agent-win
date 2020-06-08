# [Alpha] HetrixTools Server Monitoring Agent (Windows)

**Please Note:** this is an Alpha version, still needing a lot more work to be production ready.

## Method 1 - Use the already compiled agent
We have provided the already compiled agent executable, here:  
https://github.com/hetrixtools/agent-win/releases

Be sure to follow the instructions in the release notes.


## Method 2 - Compile the agent yourself
If you wish to compile the executable yourself, then please follow the steps below.

### Requirements
You will need Python 2.7 with pip installed

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
