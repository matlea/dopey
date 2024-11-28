__version__ = "24.10.10"
__author__  = "Mats Leandersson"

print(f"{__name__}, {__version__}")

"""
"""




import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from colorama import Fore
from copy import deepcopy

try: from dopey.dopey_methods import subArray, compact
except ImportError as ie: 
    try:
        from dopey_methods  import subArray, compact
    except:
        print(Fore.RED + f'\n{__name__} could not import the dopey_methods module.' + Fore.RESET)
    print(Fore.MAGENTA + ie + Fore.RESET)

try:
    from lmfit import minimize as lmfit_minimize
    from lmfit import Parameters as lmfit_Parameters
except ImportError as ie: 
    print(Fore.RED + f'\n{__name__} could not import the lmfit module.\n' + Fore.RESET)
    print(ie)

print(Fore.MAGENTA + f"{__name__} is under construction.\n" + Fore.RESET)




# ============================================================================================================================================
# ============================================================================================================================================
# ============================================================================================================================================
# ============================================================================================================================================

def fitFermiDict(D = {}, amplitude = None, fermi_level = None, temperature = None, 
             resolution = None, bkgr_offset = None, bkgr_slope = None,
             amplitude_fixed = False, fermi_level_fixed = False, temperature_fixed = True, resolution_fixed = False, bkgr_offset_fixed = False,
             x_min = None, x_max = None, y_min = None, y_max = None,
             fermi_level_min = None, fermi_level_max = None, amplitude_min = None, amplitude_max = None, temperature_min = None, temperature_max = None,
             resolution_min = None, resolution_max = None, bkgr_offset_min = None, bkgr_offset_max = None,
             shup = False, show_progress = False, hide_plot = False):
    """
    This method uses fitFermi() to fit the data in a dopey dict.
    """
    if not type(D) is dict:
        print(Fore.RED + f"fitFermiDict(): Argument D must be a dopey dict." + Fore.RESET); return {}
    DD = deepcopy(D)
    lenx = len(DD.get("x", np.zeros(0)))
    leny = len(DD.get("y", np.zeros(0)))
    lenz = len(DD.get("z", np.zeros(0)))
    if lenx + leny + lenz == 0:
        print(Fore.RED + f"fitFermiDict(): Could not find any axes (x, y, or z) in argument D." + Fore.RESET); return {}
    intensity = D.get("intensity", None)
    if type(intensity) is type(None):
        print(Fore.RED + f"fitFermiDict(): Could not find any intensity in argument D." + Fore.RESET); return {}
    #
    if lenz > 0:
        print(Fore.RED + f"fitFermiDict(): This data contains too many axes." + Fore.RESET); return {}
    #
    if type(x_min) is type(None): x_min = DD["x"].min()
    if type(x_max) is type(None): x_max = DD["x"].max()
    try: x_min = float(x_min)
    except:
        print(Fore.MAGENTA + f"fitFermiDict(): Argument x_min must be a value. Setting default x_min = {x_min}" + Fore.RESET)
    try: x_max = float(x_max)
    except:
        print(Fore.MAGENTA + f"fitFermiDict(): Argument x_max must be a value. Setting default x_max = {x_max}" + Fore.RESET)
    if x_min > x_max: x_min, x_max = x_max, x_min
    if x_min < DD["x"].min(): x_min = DD["x"].min()
    if x_max > DD["x"].max(): x_max = DD["x"].max()
    ix1, ix2 = abs(DD["x"] - x_min).argmin(), abs(DD["x"] - x_max).argmin() + 2
    DD = subArray(DD, axis = "x", v1 = x_min, v2 = x_max, shup = True)
    X = DD["x"]

    return DD

    


    
    #
    """
    fit_result = fitFermi(x = X, y = Intensity, amplitude = amplitude, fermi_level = fermi_level, temperature = temperature, 
             resolution = resolution, bkgr_offset = bkgr_offset, bkgr_slope = bkgr_slope,
             amplitude_fixed = amplitude_fixed, fermi_level_fixed = fermi_level_fixed, temperature_fixed = temperature_fixed, resolution_fixed = resolution_fixed, bkgr_offset_fixed = bkgr_offset_fixed,
             x_min = x_min, x_max = x_max, 
             fermi_level_min = fermi_level_min, fermi_level_max = fermi_level_max, amplitude_min = amplitude_min, amplitude_max = amplitude_max, temperature_min = temperature_min, temperature_max = temperature_max,
             resolution_min = resolution_min, resolution_max = resolution_max, bkgr_offset_min = bkgr_offset_min, bkgr_offset_max = bkgr_offset_max,
             shup = shup, show_progress = show_progress, hide_plot = True, figsize = (5,3))
    if type(fit_result) is type(None): return {}
    #
    if not hide_plot and len(y) == 0:
        print(Fore.MAGENTA + "\nHave not finished the plotting of the 1d cases.\n")
    #
    if not hide_plot and len(y) > 0:
        fig, ax = plt.subplots(ncols = 2, figsize = (12,4))
        #extent = [X[0], X[-1], Y[-1], Y[0]]
        #ax[0].imshow(intensity[iy[0]:iy[1]][ix[0]:ix[1]], extent = extent, aspect = "auto")
        extent = [x[0], x[-1], y[-1], y[0]]
        ax[0].imshow(intensity, extent = extent, aspect = "auto", cmap = "bone_r", vmin = None, vmax = None)
        ax[0].axvline(x = X[0], linewidth = 0.5, color = "red")
        ax[0].axvline(x = X[-1], linewidth = 0.5, color = "red")

    #
    return fit_result
    """









    """
    data, result = {}, {}
    try: typ = D.get("type", "")
    except:
        print(Fore.RED + f"fitFermiDict(): Argument D must be a dopey dict." + Fore.RESET); return result
    #accepted_dicts = ["arpes", "xps", "1d", "2d_xy"]
    #if not typ in accepted_dicts:
    #    print(Fore.RED + f"fitFermi(): Argument D must be a dopey dict (with data like ARPES or XPS)." + Fore.RESET); return result
    try: z = D["z"]
    except: z = np.array([])
    if len(z) > 0:
        print(Fore.RED + f"fitFermiDict(): Argument D must be a dopey dict (with data like ARPES or XPS)." + Fore.RESET); return result
    try: y = D["y"]
    except: y = np.array([])
    try: x = D["x"]
    except:
        print(Fore.RED + f"fitFermiDict(): Argument D must be a dopey dict (with data like ARPES or XPS)." + Fore.RESET); return result
    #
    if type(x_min) is type(None): x_min = x.min()
    if type(x_max) is type(None): x_max = x.max()
    try: x_min = float(x_min)
    except:
        x_min = x.min()
        print(Fore.MAGENTA + f"fitFermiDict(): Argument x_min must be a value. Setting default x_min = {x_min}" + Fore.RESET)
    try: x_max = float(x_max)
    except:
        x_max = x.max()
        print(Fore.MAGENTA + f"fitFermiDict(): Argument x_max must be a value. Setting default x_max = {x_max}" + Fore.RESET)
    i_min, i_max = abs(x_min - x).argmin(), abs(x_max - x).argmin()+1
    x = x[i_min:i_max]
    data = {"x": x}
    labels = {"x": D["labels"]["x"]}
    ix = [i_min, i_max]
    #
    if len(y) == 0:
        data.update({"intensity": D["intensity"][ix[0]:ix[1]]})
        data.update({"intensity": D["labels"]["intensity"]})
    if len(y) > 0:
        y = D["y"]
        if type(y_min) is type(None): y_min = y.min()
        if type(y_max) is type(None): y_max = y.max()
        try: y_min = float(y_min)
        except:
            y_min = y.min()
            print(Fore.MAGENTA + f"fitFermiDict(): Argument y_min must be a value. Setting default y_min = {y_min}" + Fore.RESET)
        try: y_max = float(y_max)
        except:
            y_max = y.max()
            print(Fore.MAGENTA + f"fitFermiDict(): Argument y_max must be a value. Setting default y_max = {y_max}" + Fore.RESET)
        i_min, i_max = abs(y_min - y).argmin(), abs(y_max - y).argmin()+1
        y = y[i_min:i_max]
        iy = [i_min, i_max]
        #
        data.update({"y": y})
        data.update({"y": D["labels"]["y"]})
        intensity = D["intensity"][iy[0]:iy[1]][ix[0]:ix[1]].sum(axis = 0)
        data.update({"intensity": intensity})
        labels.update({"intensity": D["labels"]["intensity"]})
    result = fitFermi(x = data["x"], y = data["intensity"], amplitude = amplitude, fermi_level = fermi_level, temperature = temperature, 
             resolution = resolution, bkgr_offset = bkgr_offset, bkgr_slope = bkgr_slope,
             amplitude_fixed = amplitude_fixed, fermi_level_fixed = fermi_level_fixed, temperature_fixed = temperature_fixed, resolution_fixed = resolution_fixed, bkgr_offset_fixed = bkgr_offset_fixed,
             x_min = x_min, x_max = x_max, 
             fermi_level_min = fermi_level_min, fermi_level_max = fermi_level_max, amplitude_min = amplitude_min, amplitude_max = amplitude_max, temperature_min = temperature_min, temperature_max = temperature_max,
             resolution_min = resolution_min, resolution_max = resolution_max, bkgr_offset_min = bkgr_offset_min, bkgr_offset_max = bkgr_offset_max,
             shup = shup, show_progress = show_progress, hide_plot = True, figsize = (5,3))
    if not type(result) is dict: return {}
    #
    if not hide_plot:
        if len(y) == 0:
            fig, ax = plt.subplots(ncols = 2, figsize = (10,3))
            ax[0].scatter(D["x"], D["intensity"], s = 5, color = "k")
            if not D["x"][0] == data["x"][0]: ax[0].axvline(x = data["x"][0], linestyle = "--", linewidth = 0.5, color = "k")
            if not D["x"][-1] == data["x"][-1]: ax[0].axvline(x = data["x"][-1], linestyle = "--", linewidth = 0.5, color = "k")
            ax[1].scatter(data["x"], data["intensity"], s = 5, color = "k")
            print(Fore.BLUE + "NOT READY" + Fore.RESET)
        else:
            fig, ax = plt.subplots(ncols = 2, figsize = (10,4))
            extent = [data["x"][0], data["x"][-1], data["y"][-1], data["y"][0]]
            ax[0].imshow(D["intensity"][iy[0]:iy[1]][ix[0]:ix[1]], extent = extent, cmap = "bone_r", aspect = "auto", vmin = None, vmax = None)
            ax[0].invert_yaxis()
    """

    





