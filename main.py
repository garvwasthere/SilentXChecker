import requests
import json
import time
import os
import random
import threading
import ctypes
from datetime import datetime
from colorama import Fore, Style, init; init()
from console.utils import set_title
os.system('cls')
class Counter:
    Hit = 0
    Dead = 0
    limited = 0
class Log:
    """
    A class to log messages to the console.
    
    """
    log_file = None 
    @staticmethod
    def set_log_file(filename):
        Log.log_file = open(filename, 'a')

    @staticmethod
    def _log(level, prefix, message):
        timestamp = datetime.fromtimestamp(time.time()).strftime("%H:%M:%S")
        log_message = f"[{Fore.LIGHTBLACK_EX}{timestamp}{Fore.RESET}] {prefix} {message}"
        if Log.log_file:
            Log.log_file.write(log_message + '\n')
            Log.log_file.flush()
        print(log_message)

    @staticmethod
    def Success(message, prefix="(+)", color=Fore.LIGHTGREEN_EX):
        Log._log("SUCCESS", f"{color}{prefix}{Fore.RESET}", message)

    @staticmethod
    def Error(message, prefix="(-)", color=Fore.LIGHTRED_EX):
        Log._log("ERROR", f"{color}{prefix}{Fore.RESET}", message)

    @staticmethod
    def Debug(message, prefix="(*)", color=Fore.LIGHTYELLOW_EX):
        Log._log("DEBUG", f"{color}{prefix}{Fore.RESET}", message)

    @staticmethod
    def Solved(message, prefix="(!)", color=Fore.LIGHTBLUE_EX):
        Log._log("SOLVED", f"{color}{prefix}{Fore.RESET}", message)

    @staticmethod
    def Info(message, prefix="(?)" , color=Fore.LIGHTWHITE_EX):
        Log._log("INFO", f"{color}{prefix}{Fore.RESET}", message)

    @staticmethod
    def Warning(message, prefix="(!)", color=Fore.LIGHTMAGENTA_EX):
        Log._log("WARNING", f"{color}{prefix}{Fore.RESET}", message)

    @staticmethod
    def Ask(tag: str, content: str, color=Fore.BLUE):
        ts = f"{Fore.RESET}{Fore.LIGHTBLACK_EX}{datetime.now().strftime('%H:%M:%S')}{Fore.RESET}"
        return input(Style.BRIGHT + ts + color + f" [{tag}] " + Fore.RESET + content + Fore.RESET)
    
class Checker:

    @staticmethod
    def Check(promo):
        headers = {
            'authority': 'discord.com',
            'method': 'GET',
            'scheme': 'https',
            'Accept': '*/*',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'X-Debug-Options': 'bugReporterEnabled',
            'X-Discord-Locale': 'en-GB',
            'X-Discord-Timezone': 'Asia/Calcutta',
            'Authorization': 'MTE2MjkzMjM5NDI4MjczMzcyMA.GA9BNh.Qf10knMMnYLx_N6lvOpxpS-xc27F4hfwruFMhU',
            'X-Super-Properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLUdCIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEyMC4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTIwLjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjI1NjIzMSwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0='
        }

        data = "country_code=US&with_application=false&with_subscription_plan=true"

        while True:
            response = requests.get(f"https://discord.com/api/v9/entitlements/gift-codes/{promo}?{data}", headers=headers)

            # print(response.text)

            if response.status_code == 200:

                uses = response.json()['uses']

                if uses == 0:
                    Log.Success(f"Valid: {promo}")
                    Counter.Hit +=1
                    set_title(f"Silent X Checker | Promotional Checker | Valid: {Counter.Hit} | RateLimit: {Counter.limited} | Dead: {Counter.Dead}")
                    with open("valid.txt", "a") as f:
                        f.write(f"https://promos.discord.gg/{promo}\n")

                else:
                    Log.Debug(f"Redeemed: {promo}")
                    Counter.Dead +=1
                    set_title(f"Silent X Checker | Promotional Checker | Valid: {Counter.Hit} | RateLimit: {Counter.limited} | Dead: {Counter.Dead}")
                break

            elif "The resource is being rate limited." in response.text:
                retry_after = response.json()['retry_after']
                Counter.limited +=1
                set_title(f"Silent X Checker | Promotional Checker | Valid: {Counter.Hit} | RateLimit: {Counter.limited} | Dead: {Counter.Dead}")
                Log.Warning(f"Rate limited: {promo} | Retrying in {retry_after}ms")
                time.sleep(retry_after)
                continue

            else:
                Log.Error(f"Invalid: {promo}")
                Counter.Dead +=1
                set_title(f"Silent X Checker | Promotional Checker | Valid: {Counter.Hit} | RateLimit: {Counter.limited} | Dead: {Counter.Dead}")
                break


with open("codes.txt", "r") as f:
    codes = f.read().splitlines()
            
for code in codes:
    code = code.split('/')[-1].replace('/', '')
    Checker.Check(code)

os.system('cls')
init()
print(Fore.CYAN+"""
                            ░██████╗██╗██╗░░░░░███████╗███╗░░██╗████████╗  ██╗░░██╗
                            ██╔════╝██║██║░░░░░██╔════╝████╗░██║╚══██╔══╝  ╚██╗██╔╝
                            ╚█████╗░██║██║░░░░░█████╗░░██╔██╗██║░░░██║░░░  ░╚███╔╝░
                            ░╚═══██╗██║██║░░░░░██╔══╝░░██║╚████║░░░██║░░░  ░██╔██╗░
                            ██████╔╝██║███████╗███████╗██║░╚███║░░░██║░░░  ██╔╝╚██╗
                             ╚═════╝░╚═╝╚══════╝╚══════╝╚═╝░░╚══╝░░░╚═╝░░░  ╚═╝░░╚═╝""")
print(Fore.LIGHTYELLOW_EX+"                                          Discord: .gg/mrcloud                 ")
print(Fore.LIGHTYELLOW_EX+"                                          Promotional Checker                 ")
print("")
print(Fore.LIGHTBLUE_EX+f"                                             [RESULTS]                         ")
print("")
print(Fore.GREEN+f"                                               Valid: {Counter.Hit}            ")
print(Fore.RED+f"                                               Dead: {Counter.Dead}            ")
input("")
