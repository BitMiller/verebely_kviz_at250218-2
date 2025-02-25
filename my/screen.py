
import os

def clrscr():
 os.system("cls" if os.name == "nt" else "clear")

##########

def gotoxy(x, y):
 sys.stdout.write(f"\033[{y};{x}H")
 sys.stdout.flush()

##########

def printxy(s, x, y):
 gotoxy(x+1, y+1)
 print(s)

##########

def dprint(s, debug):
 if debug:
  print("DBG: "+s)

##########