def fitFermi(x = None, y = None, amplitude = None, fermi_level = None, temperature = None, 
             resolution = None, bkgr_offset = None, bkgr_slope = None,
             amplitude_fixed = False, fermi_level_fixed = False, temperature_fixed = True, resolution_fixed = False, bkgr_offset_fixed = False,
             x_min = None, x_max = None, 
             fermi_level_min = None, fermi_level_max = None, amplitude_min = None, amplitude_max = None, temperature_min = None, temperature_max = None,
             resolution_min = None, resolution_max = None, bkgr_offset_min = None, bkgr_offset_max = None,
             shup = False, show_progress = False, hide_plot = False, figsize = (5,3)):
    """
    Fermi level fit.

    Arguments:
        x                       array       not optional
        y                       array       not optional
        
        amplitude               value       delault y.mean()
        fermi_level             value               x.mean()
        temperature             value               15 K
        resolution              value               0.050 eV
        bkgr_offset             value               0
        bkgr_slope              value/bool          False

        amplitude_fixed         bool        default False
        fermi_level_fixed       bool                False
        temperature_fixed       bool                True
        resolution_fixed        bool                False
        bkgr_offset_fixed       bool                False

        x_min                   value       default x.min()
        x_max                   value               x.max()
        amplitude_min           value               0
        amplitude_max           value               y.max()
        fermi_level_min         value               x_min       
        fermi_level_max         value               x_max
        temperature_min         value               0
        temperature_max         value               500
        resolution_min          value               0.001
        resolution_max          value               1
        temperature_max         value               500
        bkgr_offset_min         value               0
        bkgr_offset_max         value       

        shup                    bool        default False
        show_progress           bool                False
        hide_plot               bool                False

    """
    if not (type(x) is np.ndarray and type(y) is np.ndarray):
        print(Fore.RED + f"fitFermi(): arguments x and y must be numpy arrays." + Fore.RESET)
        return
    if not (len(np.shape(x)) == 1 and len(np.shape(x)) == 1):
        print(Fore.RED + f"fitFermi(): arguments x and y must be 1d numpy arrays." + Fore.RESET)
        return
    if not len(x) == len(y):
        print(Fore.RED + f"fitFermi(): arguments x and y must be 1d numpy arrays of equal size." + Fore.RESET)
        return
    if not len(x) > 4:
        print(Fore.RED + f"fitFermi(): arguments x and y contains too few points." + Fore.RESET)
        return
    if not len(x) > 10:
        print(Fore.MAGENTA + f"fitFermi(): arguments x and y contains very few points..." + Fore.RESET)
        return
    #
    try: amplitude = abs(float(amplitude))
    except:
        amplitude = y.mean()
        if not shup: print(Fore.MAGENTA + f"fitFermi(): Have to guess an initial value for the amplitude. amplitude = {amplitude}" + Fore.RESET)
    #
    try: fermi_level = float(fermi_level)
    except:
        fermi_level = x.mean()
        if not shup: print(Fore.MAGENTA + f"fitFermi(): Have to guess an initial value for the fermi_level. fermi_level = {fermi_level}" + Fore.RESET)
    if not fermi_level >= x.min() and fermi_level <= x.max():
        fermi_level = x.mean()
        if not shup: print(Fore.MAGENTA + f"fitFermi(): The initial value for the fermi_level is outside the energy range. Setting fermi_level = {fermi_level}" + Fore.RESET)
    #
    try: temperature = abs(float(temperature))
    except:
        temperature = 15
        if not shup: print(Fore.MAGENTA + f"fitFermi(): Have to guess an initial value for the temperature. temperature = {temperature}" + Fore.RESET)
    #
    try: resolution = abs(float(resolution))
    except:
        resolution = 0.050
        if not shup: print(Fore.MAGENTA + f"fitFermi(): Have to guess an initial value for the resolution. resolution = {resolution}" + Fore.RESET)
    #
    try: bkgr_offset = float(bkgr_offset)
    except:
        bkgr_offset = y.min()
        if not shup: print(Fore.MAGENTA + f"fitFermi(): Have to guess an initial value for the bkgr_offset. bkgr_offset = {bkgr_offset}" + Fore.RESET)
    #
    BKGR_slope = False
    if type(bkgr_slope) is bool:
        BKGR_slope = bkgr_slope
        bkgr_slope = -1
    else:
        try: 
            bkgr_slope = float(bkgr_slope)
        except:
            bkgr_slope = 0.
        if not bkgr_slope == 0: BKGR_slope = True
    #
    if not type(amplitude_fixed) is bool: amplitude_fixed = False
    if not type(fermi_level_fixed) is bool: fermi_level_fixed = False
    if not type(temperature_fixed) is bool: temperature_fixed = True
    if not type(resolution_fixed) is bool: resolution_fixed = False
    if not type(bkgr_offset_fixed) is bool: bkgr_offset_fixed = False
    #
    if type(x_min) is type(None): x_min = x.min()
    if type(x_max) is type(None): x_max = x.max()
    try: x_min = float(x_min)
    except:
        x_min = x.min()
        if not fermi_level_fixed:
            print(Fore.MAGENTA + f"fitFermi(): Invalid value for x_min. Setting x_min = {x_min}" + Fore.RESET)
    try: x_max = float(x_max)
    except:
        x_max = x.max()
        if not fermi_level_fixed:
            print(Fore.MAGENTA + f"fitFermi(): Invalid value for x_max. Setting x_max = {x_max}" + Fore.RESET)
    if x_min > x_max: x_min, x_max = x_max, x_min
    if x_min < x.min():
        x_min = x.min()
        if not fermi_level_fixed:
            print(Fore.MAGENTA + f"fitFermi(): Argument x_min is out of range. Setting x_min = {x_min}" + Fore.RESET)
    if x_max > x.max():
        x_max = x.max()
        if not fermi_level_fixed:
            print(Fore.MAGENTA + f"fitFermi(): Argument x_max is out of range. Setting x_max = {x_max}" + Fore.RESET)
    if x_min == x_max:
        x_min, x_max = x.min(), x.max()
        if not fermi_level_fixed:
            print(Fore.MAGENTA + f"fitFermi(): Invalid values for x_min and x_max (x_min = x_max). Setting x_min = {x_min}, x_max = {x_max}" + Fore.RESET)
    #
    index1, index2 = abs(x - x_min).argmin(), abs(x - x_max).argmin()
    _x, _y = np.copy(x), np.copy(y)
    x, y = x[index1:index2], y[index1:index2]
    #
    if type(amplitude_min) is type(None): amplitude_min = 0.
    if type(amplitude_max) is type(None): amplitude_max = y.max()
    try: amplitude_min = float(amplitude_min)
    except:
        amplitude_min = 0
        if not amplitude_fixed:
            print(Fore.MAGENTA + f"fitFermi(): Invalid value for amplitude_min. Setting amplitude_min = {amplitude_min}" + Fore.RESET)
    try: amplitude_max = float(amplitude_max)
    except:
        amplitude_max = y.max()
        if not amplitude_fixed:
            print(Fore.MAGENTA + f"fitFermi(): Invalid value for amplitude_max. Setting amplitude_max = {amplitude_max}" + Fore.RESET)
    if amplitude_min < 0:
        amplitude_min = 0
        if not amplitude_fixed:
            print(Fore.MAGENTA + f"fitFermi(): Invalid value for amplitude_min. Setting amplitude_min = {amplitude_min}" + Fore.RESET)
    if amplitude_max < 0:
        amplitude_max = y.max()
        if not amplitude_fixed:
            print(Fore.MAGENTA + f"fitFermi(): Invalid value for amplitude_max. Setting amplitude_max = {amplitude_max}" + Fore.RESET)
    if amplitude_min > amplitude_max:
        if not amplitude_fixed:
            print(Fore.MAGENTA + f"fitFermi(): Switching values for amplitude_min ({amplitude_min}) and  amplitude_max ({amplitude_max})" + Fore.RESET)
        amplitude_min, amplitude_max = amplitude_max, amplitude_min
    #
    if type(fermi_level_min) is type(None): fermi_level_min = x_min
    if type(fermi_level_max) is type(None): fermi_level_max = x_max
    try: fermi_level_min = float(fermi_level_min)
    except:
        fermi_level_min = x_min
        if not fermi_level_fixed:
            print(Fore.MAGENTA + f"fitFermi(): Invalid value for fermi_level_min. Setting fermi_level_min = {fermi_level_min}" + Fore.RESET)
    try: fermi_level_max = float(fermi_level_max)
    except:
        fermi_level_max = x_max
        if not fermi_level_fixed:
            print(Fore.MAGENTA + f"fitFermi(): Invalid value for fermi_level_max. Setting fermi_level_max = {fermi_level_max}" + Fore.RESET)
    if fermi_level_min > fermi_level_max:
        if not fermi_level_fixed:
            print(Fore.MAGENTA + f"fitFermi(): Switching values for fermi_level_min ({fermi_level_min}) and  fermi_level_max ({fermi_level_max})" + Fore.RESET)
        fermi_level_min, fermi_level_max = fermi_level_max, fermi_level_min
    if fermi_level_min < x_min:
        fermi_level_min = x_min
        if not fermi_level_fixed:
            print(Fore.MAGENTA + f"fitFermi(): Invalid value for fermi_level_min. Setting fermi_level_min = {fermi_level_min}" + Fore.RESET)
    if fermi_level_max > x_max:
        fermi_level_max = x_max
        if not fermi_level_fixed:
            print(Fore.MAGENTA + f"fitFermi(): Invalid value for fermi_level_max. Setting fermi_level_max = {fermi_level_max}" + Fore.RESET)
    #
    if type(temperature_min) is type(None): temperature_min = 0.
    if type(temperature_max) is type(None): temperature_max = 500
    try: temperature_min = float(temperature_min)
    except:
        temperature_min = 0
        if not temperature_fixed:
            print(Fore.MAGENTA + "fitFermi(): Invalid value for temperature_min. Setting temperature_min = 0" + Fore.RESET)
    try: temperature_max = float(temperature_max)
    except:
        temperature_max = 500
        if not temperature_fixed:
            print(Fore.MAGENTA + f"fitFermi(): Invalid value for temperature_max. Setting temperature_max = {temperature_max}" + Fore.RESET)
    if temperature_min > temperature_max:
        if not amplitude_fixed:
            print(Fore.MAGENTA + f"fitFermi(): Switching values for temperature_min ({temperature_min}) and  temperature_max ({temperature_max})" + Fore.RESET)
        temperature_min, temperature_max = temperature_max, temperature_min
    if temperature_min < 0:
        temperature_min = 0.
        if not temperature_fixed:
            print(Fore.MAGENTA + f"fitFermi(): Invalid value for temperature_min. Setting temperature_min = {temperature_min}" + Fore.RESET)
    if temperature_max < 0:
        temperature_max = 500.
        if not temperature_fixed:
            print(Fore.MAGENTA + f"fitFermi(): Invalid value for temperature_max. Setting temperature_max = {temperature_max}" + Fore.RESET)   
    #
    if type(resolution_min) is type(None): resolution_min = 0.001
    if type(resolution_max) is type(None): resolution_max = 0.5
    try: resolution_min = float(resolution_min)
    except:
        resolution_min = 0.001
        if not resolution_fixed:
            print(Fore.MAGENTA + "fitFermi(): Invalid value for resolution_min. Setting resolution_min = 0" + Fore.RESET)
    try: resolution_max = float(resolution_max)
    except:
        resolution_max = 0.5
        if not resolution_fixed:
            print(Fore.MAGENTA + f"fitFermi(): Invalid value for resolution_max. Setting resolution_max = {resolution_max}" + Fore.RESET)
    if resolution_min > resolution_max:
        if not resolution_fixed:
            print(Fore.MAGENTA + f"fitFermi(): Switching values for resolution_min ({resolution_min}) and  resolution_max ({resolution_max})" + Fore.RESET)
        resolution_min, resolution_max = resolution_max, resolution_min
    if resolution_min < 0:
        resolution_min = 0
        if not resolution_fixed:
            print(Fore.MAGENTA + f"fitFermi(): Invalid value for resolution_min. Setting resolution_min = {resolution_min}" + Fore.RESET)
    if resolution_max < 0:
        resolution_max = 0.5
        if not resolution_fixed:
            print(Fore.MAGENTA + f"fitFermi(): Invalid value for resolution_max. Setting resolution_max = {resolution_max}" + Fore.RESET)
    #
    if type(bkgr_offset_min) is type(None): bkgr_offset_min = 0
    if type(bkgr_offset_max) is type(None): bkgr_offset_max = 10 * y.min()
    try: bkgr_offset_min = float(bkgr_offset_min)
    except:
        bkgr_offset_min = y.min()
        if not bkgr_offset_fixed:
            print(Fore.MAGENTA + "fitFermi(): Invalid value for bkgr_offset_min. Setting bkgr_offset_min = 0" + Fore.RESET)
    try: bkgr_offset_max = float(bkgr_offset_max)
    except:
        bkgr_offset_max = y.max()
        if not bkgr_offset_fixed:
            print(Fore.MAGENTA + f"fitFermi(): Invalid value for bkgr_offset_max. Setting bkgr_offset_max = {bkgr_offset_max}" + Fore.RESET)
    if bkgr_offset_min > bkgr_offset_max:
        if not bkgr_offset_fixed:
            print(Fore.MAGENTA + f"fitFermi(): Switching values for bkgr_offset_min ({bkgr_offset_min}) and  bkgr_offset_max ({bkgr_offset_max})" + Fore.RESET)
        bkgr_offset_min, bkgr_offset_max = bkgr_offset_max, bkgr_offset_min
    if bkgr_offset_min < 0 or bkgr_offset_min > y.max():
        bkgr_offset_min = 0.
        if not bkgr_offset_fixed:
            print(Fore.MAGENTA + f"fitFermi(): Invalid value for bkgr_offset_min. Setting bkgr_offset_min = {bkgr_offset_min}" + Fore.RESET)
    if bkgr_offset_max > y.max() or bkgr_offset_max < 0:
        bkgr_offset_max = y.max()
        if not bkgr_offset_fixed:
            print(Fore.MAGENTA + f"fitFermi(): Invalid value for bkgr_offset_max. Setting bkgr_offset_max = {bkgr_offset_max}" + Fore.RESET)
    #
    # ---- debug
    debug = {}
    debug.update({"amplitude": amplitude, "amplitude_fixed": amplitude_fixed, "amplitude_min": amplitude_min, "amplitude_max": amplitude_max})
    debug.update({"fermi_level": fermi_level, "fermi_level_fixed": fermi_level_fixed, "fermi_level_min": fermi_level_min, "fermi_level_max": fermi_level_max})
    debug.update({"temperature": temperature, "temperature_fixed": temperature_fixed, "temperature_min": temperature_min, "temperature_max": temperature_max})
    debug.update({"resolution": resolution, "resolution_fixed": resolution_fixed, "resolution_min": resolution_min, "resolution_max": resolution_max})
    debug.update({"bkgr_offset": bkgr_offset, "bkgr_offset_fixed": bkgr_offset_fixed, "bkgr_offset_min": bkgr_offset_min, "bkgr_offset_max": bkgr_offset_max})
    debug.update({"BKGR_slope": BKGR_slope, "bkgr_slope": bkgr_slope})
    if 1 == 2:
        for key in debug.keys(): print(f"{key} = {debug[key]}")
    # ----
    parameters = lmfit_Parameters()
    parameters.add('amplitude',    value = amplitude,    vary = not amplitude_fixed,    min = amplitude_min,    max = amplitude_max)
    parameters.add('fermi_level',  value = fermi_level,  vary = not fermi_level_fixed,  min = fermi_level_min,  max = fermi_level_max)
    parameters.add('temperature',  value = temperature,  vary = not temperature_fixed,  min = temperature_min,  max = temperature_max)
    parameters.add('resolution',   value = resolution,   vary = not resolution_fixed,   min = resolution_min,   max = resolution_max)
    parameters.add('bkgr_offset',  value = bkgr_offset,  vary = not bkgr_offset_fixed,  min = bkgr_offset_min,  max = bkgr_offset_max)
    if BKGR_slope:
        parameters.add("bkgr_slope", value = bkgr_slope, vary = True)
    #
    if show_progress:
        print("\n--- initial parameters")
        for key in parameters.keys():
            print(f"{key} = {parameters[key].value}, limits = {parameters[key].min}, {parameters[key].max}")
        print("---")

    def fitModel(params, x, lin_bkgr):
        T = params['temperature'].value
        dE = params['resolution'].value
        boffset = params['bkgr_offset']
        A = params['amplitude']
        Ef = params["fermi_level"].value
        if lin_bkgr: slope = params["bkgr_slope"].value

        N = 4
        x_width = x[-1] - x[0]
        x_delta = (x[-1] - x[0])/(len(x)-1)

        x_conv = np.arange(-N*x_width, N*x_width, x_delta)
        conv_gauss = np.exp(-4 * np.log(2) * np.power(x_conv / dE, 2))

        x_conv = np.arange(x[0] - N * x_width, x[-1] + N * x_width, x_delta)
        unconv_model = (1 / (np.exp((x_conv - Ef)/(8.617e-5 * T)) + 1)) 

        conv_model = np.convolve(unconv_model, conv_gauss, mode="full")

        trim = int( (len(conv_model) - len(x))/2 )
        conv_model = conv_model[trim: -trim]

        conv_model /= max(conv_model)

        if lin_bkgr: conv_model = conv_model * (1 + (slope * (x - x[-1])))

        conv_model = conv_model * A
        conv_model += boffset

        return conv_model
    #

    def fitModelResiduals(params, x, y, lin_bkgr):
        if show_progress:
            print(f"Ef = {params['fermi_level'].value:7.3f},  A = {params['amplitude'].value:8.1f},    T = {params['temperature'].value:5.1f},   res = {params['resolution'].value:5.3f}")
        return (y - fitModel(params, x, lin_bkgr))
    #

    fit = lmfit_minimize(fitModelResiduals, parameters , args = (x, y, BKGR_slope), method='leastsq')
    #

    result = {"x": x,
              "y": y,
              "y_fit": fitModel(fit.params, x, BKGR_slope),
              "Ef": fit.params["fermi_level"].value,
              "dE": fit.params["resolution"].value,
              "T": fit.params["temperature"].value,
              "lmfit_result": fit,
              "type": "fermi_level_fit"}
    
    if not hide_plot:
        if not type(figsize) is tuple: figsize = (5,3)
        if not len(figsize) == 2: figsize = (5,3)
        fig, ax = plt.subplots(figsize = figsize)
        ax.scatter(x = x, y = y, marker = "x", s = 5, color = "gray")
        ax.plot(x, result["y_fit"], linewidth = 0.85, color = "tab:orange")
        ax.set_xlabel("Energy, eV", fontsize = 10); ax.set_ylabel("Intensity, a.u.", fontsize = 10)
        _ = ax.axvline(x = result["Ef"], linewidth = 0.5, linestyle = "--", color = "tab:blue")
        ax.set_title(f"Ef = {result['Ef']:.3f}, T = {result['T']:.1f}, dE = {result['dE']:.3f}", fontsize = 10)
        fig.tight_layout()

    return result



# ============================================================================================================================================
# ============================================================================================================================================
# ============================================================================================================================================
# ============================================================================================================================================







def removeBackground():
    pass

    

