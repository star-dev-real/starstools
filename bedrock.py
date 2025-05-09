import requests
import aiohttp
import asyncio
import json
import os
from colorama import Fore, Style, init
import time
from datetime import datetime
import re
from mitmproxy import http
import webbrowser
import winreg
import ctypes
import sys
import subprocess
import signal

# Colorama Initialization
init(autoreset=True)
question = f"{Fore.YELLOW}[?]{Fore.RESET} "
error = f"{Fore.RED}[!]{Fore.RESET} "
info = f"{Fore.CYAN}[=]{Fore.RESET} "
success = f"{Fore.GREEN}[+]{Fore.RESET} "
process = f"{Fore.MAGENTA}[*]{Fore.RESET} "

# Global State
captured_token = None
mitm_process = None
token_captured_event = asyncio.Event()

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

async def key_system():
    clear()
    print(f"{question}Please enter your License Key: ")
    key = input().strip()
    if not key:
        print(error + "Key cannot be empty!")
        time.sleep(2)
        sys.exit()
    
    try:
        with open("keys.txt", "r") as f:
            valid_keys = [k.strip() for k in f.readlines()]
            if key in valid_keys:
                print(success + "Key validated successfully!")
                time.sleep(1)
                return True
    except FileNotFoundError:
        print(error + "Key file missing! Contact support.")
    
    print(error + "Invalid license key!")
    time.sleep(2)
    sys.exit()

def proxy_control(enable=True):
    try:
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Internet Settings",
            0, winreg.KEY_WRITE
        ) as key:
            if enable:
                winreg.SetValueEx(key, "ProxyEnable", 0, winreg.REG_DWORD, 1)
                winreg.SetValueEx(key, "ProxyServer", 0, winreg.REG_SZ, "127.0.0.1:8080")
                winreg.SetValueEx(key, "ProxyOverride", 0, winreg.REG_SZ, "<local>")
            else:
                winreg.SetValueEx(key, "ProxyEnable", 0, winreg.REG_DWORD, 0)
            
            internet_option_refresh()
            return True
    except Exception as e:
        print(error + f"Proxy error: {str(e)}")
        return False

def internet_option_refresh():
    INTERNET_OPTION_SETTINGS_CHANGED = 39
    INTERNET_OPTION_REFRESH = 37
    ctypes.windll.Wininet.InternetSetOptionW(0, INTERNET_OPTION_SETTINGS_CHANGED, 0, 0)
    ctypes.windll.Wininet.InternetSetOptionW(0, INTERNET_OPTION_REFRESH, 0, 0)
    ctypes.windll.user32.SendMessageTimeoutW(0xFFFF, 0x001A, 0, "Internet Settings", 0, 1000, 0)

def request(flow: http.HTTPFlow):
    global captured_token
    if "api.bedrocklearning.org/api/students" in flow.request.url:
        if flow.request.method == "GET" and "authorization" in flow.request.headers:
            captured_token = flow.request.headers['authorization']
            print(f"\n{success}TOKEN CAPTURED: {captured_token}")
            proxy_control(enable=False)
            validate_token(captured_token)
            if mitm_process:
                mitm_process.send_signal(signal.CTRL_C_EVENT)
            token_captured_event.set()

async def fetch_token():
    global mitm_process
    clear()
    print(f"{process}Initializing MITM proxy...")
    
    if not proxy_control(enable=True):
        print(error + "Failed to configure system proxy!")
        return None

    print(f"{info}Opening Bedrock Learning in browser...")
    webbrowser.open("https://app.bedrocklearning.org")
    
    mitm_process = subprocess.Popen(
        ["mitmdump", "-s", __file__, "--quiet"],
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
    )
    
    try:
        print(f"{process}Waiting for authentication... (Ctrl+C to cancel)")
        await token_captured_event.wait()
    except asyncio.CancelledError:
        print(error + "Token capture cancelled")
    finally:
        proxy_control(enable=False)
        if mitm_process and mitm_process.poll() is None:
            mitm_process.terminate()
    
    return captured_token

async def validate_token(token: str):
    headers = {
        'Authorization': token,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                'https://api.bedrocklearning.org/api/students/current/dashboard',
                headers=headers
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        'valid': True,
                        'data': data,
                        'name': f"{data.get('firstname', '')} {data.get('lastname', '')}",
                        'school': data.get('schoolName', 'Unknown School')
                    }
                return {'valid': False, 'error': f"HTTP {response.status}"}
    except Exception as e:
        return {'valid': False, 'error': str(e)}

async def display_dashboard(data):
    clear()
    print(f"{success}Welcome {data['name']}!")
    print(f"{info}School: {data['school']}")
    print(f"{info}Total Points: {data['data'].get('points', 0)}")
    print(f"{info}Weekly Progress: {data['data'].get('pointsWeek', 0)} points")
    
    if 'blocks' in data['data']:
        print(f"\n{process}Recent Activity:")
        for block in data['data']['blocks'][:3]:
            print(f"• {block.get('name', 'Unnamed Block')}")
    
    input("\nPress Enter to continue...")

async def main_flow():
    while True:
        clear()
        print(f"""
        {Fore.CYAN}Bedrock Learning Toolkit
        {Fore.YELLOW}-------------------------
        {question}[1] Enter Existing Token
        {question}[2] Auto-Capture Token
        {question}[3] Exit
        """)
        
        choice = input(f"{process}Select option: ").strip()
        
        token = None
        if choice == "1":
            token = input(f"{question}Enter Bearer token: ").strip()
            if not token.startswith("Bearer "):
                token = f"Bearer {token}"
        elif choice == "2":
            token = await fetch_token()
            if not token:
                print(error + "No token captured!")
                time.sleep(2)
                continue
        elif choice == "3":
            sys.exit()
        else:
            print(error + "Invalid selection!")
            time.sleep(1)
            continue
        
        print(f"{process}Validating token...")
        validation = await validate_token(token)
        
        if not validation['valid']:
            print(error + f"Token validation failed: {validation.get('error', 'Unknown error')}")
            time.sleep(2)
            continue
        
        await display_dashboard(validation)

async def main():
    if not ctypes.windll.shell32.IsUserAnAdmin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{sys.argv[0]}"', None, 1)
        sys.exit()
    
    await key_system()
    await main_flow()

if __name__ == "__main__":
    asyncio.run(main())