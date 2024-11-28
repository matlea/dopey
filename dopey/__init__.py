__author__ = "Mats Leandersson"
__version__ = "2024.11.28"


print(f"{__name__}, {__author__}")


from colorama import Fore
#print(Fore.LIGHTBLACK_EX + "Still translating grumpy into dopey so there might be some bugs or unfinished methods...\n" + Fore.RESET)

try: from dopey.dopey_constants import *
except Exception as E1: 
    print(Fore.RED + "dopey: issue(s) with importing dopey_constants.py")
    print(E1, Fore.RESET)

try: from dopey.dopey_loader import *
except Exception as E1: 
    print(Fore.RED + "dopey: issue(s) with importing dopey_loader.py")
    print(E1, Fore.RESET)

try: from dopey.dopey_plot import *
except Exception as E1: 
    print(Fore.RED + "dopey: issue(s) with importing dopey_plot.py")
    print(E1, Fore.RESET)

try: from dopey.dopey_methods import *
except Exception as E1: 
    print(Fore.RED + "dopey: issue(s) with importing dopey_methods.py")
    print(E1, Fore.RESET)

try: from dopey.dopey_spin import *
except Exception as E1: 
    print(Fore.RED + "dopey: issue(s) with importing dopey_spin.py")
    print(E1, Fore.RESET)

try: from dopey.dopey_export2txt import *
except Exception as E1: 
    print(Fore.RED + "dopey: issue(s) with importing dopey_export2txt.py")
    print(E1, Fore.RESET)

#try: from dopey.dopey_fit import *
#except Exception as E1: 
#    print(Fore.RED + "dopey: issue(s) with importing dopey_fit.py")
#    print(E1, Fore.RESET)

try: from dopey.dopey_dichroism import *
except Exception as E1: 
    print(Fore.RED + "dopey: issue(s) with importing dopey_dichroism.py")
    print(E1, Fore.RESET)

#
print()
#try:
#    with open("dopey/dopey_help.txt", "r") as f:
#        for row in f: print(row.strip("\n"))
#except:
#    pass



