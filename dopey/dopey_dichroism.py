__version__ = "24.11.22b"
__author__  = "Mats Leandersson"

print(f"{__name__}, {__version__}")




import numpy as np
from colorama import Fore 
import matplotlib.pyplot as plt
import matplotlib as mpl
from copy import deepcopy

try: 
    import ipywidgets as ipw
    from IPython.display import display
except: 
    print(Fore.RED + f'\n{__name__} could not import the ipywidget module and/or display from IPython.display.') 
    print('Interactive plots will not work.\n' + Fore.RESET)

try:
    from dopey.dopey_methods import subArray, compact 
except:
    try:
        from dopey_methods  import subArray, compact
    except:
        print(Fore.RED + f'\n{__name__} could not import the dopey_methods module.' + Fore.RESET)







def plotDichroism(D1 = {}, D2 = {}, shup = False, **kwargs):
    """
    """
    valid_types = ["arpes", "fermi_map", "2d_xy", "2d_xz", "2d_yz"]
    try: type1 = D1.get("type", "none1")
    except: type1 = "none1"
    try: type2 = D2.get("type", "none2")
    except: type2 = "none2"
    if not type1 == type2:
        print(Fore.RED + "plotDichroism(): Arguments D1 and D2 must be dopey dicts of the same type." + Fore.RESET); return
    if not type1 in valid_types:
        print(Fore.RED + f"plotDichroism(): Arguments D1 and D2 must be dopey dicts of the same type. Valids type so far are: {valid_types}" + Fore.RESET); return 
    #
    if not np.array_equal(D1["x"], D2["x"]):
        print(Fore.RED + "plotDichroism(): Arguments D1 and D2 have different energy axes." + Fore.RESET); return
    #
    if type1 == "fermi_map":
        if not np.array_equal(D1["y"], D2["y"]):
            print(Fore.RED + "plotDichroism(): Arguments D1 and D2 have different y angle axes." + Fore.RESET); return
        if not np.array_equal(D1["z"], D2["z"]):
            print(Fore.RED + "plotDichroism(): Arguments D1 and D2 have different x angle axes." + Fore.RESET); return
        _ = _plotDichroism(D1 = D1, D2 = D2, shup = shup, data_type = "fermi_map", **kwargs)
    elif type1 in ["arpes", "2d_xy", "2d_xz", "2d_yz"]:
        if not np.array_equal(D1["y"], D2["y"]):
            print(Fore.RED + "plotDichroism(): Arguments D1 and D2 have different y angle axes." + Fore.RESET); return
        _ = _plotDichroism(D1 = D1, D2 = D2, shup = shup, data_type = type1, **kwargs)

