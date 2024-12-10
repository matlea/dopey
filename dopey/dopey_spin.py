__version__ = "24.12.05b"
__author__  = "Mats Leandersson"

print(f"{__name__}, {__version__}")


import numpy as np
from colorama import Fore
from copy import deepcopy
import matplotlib.pyplot as plt
from copy import deepcopy

from dopey import CCD_ANALYZERS, SPIN_ANALYZERS, SHERMAN
from dopey.dopey_plot import plot



# ========================================================================================================================
# ========================================================================================================================
# ========================================================================================================================


# ----------------------
def _thisIsSpinData(D = {}):
    """ Quick check to make sure it is spin data. Not a user method."""
    if not type(D) is dict: return False
    if not D.get("experiment", {}).get("Analyzer", "") in SPIN_ANALYZERS: return False
    return True


# ========================================================================================================================
# ========================================================================================================================
# ========================================================================================================================



def quickSpin(D = {}, coil = None, rotator = None, shup = False, hide_plot = False, **kwargs):
    """
    Quick data analysis for spin data. Returns a dict.
    D is a dopey dict from load().
    coil and rotator are optional and integers (1 or 2, and -1 or 1). Needed if the polarization method is used.
    """
    #
    result = {"type": "result", "kind": None}
    #
    try: coil = int(coil)
    except: coil = 0
    try: rotator = int(rotator)
    except: rotator = 0
    if not coil in [1,2]: coil = 0
    if not rotator in [-1,1]: rotator = 0
    result.update({"coil": coil, "rotator": rotator})
    #
    if not _thisIsSpinData(D):
        print(Fore.RED + "quickSpin(): I do not recognize this as being spin data." + Fore.RESET)
        return result
    #

    if D["type"] == "spin_edc":
        result.update({"kind": D["type"]})
        #
        asym = (D["intensity_mean"][1] - D["intensity_mean"][0])/(D["intensity_mean"][1] + D["intensity_mean"][0])
        compp = (D["intensity_mean"][0] + D["intensity_mean"][1]) * (1 + asym) / 2 
        compn = (D["intensity_mean"][0] + D["intensity_mean"][1]) * (1 - asym) / 2 
        #
        result.update({"x": D["x"]})
        labels = {"x": D.get("labels", {}).get("x", np.array([]))}
        result.update({"intensity": D["intensity_mean"]})
        labels.update({"intensity": D.get("labels", {}).get("intensity", "")})
        result.update({"asymmetry": asym})
        labels.update({"asymmetry": "Asymmetry"})
        result.update({"component": np.array([compn, compp])})
        labels.update({"component": D.get("labels", {}).get("intensity", "")})
        result.update({"labels": labels})
        #
        if not hide_plot: plot(D = result, shup = shup, **kwargs)

    
    elif D["type"] == "spin_mdc" and D["experiment"]["Scan_Mode"] == "FixedEnergies":
        result.update({"kind": D["type"]})
        #
        asym = np.array((D["intensity_mean"][1] - D["intensity_mean"][0]) / (D["intensity_mean"][1] + D["intensity_mean"][0]) )
        totint = D["intensity_mean"][0] + D["intensity_mean"][1]
        c1 = (1 + asym) * totint/2 
        c2 = (1 - asym) * totint/2
        #
        result.update({"x": D["y"]})
        labels = {"x": D.get("labels", {}).get("y", np.array([]))}
        result.update({"intensity": D["intensity_mean"]})
        labels.update({"intensity": D.get("labels", {}).get("intensity", "")})
        result.update({"asymmetry": asym})
        labels.update({"asymmetry": "Asymmetry"})
        result.update({"component": np.array([c2, c1])})
        labels.update({"component": D.get("labels", {}).get("intensity", "")})
        result.update({"labels": labels})
        #
        if not hide_plot:
            _ = plot(D = result, shup = shup, **kwargs)
    
    elif D["type"] == "spin_mdc" and D["experiment"]["Scan_Mode"] == "FixedAnalyzerTransmission":
        result.update({"kind": D["type"]})
        #
        asym = (D["intensity_mean"][1] - D["intensity_mean"][0])/(D["intensity_mean"][1] + D["intensity_mean"][0])
        componentp = (D["intensity_mean"][1]  + D["intensity_mean"][0]) * (1 + asym)
        componentm = (D["intensity_mean"][1]  + D["intensity_mean"][0]) * (1 - asym)
        #
        result.update({"x": D["x"]})
        labels = {"x": D.get("labels", {}).get("x", np.array([]))}
        result.update({"y": D["y"]})
        labels.update({"y": D.get("labels", {}).get("y", np.array([]))})
        result.update({"intensity": D["intensity_mean"]})
        labels.update({"intensity": D.get("labels", {}).get("intensity", "")})
        result.update({"asymmetry": asym})
        labels.update({"asymmetry": "Asymmetry"})
        result.update({"component": np.array([componentm, componentp])})
        labels.update({"component": D.get("labels", {}).get("intensity", "")})
        result.update({"labels": labels})
        #
        if not hide_plot:
            _ = plot(D = result, shup = shup, **kwargs)
    
    elif D["type"] == "spin_map" and D["experiment"]["Scan_Mode"] == "FixedEnergies":
        result.update({"kind": D["type"]})
        #
        asym = (D["intensity_mean"][1] - D["intensity_mean"][0])/(D["intensity_mean"][1] + D["intensity_mean"][0])
        componentp = (D["intensity_mean"][1]  + D["intensity_mean"][0]) * (1 + asym)
        componentm = (D["intensity_mean"][1]  + D["intensity_mean"][0]) * (1 - asym)
        #
        result.update({"x": D["y"]})
        labels = {"x": D.get("labels", {}).get("y", np.array([]))}
        result.update({"y": D["z"]})
        labels.update( {"y": D.get("labels", {}).get("z", np.array([]))} )
        result.update({"intensity": D["intensity_mean"]})
        labels.update({"intensity": D.get("labels", {}).get("intensity", "")})
        result.update({"asymmetry": asym})
        labels.update({"asymmetry": "Asymmetry"})
        result.update({"component": np.array([componentm, componentp])})
        labels.update({"component": D.get("labels", {}).get("intensity", "")})
        result.update({"labels": labels})
        #
        if not hide_plot:
            _ = plot(D = result, shup = shup, **kwargs)
    
    else:
        print(Fore.MAGENTA + "quickSpin(): This combination of measurement and scan mode is not accounted for yet. Check back later." + Fore.RESET)
        print(Fore.MAGENTA + f'             (measurement = {D.get("Type", "?")}, and scan mode = {D.get("Experiment",{}).get("Scan_Mode","?")})' + Fore.RESET)

    return result



# ========================================================================================================================
# ========================================================================================================================
# ========================================================================================================================


