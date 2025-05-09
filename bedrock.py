import requests
import aiohttp
import asyncio
import json
import os
from colorama import Fore, Style, init
import time
from datetime import datetime
import re

# Token = Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1bmlxdWVfbmFtZSI6InJhbHBoLmJ1dGxlci40MjE1NSIsInJvbGUiOiJzdHVkZW50Iiwic3R1ZGVudElEIjoiNzg0ZmNjYTgtOTEyNS00ZmNjLTgxYzgtYzFlYmFiOGFiZmNjIiwicGFyZW50SUQiOiIiLCJzdGFmZklEIjoiIiwiYWRtaW5JRCI6IiIsInNjaG9vbElEIjoiMzA3ZGYwM2EtOWY5ZS00MjM2LTkwZWItYTA4Yjk5OWIwY2EzIiwibmJmIjoxNzQ1NzY0NzQyLCJleHAiOjE3NDU4MDc5NDIsImlhdCI6MTc0NTc2NDc0Mn0.8JJL3mYXnjsK-T7dZSvlyFFCn_y7RqjNdJ5QdQf1OF4

question = f"{Fore.YELLOW}[?]{Fore.RESET} "
error = f"{Fore.RED}[!]{Fore.RESET} "
info = f"{Fore.CYAN}[=]{Fore.RESET} "
success = f"{Fore.GREEN}[+]{Fore.RESET} "
process = f"{Fore.MAGENTA}[*] "

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

clear()

init(autoreset=True)

async def check_token():
    token = input("Enter your bearer token: ")
    if not token:
        print(error + "Please enter a token.")
        time.sleep(2)
        clear()
        exit()
        return None
    elif token.lower().startswith("bearer "):
        token = "Bearer " + token[len("bearer "):].strip()
    else:
        token = "Bearer " + token.strip()

    print(process + "Logging in...")
    time.sleep(2)
    clear()

    headers = {
        'Origin': 'https://app.bedrocklearning.org',
        'Host': 'api.bedrocklearning.org',
        'Sec-Fetch-Mode': 'cors',
        'Authorization': token,
        'Priority': 'u=3, i',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_3_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.3.1 Mobile/15E148 Safari/604.1',
        'Referer': 'https://app.bedrocklearning.org/',
        'Accept-Language': 'en-GB,en;q=0.9',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Dest': 'empty',
        'Accept': 'application/json, text/plain, */*',
        'Connection': 'keep-alive',
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                'https://api.bedrocklearning.org/api/students/784fcca8-9125-4fcc-81c8-c1ebab8abfcc/dashboard',
                headers=headers
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    full_name = data.get('firstname') + " " + data.get('lastname')
                    print(f"{success}Token is valid.\nWelcome {full_name}")
                    time.sleep(1)
                    input("Press enter to continue...")
                    clear()
                    return data
                else:
                    print(error + "Invalid token. Please check your token and try again.")
                    time.sleep(2)
                    exit()
    except Exception as e:
        print(error + f"An error occurred: {str(e)}")
        return None

async def get_assignments(data):
    if not data:
        print(error + "No data provided.")
        return

    print(f"{process}Fetching Info...")
    time.sleep(1)
    school_id = data.get('schoolID')
    print(f"{success}School ID: {school_id}")
    time.sleep(0.8)
    print(f"{success}Dripfeed: {data.get('dripfeed', 'N/A')}")
    time.sleep(0.8)
    print(f"{success}Last Active: {data.get('lastActive', 'N/A')}")
    time.sleep(0.8)
    print(f"{success}Class ID: {data.get('classID', 'N/A')}")
    time.sleep(0.8)
    print(f"{success}Total Points: {data.get('points', 'N/A')}")
    time.sleep(0.8)
    print(f"{success}Points (This Week): {data.get('pointsWeek', 'N/A')}")
    time.sleep(0.8)
    total_time = data.get('timeweek', 'N/A') / 60
    print(f"{success}Total Time (This Week): {total_time} minutes")
    time.sleep(0.8)
    print(f"{success}Username: {data.get('username', 'N/A')}")
    time.sleep(0.8)
    current_lesson_number = -1
    current_lesson_name = ""
    pattern = re.compile(r'Lesson (\d+)$')
    for block in data.get('blocks', []):
        for topic in block.get('topics', []):
            for lesson in topic.get('lessons', []):
                if lesson.get("finish") is not None:
                    lesson_name = lesson.get('name', "")
                    match = pattern.match(lesson_name)
                    if match:
                        try:
                            lesson_number = int(match.group(1))
                            if lesson_number > current_lesson_number:
                                current_lesson_number = lesson_number
                                current_lesson_name = lesson_name
                        except ValueError:
                            continue
    print(f"{success}Completed Lessons: {current_lesson_name}")
    time.sleep(0.8)
    input("Press enter to continue...")
    clear()

async def options(full_name):
    print(f"{error}Sorry {full_name}, this feature is not fully out yet.")
        
    
    
    


async def main():
    data = await check_token()
    full_name = data.get('firstname') + " " + data.get('lastname')
    if data:
        await get_assignments(data)
        await options(full_name)

if __name__ == "__main__":
    asyncio.run(main())