def _plotDichroism(D1 = {}, D2 = {}, shup = False, data_type = "", **kwargs):
    """
    """ 
    valid_data_types_2d = ["arpes", "2d_xy", "2d_xz", "2d_yz"]

    extent1, extent2, extent3 = [], [], []

    SliderVmin = ipw.FloatSlider(min=0, max=100, step = 2, description = 'Imin', value = 0, readout_format = ".0f")
    SliderVmax = ipw.FloatSlider(min=0, max=100, step = 2, description = 'Imax', value = 100, readout_format = ".0f")

    if data_type in valid_data_types_2d:
        ENERGY = D1.get('x')
        ANGLEY = D1.get('y')
        extent1 = [ANGLEY[0], ANGLEY[-1], ENERGY[-1], ENERGY[0]]

        DropdownNorm = ipw.Dropdown(options = ["None", "Total counts", "Per column", "Per row", "Slider"], value = "None", description = "Norm.")

        box_top = ipw.VBox([ipw.HBox([DropdownNorm]),
                            ipw.HBox([SliderVmin, SliderVmax])])

    if data_type == "fermi_map":
        ENERGY = D1.get('x')
        dENERGY = (ENERGY[-1]-ENERGY[0])/len(ENERGY)
        SliderE = ipw.FloatSlider(min=ENERGY[0], max=ENERGY[-1], step = dENERGY, description = 'Energy', value = ENERGY.mean(), readout_format = ".3f")
        SliderDE = ipw.FloatSlider(min=0, max=(ENERGY[-1]-ENERGY[0]), step = dENERGY, description = 'dE', value = 1*dENERGY, readout_format = ".3f")

        ANGLEY = D1.get('y')
        dANGLEY = abs(ANGLEY[1]-ANGLEY[0])
        SliderY = ipw.FloatSlider(min=ANGLEY[0], max=ANGLEY[-1], step = dANGLEY, description = 'Angle Y', value = ANGLEY.mean(), readout_format = ".2f")
        SliderDY = ipw.FloatSlider(min=0, max=(ANGLEY[-1]-ANGLEY[0]), step = dANGLEY, description = 'dY', value = 1*dANGLEY, readout_format = ".2f")

        ANGLEX = D1.get('z')
        dANGLEX = abs(ANGLEX[1]-ANGLEX[0])
        SliderX = ipw.FloatSlider(min=ANGLEX.min(), max=ANGLEX.max(), step = dANGLEX, description = 'Deflection X', value = ANGLEX.mean(), readout_format = ".2f")
        SliderDX = ipw.FloatSlider(min=0, max=(ANGLEX.max()-ANGLEX.min()), step = dANGLEX, description = 'dX', value = dANGLEX, readout_format = ".2f")

        extent1 = [ANGLEX[0], ANGLEX[-1], ANGLEY[-1], ANGLEY[0]] 
        extent2 = [ANGLEY[0], ANGLEY[-1], ENERGY[-1], ENERGY[0]]
        extent3 = [ANGLEX[0], ANGLEX[-1], ENERGY[-1], ENERGY[0]]

        DropdownCut = ipw.Dropdown(options = ["X-Y", "Y-E", "X-E"], value = "X-Y", description = "Cut")
        DropdownNorm = ipw.Dropdown(options = ["None", "Total counts (3D)", "Total counts", "Per column", "Per row", "Slider"], value = "None", description = "Norm.")

        box_top = ipw.VBox([ipw.HBox([SliderE, SliderX, SliderY, SliderVmin, DropdownCut]), 
                            ipw.HBox([SliderDE, SliderDX, SliderDY, SliderVmax, DropdownNorm])])
    
    
    SliderIntenistyRatio = ipw.FloatSlider(min=0.1, max=10, step = 0.1, description = 'Int. ratio', value = 1, readout_format = ".1f")
    
    box_bottom = ipw.VBox([ipw.HBox([SliderIntenistyRatio])])


    def plot(X, Y, E, DX, DY, DE, VMIN, VMAX, CUT, NORM, RATIO):
        fig, ax = plt.subplots(figsize = (14,4), ncols = 3)
        plt.tight_layout()
        #
        map1, map2 = D1["intensity"], D2["intensity"]

        if data_type in valid_data_types_2d:
            map1c = np.copy(map1)
            map2c = np.copy(map2)
            xlabel, ylabel = "Y", "E"
            extent = extent1
            aspect = "auto"

        elif data_type == "fermi_map":
            if CUT == "X-Y":
                indx1, indx2 = abs((E-DE) - ENERGY).argmin(), abs((E+DE) - ENERGY).argmin()
                map1c = map1[:,:,indx1:indx2].sum(axis = 2)
                map2c = map2[:,:,indx1:indx2].sum(axis = 2)
                xlabel, ylabel = "X", "Y"
                extent = extent1
                aspect = "equal"
            elif CUT == "Y-E":
                indx1, indx2 = abs((X-DX) - ANGLEX).argmin(), abs((X+DX) - ANGLEX).argmin()
                map1c = map1[indx1:indx2,:,:].sum(axis = 0)
                map2c = map2[indx1:indx2,:,:].sum(axis = 0)
                xlabel, ylabel = "Y", "E"
                extent = extent2
                aspect = "auto"
            elif CUT == "X-E":
                indx1, indx2 = abs((Y-DX) - ANGLEY).argmin(), abs((Y+DY) - ANGLEY).argmin()
                map1c = map1[:,indx1:indx2,:].sum(axis = 1)
                map2c = map2[:,indx1:indx2,:].sum(axis = 1)
                xlabel, ylabel = "X", "E"
                extent = extent3
                aspect = "auto"
        #
        if NORM == "None":
            pass
        elif NORM == "Total counts (3D)":
            r = map1.sum() / map2.sum()
            map2c *= r
        elif NORM == "Total counts cut":
            r = map1c.sum() / map2c.sum()
            map2c *= r
        elif NORM == "Slider":
            r = map1c.sum() / map2c.sum() * RATIO
            map2c *= r
        elif NORM == "Per column":
            new_map1c = np.zeros(np.shape(map1c))*np.NaN
            new_map2c = np.zeros(np.shape(map2c))*np.NaN
            for i, curve in enumerate(map1c): new_map1c[i] = curve / curve.sum()
            for i, curve in enumerate(map2c): new_map2c[i] = curve / curve.sum()
            map1c, map2c = np.copy(new_map1c), np.copy(new_map2c)
        elif NORM == "Per row":
            new_map1c = np.zeros(np.shape(map1c)).transpose()*np.NaN
            new_map2c = np.zeros(np.shape(map2c)).transpose()*np.NaN
            for i, curve in enumerate(map1c.transpose()): new_map1c[i] = curve / curve.sum()
            for i, curve in enumerate(map2c.transpose()): new_map2c[i] = curve / curve.sum()
            map1c, map2c = np.copy(new_map1c.transpose()), np.copy(new_map2c.transpose())
        #
        map3c = map1c - map2c
        #
        vmin12, vmax12 = min([map1c.min(), map2c.min()]), max([map1c.max(), map2c.max()])
        VMIN12, VMAX12 = np.linspace(vmin12, vmax12, 101)[int(VMIN)], np.linspace(vmin12, vmax12, 101)[int(VMAX)]
        VMIN3, VMAX3 = np.linspace(map3c.min(), map3c.max(), 101)[int(VMIN)], np.linspace(map3c.min(), map3c.max(), 101)[int(VMAX)]
        if VMIN12 >= VMAX12: VMIN12 = 0.99*VMAX12
        if VMIN3 >= VMAX3: VMIN3 = 0.99*VMAX3
        #
        _ = ax[0].imshow(map1c.transpose(), extent = extent, aspect = aspect, cmap = "bone_r", vmin = VMIN12, vmax = VMAX12)
        _ = ax[1].imshow(map2c.transpose(), extent = extent, aspect = aspect, cmap = "bone_r", vmin = VMIN12, vmax = VMAX12)
        _ = ax[2].imshow(map3c.transpose(), extent = extent, aspect = aspect, cmap = "bwr", vmin = VMIN3, vmax = VMAX3)
        for a in ax:
            a.invert_yaxis()
            a.set_xlabel(xlabel)
            a.set_ylabel(ylabel)
        #
        fig.tight_layout()
    
    if data_type in valid_data_types_2d:
        Interact = ipw.interactive_output(plot, {'X': SliderVmin,   # fake
                                                'Y': SliderVmin,    # fake
                                                'E': SliderVmin,    # fake
                                                'DX': SliderVmin,   # fake
                                                'DY': SliderVmin,   # fake
                                                'DE': SliderVmin,   # fake
                                                "VMIN": SliderVmin,
                                                "VMAX": SliderVmax,
                                                "CUT": SliderVmin,  # fake
                                                "NORM": DropdownNorm,
                                                "RATIO": SliderIntenistyRatio})
    if data_type == "fermi_map":
        Interact = ipw.interactive_output(plot, {'X': SliderX, 
                                                'Y': SliderY, 
                                                'E': SliderE, 
                                                'DX': SliderDX,
                                                'DY': SliderDY, 
                                                'DE': SliderDE,
                                                "VMIN": SliderVmin,
                                                "VMAX": SliderVmax,
                                                "CUT": DropdownCut,
                                                "NORM": DropdownNorm,
                                                "RATIO": SliderIntenistyRatio})

    box_out = ipw.VBox([box_top, Interact, box_bottom])
    box_out.layout = ipw.Layout(border="solid 1px gray", margin="5px", padding="2")
    display(box_out)



# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================
# =========================================================================================================================



def dichroism(D1 = {}, D2 = {}, shup = False, **kwargs):
    """
    Arguments: D1 and D2 as the same type of dopey dics (fermi maps or arpes cuts or similar).

    Keyword arguments: For fermi maps the arguments are e1, e2, x1, x2, y1, y2, and norm. For cuts the argument is norm.

    Normalization: pass keyword argument norm as an integer.
        0: no normalization (default)
        1: normalize to total intensity
        2: ratio (also pass keyord argument ratio as a float. the raw intensity in D1 will be 'ratio' times higher than that in D2)
        3: ratio (also pass keyord argument ratio as a float. the summed up intensity in D1 will be 'ratio' times higher than that in D2)
        4: normalize per column (keyword ratio can also be passed as in option 3)
    """
    valid_types = ["arpes", "fermi_map", "2d_xy", "2d_xz", "2d_yz"]
    try: type1 = D1.get("type", "none1")
    except: type1 = "none1"
    try: type2 = D2.get("type", "none2")
    except: type2 = "none2"
    if not type1 == type2:
        print(Fore.RED + "dichroism(): Arguments D1 and D2 must be dopey dicts of the same type." + Fore.RESET); return
    if not type1 in valid_types:
        print(Fore.RED + f"dichroism(): Arguments D1 and D2 must be dopey dicts of the same type. Valids type so far are: {valid_types}" + Fore.RESET); return 
    #
    if not np.array_equal(D1["x"], D2["x"]):
        print(Fore.RED + "dichroism(): Arguments D1 and D2 have different energy axes." + Fore.RESET); return
    #
    if type1 == "fermi_map":
        if not np.array_equal(D1["y"], D2["y"]):
            print(Fore.RED + "dichroism(): Arguments D1 and D2 have different y angle axes." + Fore.RESET); return
        if not np.array_equal(D1["z"], D2["z"]):
            print(Fore.RED + "dichroism(): Arguments D1 and D2 have different x angle axes." + Fore.RESET); return
        return _dichroism3d(D1 = D1, D2 = D2, shup = shup, data_type = "fermi_map", **kwargs)
    elif type1 in ["arpes", "2d_xy", "2d_xz", "2d_yz"]:
        if not np.array_equal(D1["y"], D2["y"]):
            print(Fore.RED + "dichroism(): Arguments D1 and D2 have different y angle axes." + Fore.RESET); return
        return _dichroism2d(D1 = D1, D2 = D2, shup = shup, data_type = type1, **kwargs)