def despikeSpin(D = {}, N = 3, shup = False, **kwargs):
    """
    Removes all points with intensity larger than mean + N * stdev.
    Pass Nm and/or Np as keyword arguments for using separate factors (for N) for negative and positive polarity.
    """
    if not _thisIsSpinData(D):
        print(Fore.RED + "despikeSpin(): I do not recognize this as being spin data." + Fore.RESET); return
    #
    Nm = kwargs.get("Nm", N)
    Np = kwargs.get("Np", N)
    if not shup:
        print(Fore.BLUE + f"despikeSpin(): Removes all data points that are outside mean + N * stdev. Pass N as an integer/float." + Fore.RESET)
        print(Fore.BLUE + f"               Use different N's for minus and plus polarity by passing Nm and/or Np." + Fore.RESET)
        if Nm == Np:
            print(Fore.BLUE + f"               Now using the same value, N = {N}." + Fore.RESET)
        else: print(Fore.BLUE + f"               Now using Nm = {Nm} for minus polarity and Np = {Np} for plus polarity." + Fore.RESET)
    #
    if D["type"] == "spin_edc":  # -------------- EDC
        if D["experiment"]["Scan_Mode"] in ["FixedAnalyzerTransmission"]:
            newD = deepcopy(D)
            MeanM, MeanP = np.nanmean(D["intensity"][0], axis = 0), np.nanmean(D["intensity"][1], axis = 0)
            StDevM, StDevP = np.std(D["intensity"][0], axis = 0), np.std(D["intensity"][1], axis = 0)
            newIntM, newIntP = D["intensity"][0], D["intensity"][1]
            #
            for i, curve in enumerate(D["intensity"][0]):
                for j, value in enumerate(curve):
                    if value > MeanM[j] + Nm * StDevM[j]: newIntM[i,j] = np.NaN 
                    if value < MeanM[j] - Nm * StDevM[j]: newIntM[i,j] = np.NaN 
            for i, curve in enumerate(D["intensity"][1]):
                for j, value in enumerate(curve):
                    if value > MeanP[j] + Np * StDevP[j]: newIntP[i,j] = np.NaN 
                    if value < MeanP[j] - Np * StDevP[j]: newIntP[i,j] = np.NaN 
            newD.update({"intensity": [newIntM, newIntP]})
            newD.update({"intensity_mean": [np.nanmean(newIntM, axis = 0), np.nanmean(newIntP, axis = 0)]})
            return newD
        else:
            print(Fore.MAGENTA + f'despikeSpin(): I have not looked into spin edc data reccorded in scan mode {D["Experiment"]["Scan_Mode"]} yet...' + Fore.RESET)
            return D
    
    elif D["type"] == "spin_mdc":  # -------------- MDC
        if D["experiment"]["Scan_Mode"] in ["FixedAnalyzerTransmission", "FixedEnergies"]:
            newD = deepcopy(D)
            MeanM, MeanP = np.nanmean(D["intensity"][0], axis = 0), np.nanmean(D["intensity"][1], axis = 0)
            StDevM, StDevP = np.std(D["intensity"][0], axis = 0), np.std(D["intensity"][1], axis = 0)
            newIntM, newIntP = D["intensity"][0], D["intensity"][1]
            for i, map in enumerate(D["intensity"][0]):
                for j, curve in enumerate(map):
                    for k, value in enumerate(curve):
                        if value > MeanM[j][k] + Nm * StDevM[j][k]: newIntM[i,j,k] = np.NaN 
                        if value < MeanM[j][k] - Nm * StDevM[j][k]: newIntM[i,j,k] = np.NaN 
            for i, map in enumerate(D["intensity"][1]):
                for j, curve in enumerate(map):
                    for k, value in enumerate(curve):
                        if value > MeanP[j][k] + Np * StDevP[j][k]: newIntP[i,j,k] = np.NaN 
                        if value < MeanP[j][k] - Np * StDevP[j][k]: newIntP[i,j,k] = np.NaN
            newD.update({"intensity": [newIntM, newIntP]})
            newD.update({"intensity_mean": [np.nanmean(newIntM, axis = 0), np.nanmean(newIntP, axis = 0)]})
            return newD
        #
        else:
            print(Fore.MAGENTA + f'despikeSpin(): I have not looked into spin mdc data reccorded in scan mode {D["Experiment"]["Scan_Mode"]} yet...' + Fore.RESET)
            return D
    
    elif D["type"] == "spin_map":
        if D["experiment"]["Scan_Mode"] == "FixedEnergies":
            newD = deepcopy(D)
            MeanM, MeanP = np.nanmean(D["intensity"][0], axis = 0), np.nanmean(D["intensity"][1], axis = 0)
            StDevM, StDevP = np.std(D["intensity"][0], axis = 0), np.std(D["intensity"][1], axis = 0)
            newIntM, newIntP = D["intensity"][0], D["intensity"][1]
            for i, map in enumerate(D["intensity"][0]):
                for j, curve in enumerate(map):
                    for k, value in enumerate(curve):
                        if value > MeanM[j][k] + Nm * StDevM[j][k]: newIntM[i,j,k] = np.NaN 
                        if value < MeanM[j][k] - Nm * StDevM[j][k]: newIntM[i,j,k] = np.NaN 
            for i, map in enumerate(D["intensity"][1]):
                for j, curve in enumerate(map):
                    for k, value in enumerate(curve):
                        if value > MeanP[j][k] + Np * StDevP[j][k]: newIntP[i,j,k] = np.NaN 
                        if value < MeanP[j][k] - Np * StDevP[j][k]: newIntP[i,j,k] = np.NaN
            newD.update({"intensity": [newIntM, newIntP]})
            newD.update({"intensity_mean": [np.nanmean(newIntM, axis = 0), np.nanmean(newIntP, axis = 0)]})
            return newD
        #
        else:
            print(Fore.MAGENTA + f'despikeSpin(): I have not looked into spin map data reccorded in scan mode {D["Experiment"]["Scan_Mode"]} yet...' + Fore.RESET)
            return D

    else:
        print(Fore.MAGENTA + f'despikeSpin(): The method is ready for EDC (FAT), MDC (FAT and FE), and map (FE).' + Fore.RESET)
        return D    




# ========================================================================================================================
# ========================================================================================================================
# ========================================================================================================================



def normalizeSpin(D = {}, shup = False, **kwargs):
    """
    Normalize the polarity plus and minus to each other at an appropriate energy / energy range.
    Pass keyword arguments p and pnum, where p is the point number and pnum is the number of points
    (starting at p) over which to find an average normalization intensity.
    """
    if not _thisIsSpinData(D):
        print(Fore.RED + "normalizeSpin(): I do not recognize this as being loaded spin data." + Fore.RESET); return
    #
    DD = deepcopy(D)
    #
    if D.get("type", "") == "spin_edc":
        accepted_kwargs = ["p", "nump"]
        if not shup:
            print(Fore.BLUE + f"normalizeSpin(): Accepted keyword arguments are: {accepted_kwargs}" + Fore.RESET)
        #
        p = abs(int(kwargs.get("p", 0)))
        nump = abs(int(kwargs.get("nump", 5)))
        if p > len(D["x"]): p = len(D.get(D["x"]))
        if nump < 1: nump = 1
        if p + nump > len(D["x"]) + 1 : nump = len(D["x"]) + 1 - p
        #
        norm_factors = []
        Int0, Int1 = D["intensity"][0], D["intensity"][1]
        for i, edc in enumerate(D["intensity"][0]):
            norm_factors.append(edc[p:p+nump].sum())
            if i > 0: Int0[i] = edc/norm_factors[-1]*norm_factors[0]
        for i, edc in enumerate(D["intensity"][1]):
            norm_factors.append(edc[p:p+nump].sum())
            Int1[i] = edc/norm_factors[-1]*norm_factors[0]
        DD.update({"intensity": np.array([Int0, Int1])})
        DD.update({"intensity_mean": np.array([Int0.mean(axis = 0), Int1.mean(axis = 0)])})
        if not shup:
            print(Fore.BLUE + f"normalizeSpin(): Normalized over {nump} points from {D['x'][p]:.3f} to {D['x'][p+nump]:.3f} eV" + Fore.RESET)
    
    #
    elif D.get("type", "") == "spin_mdc" and D.get("experiment", {}).get("Scan_Mode", "") == "FixedEnergies":
        accepted_kwargs = ["p", "nump"]
        if not shup:
            print(Fore.BLUE + f"normalizeSpin(): Accepted keyword arguments are: {accepted_kwargs}" + Fore.RESET)
        #
        # make proper arrays out of the minus and plus data
        int_m, int_p = [], []
        for curve in D["intensity"][0]: int_m.append( curve.transpose()[0] )
        for curve in D["intensity"][1]: int_p.append( curve.transpose()[0] )
        int_m, int_p = np.array(int_m), np.array(int_p)
        #
        p = abs(int(kwargs.get("p", 0)))
        nump = abs(int(kwargs.get("nump", 5)))
        if p > len(D["y"]): p = len(D.get(D["y"]))
        if nump < 1: nump = 1
        if p + nump > len(D["y"]) + 1 : nump = len(D["y"]) + 1 - p
        #
        INT_M, INT_P = np.zeros(np.shape(int_m)), np.zeros(np.shape(int_p))
        for i, curve in enumerate(int_m): INT_M[i] = curve / curve[p:p+nump].sum()
        for i, curve in enumerate(int_p): INT_P[i] = curve / curve[p:p+nump].sum()
        #
        # make "improper" arrays again
        INT_M2, INT_P2 = [], []
        for curve in INT_M: INT_M2.append( np.array([curve.transpose()]).transpose())
        for curve in INT_P: INT_P2.append( np.array([curve.transpose()]).transpose())
        INT_M2, INT_P2 = np.array(INT_M2), np.array(INT_P2)
        #
        DD = deepcopy(D)
        DD.update({"intensity": np.array([INT_M2, INT_P2])})
        DD.update({"intensity_mean": np.array([int_m.sum(axis = 0)/len(int_m), int_p.sum(axis = 0)/len(int_p)])})
        #
        labels = D["labels"]
        labels.update({"intensity": "Normalized intensity [a.u]", "intensity_mean": "Normalized intensity [a.u]"})
        DD.update({"labels": labels})
        return DD


    #
    elif D.get("type", "") == "spin_map" and D.get("experiment", {}).get("Scan_Mode", "") == "FixedAnalyzerTransmission":
        print(Fore.MAGENTA + "normalizeSpin(): Normalization of spin maps is not ready. Working on it right now...." + Fore.RESET)
        #
        # Where to normalize...
        return {}
    #
    elif D.get("Type", "") == "spin_map" and D.get("experiment", {}).get("Scan_Mode", "") == "FixedEnergies":
        print(Fore.MAGENTA + "normalizeSpin(): Not ready for MDC (FE)." + Fore.RESET); return {}
    #
    else:
        print(Fore.BLUE + "normalizeSpin(): Not ready for all types of spin data yet. Work in progress" + Fore.RESET); return {}
    #
    return DD







