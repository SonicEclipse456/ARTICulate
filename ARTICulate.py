# ARTICulate v0.1
# ------------------
# A small python script for Azahar that 
# automatically connects to Artic Base 
# on your 3DS in one click after you've
# provided the location of Azahar's 
# executable, and your 3DS's IP adress.
# ------------------
# Created by SonicEclipse456


# Libraries needed
import sys
import json
import ctypes
import ipaddress 
import subprocess
import tkinter as tk
from pathlib import Path
from tkinter import filedialog

ctypes.windll.kernel32.SetConsoleTitleW("ARTICulate v0.1")

print(r"""
   ░███    ░█████████  ░██████████░██████  ░██████             ░██               ░██               
  ░██░██   ░██     ░██     ░██      ░██   ░██   ░██            ░██               ░██               
 ░██  ░██  ░██     ░██     ░██      ░██  ░██        ░██    ░██ ░██  ░██████   ░████████  ░███████  
░█████████ ░█████████      ░██      ░██  ░██        ░██    ░██ ░██       ░██     ░██    ░██    ░██ 
░██    ░██ ░██   ░██       ░██      ░██  ░██        ░██    ░██ ░██  ░███████     ░██    ░█████████ 
░██    ░██ ░██    ░██      ░██      ░██   ░██   ░██ ░██   ░███ ░██ ░██   ░██     ░██    ░██        
░██    ░██ ░██     ░██     ░██    ░██████  ░██████   ░█████░██ ░██  ░█████░██     ░████  ░███████  v0.1
-------------------------------------------------------------------------------------------------------
「Created by SonicEclipse456」
""") 

# Check if we already have a "config.json" 
if getattr(sys, "frozen", False):
    # when running as a compiled EXE
        CONFIG_FILE = Path(sys.executable).parent / "config.json"
else:
    # when running as a python script
    CONFIG_FILE = Path(__file__).parent / "config.json"
# If it does exist, set "azahar" and "ip" to the values already saved in the json
if CONFIG_FILE.exists():
    with open(CONFIG_FILE, "r") as file:
        config = json.load(file)

    azahar = config["azahar"]
    ip = config["ip"]

# Otherwise, continue with the setup
else:
    root = tk.Tk()
    root.withdraw()

    # Ask user to select "azahar.exe" (anything else gets rejected)
    while True:
        azahar = filedialog.askopenfilename(
            title = "Select azahar.exe",
            filetypes = [("azahar", "azahar.exe")] 
            )
        print("Please select \"azahar.exe...\"")
        if Path(azahar).name.lower() == "azahar.exe":
            break
        print(f"The executable you selected: {azahar}\n isn't the correct one. Please select azahar.exe and try again!")

    # Ask user to type the console's IPv4 address (usually looks like this: 192.168.1.XXX)
    while True:
        ip = input("Enter the IPv4 address of your 3DS or 2DS console (192.168.1.XXX): ")
        try: 
            ipaddress.IPv4Address(ip)
            break
        except ValueError:
            print(f"\"{ip}\" isn't a valid IPv4 address. Please type the IPv4 address of your 3DS or 2DS and try again!")

    # Save inputs to a "config.json" file, so the user doesn't need to type these inputs again on next launch.
    # (if their 3DS gets a new IPv4 address for some reason, they can delete the json file and start again)
    config = {
        "azahar": azahar,
        "ip": ip
    }

    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file, indent=4)

print(f"2DS/3DS IPv4 address: {ip}\n",
      f"Path to Azahar: {azahar}\n",
      f"(configuration has been saved to {CONFIG_FILE}"
      )

# Launch Azahar
try:
    print("Launching Azahar...")
    subprocess.Popen([
        azahar,
        f"articbase://{ip}"
        ])
    ("Azahar launched successfully, closing ARTICulate...")

    # Does the user want to delete their config file or just close the program?
    while True:
        user_choice = input("Choose what you want to do:\n"
                        "[1] Delete the configuration file\n"
                        "[2] Exit\n"
                        "> "
                        )

        if user_choice == "1":
            confirm = input("Are you sure? [y/n]: ")

            if confirm.lower() == "y":
                CONFIG_FILE.unlink()
                print("Configuration file has been deleted, exiting...")
                raise SystemExit
            else:
                print("Configuration file was NOT deleted, exiting...")
                raise SystemExit

        elif user_choice == "2":
            print("Exiting...")
            raise SystemExit
        else:
            print("Response invalid, type either 1 or 2")

except OSError as e:
    print(f"Failed to launch azahar.exe {e}")