def _dichroism3d(D1 = {}, D2 = {}, shup = False, data_type = "", **kwargs):
    """
    """
    #
    accepted_kwargs = ["axis", "e1", "e2", "x1", "x2", "y1", "y2", "norm"]
    if not shup: print(Fore.BLUE + f"dichroism(): Accepted keyword arguments for this data are {accepted_kwargs}." + Fore.RESET)
    #
    axis =  kwargs.get("axis", "").lower()
    e1 =    kwargs.get("e1", np.NaN)
    e2 =    kwargs.get("e2", np.NaN)
    x1 =    kwargs.get("x1", np.NaN)
    x2 =    kwargs.get("x2", np.NaN)  
    y1 =    kwargs.get("y1", np.NaN)
    y2 =    kwargs.get("y2", np.NaN) 
    #norm = kwargs.get("norm", 0)    # this one goes straight through with the kwargs to the normalization method
    #
    if not axis in ["e", "x", "y"]: 
        axis = "e"
        if not shup: print(Fore.MAGENTA + "dichroism(): Argument axis was not passed. Setting it to default 'e' (energy)." + Fore.RESET)
    #
    if not(np.isnan(e1) or np.isnan(e2)):
        D1c = subArray(D1, axis = "x", v1 = e1, v2 = e2, shup = True)
        D2c = subArray(D2, axis = "x", v1 = e1, v2 = e2, shup = True)
    else: 
        D1c, D2c = deepcopy(D1), deepcopy(D2)
    #
    if not(np.isnan(x1) or np.isnan(x2)):
        D1c = subArray(D1c, axis = "z", v1 = x1, v2 = x2, shup = True)
        D2c = subArray(D2c, axis = "z", v1 = x1, v2 = x2, shup = True)
    #
    if not(np.isnan(y1) or np.isnan(y2)):
        D1c = subArray(D1c, axis = "y", v1 = y1, v2 = y2, shup = True)
        D2c = subArray(D2c, axis = "y", v1 = y1, v2 = y2, shup = True)
    #
    labels = {"x": "", "y": "", "intensity": D1["labels"]["x"]}
    if axis == "e":
        D1c = compact(D1c, axis = "x", shup = True)
        D2c = compact(D2c, axis = "x", shup = True)
    elif axis == "y":
        D1c = compact(D1c, axis = "y", shup = True)
        D2c = compact(D2c, axis = "y", shup = True)
    elif axis == "x":
        D1c = compact(D1c, axis = "z", shup = True)
        D2c = compact(D2c, axis = "z", shup = True)
    #
    
    experiment = D1c["experiment"]
    experiment.update({"Spectrum_ID": 99999})
    ret_dict = {"file_name": "file.xy", "spectrum_id": 99999}
    ret_dict.update({"experiment": experiment, "type": "dichroism"})
    ret_dict.update({"x": D1c["x"], "y": D1c["y"]})
    ret_dict.update({"intensity": np.zeros(np.shape(D1c["intensity"]))*np.NaN, "intensity+": D1c["intensity"], "intensity-": D2c["intensity"]})
    labels = D1c["labels"]
    labels.update({"intensity": "", "intensity+": labels["intensity"], "intensity-": labels["intensity"]})
    ret_dict.update({"labels": labels})
    #
    return _dichroNorm(D = ret_dict, **kwargs)


    