# ========================================================================================================================
# ========================================================================================================================
# ========================================================================================================================


def insertSpinData(D1 = {}, D2 = {}, shup = True):
    """
    See methods mergeSpinEDC() and mergeSpinMDC().
    """
    valid_types = ["spin_edc", "spin_mdc", "spin_map"]
    if not shup:
        print(Fore.BLUE + "insertSpinData(): This method is a 'wrapper' for the following methods: insertSpinEDC(), insertSpinMDC(), and insertSpinMap().")
        print("                 It combines two spin measurements of the same type with the same settings into one and returns a dopey dict of the same type.")
        print("                 Arguments: D1 and D2 as dopey spin dicts." + Fore.RESET)
    #
    try: typ1, typ2 = D1.get("type", ""), D2.get("type", "")
    except:
        print(Fore.RED + "insertSpinData(): Arguments D1 and D2 must both be spin data dopey dicts." + Fore.RESET); return {}
    if not (typ1 in valid_types and typ2 in valid_types):
        print(Fore.RED + f"insertSpinData(): Arguments D1 and D2 must both be spin data dopey dicts of types {valid_types}." + Fore.RESET); return {}
    if not typ1 == typ2:
        print(Fore.RED + f"insertSpinData(): Arguments D1 and D2 must both be spin data dopey dicts of the same type." + Fore.RESET); return {}
    #
    if typ1 == "spin_edc": return insertSpinEDC(D1 = D1, D2 = D2, shup = shup)
    elif typ1 == "spin_mdc": return insertSpinMDC(D1 = D1, D2 = D2, shup = shup)


def insertSpinEDC(D1 = {}, D2 = {}, shup = False):
    """
    Insert data from one spin edc measurement into another, if they are compatible. Pass arguments D1 and D2 (type spin_edc).
    Returns a type spin_edc dict.
    """
    if not shup:
        print(Fore.BLUE + "insertSpinEDC(): Combines two spin measurements of type spin_edc." + Fore.RESET)
        print(Fore.BLUE + "                 Arguments: D1 and D2 as dopey dicts of type spin_edc (with the same settings)." + Fore.RESET)
    #
    if not (type(D1) is dict and type(D2) is dict):
        print(Fore.RED + "insertSpinEDC(): Arguments D1 and D2 must both be spin edc data." + Fore.RESET); return {}
    if not (D1.get("type", "") == "spin_edc" and D2.get("type", "") == "spin_edc"):
        print(Fore.RED + "insertSpinEDC(): Arguments D1 and D2 must both be spin edc data." + Fore.RESET); return {}
    #
    if not np.array_equal(D1["x"], D2["x"]):
        print(Fore.RED + "insertSpinEDC(): The energy axes in the arguments (D1, D2) are not the same." + Fore.RESET); return {}
    #
    if not (D1["experiment"]["Ep"] == D2["experiment"]["Ep"]):
        print(Fore.MAGENTA + "insertSpinEDC(): Warning: the data are collected with different pass energies." + Fore.RESET)
    #
    D = deepcopy(D1)
    D["file"] = "merged_files"
    D["spectrum_id"] = 999999
    experiment = D["experiment"]
    experiment.update({"Spectrum_ID": 999999})
    if not D1["experiment"]["Dwell_Time"] == D2["experiment"]["Dwell_Time"]:
        print(Fore.MAGENTA + "insertSpinEDC(): Warning: the dwell times in the data are differnt." + Fore.RESET)
    if not D1["experiment"]["Curves_Per_Scan"] == D2["experiment"]["Curves_Per_Scan"]:
        print(Fore.MAGENTA + "insertSpinEDC(): Warning: the numbers of curves per scan in the data are differnt." + Fore.RESET)
    D.update({"experiment": experiment})
    #
    curves_m, curves_p = [], []
    for curve in D1["intensity"][0]: curves_m.append(curve)
    for curve in D2["intensity"][0]: curves_m.append(curve)
    for curve in D1["intensity"][1]: curves_p.append(curve)
    for curve in D2["intensity"][1]: curves_p.append(curve)
    curves_m, curves_p = np.array(curves_m), np.array(curves_p)
    D.update({"intensity": np.array([curves_m, curves_p])})
    #
    mean_m, mean_p = np.zeros(len(D["x"])), np.zeros(len(D["x"]))
    for curve in curves_m: mean_m += curve
    for curve in curves_p: mean_p += curve
    mean_m, mean_p = mean_m / len(curves_m), mean_p / len(curves_p)
    D.update({"intensity_mean": np.array([mean_m, mean_p])})
    #
    if not shup:
        print(Fore.BLUE + "insertSpinEDC():")
        print(f"   Merged data from id{D1['spectrum_id']} with {len(D1['intensity'][0])} polarity {D1['polarity'][0]} curves and {len(D1['intensity'][1])} polarity {D1['polarity'][1]} curves")
        print(f"   with data from id{D2['spectrum_id']} with {len(D2['intensity'][0])} polarity {D2['polarity'][0]} curves and {len(D2['intensity'][1])} polarity {D2['polarity'][1]} curves." + Fore.RESET)
    #
    return D



