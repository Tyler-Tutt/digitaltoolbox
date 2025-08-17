# Windows & Linux Compatible Utility Application
- MacOS Not Supported

# File Structure:
- Project folder on Windows file system
- Use Linux (WSL) as primary dev environment
- Windows for testing & files

# Environments:
- pip's (libraries) need to be maintained between both Linux & Windows

# Initial Dev Environment:
## Create Linux Virtual Environment:
    python -m venv .venv
## Create Windows Virtual Environment:
    python3 -m venv venv_win

Dev Environment Routine:
# Bash Activate Linux Virutal Environment:
    source venv/bin/activate
# Powershell Activate Windows Virutal Environment
    .\venv_win\Scripts\activate