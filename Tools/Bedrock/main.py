import json
import os
import time
import asyncio
import threading
import webbrowser
import sys
from mitmproxy import http, options
from mitmproxy.tools.dump import DumpMaster
import random
import atexit
import winreg
import jsonschema

def clear():
    os.system("cls" if os.name == "nt" else "clear")


DEFAULT_SETTINGS = {
    "proxy_config": {
        "ip": "127.0.0.1",
        "port": 8192
    },
    "mitmproxy_config": {
        "windows_cert": "http://mitm.it/cert/p12",
        "linux_cert": "http://mitm.it/cert/pem",
        "mac_cert": "http://mitm.it/cert/pem",
        "ios_cert": "http://mitm.it/cert/pem",
        "android_cert": "http://mitm.it/cert/cer"
    },
    "tools": {
        "bedrock": {
            "time_spent": 0,
            "points": 0,
            "lessons_complete": False,
            "auto_answer": False,
            "drip_feed": 2,
            "bedrock_login": "https://app.bedrocklearning.org/"
        },
        "sparxMaths": {
            "sparx_login": "https://www.sparx.co.uk/login"
        },
        "blooket": {
            "blooks": ["Old Boot", "Jellyfish", "Clownfish", "Frog", "Crab", "Pufferfish", "Blobfish", "Octopus", "Narwhal", "Dolphin", "Baby Shark", "Megalodon", "Snowy Owl", "Polar Bear", "Arctic Fox", "Baby Penguin", "Penguin", "Arctic Hare", "Seal", "Walrus", "Snow Globe", "Holiday Gift", "Hot Chocolate", "Holiday Wreath", "Stocking", "Gingerbread Man", "Gingerbread House", "Reindeer", "Snowman", "Santa Claus", "Lil Bot", "Lovely Bot", "Angry Bot", "Happy Bot", "Watson", "Buddy Bot", "Brainy Bot", "Mega Bot", "Toast", "Cereal", "Yogurt", "Breakfast Combo", "Orange Juice", "Milk", "Waffle", "Pancakes", "French Toast", "Pizza", "Light Blue", "Black", "Red", "Purple", "Pink", "Orange", "Lime", "Green", "Teal", "Tan", "Maroon", "Gray", "Mint", "Salmon", "Burgandy", "Baby Blue", "Dust", "Brown", "Dull Blue", "Yellow", "Blue", "Amber", "Dino Egg", "Dino Fossil", "Stegosaurus", "Velociraptor", "Brontosaurus", "Triceratops", "Tyrannosaurus Rex", "Chick", "Chicken", "Cow", "Goat", "Horse", "Pig", "Sheep", "Duck", "Alpaca", "Bear", "Moose", "Fox", "Raccoon", "Squirrel", "Owl", "Hedgehog", "Deer", "Wolf", "Beaver", "Rainbow Jellyfish", "Blizzard Clownfish", "Lovely Frog", "Lucky Frog", "Spring Frog", "Poison Dart Frog", "Lucky Hamster", "Chocolate Rabbit", "Lemon Crab", "Pirate Pufferfish", "Donut Blobfish", "Crimson Octopus", "Rainbow Narwhal", "Frost Wreath", "Tropical Globe", "New York Snow Globe", "London Snow Globe", "Japan Snow Globe", "Egypt Snow Globe", "Paris Snow Globe", "Red Sweater Snowman", "Blue Sweater Snowman", "Elf Sweater Snowman", "Santa Claws", "Cookies Combo", "Chilly Flamingo", "Snowy Bush Monster", "Nutcracker Koala", "Sandwich", "Ice Slime", "Frozen Fossil", "Ice Crab", "Rainbow Panda", "White Peacock", "Tiger Zebra", "Teal Platypus", "Red Astronaut", "Orange Astronaut", "Yellow Astronaut", "Lime Astronaut", "Green Astronaut", "Cyan Astronaut", "Blue Astronaut", "Pink Astronaut", "Purple Astronaut", "Brown Astronaut", "Black Astronaut", "Lovely Planet", "Lovely Peacock", "Haunted Pumpkin", "Pumpkin Cookie", "Ghost Cookie", "Red Gummy Bear", "Blue Gummy Bear", "Green Gummy Bear", "Chick Chicken", "Chicken Chick", "Raccoon Bandit", "Owl Sheriff", "Vampire Frog", "Pumpkin King", "Anaconda Wizard", "Spooky Pumpkin", "Spooky Mummy", "Agent Owl", "Master Elf", "Party Pig", "Wise Owl", "Spooky Ghost", "Phantom King", "Tim the Alien", "Rainbow Astronaut", "Hamsta Claus", "Ice Bat", "Ice Bug", "Ice Elemental", "Rock Monster", "Dink", "Donk", "Bush Monster", "Yeti", "Witch", "Wizard", "Elf", "Fairy", "Slime Monster", "Jester", "Dragon", "Queen", "Unicorn", "King", "Dingo", "Echidna", "Koala", "Kookaburra", "Platypus", "Joey", "Kangaroo", "Crocodile", "Sugar Glider", "Dog", "Cat", "Rabbit", "Goldfish", "Hamster", "Turtle", "Kitten", "Puppy", "Panda", "Sloth", "Tenrec", "Flamingo", "Zebra", "Elephant", "Lemur", "Peacock", "Chameleon", "Lion", "Earth", "Meteor", "Stars", "Alien", "Planet", "UFO", "Spaceship", "Astronaut", "Pumpkin", "Swamp Monster", "Frankenstein", "Vampire", "Zombie", "Mummy", "Caramel Apple", "Candy Corn", "Werewolf", "Ghost", "Tiger", "Orangutan", "Cockatoo", "Parrot", "Anaconda", "Jaguar", "Macaw", "Toucan", "Panther", "Capuchin", "Gorilla", "Hippo", "Rhino", "Giraffe", "Two of Spades", "Eat Me", "Drink Me", "Alice", "Queen of Hearts", "Dormouse", "White Rabbit", "Cheshire Cat", "Caterpillar", "Mad Hatter", "King of Hearts", "Deckhand", "Buccaneer", "Swashbuckler", "Treasure Map", "Seagull", "Jolly Pirate", "Pirate Ship", "Kraken", "Captain Blackbeard"],
            "custom_blooks": ["1#0#1#0#1$3#0#0#1#6#0#0$0"],
            "unlock_all": False,
            "blooket_link": "https://www.blooket.com/"
        }
    }
}