def insertSpinMDC(D1 = {}, D2 = {}, shup = False):
    """
    Insert spin mdc data from one measurement into another, if they are compatible. Pass arguments D1 and D2 (type spin_edc).
    Returns a type spin_edc dict.
    """
    if not shup:
        print(Fore.BLUE + "insertSpinMDC(): Combines two spin measurements of type spin_mdc." + Fore.RESET)
        print(Fore.BLUE + "                 Arguments: D1 and D2 as dopey dicts of type spin_mdc (with the same settings)." + Fore.RESET)
    #
    if not (type(D1) is dict and type(D2) is dict):
        print(Fore.RED + "insertSpinMDC(): Arguments D1 and D2 must both be spin mdc data." + Fore.RESET); return {}
    if not (D1.get("type", "") == "spin_mdc" and D2.get("type", "") == "spin_mdc"):
        print(Fore.RED + "insertSpinMDC(): Arguments D1 and D2 must both be spin mdc data." + Fore.RESET); return {}
    #
    ok_x  = np.array_equal(D1["x"], D2["x"])
    ok_y  = np.array_equal(D1["y"], D2["y"])
    ok_ep = np.array_equal(D1["experiment"]["Ep"], D2["experiment"]["Ep"])
    if not ok_x and ok_y and ok_ep:
        print(Fore.RED + "insertSpinMDC(): The data in arguments D1 and D2 are not possible to merge." + Fore.RESET)
        print(Fore.RED + "                 The energy axis, deflector axis, and pass energy must be the same." + Fore.RESET); return {}
    #
    D = deepcopy(D1)
    D["file"] = "merged_files"
    D["spectrum_id"] = 999999
    experiment = D["experiment"]
    experiment.update({"Spectrum_ID": 999999})
    if not D1["experiment"]["Dwell_Time"] == D2["experiment"]["Dwell_Time"]:
        print(Fore.MAGENTA + "insertSpinMDC(): Warning: the dwell times in the data are differnt." + Fore.RESET)
    if not D1["experiment"]["Curves_Per_Scan"] == D2["experiment"]["Curves_Per_Scan"]:
        print(Fore.MAGENTA + "insertSpinMDC(): Warning: the numbers of curves per scan in the data are differnt." + Fore.RESET)
    D.update({"experiment": experiment})
    #
    curves_m, curves_p = [], []
    for curve in D1["intensity"][0]: curves_m.append(curve)
    for curve in D2["intensity"][0]: curves_m.append(curve)
    for curve in D1["intensity"][1]: curves_p.append(curve)
    for curve in D2["intensity"][1]: curves_p.append(curve)
    curves_m, curves_p = np.array(curves_m), np.array(curves_p)
    D.update({"intensity": np.array([curves_m, curves_p])})
    #
    mean_m, mean_p = np.zeros(np.shape(D["intensity_mean"][0])), np.zeros(np.shape(D["intensity_mean"][0]))
    for curve in curves_m: mean_m += curve
    for curve in curves_p: mean_p += curve
    mean_m, mean_p = mean_m / len(curves_m), mean_p / len(curves_p)
    D.update({"intensity_mean": np.array([mean_m, mean_p])})
    #
    if not shup:
        print(Fore.BLUE + "insertSpinMDC():")
        print(f"   Merged data from id{D1['spectrum_id']} with {len(D1['intensity'][0])} polarity {D1['polarity'][0]} curves and {len(D1['intensity'][1])} polarity {D1['polarity'][1]} curves")
        print(f"   with data from id{D2['spectrum_id']} with {len(D2['intensity'][0])} polarity {D2['polarity'][0]} curves and {len(D2['intensity'][1])} polarity {D2['polarity'][1]} curves." + Fore.RESET)
    return D



def insertSpinMap(D1 = {}, D2 = {}, shup = False):
    """
    Insert spin map data from one measurement into another, if they are compatible. Pass arguments D1 and D2 (type spin_map).
    Returns a type spin_map dict.
    """
    print(Fore.LIGHTBLACK_EX + "insertSpinMap(): This method is under construction. Be aware that the result might not yet be correct." + Fore.RESET)
    if not shup:
        print(Fore.BLUE + "insertSpinMap(): Combines two spin measurements of type spin_map." + Fore.RESET)
        print(Fore.BLUE + "                 Arguments: D1 and D2 as dopey dicts of type spin_map (with the same settings)." + Fore.RESET)
    #
    if not (type(D1) is dict and type(D2) is dict):
        print(Fore.RED + "insertSpinMap(): Arguments D1 and D2 must both be spin mdc data." + Fore.RESET); return {}
    if not (D1.get("type", "") == "spin_map" and D2.get("type", "") == "spin_map"):
        print(Fore.RED + "insertSpinMap(): Arguments D1 and D2 must both be spin mdc data." + Fore.RESET); return {}
    #
    ok_x  = np.array_equal(D1["x"], D2["x"])
    ok_y  = np.array_equal(D1["y"], D2["y"])
    ok_z  = np.array_equal(D1["z"], D2["z"])
    ok_ep = np.array_equal(D1["experiment"]["Ep"], D2["experiment"]["Ep"])
    if not ok_x and ok_y and ok_z and ok_ep:
        print(Fore.RED + "insertSpinMap(): The data in arguments D1 and D2 are not possible to merge." + Fore.RESET)
        print(Fore.RED + "                 The energy axis, deflector axes, and pass energy must be the same." + Fore.RESET); return {}
    #
    D = deepcopy(D1)
    D["file"] = "merged_files"
    D["spectrum_id"] = 999999
    experiment = D["experiment"]
    experiment.update({"Spectrum_ID": 999999})
    if not D1["experiment"]["Dwell_Time"] == D2["experiment"]["Dwell_Time"]:
        print(Fore.MAGENTA + "insertSpinMap(): Warning: the dwell times in the data are differnt." + Fore.RESET)
    if not D1["experiment"]["Curves_Per_Scan"] == D2["experiment"]["Curves_Per_Scan"]:
        print(Fore.MAGENTA + "insertSpinMap(): Warning: the numbers of curves per scan in the data are differnt." + Fore.RESET)
    D.update({"experiment": experiment})
    #
    curves_m, curves_p = [], []
    for curve in D1["intensity"][0]: curves_m.append(curve)
    for curve in D2["intensity"][0]: curves_m.append(curve)
    for curve in D1["intensity"][1]: curves_p.append(curve)
    for curve in D2["intensity"][1]: curves_p.append(curve)
    curves_m, curves_p = np.array(curves_m), np.array(curves_p)
    D.update({"intensity": np.array([curves_m, curves_p])})
    #
    mean_m, mean_p = np.zeros(np.shape(D["intensity_mean"][0])), np.zeros(np.shape(D["intensity_mean"][0]))
    for curve in curves_m: mean_m += curve
    for curve in curves_p: mean_p += curve
    mean_m, mean_p = mean_m / len(curves_m), mean_p / len(curves_p)
    D.update({"intensity_mean": np.array([mean_m, mean_p])})
    #
    if not shup:
        print(Fore.BLUE + "insertSpinMap():")
        print(f"   Merged data from id{D1['spectrum_id']} with {len(D1['intensity'][0])} polarity {D1['polarity'][0]} curves and {len(D1['intensity'][1])} polarity {D1['polarity'][1]} curves")
        print(f"   with data from id{D2['spectrum_id']} with {len(D2['intensity'][0])} polarity {D2['polarity'][0]} curves and {len(D2['intensity'][1])} polarity {D2['polarity'][1]} curves." + Fore.RESET)
    return D





# ========================================================================================================================
# ========================================================================================================================
# ========================================================================================================================


def updateSpinData(D = {}, polarity = 0, curve = -1, point = -1, value = None, shup = False):
    """
    See updateSpinEDC() and updateSpinMDC()
    """
    valid_types = ["spin_edc", "spin_mdc"]
    try: typ = D.get("type", "")
    except:
        print(Fore.RED + f"updateSpinData(): Argument D must be a spin data dopey dict (valid types: {valid_types})" + Fore.RESET); return D
    if not typ in valid_types:
        print(Fore.RED + f"updateSpinData(): Argument D must be a spin data dopey dict (valid types: {valid_types})" + Fore.RESET); return D
    #
    if typ == "spin_edc": return updateSpinEDC(D = D, polarity = polarity, curve = curve, point = point, value = value, shup = shup)
    elif typ == "spin_mdc": return updateSpinMDC(D = D, polarity = polarity, curve = curve, point = point, value = value, shup = shup)



