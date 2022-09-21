'''

            ISO - In Side Out
            
        created by CookiesKush420
           github.com/Callumgm
       
       
    This a highly sophisticated backdoor that can be
    used to gain access to a target machine and execute terminal commands.
    
    CREATED FOR EDUCATIONAL PURPOSES ONLY.
     
'''

import os

from asciimatics.exceptions import ResizeScreenError
from asciimatics.renderers import ImageFile
from asciimatics.screen import Screen
from asciimatics.effects import Print
from asciimatics.scene import Scene

temp = os.getenv('temp')

def globe(screen):
		effects = [
			Print(screen, ImageFile(f"{temp}\\globe.gif", screen.height - 2, colours=screen.colours),
				0,
				speed=1),
		]
		screen.play([Scene(effects, duration=25)], stop_on_resize=True, repeat=False)

def download_gif():
    # Download Globe.gif ready for animation 
    try:
        os.system(f"curl -s https://cdn.discordapp.com/attachments/997264320398364742/997274724373631046/globe.gif -o {temp}\\globe.gif")
        Screen.wrapper(globe)
    except ResizeScreenError: pass