def load_config(filename='settings.json'):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading config from {filename}: {str(e)}\nUsing DEFAULT_SETTINGS instead.")
        return DEFAULT_SETTINGS


def bedrock_details(config):
    if not config:
        return 0, 0, False, False, 0, ""
    bedrock = config.get('tools', {}).get('bedrock', {})
    return (
        bedrock.get('time_spent', 0),
        bedrock.get('points', 0),
        bedrock.get('lessons_complete', False),
        bedrock.get('auto_answer', False),
        bedrock.get('drip_feed', 0),
        bedrock.get('bedrock_login', "https://app.bedrocklearning.org/")
    )


def proxy_details(config):
    if not config:
        return "127.0.0.1", 8080
    proxy = config.get('proxy_config', {})
    return (
        proxy.get('ip', '127.0.0.1'),
        proxy.get('port', 8080)
    )

def blooket_details(config):
    if not config:
        return [], []
    blooket = config.get('tools', {}).get('blooket', {})
    return (
        blooket.get('blooks', []),
        blooket.get('custom_blooks', []),
        blooket.get('unlock_all', False),
        blooket.get('blooket_link', "https://www.blooket.com/")
    )

def sparx_details(config):
    if not config:
        return "https://www.sparx.co.uk/login"
    sparx = config.get('tools', {}).get('sparxMaths', {})
    return (
        sparx.get('sparx_login', "https://www.sparx.co.uk/login")
    )

def cert_details(config):
    if not config:
        return "http://mitm.it/cert/p12"
    mitmproxy = config.get('mitmproxy_config', {})
    windows_cert = mitmproxy.get('windows_cert', "http://mitm.it/cert/p12")
    linux_cert = mitmproxy.get('linux_cert', "http://mitm.it/cert/pem")
    mac_cert = mitmproxy.get('mac_cert', "http://mitm.it/cert/pem")
    ios_cert = mitmproxy.get('ios_cert', "http://mitm.it/cert/pem")
    android_cert = mitmproxy.get('android_cert', "http://mitm.it/cert/cer")
    return (
        windows_cert,
        linux_cert,
        mac_cert,
        ios_cert,
        android_cert
    )