def updateSpinEDC(D = {}, polarity = 0, curve = -1, point = -1, value = None, shup = False):
    """
    Use this if you have tampered with the individual edcs in D['intensity'] to update D['intensity_mean']
    or if you want to tamper with them. If you tamper with them in here you must pass the following arguments:

    polarity (-1 or 1), curve (0 to whatever, usually 3), point (0 to whatever), and value (the new value for that data point).
    All these args are integers except value which is a float.
    """
    try: typ = D.get("type", "")
    except: typ = ""
    if not typ == "spin_edc":
        print(Fore.RED + f"updateSpinEDC(): The argument D must containg a dopey spin edc dict." + Fore.RESET); return D
    #
    DD = deepcopy(D)
    try: polarity = int(polarity)
    except: polarity = 0
    try: curve = int(curve)
    except: curve = -1
    try: point = int(point)
    except: point = -1
    #
    edit_in_method = True
    if not polarity == 0 and curve >= 0 or point >= 0:
        if polarity == -1:
            if curve >= len(DD["intensity"][0]): edit_in_method = False
        if polarity == 1:
            if curve >= len(DD["intensity"][1]): edit_in_method = False
        if edit_in_method:
            if point >= len(DD["intensity"][0][0]): edit_in_method = False
        try: value = float(value)
        except: value, edit_in_method = None, False
    #
    if edit_in_method:
        tmp_intensity = DD["intensity"]
        if polarity == -1: pi, ptxt = 0, "negative"
        else: pi, ptxt = 1, "positive"
        tmp_intensity[pi][curve][point] = value
        DD.update({"intensity": tmp_intensity})
        if not shup:
            print(Fore.BLUE + f"updateSpinEDC(): Updated intensity_mean for point {point} for curve {curve} with {ptxt} polarity." + Fore.RESET)
    else:
        if not shup:
            print(Fore.BLUE + f"updateSpinEDC(): Updated intensity_mean." + Fore.RESET)
    #
    cm, cp = 0, 0
    curvem = np.zeros(len(DD["intensity"][0][0]))
    curvep = np.copy(curvem)
    #
    for curve in DD["intensity"][0]:
        curvem += curve
        cm += 1
    for curve in DD["intensity"][1]:
        curvep += curve
        cp += 1
    curvem /= cm
    curvep /= cp
    intensity_mean = np.array([curvem, curvep])
    DD.update({"intensity_mean": intensity_mean})
    if not shup:
        print(Fore.BLUE + "updateSpinEDC(): Updated intensity_mean." + Fore.RESET)
    return DD

    
def updateSpinMDC(D = {}, polarity = 0, curve = -1, point = -1, value = None, shup = False):
    """
    Use this if you have tampered with the individual mdcs in D['intensity'] to update D['intensity_mean']
    or if you want to tamper with them. If you tamper with them in here you must pass the following arguments:

    polarity (-1 or 1), curve (0 to whatever, usually 3), point (0 to whatever), and value (the new value for that data point).
    All these args are integers except value which is a float.
    """
    print(Fore.MAGENTA + "updateSpinMDC(): Not finished. Don't use yet." + Fore.RESET)
    #
    scan_modes = ["FixedEnergies", "FixedAnalyzerTransmission"]
    #
    try: typ = D.get("type", "")
    except: typ = ""
    if not typ == "spin_mdc":
        print(Fore.RED + f"updateSpinMDC(): The argument D must containg a dopey spin mdc dict." + Fore.RESET); return D
    #
    scan_mode = D["experiment"]["Scan_Mode"]
    if not scan_mode in scan_modes:
        print(Fore.RED + f"updateSpinMDC(): Sorry, this method is currently only prepared for scan modes {scan_modes}." + Fore.RESET); return D
    #
    DD = deepcopy(D)
    try: polarity = int(polarity)
    except: polarity = 0
    try: curve = int(curve)
    except: curve = -1
    try: point = int(point)
    except: point = -1
    #
    edit_in_method = True
    if not polarity == 0 and curve >= 0 or point >= 0:
        if polarity == -1:
            if curve >= len(DD["intensity"][0]): edit_in_method = False
        if polarity == 1:
            if curve >= len(DD["intensity"][1]): edit_in_method = False
        if edit_in_method:
            if point >= len(DD["intensity"][0][0]): edit_in_method = False
        try: value = float(value)
        except: value, edit_in_method = None, False
    #
    if edit_in_method:
        tmp_intensity = DD["intensity"]
        if polarity == -1: pi, ptxt = 0, "negative"  # pi is polarity index. if polarity = -1,+1 then pi = 0,1 
        else: pi, ptxt = 1, "positive"
        tmp_intensity[pi][curve][point][0] = value
        DD.update({"intensity": tmp_intensity})
        if not shup:
            print(Fore.BLUE + f"updateSpinMDC(): Updated intensity_mean for point {point} for curve {curve} with {ptxt} polarity." + Fore.RESET)
    else:
        if not shup:
            print(Fore.BLUE + f"updateSpinMDC(): Updated intensity_mean." + Fore.RESET)
    #
    mean_m, mean_p = np.zeros(np.shape(DD["intensity_mean"][0])), np.zeros(np.shape(DD["intensity_mean"][0]))
    for curve in DD["intensity"][0]: mean_m += curve
    for curve in DD["intensity"][1]: mean_p += curve
    mean_m, mean_p = mean_m / len(DD["intensity"][0]), mean_p / len(DD["intensity"][1])
    DD.update({"intensity_mean": np.array([mean_m, mean_p])})
    return DD



# ========================================================================================================================
# ========================================================================================================================
# ========================================================================================================================