def _dichroism2d(D1 = {}, D2 = {}, shup = False, data_type = "", **kwargs):
    """
    """
    #
    accepted_kwargs = ["norm"]
    if not shup: print(Fore.BLUE + f"dichroism(): Accepted keyword arguments for this data are {accepted_kwargs}." + Fore.RESET)
    #
    experiment = D1["experiment"]
    experiment.update({"Spectrum_ID": 99999})
    ret_dict = {"file_name": "file.xy", "spectrum_id": 99999}
    ret_dict.update({"experiment": experiment, "type": "dichroism"})
    ret_dict.update({"x": D1["x"], "y": D1["y"]})
    ret_dict.update({"intensity": np.zeros(np.shape(D1["intensity"]))*np.NaN, "intensity+": D1["intensity"], "intensity-": D2["intensity"]})
    labels = D1["labels"]
    labels.update({"intensity": "", "intensity+": labels["intensity"], "intensity-": labels["intensity"]})
    ret_dict.update({"labels": labels})
    #
    return _dichroNorm(D = ret_dict, **kwargs)
    



        
def _dichroNorm(D = {}, **kwargs):
    """
    """
    norms = [0, 1, 2, 3, 4, 5]
    ret_dict = deepcopy(D)
    #
    norm = kwargs.get("norm", 0)
    try: norm = int(norm)
    except:
        norm = 0
        print(Fore.MAGENTA + "dichroism(): Keyword argument norm must be an integer. Setting it to default 0 (no normalization)." + Fore.RESET)
    if not norm in norms:
        norm = 0
        print(Fore.MAGENTA + f"dichroism(): Keyword argument norm must one of {norms}. Setting it to default 0 (no normalization). See help for description." + Fore.RESET)
    #
    if norm == 0:
        #do nothing
        pass
    if norm == 1:
        ret_dict.update({"intensity+": ret_dict["intensity+"]/ret_dict["intensity+"].sum()})
        ret_dict.update({"intensity-": ret_dict["intensity-"]/ret_dict["intensity-"].sum()})
    if norm == 2:
        ratio = kwargs.get("ratio", 1.)
        try: ratio = float(ratio)
        except:
            ratio = 1
            print(Fore.MAGENTA + f"dichroism(): Keyword ratio must be a float. Setting it to default 1. (i.e. no change)." + Fore.RESET)
        ret_dict.update({"intensity+": ret_dict["intensity+"] * ratio})
    if norm == 3:
        ratio = kwargs.get("ratio", 1.)
        try: ratio = float(ratio)
        except:
            ratio = 1
            print(Fore.MAGENTA + f"dichroism(): Keyword ratio must be a float. Setting it to default 1. (i.e. no change)." + Fore.RESET)
        ret_dict.update({"intensity+": ret_dict["intensity+"]/ret_dict["intensity+"].sum()})
        ret_dict.update({"intensity-": ret_dict["intensity-"]/ret_dict["intensity-"].sum()})
        ret_dict.update({"intensity+": ret_dict["intensity+"] * ratio})
    if norm == 4:
        ratio = kwargs.get("ratio", 1.)
        try: ratio = float(ratio)
        except:
            ratio = 1
            print(Fore.MAGENTA + f"dichroism(): Keyword ratio must be a float. Setting it to default 1. (i.e. no change)." + Fore.RESET)
        int1 = np.zeros(np.shape(ret_dict["intensity"]))*np.NaN
        int2 = np.copy(int1)
        for i, curve in enumerate(ret_dict["intensity+"]): int1[i] = curve / curve.sum()
        for i, curve in enumerate(ret_dict["intensity-"]): int2[i] = curve / curve.sum()
        ret_dict.update({"intensity+": int1*ratio, "intensity-": int2})
    if norm == 5:
        ratio = kwargs.get("ratio", 1.)
        try: ratio = float(ratio)
        except:
            ratio = 1
            print(Fore.MAGENTA + f"dichroism(): Keyword ratio must be a float. Setting it to default 1. (i.e. no change)." + Fore.RESET)
        int1 = np.zeros(np.shape(ret_dict["intensity"].transpose()))*np.NaN
        int2 = np.copy(int1)
        for i, curve in enumerate(ret_dict["intensity+"].transpose()): int1[i] = curve / curve.sum()
        for i, curve in enumerate(ret_dict["intensity-"].transpose()): int2[i] = curve / curve.sum()
        ret_dict.update({"intensity+": int1.transpose()*ratio, "intensity-": int2.transpose()})
    #
    ret_dict.update({"intensity": ret_dict["intensity+"] - ret_dict["intensity-"]})
    return ret_dict

