import json, os, time, asyncio, threading, winreg, atexit
from mitmproxy import http, options
from mitmproxy.tools.dump import DumpMaster

time_spent = 0
points = 0
lesson = 0

def set_proxy():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                         r"Software\Microsoft\Windows\CurrentVersion\Internet Settings",
                         0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(key, "ProxyEnable", 0, winreg.REG_DWORD, 1)
    winreg.SetValueEx(key, "ProxyServer", 0, winreg.REG_SZ, "127.0.0.1:8082")
    winreg.CloseKey(key)

def disable_proxy():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                         r"Software\Microsoft\Windows\CurrentVersion\Internet Settings",
                         0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(key, "ProxyEnable", 0, winreg.REG_DWORD, 0)
    winreg.CloseKey(key)

atexit.register(disable_proxy)

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def print_header():
    print("=" * 50)
    print("⭐ Star Bedrock Proxy - Customize Your Stats ⭐")
    print("=" * 50)
    print()

def print_menu():
    print("[0] Edit Time")
    print("[1] Edit Points")
    print("[2] Edit Lesson")
    print("[3] Start Proxy")
    print("[4] Exit")
    print()

def request(flow: http.HTTPFlow):
    pass

def response(flow: http.HTTPFlow):
    global time_spent, points, lesson
    url = flow.request.pretty_url

    if "api.bedrocklearning.org/api/students" in url and "dashboard" in url:
        try:
            data = json.loads(flow.response.content.decode("utf-8"))
            data["firstname"] = f"{data.get('firstname', '')} (Star)"
            data["points"] = points
            data["pointsWeek"] = points
            data["time"] = time_spent
            data["timeweek"] = time_spent
            data["lesson"] = lesson
            flow.response.content = json.dumps(data).encode("utf-8")
        except: pass

    if "api.bedrocklearning.org/api/notifications/" in url:
        flow.response.content = json.dumps({
            "count": 999,
            "unread": 999,
            "items": []
        }).encode("utf-8")

class MitmAddon:
    def request(self, flow): request(flow)
    def response(self, flow): response(flow)

async def run_proxy():
    opts = options.Options(listen_host='127.0.0.1', listen_port=8082, ssl_insecure=True)
    master = DumpMaster(opts, with_termlog=False, with_dumper=False)
    master.addons.add(MitmAddon())
    await master.run()

def start_proxy():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try: loop.run_until_complete(run_proxy())
    except KeyboardInterrupt: pass
    finally: loop.close()

def menu():
    global time_spent, points, lesson
    while True:
        clear()
        print_header()
        print(f" Current Values:")
        print(f"   → Time Spent : {time_spent}")
        print(f"   → Points     : {points}")
        print(f"   → Lesson     : {lesson}")
        print()
        print_menu()
        try:
            choice = int(input(" Enter your choice: "))
            print()
            if choice == 0:
                time_spent = int(input("  Set Time Spent: "))
            elif choice == 1:
                points = int(input("  Set Points: "))
            elif choice == 2:
                lesson = int(input("  Set Lesson: "))
            elif choice == 3:
                clear()
                break
            elif choice == 4:
                print("\nExiting...\n")
                time.sleep(1)
                exit()
        except:
            print(" Invalid input. Try again.")
            time.sleep(1.5)

if __name__ == "__main__":
    clear()
    menu()
    set_proxy()
    print_header()
    print(" Proxy is now active on 127.0.0.1:8082.")
    print(" Press Ctrl+C to stop.\n")
    proxy_thread = threading.Thread(target=start_proxy, daemon=True)
    proxy_thread.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down proxy...")