def inspectSpin(D = {}, shup = False, **kwargs):
    """
    Show the data in spin dicts.

    Arguments:
        D               dopey spin dict
        shup            bool

    Keyword arguments:
        figsize         tuple
        marker          bool or string
        marker_size     number
    """
    try: typ = D.get("type")
    except:
        print(Fore.RED + f"inspectSpin(): The argument D must contain a dopey spin dict." + Fore.RESET); return D
    #
    accepted_types = ["spin_edc", "spin_mdc"]
    if not typ in accepted_types:
        print(Fore.RED + f"inspectSpin(): The argument D must contain a dopey spin dict of type {accepted_types}" + Fore.RESET); return D
    #
    if typ == accepted_types[0]: #-----------------------
        #
        if not shup:
            print(Fore.BLUE + f"inspectSpin(): Keyword arguments for this type of data: figsize, marker, markersize." + Fore.RESET)
        #
        figsize = kwargs.get("figsize", (10,5))
        marker = kwargs.get("marker", None)
        if type(marker) is bool: marker = "x"
        markersize = kwargs.get("markersize", 5)
        #
        fig, ax = plt.subplots(ncols = 3, figsize = figsize)
        for i, curve in enumerate(D["intensity"][0]): ax[0].plot(D["x"], curve, label = f"{i}", marker = marker, markersize = markersize)
        for i, curve in enumerate(D["intensity"][1]): ax[1].plot(D["x"], curve, label = f"{i}", marker = marker, markersize = markersize)
        ax[2].plot(D["x"], D["intensity_mean"][0], label = "M = -1", color = "red", marker = marker, markersize = markersize)
        ax[2].plot(D["x"], D["intensity_mean"][1], label = "M = +1", color = "blue", marker = marker, markersize = markersize)
        titles = ["M-", "M+", "Mean intensity"]
        for i, a in enumerate(ax): 
            a.set_xlabel(D["labels"]["x"], fontsize = 10)
            a.legend(fontsize = 10)
            a.set_title(titles[i], fontsize = 12)
        ax[0].set_ylabel(D["labels"]["intensity_mean"], fontsize = 10)
        fig.tight_layout()
    
    elif typ == "spin_mdc" and D["experiment"]["Scan_Mode"] == "FixedEnergies": #-----------------------
        #
        if not shup:
            print(Fore.BLUE + f"inspectSpin(): Keyword arguments for this type of data: figsize, marker, markersize, legend." + Fore.RESET)
        #
        figsize = kwargs.get("figsize", (10,5))
        marker = kwargs.get("marker", None)
        if type(marker) is bool: marker = "x"
        markersize = kwargs.get("markersize", 5)
        legend = kwargs.get("legend", True)
        #
        fig = plt.figure(figsize = figsize)
        ax = []
        ax.append(plt.subplot2grid((1, 10), (0, 1), colspan = 1))
        ax.append(plt.subplot2grid((1, 10), (0, 2), colspan = 1))
        ax.append(plt.subplot2grid((1, 10), (0, 3), colspan = 2))
        ax.append(plt.subplot2grid((1, 10), (0, 5), colspan = 2))
        ax.append(plt.subplot2grid((1, 10), (0, 7), colspan = 2))
        
        extent = [D["x"][0]-0.01, D["x"][-1]+0.01, D["y"][-1], D["y"][0]]
        _ = ax[0].imshow(D["intensity_mean"][0], extent = extent, aspect = "auto")
        _ = ax[1].imshow(D["intensity_mean"][1], extent = extent, aspect = "auto")
        for a in [0,1]:
            ax[a].invert_yaxis()
            ax[a].set_xticks([D["x"][0]])
        
        ax[2].plot(D["intensity_mean"][0], D["y"], color = "red",  label = "M = -1", marker = marker, markersize = markersize)
        ax[2].plot(D["intensity_mean"][1], D["y"], color = "blue", label = "M = +1", marker = marker, markersize = markersize)
        
        for i, curve in enumerate(D["intensity"][0]):
            ax[3].plot(curve, D["y"], label = f"{i}", marker = marker, markersize = markersize)
        for i, curve in enumerate(D["intensity"][1]):
            ax[4].plot(curve, D["y"], label = f"{i}", marker = marker, markersize = markersize)

        for a, xlabel in enumerate(["Ek", "Ek", "Intensity", "Intensity", "Intensity"]): ax[a].set_xlabel(xlabel, fontsize = 10)
        for a, ylabel in enumerate(["Deflector", "", "", "", ""]): ax[a].set_ylabel(ylabel, fontsize = 10)
        for a, title in enumerate(["M-", "M+", "M- & M+", "Individual M-", "Individual M+"]): ax[a].set_title(title, fontsize = 10)

        if legend:
            for a in [2,3,4]: ax[a].legend(fontsize = 8)

        fig.tight_layout()
    
    elif typ == "spin_mdc" and D["experiment"]["Scan_Mode"] == "FixedAnalyzerTransmission": #-----------------------
        #
        if not shup:
            print(Fore.BLUE + f"inspectSpin(): Keyword arguments for this type of data: figsize, show_asym." + Fore.RESET)
        #
        show_asym = kwargs.get("show_asym", True)
        if show_asym:
            figsize = kwargs.get("figsize", (10, 4))
            fig = plt.figure(figsize = figsize)
            ax = []
            ax.append(plt.subplot2grid((1, 11), (0, 1), colspan = 3))
            ax.append(plt.subplot2grid((1, 11), (0, 4), colspan = 3))
            ax.append(plt.subplot2grid((1, 11), (0, 8), colspan = 3))
            titles = ["Polarity -", "Polarity +", "Asymmetry"]
        else:
            figsize = kwargs.get("figsize", (8, 4))
            fig, ax = plt.subplots(ncols = 2, figsize = figsize)
            titles = ["Polarity -", "Polarity +"]
        #
        extent = [D["x"][0]-0.01, D["x"][-1]+0.01, D["y"][-1], D["y"][0]]
        _ = ax[0].imshow(D["intensity_mean"][0], extent = extent, aspect = "auto", cmap = "bone_r")
        _ = ax[1].imshow(D["intensity_mean"][1], extent = extent, aspect = "auto", cmap = "bone_r")
        if show_asym:
            asym = ( D["intensity_mean"][1] - D["intensity_mean"][0] ) / ( D["intensity_mean"][1] + D["intensity_mean"][0] ) / 1
            _ = ax[2].imshow(asym, extent = extent, aspect = "auto", cmap = "bwr")
        for a, txt in enumerate(titles):
            ax[a].invert_yaxis()
            ax[a].set_xlabel(D["labels"]["x"], fontsize = 10)
            ax[a].set_title(txt, fontsize = 12)
        ax[0].set_ylabel(D["labels"]["y"], fontsize = 10)
        fig.tight_layout()

    


        





# ========================================================================================================================
# ========================================================================================================================
# ========================================================================================================================



