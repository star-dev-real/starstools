import customtkinter as ctk
import threading, asyncio, winreg, atexit, os, time
from mitmproxy import options
from mitmproxy.tools.dump import DumpMaster
from proxy_module import ProxyModifier

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

proxy_state = {"time": 0, "points": 0, "lesson": 0}
proxy_thread = None

def set_proxy():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                         r"Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings", 0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(key, "ProxyEnable", 0, winreg.REG_DWORD, 1)
    winreg.SetValueEx(key, "ProxyServer", 0, winreg.REG_SZ, "127.0.0.1:8082")
    winreg.CloseKey(key)

def disable_proxy():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                         r"Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings", 0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(key, "ProxyEnable", 0, winreg.REG_DWORD, 0)
    winreg.CloseKey(key)

atexit.register(disable_proxy)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("⭐ Star Bedrock Modifier")
        self.geometry("500x400")
        self.resizable(False, False)

        self.label = ctk.CTkLabel(self, text="Edit Stats Live", font=ctk.CTkFont(size=20, weight="bold"))
        self.label.pack(pady=10)

        self.time_entry = self.make_input("Time Spent:")
        self.points_entry = self.make_input("Points:")
        self.lesson_entry = self.make_input("Lesson:")

        self.start_button = ctk.CTkButton(self, text="Start Proxy", command=self.toggle_proxy)
        self.start_button.pack(pady=15)

        self.status_label = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=14))
        self.status_label.pack(pady=5)

    def make_input(self, label_text):
        frame = ctk.CTkFrame(self)
        frame.pack(pady=5)
        label = ctk.CTkLabel(frame, text=label_text, width=100)
        label.pack(side="left", padx=10)
        entry = ctk.CTkEntry(frame)
        entry.pack(side="right", fill="x", expand=True, padx=10)
        return entry

    def toggle_proxy(self):
        global proxy_thread
        try:
            proxy_state["time"] = int(self.time_entry.get())
            proxy_state["points"] = int(self.points_entry.get())
            proxy_state["lesson"] = int(self.lesson_entry.get())
        except ValueError:
            self.status_label.configure(text="❌ Invalid input!", text_color="red")
            return

        if not proxy_thread:
            proxy_thread = threading.Thread(target=self.run_proxy, daemon=True)
            proxy_thread.start()
            set_proxy()
            self.status_label.configure(text="✅ Proxy Running", text_color="green")
        else:
            self.status_label.configure(text="✔ Updated values (Proxy still running)", text_color="yellow")

    def run_proxy(self):
        opts = options.Options(listen_host="127.0.0.1", listen_port=8082, ssl_insecure=True)
        master = DumpMaster(opts, with_termlog=False, with_dumper=False)
        addon = ProxyModifier(proxy_state)
        master.addons.add(addon)
        asyncio.run(master.run())

if __name__ == "__main__":
    app = App()
    app.mainloop()
