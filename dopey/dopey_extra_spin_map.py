"""
This is an extra module for manipulating spinmap data.

Methods:

concatSpinmaps(D1, D2)
    D1 and D2 are two spinmaps, measured with the same settings except for one deflector axis. Returns a new dopey spinmap dict.


"""



__version__ = "24.11.26"
__author__  = "Mats Leandersson"


import numpy as np
from colorama import Fore
from copy import deepcopy
import matplotlib.pyplot as plt
from copy import deepcopy

print(f"{__name__}, {__version__}, beta")
print(Fore.LIGHTBLACK_EX + "Note: This module is intended for merging spin maps with fixed energies, nothing else." + Fore.RESET + "\n")



def concatSpinmaps(D1 = {}, D2 = {}, shup = True, intensity_ratio = 1):
    """
    This method contatenates two spin maps that for instance has been reccorded for deflector range -8 to 1 and for 2 to 8.
    It returns a new dopey dict of type spin_map.

    Arguments:  D1 and D2 are dopey spin_map dicts.

    """
    DD = {}
    #
    try: typ1, typ2 = D1.get("type", ""), D2.get("type", "")
    except: typ1, typ2 = "", ""
    if not typ1 == typ2:
        print(Fore.RED + "concatSpinmaps(): Arguments D1 and D2 must both be dopey spin map dicts." + Fore.RESET); return DD
    if not typ1 == "spin_map":
        print(Fore.RED + "concatSpinmaps(): Arguments D1 and D2 must be dopey spin map dicts." + Fore.RESET); return DD
    #
    energy1, energy2 = D1["x"], D2["x"]
    if not np.array_equal(energy1, energy2):
        print(Fore.RED + "concatSpinmaps(): Arguments D1 and D2 does not have the same energy (axis)." + Fore.RESET); return DD
    
    # ---------- check for what axis we are going to concatenate
    def11, def12 = D1["y"], D2["y"]
    def21, def22 = D1["z"], D2["z"]
    if np.array_equal(def11, def12) and not np.array_equal(def21, def22): conc_ax = "def2"
    elif not np.array_equal(def11, def12) and np.array(def21, def22): conc_ax = "def1"
    else: conc_ax = ""
    if not conc_ax in ["def1", "def2"]:
        print(Fore.RED + "concatSpinmaps(): Arguments D1 and D2 must have one common deflector axis and one that will be concatenated." + Fore.RESET); return DD
    
    # intensity: [polarity][scan][delf][defl][data]

    if conc_ax == "def2": axis1, axis2, axis = np.copy(D1["y"]), np.append(D1["z"], D2["z"]), 0
    else: axis1, axis2, axis = np.append(D1["y"], D2["y"]), np.copy(D1["z"]), 1
    DM, DP = [], []
    for dm1, dm2, dp1, dp2 in zip(D1["intensity"][0], D2["intensity"][0], D1["intensity"][1], D2["intensity"][1]):
        dm, dp = np.append(dm1, dm2, axis = axis), np.append(dp1, dp2, axis = axis)
        DM.append(dm)
        DP.append(dp)
    DM, DP = np.array(DM), np.array(DP)

    DD = deepcopy(D1)
    experiment = DD.get("experiment"); experiment.update({"Spectrum_ID": 999999}); DD.update({"experiment": experiment})
    DD.update({"y": axis1, "z": axis2, "intensity": np.array([DM, DP])})
    
    mean_m, mean_p = np.zeros([len(axis1), len(axis2), 1]), np.zeros([len(axis1), len(axis2), 1])
    for curve in DM: mean_m += curve
    for curve in DP: mean_p += curve
    mean_m, mean_p = mean_m / len(DM), mean_p / len(DP)
    DD.update({"intensity_mean": np.array([mean_m, mean_p])})

    return DD