def polarization(D = [], sherman = None, shup = True):
    """
    Pass D as a list of 1, 2, or 3 dicts from quickSpin(). The dict/dicts should fulfill being:
        (a) one coil 1 dict
        (b) two coil 2 dicts, one for each rotator setting (-1 and +1)
        (c) three dicts (a+b)
    Note that you need to specify coil and rotator when using quickSpin().
    """
    #
    R = {}
    #
    try: sherman = float(sherman)
    except: sherman = SHERMAN
    #
    if not shup:
        print(Fore.BLUE + "polarization(): Pass D as a list of suitable result dicts from quickSpin() to calculate polarizations." + Fore.RESET)
        print(Fore.BLUE + "                sherman = {sherman}. Pass argument sherman to use another value." + Fore.RESET)
    #
    if not type(D) is list:
        print(Fore.RED + "polarization(): Argument D must be a list of dicts." + Fore.RESET); return R
    if len(D) == 0:
        print(Fore.RED + "polarization(): Argument D must be a list of dicts.." + Fore.RESET); return R
    for item in D:
        if not type(item) is dict:
            print(Fore.RED + "polarization(): Found an item in the list that is not a dict." + Fore.RESET); return R
        if not item.get("type", "NONE") == "result":
            print(Fore.RED + "polarization(): Found an item in the list that is not a result dict." + Fore.RESET); return R
        if not item.get("kind", "NONE").startswith("spin"):
            print(Fore.RED + "polarization(): Found an item in the list that is not a spin result dict." + Fore.RESET); return R
    if len(D) > 3:
        print(Fore.RED + "polarization(): There are too many dicts in argument D." + Fore.RESET); return R
    #
    D1, D2, D3 = {}, {}, {}
    the_case = 0
    #
    # --- coil 1 only
    if len(D) == 1:
        D3 = deepcopy(D[0])
        if D3["coil"] == 0:
            print(Fore.RED + "polarization(): Missing coil information." + Fore.RESET); return R
        if not D3["coil"] == 1:
            print(Fore.RED + "polarization(): The dict is not a coil 1 dict." + Fore.RESET); return R
        the_case = 1
    # --- coil 2 only
    if len(D) == 2:
        Da, Db = deepcopy(D[0]), deepcopy(D[1])
        if Da["coil"] == 0 or Db["coil"] == 0:
            print(Fore.RED + "polarization(): Missing coil information." + Fore.RESET); return R
        if not Da["coil"] == Db["coil"] == 2:
            print(Fore.RED + "polarization(): The two dicts must be coil 2 dicts." + Fore.RESET); return R
        if Da["rotator"] == 0 or Db["rotator"] == 0:
            print(Fore.RED + "polarization(): Missing rotator information." + Fore.RESET); return R
        if Da["rotator"] == Db["rotator"]:
            print(Fore.RED + "polarization(): The two dicts must contain results from different rotator values." + Fore.RESET); return R
        #
        if Da["rotator"] == 1: D1, D2 = deepcopy(Da), deepcopy(Db)
        else: D2, D1 = deepcopy(Da), deepcopy(Db)
        del Da, Db
        the_case = 2
    # --- coil 1 and coil 2
    if len(D) == 3:
        Da, Db, Dc = deepcopy(D[0]), deepcopy(D[1]), deepcopy(D[2])
        #
        coils = [Da["coil"], Db["coil"], Dc["coil"]]
        if 0 in coils:
            print(Fore.RED + "polarization(): Missing coil information." + Fore.RESET); return R
        if not np.array(coils).sum() == 5:
            print(Fore.RED + "polarization(): Expected one dict from coil one and two dicts from coil 2." + Fore.RESET); return R
        #
        if Da["coil"] == 1:
            D3 = deepcopy(Da); Da, Db = deepcopy(Db), deepcopy(Dc)
        elif Db["coil"] == 1:
            D3 = deepcopy(Db); Da, Db = Da, deepcopy(Dc) 
        elif Dc["coil"] == 1:
            D3 = deepcopy(Dc); Da, Db = Da, Db
        del Dc
        #
        if Da["rotator"] == 1 and Db["rotator"] == -1: D1, D2 = deepcopy(Da), deepcopy(Db)
        elif Da["rotator"] == -1 and Db["rotator"] == 1: D2, D1 = deepcopy(Da), deepcopy(Db)
        else:
            print(Fore.RED + "polarization(): Missing rotator information for the coil 2 dicts." + Fore.RESET); return R
        the_case = 3
    #
    if the_case in [2,3]: a = np.zeros(np.shape(D1["intensity"][0])) * np.NaN
    else: a = np.zeros(np.shape(D3["intensity"][0])) * np.NaN
    asym_c1, asym_c2rp, asym_c2rm = np.copy(a), np.copy(a), np.copy(a) 
    px, py, pz = np.copy(a), np.copy(a), np.copy(a)
    cxp, cxm, cyp, cym, czp, czm = np.copy(a), np.copy(a), np.copy(a), np.copy(a), np.copy(a), np.copy(a)
    #
    P = ""
    if the_case == 1:
        asym_c1 = (D3["intensity"][1] - D3["intensity"][0]) / (D3["intensity"][1] + D3["intensity"][0])
        pz = 1/sherman * asym_c1
        tot_int = (D3["intensity"][1] + D3["intensity"][0])/2
        czp = tot_int * (1 + pz)
        czm = tot_int * (1 - pz)
        P = "z"
    if the_case == 2:
        asym_c2rp = (D1["intensity"][1] - D1["intensity"][0]) / (D1["intensity"][1] + D1["intensity"][0])
        asym_c2rm = (D2["intensity"][1] - D2["intensity"][0]) / (D2["intensity"][1] + D2["intensity"][0])
        px =  1/np.sqrt(2)/sherman * (asym_c2rp - asym_c2rm)
        py = -1/np.sqrt(2)/sherman * (asym_c2rp + asym_c2rm)
        tot_int = (D1["intensity"][1] + D1["intensity"][0] + D2["intensity"][1] + D2["intensity"][0])/4
        cxp = tot_int * (1 + px)
        cxm = tot_int * (1 - px)
        cyp = tot_int * (1 + py)
        cym = tot_int * (1 - py)
        P = "xy"
    if the_case == 3:
        asym_c1 = (D3["intensity"][1] - D3["intensity"][0]) / (D3["intensity"][1] + D3["intensity"][0])
        asym_c2rp = (D1["intensity"][1] - D1["intensity"][0]) / (D1["intensity"][1] + D1["intensity"][0])
        asym_c2rm = (D2["intensity"][1] - D2["intensity"][0]) / (D2["intensity"][1] + D2["intensity"][0])
        px =  1/np.sqrt(2)/sherman * (asym_c2rp - asym_c2rm)
        py = -1/np.sqrt(2)/sherman * (asym_c2rp + asym_c2rm)
        pz = 1/sherman * asym_c1
        tot_int = (D1["intensity"][1] + D1["intensity"][0] + D2["intensity"][1] + D2["intensity"][0] + D3["intensity"][1] + D3["intensity"][0])/6
        cxp = tot_int * (1 + px)
        cxm = tot_int * (1 - px)
        cyp = tot_int * (1 + py)
        cym = tot_int * (1 - py)
        czp = tot_int * (1 + pz)
        czm = tot_int * (1 - pz)
        P = "xyz"
    #
    if the_case == 1: DD = deepcopy(D3)
    else: DD = deepcopy(D2)
    R.update({"type": DD["type"]})      # always 'result'
    R.update({"kind": f'{DD["kind"]}_polarization'})
    R.update({"polarizations": P})
    labels = {}
    #if DD["Kind"] == "spin_edc":        # Update the dict updating below! <<<<<<<<================================
    #    R.update({"x": DD["x"]})
    #    labels.update({"x": DD["labels"]["x"]})
    #if DD["Kind"] == "spin_mdc":
    #    if "x" in DD.keys():  # always...
    #        R.update({"x": DD["x"]})
    #        labels.update({"x": DD["labels"]["x"]})
    #    if "y" in DD.keys():
    #        R.update({"y": DD["y"]})
    #        labels.update({"y": DD["labels"]["y"]})
    #    if "Ek" in DD.keys():
    #        R.update({"Ek": DD["Ek"]})
    #if DD["Kind"] == "spin_map":                        # Only for FE at the moment! Update here when FAT is done.
    #    if "x" in DD.keys():  # always...
    #        R.update({"x": DD["x"]})
    #        labels.update({"x": DD["labels"]["x"]})
    #    if "y" in DD.keys():
    #        R.update({"y": DD["y"]})
    #        labels.update({"y": DD["labels"]["y"]})
    #    if "Ek" in DD.keys():
    #        R.update({"Ek": DD["Ek"]})
    #
    R.update({"x": DD["x"]})
    labels.update({"x": DD["labels"]["x"]})
    if "y" in DD.keys():
        R.update({"y": DD["y"]})
        labels.update({"y": DD["labels"]["y"]})
    #
    if P in ["z", "xyz"]:
        R.update({"asym_c1": asym_c1})
        labels.update({"asym_c1": "Asymmetry"})
    if P in ["xy", "xyz"]:
        R.update({"asym_c2rp": asym_c2rp})
        labels.update({"asym_c2rp": "Asymmetry"})
        R.update({"asym_c2rm": asym_c2rm})
        labels.update({"asym_c2rm": "Asymmetry"})
        R.update({"px": px})
        labels.update({"px": "Polarization"})
        R.update({"py": py})
        labels.update({"py": "Polarization"})
    if P in ["z", "xyz"]:
        R.update({"pz": pz})
        labels.update({"pz": "Polarization"})
    R.update({"intensity": tot_int})
    labels.update({"intensity": DD["labels"]["intensity"]})
    if P in ["xy", "xyz"]:
        R.update({"component_intensity_px": np.array([cxp, cxm])})
        labels.update({"component_intensity_px": D1.get("labels", {}).get("intensity", "")})
        R.update({"component_intensity_py": np.array([cyp, cym])})
        labels.update({"component_intensity_py": D1.get("labels", {}).get("intensity", "")})
    if P in ["z", "xyz"]:
        R.update({"component_intensity_pz": np.array([czp, czm])})
        labels.update({"component_intensity_pz": D3.get("labels", {}).get("intensity", "")})
    R.update({"labels": labels})
    #
    return R