def set_proxy(ip, port):
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                         r"Software\Microsoft\Windows\CurrentVersion\Internet Settings",
                         0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(key, "ProxyEnable", 0, winreg.REG_DWORD, 1)
    winreg.SetValueEx(key, "ProxyServer", 0, winreg.REG_SZ, f"{ip}:{port}")
    winreg.CloseKey(key)


def disable_proxy():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                         r"Software\Microsoft\Windows\CurrentVersion\Internet Settings",
                         0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(key, "ProxyEnable", 0, winreg.REG_DWORD, 0)
    winreg.CloseKey(key)


atexit.register(disable_proxy)


class Bedrock:
    def __init__(self, config_file='settings.json'):
        config_file = os.path.join(os.path.dirname(__file__), config_file)
        self.config = load_config(config_file)
        if not self.config:
            print("Failed to load configuration.")
            exit(1)

        (
            self.time_spent,
            self.points,
            self.lessons_complete,
            self.auto_answer,
            self.drip_feed,
            self.bedrock_login,
        ) = bedrock_details(self.config)

        self.proxy_ip, self.proxy_port = proxy_details(self.config)

        print(f"Loaded configuration: {self.config}")

    def clear(self):
        os.system("cls" if os.name == "nt" else "clear")

    def enable_proxy(self):
        set_proxy(self.proxy_ip, self.proxy_port)

    def disable_proxy(self):
        disable_proxy()

    def print_header(self):
        print("""
███████╗████████╗ █████╗ ██████╗     ██████╗ ███████╗██████╗ ██████╗  ██████╗  ██████╗██╗  ██╗
██╔════╝╚══██╔══╝██╔══██╗██╔══██╗    ██╔══██╗██╔════╝██╔══██╗██╔══██╗██╔═══██╗██╔════╝██║ ██╔╝
███████╗   ██║   ███████║██████╔╝    ██████╔╝█████╗  ██║  ██║██████╔╝██║   ██║██║     █████╔╝ 
╚════██║   ██║   ██╔══██║██╔══██╗    ██╔══██╗██╔══╝  ██║  ██║██╔══██╗██║   ██║██║     ██╔═██╗ 
███████║   ██║   ██║  ██║██║  ██║    ██████╔╝███████╗██████╔╝██║  ██║╚██████╔╝╚██████╗██║  ██╗
╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝    ╚═════╝ ╚══════╝╚═════╝ ╚═╝  ╚═╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝
        """)
        print()

    def print_menu(self):
        print("[0] Edit Time Spent")
        print("[1] Edit Points")
        print("[2] Complete Lessons Toggle")
        print("[3] Auto Answer Toggle")
        print("[4] Edit Dripfeed")
        print("[5] Start Proxy")
        print("[6] Exit\n")

    def request(self, flow: http.HTTPFlow):
        if any(flow.request.pretty_url.endswith(ext) for ext in ['.png', '.jpg', '.jpeg']):
            return

    def response(self, flow: http.HTTPFlow):
        url = flow.request.pretty_url
        try:
            if "api.bedrocklearning.org/api/students" in url and "dashboard" in url:
                data = json.loads(flow.response.content.decode("utf-8"))
                data["firstname"] = f"{data.get('firstname', '')} (Star)"
                data["points"] = self.points
                data["pointsWeek"] = self.points
                data["time"] = self.time_spent
                data["timeweek"] = self.time_spent
                flow.response.content = json.dumps(data).encode("utf-8")
        except:
            pass

        try:
            if "api.bedrocklearning.org" in url and "dashboard" in url and self.lessons_complete:
                data = json.loads(flow.response.content.decode("utf-8"))
                for block in data.get("blocks", []):
                    for lesson in block.get("topics", []):
                        lesson["progress"] = None
                        lesson["start"] = "2025-05-11T12:12:50.077"
                        lesson["finish"] = "2025-05-11T12:15:25.67"
                        lesson["score"] = 100.0
                        lesson["score2"] = 100.0
                        lesson["points"] = 0
                flow.response.content = json.dumps(data).encode("utf-8")
        except:
            pass

        try:
            if "api.bedrocklearning.org/api/notifications/" in url:
                flow.response.content = json.dumps({"count": 999, "unread": 999, "items": []}).encode("utf-8")
        except:
            pass

        try:
            if "https://api.bedrocklearning.org/api/learningcontent" in url and \
               "/submit" in url and flow.request.method == "POST" and self.auto_answer:
                data = json.loads(flow.response.content.decode("utf-8"))
                new_data = {
                    "success": True,
                    "tryagain": False,
                    "audio": data.get("audio"),
                    "message": f"{"Auto Answered by Star!" if data.get('message') == "Sorry, that is incorrect." else data.get('message')}",
                    "image": data.get("image"),
                    "studentResponse": data.get("studentResponse"),
                    "correctResponse": data.get("correctResponse"),
                    "hideFeedback": False,
                    "lessonFinished": data.get("lessonFinished"),
                    "endWithResults": False,
                    "stage": data.get("stage"),
                    "topicFeedback": data,
                    "oneOffActivity": data.get("oneOffActivity"),
                }
                flow.response.content = json.dumps(new_data).encode("utf-8")
        except:
            pass

        try:
            if ("https://api.bedrocklearning.org/api/students" in url and "dashboard" in url) or \
               ("https://api.bedrocklearning.org/api/school" in url and "name" in url):
                data = json.loads(flow.response.content.decode("utf-8"))
                data["dripfeed"] = self.drip_feed
                data["dripfeedDays"] = self.drip_feed
                flow.response.content = json.dumps(data).encode("utf-8")
        except:
            pass

        if "https://api.bedrocklearning.org/api/students" in flow.request.pretty_url and "history" in flow.request.pretty_url and flow.request.method == "GET":
            try:
                response_text = flow.response.text.decode('utf-8')
                data = json.loads(response_text)

                result = data['result']

                for r in result:
                    r['score'] = 100.0
                    r['start'] = "2017-04-20T12:12:50.077"
                    r['finish'] = "2017-04-20T12:15:25.670"

                for i in range(100):
                    new_result = {
                        "learningType": "LESSON",
                        "start": "2017-04-20T12:12:50.077",
                        "finish": "2017-04-20T12:15:25.670",
                        "score": 100.0,
                        "blockName": "Block 69",
                        "topicName": f"B 69 T {i + 1}: Auto Complete by Star",
                        "learningName": f"Lesson {i + 1}"
                    }
                    result.append(new_result)

                data['totalCount'] = len(result)
                data['totalPages'] = (len(result) + 19) // 20 

                flow.response.text = json.dumps(data, indent=4).encode('utf-8')

            except Exception as e:
                print("Error modifying Bedrock data:", e)


    async def run_proxy(self):
        opts = options.Options(listen_host=self.proxy_ip,
                            listen_port=self.proxy_port,
                            ssl_insecure=True)
        master = DumpMaster(opts, with_termlog=False, with_dumper=False)
        master.addons.add(BedrockAddon(self))  
        await master.run()

    def start_proxy(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(self.run_proxy())
        except KeyboardInterrupt:
            pass
        finally:
            loop.close()

    def menu(self):
        while True:
            self.clear()
            self.print_header()
            print(f" Current Values:\n"
                  f"   → Time Spent        : {self.time_spent}\n"
                  f"   → Points            : {self.points}\n"
                  f"   → Complete Lessons : {'Enabled' if self.lessons_complete else 'Disabled'}\n"
                  f"   → Auto Answer      : {'Enabled' if self.auto_answer else 'Disabled'}\n"
                  f"   → Dripfeed         : {self.drip_feed}\n")
            self.print_menu()
            try:
                choice = int(input(" Enter your choice: ").strip())
                if choice == 0:
                    self.time_spent = int(input("  Set Time Spent: ").strip())
                elif choice == 1:
                    self.points = int(input("  Set Points: ").strip())
                elif choice == 2:
                    self.lessons_complete = not self.lessons_complete
                elif choice == 3:
                    self.auto_answer = not self.auto_answer
                elif choice == 4:
                    self.drip_feed = int(input("  Set Dripfeed: ").strip())
                elif choice == 5:
                    self.clear()
                    break
                elif choice == 6:
                    print("\nExiting...\n")
                    time.sleep(1)
                    exit()
            except:
                print("\nInvalid input. Try again.")
                time.sleep(1.5)

    def run(self):
        self.menu()
        self.enable_proxy()
        self.print_header()
        print(f" Proxy is now active on {self.proxy_ip}:{self.proxy_port}.")
        print(" Press Ctrl+C to stop.\n")
        webbrowser.open(self.bedrock_login)

        proxy_thread = threading.Thread(target=self.start_proxy, daemon=True)
        proxy_thread.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nShutting down proxy...")
            disable_proxy()

class SparxMaths:
    def __init__(self, config_file='settings.json'):
        config_file = os.path.join(os.path.dirname(__file__), config_file)
        self.config = load_config(config_file)
        if not self.config:
            print("Failed to load configuration.")
            exit(1)

        (
            self.sparx_login
        ) = sparx_details(self.config)

        self.proxy_ip, self.proxy_port = proxy_details(self.config)

        print(f"Loaded configuration: {self.config}")

    def clear(self):
        os.system("cls" if os.name == "nt" else "clear")

    def enable_proxy(self):
        set_proxy(self.proxy_ip, self.proxy_port)

    def disable_proxy(self):
        disable_proxy()

    def print_header(self):
        print("""███████╗████████╗ █████╗ ██████╗     ███████╗██████╗  █████╗ ██████╗ ██╗  ██╗
██╔════╝╚══██╔══╝██╔══██╗██╔══██╗    ██╔════╝██╔══██╗██╔══██╗██╔══██╗╚██╗██╔╝
███████╗   ██║   ███████║██████╔╝    ███████╗██████╔╝███████║██████╔╝ ╚███╔╝ 
╚════██║   ██║   ██╔══██║██╔══██╗    ╚════██║██╔═══╝ ██╔══██║██╔══██╗ ██╔██╗ 
███████║   ██║   ██║  ██║██║  ██║    ███████║██║     ██║  ██║██║  ██║██╔╝ ██╗
╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝    ╚══════╝╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝
                                                                            """)
        print()

    def print_menu(self):
        print("""This tool is not here yet as the Sparx server is encrypted and looks like: 
              ....4
$7a66c3d8-1e14-439f-9113-4104898da875...\xfd\x92\xec\xc2..̭\xdb\xe6.\x80....grpc-status: 0
              So if any of you know how to decrypt it, please let me know.""")

    def request(self, flow: http.HTTPFlow):
        pass

    async def run_proxy(self):
        opts = options.Options(listen_host=self.proxy_ip,
                            listen_port=self.proxy_port,
                            ssl_insecure=True)

        master = DumpMaster(opts, with_termlog=False, with_dumper=False)
        master.addons.add(SparxAddon(self))  
        await master.run()

    def start_proxy(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(self.run_proxy())
        except KeyboardInterrupt:
            pass
        finally:
            loop.close()

    def menu(self):
        while True:
            self.clear()
            self.print_header()
            print("To be made.")
            self.print_menu()
            try:
                choice = int(input(" Enter your choice: ").strip())
                if choice == 0:
                    self.time_spent = int(input("  Set Time Spent: ").strip())
                elif choice == 1:
                    self.points = int(input("  Set Points: ").strip())
                elif choice == 2:
                    self.lessons_complete = not self.lessons_complete
                elif choice == 3:
                    self.auto_answer = not self.auto_answer
                elif choice == 4:
                    self.drip_feed = int(input("  Set Dripfeed: ").strip())
                elif choice == 5:
                    self.clear()
                    break
                elif choice == 6:
                    print("\nExiting...\n")
                    time.sleep(1)
                    exit()
            except:
                print("\nInvalid input. Try again.")
                time.sleep(1.5)

    def run(self):
        self.menu()
        self.enable_proxy()
        self.print_header()
        print(f" Proxy is now active on {self.proxy_ip}:{self.proxy_port}.")
        print(" Press Ctrl+C to stop.\n")
        webbrowser.open(self)

        proxy_thread = threading.Thread(target=self.start_proxy, daemon=True)
        proxy_thread.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nShutting down proxy...")
            disable_proxy()

class Blooket:
    def __init__(self, config_file='settings.json'):
        config_file = os.path.join(os.path.dirname(__file__), config_file)
        self.config = load_config(config_file)
        if not self.config:
            print("Failed to load configuration.")
            exit(1)

        (
            self.blooks,
            self.custom_blooks,
            self.unlock_all,
            self.blooket_link
        ) = blooket_details(self.config)

        self.proxy_ip, self.proxy_port = proxy_details(self.config)

        print(f"Loaded configuration: {self.config}")

    def clear(self):
        os.system("cls" if os.name == "nt" else "clear")

    def enable_proxy(self):
        set_proxy(self.proxy_ip, self.proxy_port)

    def disable_proxy(self):
        disable_proxy()

    def print_header(self):
        print("""███████╗████████╗ █████╗ ██████╗     ██████╗ ██╗      ██████╗  ██████╗ ██╗  ██╗███████╗████████╗
██╔════╝╚══██╔══╝██╔══██╗██╔══██╗    ██╔══██╗██║     ██╔═══██╗██╔═══██╗██║ ██╔╝██╔════╝╚══██╔══╝
███████╗   ██║   ███████║██████╔╝    ██████╔╝██║     ██║   ██║██║   ██║█████╔╝ █████╗     ██║   
╚════██║   ██║   ██╔══██║██╔══██╗    ██╔══██╗██║     ██║   ██║██║   ██║██╔═██╗ ██╔══╝     ██║   
███████║   ██║   ██║  ██║██║  ██║    ██████╔╝███████╗╚██████╔╝╚██████╔╝██║  ██╗███████╗   ██║   
╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝    ╚═════╝ ╚══════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚══════╝   ╚═╝""")
        print()

    def print_menu(self):
        print("[0] Unlock All Blooks")
        print("[1] Start Proxy")
        print("[2] Exit")

    def request(self, flow: http.HTTPFlow):
        if "blooket.com/api/users/unlocks" in flow.request.pretty_url:
            try:
                data = json.loads(flow.response.content)

                data["unlocks"] = self.blooks

                data["customBlooks"] = self.custom_blooks

                flow.response.text = json.dumps(data)
            except Exception as e:
                print("[ERROR] Failed to patch blooks:", e)

    async def run_proxy(self):
        opts = options.Options(listen_host=self.proxy_ip,
                            listen_port=self.proxy_port,
                            ssl_insecure=True)

        master = DumpMaster(opts, with_termlog=False, with_dumper=False)
        master.addons.add(BlooketAddon(self)) 
        await master.run()

    def start_proxy(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(self.run_proxy())
        except KeyboardInterrupt:
            pass
        finally:
            loop.close()

    def menu(self):
        while True:
            self.clear()
            self.print_header()
            print(f" Current Values:\n"
                  f"   → Unlock All        : {'Enabled' if self.unlock_all else 'Disabled'}\n"
                  f"   → Custom Blooks            : {len(self.custom_blooks)}\n"
            )
            self.print_menu()
            try:
                choice = int(input(" Enter your choice: ").strip())
                if choice == 0:
                    if self.unlock_all:
                        self.unlock_all = False
                    else:
                        self.unlock_all = True
                elif choice == 1:
                    self.clear()
                    break
                elif choice == 2:
                    print("\nExiting...\n")
                    time.sleep(1)
                    exit()
            except:
                print("\nInvalid input. Try again.")
                time.sleep(1.5)

    def run(self):
        self.menu()
        self.enable_proxy()
        self.print_header()
        print(f" Proxy is now active on {self.proxy_ip}:{self.proxy_port}.")
        print(" Press Ctrl+C to stop.\n")
        webbrowser.open(self.blooket_link)

        proxy_thread = threading.Thread(target=self.start_proxy, daemon=True)
        proxy_thread.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nShutting down proxy...")
            disable_proxy()


class Certificates:
    def __init__(self, config_file='settings.json'):
        config_file = os.path.join(os.path.dirname(__file__), config_file)
        self.config = load_config(config_file)
        if not self.config:
            print("Failed to load configuration.")
            exit(1)

        self.windows_cert = "http://mitm.it/cert/p12"

        self.proxy_ip, self.proxy_port = proxy_details(self.config)

    def enable_proxy(self):
        set_proxy(self.proxy_ip, self.proxy_port)

    def disable_proxy(self):
        disable_proxy()

    def clear(self):
        os.system("cls" if os.name == "nt" else "clear")

    async def run_proxy(self):
        opts = options.Options(
            listen_host=self.proxy_ip,
            listen_port=self.proxy_port,
            ssl_insecure=True
        )
        self.master = DumpMaster(opts, with_termlog=False, with_dumper=False)
        self.master.addons.add(CertificatesAddon(self))
        await self.master.run()

    def start_proxy(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(self.run_proxy())
        except KeyboardInterrupt:
            pass
        finally:
            loop.close()

    def print_header(self):
        print("""███████╗████████╗ █████╗ ██████╗      ██████╗███████╗██████╗ ████████╗███████╗
██╔════╝╚══██╔══╝██╔══██╗██╔══██╗    ██╔════╝██╔════╝██╔══██╗╚══██╔══╝██╔════╝
███████╗   ██║   ███████║██████╔╝    ██║     █████╗  ██████╔╝   ██║   ███████╗
╚════██║   ██║   ██╔══██║██╔══██╗    ██║     ██╔══╝  ██╔══██╗   ██║   ╚════██║
███████║   ██║   ██║  ██║██║  ██║    ╚██████╗███████╗██║  ██║   ██║   ███████║
╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝     ╚═════╝╚══════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝
                                                                              """)
        print()

    def print_menu(self):
        print("[0] Install Windows Certificate")
        print("[1] Exit\n")

    def menu(self):
        while True:
            self.clear()
            self.print_header()
            self.print_menu()
            try:
                choice = int(input(" Enter your choice: ").strip())
                if choice == 0:
                    self.clear()
                    break
                elif choice == 1:
                    print("\nExiting...\n")
                    time.sleep(1)
                    exit()
                else:
                    print("\nInvalid input. Try again.")
                    time.sleep(1.5)
            except ValueError:
                print("\nInvalid input. Try again.")
                time.sleep(1.5)
        try:
            proxy_thread = threading.Thread(target=self.start_proxy, daemon=True)
            proxy_thread.start()

            time.sleep(2)

            webbrowser.open("http://mitm.it/cert/p12")
            print(f"Certificate installation link opened in your browser: http://mitm.it/cert/p12")

        except Exception as e:
            print(f"Failed to open certificate link: {str(e)}")

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nShutting down proxy...")
            self.disable_proxy()


    def run(self):
        self.menu()


class BedrockAddon:

    def __init__(self, bedrock):
        self.bedrock = bedrock

    def request(self, flow):
        self.bedrock.request(flow)

    def response(self, flow):
        self.bedrock.response(flow)

class SparxAddon:

    def __init__(self, sparxmaths):
        self.sparx = sparxmaths

    def request(self, flow):
        self.sparx.request(flow)

    def response(self, flow):
        self.sparx.response(flow)

class BlooketAddon:

    def __init__(self, blooket):
        self.blooket = blooket

    def request(self, flow):
        self.blooket.request(flow)

    def response(self, flow):
        self.blooket.response(flow)

class CertificatesAddon:

    def __init__(self, certificates):
        self.certificates = certificates

    def request(self, flow):
        self.certificates.request(flow)

    def response(self, flow):
        self.certificates.response(flow)


def main():
    while True:
        clear()
        print("""███████╗████████╗ █████╗ ██████╗     ████████╗ ██████╗  ██████╗ ██╗     ███████╗
██╔════╝╚══██╔══╝██╔══██╗██╔══██╗    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝
███████╗   ██║   ███████║██████╔╝       ██║   ██║   ██║██║   ██║██║     ███████╗
╚════██║   ██║   ██╔══██║██╔══██╗       ██║   ██║   ██║██║   ██║██║     ╚════██║
███████║   ██║   ██║  ██║██║  ██║       ██║   ╚██████╔╝╚██████╔╝███████╗███████║
╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝       ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝
                                                                               """)
        print("[1] Bedrock Tool")
        print("[2] Sparx Maths Tool")
        print("[3] Blooket Tool")
        print("[4] Install Certificates")
        print("[5] Exit\n")
        choice = input("Select an option: ").strip()
        
        if choice == "1":
            Bedrock().run()
        elif choice == "2":
            SparxMaths().run()
        elif choice == "3":
            Blooket().run()
        elif choice == "4":
            Certificates().run()
        elif choice == "5":
            print("\nExiting...\n")
            time.sleep(1)
            exit()

if __name__ == "__main__":
    main()