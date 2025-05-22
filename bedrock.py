import aiohttp
import asyncio
import json
import os
from colorama import Fore, Style, init
import time
import sys
import ctypes
import msvcrt

init(autoreset=True)
error = f"{Fore.RED}[!]{Fore.RESET} "
success = f"{Fore.GREEN}[+]{Fore.RESET} "
process = f"{Fore.MAGENTA}[*]{Fore.RESET} "

API_FILE = "api.json"

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

async def async_get_key():
    while True:
        if msvcrt.kbhit():
            key = msvcrt.getch()
            if key == b'\xe0': 
                key = msvcrt.getch()
                return key
            elif key == b'\r':  
                return 'enter'
        await asyncio.sleep(0.01)

async def arrow_menu(options):
    selected = 0
    while True:
        clear()
        print(f"{process}Main Menu (Use ↑/↓ to navigate, Enter to select)\n")
        for i, option in enumerate(options):
            prefix = f"{Fore.CYAN}> " if i == selected else "  "
            print(f"{prefix}{option}")
        
        key = await async_get_key()
        
        if key == b'H': 
            selected = max(0, selected - 1)
        elif key == b'P':  
            selected = min(len(options)-1, selected + 1)
        elif key == 'enter':
            return selected

def load_api_data():
    try:
        with open(API_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def save_api_data():
    clear()
    print(f"{process}API Configuration")
    token = input("Enter your API token: ").strip()
    url = input("Enter API URL: ").strip()
    
    data = {
        'token': token,
        'api-url': url,
        'timestamp': time.time()
    }
    
    with open(API_FILE, 'w') as f:
        json.dump(data, f)
    
    print(f"{success}Credentials saved to {API_FILE}")
    time.sleep(1.5)

async def validate_token(token: str, api_url: str):
    headers = {
        'authorization': token,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, headers=headers) as response:
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

async def hacks(token: str):
    clear()
    menu_options = [
        "Change Score",
        "Spam API",
        "Complete Homework",
        "Exit"
    ]
    
    while True:
        selected = await arrow_menu(menu_options)
        
        if selected == 0:
            print("This is being worked on.")
            time.sleep(0.5)
            input("Press Enter to return to menu...")
            continue
        elif selected == 1:
            clear()
            print(f"""{Fore.CYAN}███████╗██████╗     ██╗  ██╗ █████╗  ██████╗██╗  ██╗███████╗
        ██╔════╝██╔══██╗    ██║  ██║██╔══██╗██╔════╝██║ ██╔╝██╔════╝
        ███████╗██║  ██║    ███████║███████║██║     █████╔╝ ███████╗
        ╚════██║██║  ██║    ██╔══██║██╔══██║██║     ██╔═██╗ ╚════██║
        ███████║██████╔╝    ██║  ██║██║  ██║╚██████╗██║  ██╗███████║
        ╚══════╝╚═════╝     ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝""")
            await asyncio.sleep(2)
            print(f"{process}Spamming API...")
            headers = {
                'authorization': token,
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            async with aiohttp.ClientSession() as session:
                amt = 0
                amount = int(input("Enter the number of requests to send to the server: "))
                if amount <= 0:
                    print(error + "Invalid amount!")
                    time.sleep(1.5)
                    return False
                for i in range(amount):
                    try:
                        async with session.get("https://api.bedrocklearning.org/api/sitemessages", headers=headers) as response:
                            if response.status == 200:
                                amt += 1
                                print(f"{success}Sent {amt}/{amount} requests.")
                            else:
                                print(error + f"Failed to send request: {response.status}")
                    except Exception as e:
                        print(error + f"Error: {str(e)}")
                    await asyncio.sleep(0.1)
                input("Press Enter to return to menu...")
                continue
        elif selected == 2:
            print("This is being worked on.")
            time.sleep(0.5)
            input("Press Enter to return to menu...")
            continue
        elif selected == 3:
            print(f"{success}Exiting...")
            sys.exit()

    

async def display_dashboard(data):
    clear()
    print(f"{success}Welcome {data['name']}!")
    print(f"{process}School: {data['school']} (ID: {data['data'].get('schoolID', 'Unknown')})")
    print(f"{process}Username: {data['data'].get('username', 'Unknwown')}")
    print(f"{process}Total Points: {data['data'].get('points', 0)}")
    print(f"{process}Total Time: {data['data'].get('time', 'Unknown')}")
    print(f"{process}Last Online: {data['data'].get('lastActive', 'Unknown')}")
    print(f"{process}Weekly Progress: {data['data'].get('pointsWeek', 0)}")

    with open("userapi.json", "w") as f:
        f.truncate(0)
        json.dump(data, f, indent=4)
    
    if 'blocks' in data['data']:
        print(f"\n{process}Recent Activity:")
        for block in data['data']['blocks'][:3]:
            print(f"• {block.get('name', 'Unnamed Block')}")
    
    input("\nPress Enter to return to menu...")

async def check_api_json():
    api_data = load_api_data()
    if not api_data:
        print(error + "No API configuration found!")
        time.sleep(1.5)
        return False
    
    print(f"{process}Validating API credentials...")
    validation = await validate_token(api_data['token'], api_data['api-url'])
    
    if not validation['valid']:
        print(error + f"Validation failed: {validation.get('error', 'Unknown error')}")
        time.sleep(2)
        return False
    
    await display_dashboard(validation)
    return True

async def main_menu():
    menu_options = [
        "Configure API Credentials",
        "Check API Connection",
        "Hacks",
        "Exit"
    ]
    
    while True:
        selected = await arrow_menu(menu_options)
        
        if selected == 0:
            save_api_data()
        elif selected == 1:
            if await check_api_json():
                continue
        elif selected == 2:
            with open("api.json", "r") as f:
                api_data = json.load(f)
                if not api_data:
                    print(error + "No API data found!")
                    time.sleep(1.5)
                    return False
                token = api_data['token']
            await hacks(token)
        elif selected == 3:
            print(f"{success}Exiting...")
            sys.exit()

async def key_system():
    clear()
    print(f"{process}License Key Check")
    try:
        with open("keys.txt", "r") as f:
            valid_keys = [k.strip() for k in f.readlines()]
            if not valid_keys:
                print(error + "No valid keys in keys.txt")
                time.sleep(2)
                sys.exit()
    except FileNotFoundError:
        print(error + "Key file missing! Contact support.")
        time.sleep(2)
        sys.exit()

async def main():
    if not ctypes.windll.shell32.IsUserAnAdmin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{sys.argv[0]}"', None, 1)
        sys.exit()
    
    await key_system()
    await main_menu()

if __name__ == "__main__":
    asyncio.run(main())