def rotatePolarization(D = {}, polar = 0., shup = True):
    """
    Pass D (dict) as an ouput from polarization(). The argument polar (int, float) is the value of the polar angle during measurement.
    """
    if not shup:
        print(Fore.BLUE + "rotatePolarization(): Pass argument D as a dict from polarization and argument polar as a scalar value (deg.)." + Fore.RESET)
    #
    if not type(D) is dict:
        print(Fore.RED + "rotatePolarization(): Argument D must be a dict from polarization()." + Fore.RESET); return D
    if not D.get("type", "") == "result" and D.get("kind", "").endswith("polarization"):
        print(Fore.RED + "rotatePolarization(): Argument D must be a dict from polarization()." + Fore.RESET); return D
    #
    try: polar = float(polar)
    except:
        print(Fore.RED + "rotatePolarization(): Argument polar must be a scalar (deg.)." + Fore.RESET); return D
    #
    if polar == 0: return D
    #
    newD = deepcopy(D)
    #
    intensity = D.get("intensity", np.array(0))
    data_shape = np.shape(intensity)
    data_dim = len(data_shape)
    px = D.get("px", np.zeros(data_shape))
    py = D.get("py", np.zeros(data_shape))
    pz = D.get("pz", np.zeros(data_shape))
    angle = np.deg2rad(polar)
    #
    p1, p2, p3 = np.copy(pz), np.copy(px), np.copy(py)
    P1 = p1 * np.cos(angle) - p2 * np.sin(angle)
    P2 = p1 * np.sin(angle) + p2 * np.cos(angle)
    P3 = p3 # not rotated by the polar angle
    Px = np.copy(P2)
    Py = np.copy(P3)
    Pz = np.copy(P1)
    cunt = 0
    if not np.nansum(Px) == 0: cunt += 1
    if not np.nansum(Py) == 0: cunt += 1
    if not np.nansum(Pz) == 0: cunt += 1
    cxp, cxm = intensity * (1 + Px) / cunt, intensity * (1 - Px) / cunt
    cyp, cym = intensity * (1 + Py) / cunt, intensity * (1 - Py) / cunt
    czp, czm = intensity * (1 + Pz) / cunt, intensity * (1 - Pz) / cunt
    #
    Pstr = ""
    if not np.nansum(Px) == 0:
        Pstr = f"{Pstr}x"
        newD.update({"px": Px, "component_intensity_px": np.array([cxp, cxm])})
    if not np.nansum(Py) == 0:
        Pstr = f"{Pstr}y"
        newD.update({"py": Py, "component_intensity_py": np.array([cyp, cym])})
    if not np.nansum(Pz) == 0:
        Pstr = f"{Pstr}z"
        newD.update({"pz": Pz, "component_intensity_pz": np.array([czp, czm])})
    newD.update({"polarizations": Pstr})
    #
    return newD
    







# ========================================================================================================================
# ========================================================================================================================
# ========================================================================================================================


def getSpinEDCfromMDC(D = {}, N = 0, shup = False):
    """
    Extract one edc from an mdc.
    D is a dopey dict from load().
    N is an integer and the N:th edc in the mdc scan.
    """
    #
    if not _thisIsSpinData(D):
        print(Fore.RED + "getSpinEDCfromMDC(): I do not recognize this as being loaded spin data." + Fore.RESET); return {}
    #
    if not D["type"] == "spin_mdc":
        print(Fore.RED + "getSpinEDCfromMDC(): This is not spin mdc data." + Fore.RESET); return {}
    #
    if not shup:
        print(Fore.BLUE + f"getSpinEDCfromMDC(): Argument N is an integer in the range 0 to {len(D['y'])-1}, where 0 refers to the edc for deflector {D['y'][0]:.0f} and {len(D['y'])-1:.0f} to the edc for deflector {D['y'][-1]}." + Fore.RESET)
    nok = True
    try: N = int(abs(N))   
    except:
        print(Fore.RED + "getSpinEDCfromMDC(): Argument N must be an integer." + Fore.RESET); return {}
    if N > len(D["y"]) - 1:
        print(Fore.RED + "getSpinEDCfromMDC(): Argument N is out of range." + Fore.RESET); return {}
    #
    DD = deepcopy(D)
    intensity = np.array([ D["intensity"][0][:,N,:], D["intensity"][1][:,N,:] ])
    DD.update({"intensity": intensity})
    intensity_avg = np.array([ D["intensity_mean"][0][N,:], D["intensity_mean"][1][N,:] ])
    DD.update({"intensity_mean": intensity_avg})
    DD.update({"type": "spin_edc"})
    del DD["y"]
    labels = DD["labels"]
    del labels["y"]
    DD.update({"labels": labels})
    experiment = DD["experiment"]
    experiment.update({"parameters": ['NegativePolarity', 'Step']})
    DD.update({"experiment": experiment})
    if "raw_data" in DD: del DD["raw_data"]
    if not shup:
        print(Fore.BLUE + f"getSpinEDCfromMDC(): Returning a spin EDC for deflector value {D['y'][N]}." + Fore.RESET)
    return DD


    



# ========================================================================================================================
# ========================================================================================================================
# ========================================================================================================================


#def deleteSpinEDCCurve(D = {}, graph = True, polarity = 0, index = -1, figsize = (8, 3.5), shup = False):
#    """
#    Deletes a particular scan from spin_edc data. Pass graph = True (default) to plot all scans,
#    the pass graph = False, polarity = -1 or 1, and index = i where i is found in the graph.
#    Returns a new spin_edc dict.
#    """
#    try: data_type = D.get("type", "invalid")
#    except: data_type = "invalid"
#    if not data_type == "spin_edc":
#        print(Fore.RED + "deleteSpinEDCCurve(): The argument D must be a spin_edc dict." + Fore.RESET); return D
#    #
#    if graph:
#        if not type(figsize) is tuple: figsize = (8, 3.5)
#        fig, ax = plt.subplots(ncols = 2, figsize = (8,3.5))
#        for i, curve in enumerate(D["intensity"][0]): ax[0].plot(D["x"], curve, label = f"{i}")
#        for i, curve in enumerate(D["intensity"][1]): ax[1].plot(D["x"], curve, label = f"{i}")
#        for i in [0, 1]:
#            ax[i].set_xlabel(D["labels"]["x"]); ax[i].set_ylabel(D["labels"]["intensity"])
#            ax[i].legend(fontsize = 10)
#            ax[i].set_title(f"polarity {D['polarity'][i]}")
#        print(Fore.BLUE + "To delete a curve, pass graph = False, polarity = -1 or 1, and index = i where")
#        print("i is the index of the curve (see left and right panel in the graph)." + Fore.RESET)
#        return D
#    #
#    try:
#        polarity, index = int(polarity), int(index)
#    except:
#        print(Fore.RED + "deleteSpinEDCCurve(): The arguments polarity and index must integers." + Fore.RESET); return D
#    if not polarity in [-1, 1]:
#        print(Fore.RED + "deleteSpinEDCCurve(): The argument polarity must be -1 or 1 (integer)." + Fore.RESET); return D
#    intensityn = D["intensity"][0]
#    intensityp = D["intensity"][1]
#    if polarity == -1: pindex = 0
#    else: pindex = 1
#    max_index = len(D["intensity"][pindex]) - 1
#    if not max_index >= 1:
#        print(Fore.RED + f"deleteSpinEDCCurve(): We have to keep at least one curve for polarity {polarity}." + Fore.RESET); return D
#    if not( index >= 0 and index <= max_index ):
#        print(Fore.RED + f"deleteSpinEDCCurve(): The argument index must be between 0 and {max_index} (integer)." + Fore.RESET); return D
#    #
#    if polarity == -1: intensityn = np.delete(intensityn, (index), axis = 0)
#    else: intensityp = np.delete(intensityp, (index), axis = 0)
#    newD = deepcopy(D)
#    newD.update({"intensity": [intensityn, intensityp]})
#    mean_m, mean_p = np.zeros(len(newD["x"])), np.zeros(len(newD["x"]))
#    for curve in newD["intensity"][0]: mean_m += curve
#    for curve in newD["intensity"][1]: mean_p += curve
#    mean_m, mean_p = mean_m / len(newD["intensity"][0]), mean_p / len(newD["intensity"][1])
#    newD.update({"intensity_mean": np.array([mean_m, mean_p])})
#    if not shup:
#        print(Fore.BLUE + "deleteSpinEDCCurve():")
#        print(f'Deleted curve {index} for polarity {polarity}. There are now {len(newD["intensity"][0])} curves')
#        print(f'for polarity {newD["polarity"][0]} and {len(newD["intensity"][1])} curves for polarity {newD["polarity"][1]}.')
#    return newD
        
        








