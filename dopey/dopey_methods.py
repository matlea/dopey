__version__ = "24.12.05"
__author__  = "Mats Leandersson"

print(f"{__name__}, {__version__}")

import numpy as np
import scipy as sp
from colorama import Fore
import copy
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon, Circle, Ellipse, Rectangle


try: 
    from dopey.dopey_constants import CCD_ANALYZERS, SPIN_ANALYZERS, DEFLECTORS, DATA_AXES, DATA_INTENSITIES
    DEFLECTORX, DEFLECTORY = DEFLECTORS[0], DEFLECTORS[1]
except:
    try:
        from dopey_constants import CCD_ANALYZERS, SPIN_ANALYZERS, DELFECTORS, DATA_AXES, DATA_INTENSITIES
        DEFLECTORX, DEFLECTORY = DEFLECTORS[0], DEFLECTORS[1]
    except: 
        print(Fore.RED + "dopey_loader.py: coluld not import from dopey_constants.py" + Fore.RESET)
        DEFLECTORX, DEFLECTORY = "", ""


try: 
    import ipywidgets as ipw
    from IPython.display import display
except: 
    print(Fore.RED + f'\n{__name__} could not import the ipywidget module and/or display from IPython.display.') 
    print('Interactive plots will not work.\n' + Fore.RESET)

# ==================================================================================================
# ==================================================================================================
# ==================================================================================================


def subArray(D = {}, axis = "", v1 = None, v2 = None, v = None, dv = None, i1 = None, i2 = None, shup = False):
    """
    """
    if not type(D) is dict:
        print(Fore.RED + "subArray(): Argument D must be a dopey dict. {}" + Fore.RESET)
        return D
    if not "type" in D:
        print(Fore.RED + "subArray(): Argument D must be a dopey dict (did not find key 'type')." + Fore.RESET)
        return D
    #
    if not type(axis) is str:
        print(Fore.RED + "subArray(): Argument axis must be a string ('x', 'y', or 'z' if applicable.)." + Fore.RESET)
        print(Fore.RED + "            Setting default axis = 'x'" + Fore.RESET)
        axis = "x"
    #
    axis = axis.lower()
    if not axis in ["x", "y", "z"]:
        print(Fore.RED + "subArray(): Argument axis must be a string ('x', 'y', or 'z' if applicable)." + Fore.RESET)
        print(Fore.RED + "            Setting default axis = 'x'" + Fore.RESET)
        axis = "x"
    #
    if not axis in D:
        print(Fore.RED + f"subArray(): axis = '{axis}' is not applicable for this data ({D['Type']})." + Fore.RESET)
        return D
    #
    m = 0
    try: v1, v2, m = float(v1), float(v2), 1
    except:
        try: v, dv, m = float(v), float(dv), 2
        except:
            try: i1, i2, m = float(i1), float(i2), 3
            except:
                pass
    if m == 0:
        print(Fore.RED + f"subArray(): You must provide a pair of arguments. The alternatives:" + Fore.RESET)
        print(Fore.RED + f"            1. a range from v1 to v2" + Fore.RESET)
        print(Fore.RED + f"            2. a range from v-dv/2 to v+dv/2" + Fore.RESET)
        print(Fore.RED + f"            3. a range from from index i1 to i2" + Fore.RESET)
        return D 
    #
    ax = D[axis]
    if m == 1:
        indx1, indx2 = abs(ax - v1).argmin(), abs(ax - v2).argmin()
        if indx1 > indx2: indx1, indx2 = indx2, indx1
    if m == 2:
        indx1, indx2 = abs(ax - (v-dv/2)).argmin(), abs(ax - (v+dv/2)).argmin()
        if indx1 > indx2: indx1, indx2 = indx2, indx1
    if m == 3:
        if i1 < 0: i1 = 0
        if i2 < 0: i2 = 0
        if i1 >= len(ax): i1 = len(ax) - 1
        if i2 >= len(ax): i2 = len(ax) - 1
        if i1 > i2: i1, i2 = i2, i1
        indx1, indx2 = i1, i2
    if indx1 == indx2:
        if indx2 < len(ax) - 1: indx2 += 1
        else: indx1 -= 1
    #
    newD = copy.deepcopy(D)
    #
    if D["experiment"]["Analyzer"] in CCD_ANALYZERS:
        if len(np.shape(newD["intensity"])) == 1:
            newD.update({"x": newD["x"][indx1:indx2]})  
            newD.update({"intensity": newD["intensity"][indx1:indx2]})
        if len(np.shape(newD["intensity"])) == 2:
            if axis == "x":  
                newD.update({"x": newD["x"][indx1:indx2]})  
                newD.update({"intensity": newD["intensity"][:,indx1:indx2]})
            elif axis == "y":
                newD.update({"y": newD["y"][indx1:indx2]})  
                newD.update({"intensity": newD["intensity"][indx1:indx2, :]})
        elif len(np.shape(newD["intensity"])) == 3:
            if axis == "x":  
                newD.update({"x": newD["x"][indx1:indx2]})  
                newD.update({"intensity": newD["intensity"][:,:,indx1:indx2]})
            elif axis == "y":  
                newD.update({"y": newD["y"][indx1:indx2]})  
                newD.update({"intensity": newD["intensity"][:,indx1:indx2,:]})
            elif axis == "z":  
                newD.update({"z": newD["z"][indx1:indx2]})  
                newD.update({"intensity": newD["intensity"][indx1:indx2,:,:]})
    #
    elif D["experiment"]["Analyzer"] in SPIN_ANALYZERS:
        if len(np.shape(newD["intensity"])) == 2:
            newD.update({"x": newD["x"][indx1:indx2]})  
            newD.update({"intensity": newD["intensity"][:,indx1:indx2]})
            newD.update({"intensity_avg": newD["intensity_avg"][:,indx1:indx2]})
        if len(np.shape(newD["intensity"])) == 3:
            if axis == "x":
                newD.update({"x": newD["x"][indx1:indx2]})  
                newD.update({"intensity": newD["intensity"][:,:,indx1:indx2]})
                newD.update({"intensity_mean": newD["intensity_mean"][:,:,indx1:indx2]})
            if axis == "y":
                newD.update({"y": newD["y"][indx1:indx2]})  
                newD.update({"intensity": newD["intensity"][:,indx1:indx2,:]})
                newD.update({"intensity_mean": newD["intensity_mean"][:,indx1:indx2,:]})
        if len(np.shape(newD["intensity"])) == 4:
            if axis == "x":
                newD.update({"x": newD["x"][indx1:indx2]})  
                newD.update({"intensity": newD["intensity"][:,:,:,indx1:indx2]})
                newD.update({"intensity_mean": newD["intensity_mean"][:,:,:,indx1:indx2]})
            if axis == "y":
                newD.update({"y": newD["y"][indx1:indx2]})  
                newD.update({"intensity": newD["intensity"][:,:,indx1:indx2,:]})
                newD.update({"intensity_mean": newD["intensity_mean"][:,:,indx1:indx2,:]})
            if axis == "z":
                newD.update({"z": newD["z"][indx1:indx2]})  
                newD.update({"intensity": newD["intensity"][:,indx1:indx2,:,:]})
                newD.update({"intensity_mean": newD["intensity_mean"][:,indx1:indx2,:,:]})
    #
    else:
        print(Fore.RED + f"subArray(): This data was collected with an 'analyzer' I don't recognize. Sorry." + Fore.RESET)
    #
    return newD



# ============================================================================================ 
# ============================================================================================
# ============================================================================================


def compact(D = {}, axis = "", shup = False):
    """
    """
    if not type(D) is dict:
        print(Fore.RED + "compact(): Argument D must be a dopey dict." + Fore.RESET)
        return D
    if not "type" in D:
        print(Fore.RED + "compact(): Argument D must be a dopey dict." + Fore.RESET)
        return D
    #
    if not type(axis) is str:
        print(Fore.RED + "compact(): Argument axis must be a string ('x', 'y', or 'z' if applicable.)." + Fore.RESET)
        print(Fore.RED + "           Setting default axis = 'x'" + Fore.RESET)
        axis = "x"
    #
    axis = axis.lower()
    if not axis in ["x", "y", "z", "p"]:
        print(Fore.RED + "compact(): Argument axis must be a string ('x', 'y', or 'z' if applicable)." + Fore.RESET)
        print(Fore.RED + "           Setting default axis = 'x'" + Fore.RESET)
        axis = "x"
    #
    if not axis in D:
        print(Fore.RED + f"compact(): axis = '{axis}' is not applicable for this data ({D['type']})." + Fore.RESET)
        return D
    #
    # ------
    #
    newD = copy.deepcopy(D)
    #
    if newD["experiment"]["Analyzer"] in CCD_ANALYZERS:
        if len(np.shape(newD["intensity"])) == 1:
            print(Fore.MAGENTA + f"compact(): Not much to compact with 1d data..." + Fore.RESET)
            return newD
        #
        elif len(np.shape(newD["intensity"])) == 2:
            labels = newD.get("labels")
            if axis == "x":
                newD.update({"intensity": D["intensity"].sum(axis = 1)})
                newD.update({"x": D["y"]})
                del newD["y"]
                labels.update({"x": labels["y"]})
                del labels["y"]
            elif axis == "y":
                newD.update({"intensity": D["intensity"].sum(axis = 0)})
                del newD["y"]
                del labels["y"]
            newD.update({"labels": labels})
            newD.update({"type": "1d"})
        #
        elif len(np.shape(newD["intensity"])) == 3:
            labels = D.get("labels")
            if axis == "x":
                newD.update({"intensity": D["intensity"].sum(axis = 2)})
                newD.update({"x": D["y"]})
                newD.update({"y": D["z"]})
                del newD["z"] #
                labels.update({"x": labels["y"]})
                labels.update({"y": labels["z"]})
                del labels["z"]
                newD.update({"type": "2d_yz"})
            if axis == "y":
                newD.update({"intensity": D["intensity"].sum(axis = 1)})
                #newD.update({"x": D["x"]})
                newD.update({"y": D["z"]})
                del newD["z"]
                #labels.update({"x": labels["x"]})
                labels.update({"y": labels["z"]})
                del labels["z"]
                newD.update({"type": "2d_xz"})
            if axis == "z":
                newD.update({"intensity": D["intensity"].sum(axis = 0)})
                #newD.update({"x": D["x"]})
                #newD.update({"y": D["y"]})
                del newD["z"]
                #labels.update({"x": labels["x"]})
                #labels.update({"y": labels["z"]})
                del labels["z"]
                newD.update({"type": "2d_xy"})
            newD.update({"labels": labels})

    elif D["experiment"]["Analyzer"] in SPIN_ANALYZERS:
        print(Fore.MAGENTA + f"compact(): I have not found a reason for readying this method for spin data" + Fore.RESET)
        print(Fore.MAGENTA + f"           but you apparently have. Please let me know. Thanks." + Fore.RESET)
    
    else:
        print(Fore.RED + f"compact(): This data was collected with an 'analyzer' I don't recognize. Sorry." + Fore.RESET)

    return newD





# ============================================================================================ 
# ============================================================================================
# ============================================================================================


def secondDerivative(D = {}, axis = "x", shup = False, **kwargs):
    """
    """
    result = copy.deepcopy(D)

    #
    if not(type(D) is dict):
        print(Fore.RED + "secondDerivative(): Argument D must be a dopey dict." + Fore.RESET); return result
    #if not D.get("Type", "") in ["arpes", "xps", "1d", "2d_xy", "2d_xz", "2d_yz"]:
    #    print(Fore.RED + "secondDerivative(): The method is not prepared for this type of data. Please ask/inform the staff." + Fore.RESET); return result
    if not D.get("experiment", {}).get("Analyzer", "") in CCD_ANALYZERS:
        print(Fore.RED + "secondDerivative(): The method is not prepared for this type of data. Please ask/inform the staff." + Fore.RESET); return result
    #
    axes, axes_labels = [], []
    for a in ["x", "y", "z"]:
        if a in D.keys():
            axes.append(a)
            axes_labels.append(D.get("labels", {}).get(a, ""))
    if len(axes) == 0:
        print(Fore.RED + "secondDerivative(): I did not find any axes in this data." + Fore.RESET); return result
    if not shup:
        print(Fore.BLUE + f"secondDerivative(): I found {len(axes)} axis/axes, {axes}, is the data. One of them is passed as argument axis." + Fore.RESET)
        for a, alab in zip(axes, axes_labels):
            print(Fore.BLUE + f"                    {a} : {alab}" + Fore.RESET)
    if not type(axis) is str:
        print(Fore.MAGENTA + f"secondDerivative(): Argument axis must be a string. Setting it to the first axis I found in the data: {axes[0]}" + Fore.RESET)
        axis = axes[0]
    if not axis in axes:
        print(Fore.MAGENTA + f"secondDerivative(): {axis} is not a valid value for argument axis. Setting it to the first axis I found in the data: {axes[0]}" + Fore.RESET)
        axis = axes[0]
    #
    intensity = D.get("intensity", [])
    if axis == "x": daxis = 0
    elif axis == "y": daxis = 1
    elif axis == "z": daxis = 2
    else:
        print(Fore.RED + "secondDerivative(): Unexpected error, most likely due to sloppy coding." + Fore.RESET); return result
    dintensity = np.diff(intensity, n = 1, axis = daxis, append = 0)
    dintensity = np.diff(dintensity, n = 1, axis = daxis, append = 0)
    #
    result.update({"intensity": dintensity})
    labels = D.get("labels", {})
    labels.update({"intensity": "2nd derivative of the intensity"})
    result.update({"labels": labels})
    return result



# ============================================================================================ 
# ============================================================================================
# ============================================================================================


def shiftAxis(D = {}, axis = "x", shift = 0, shup = False):
    """
    """

    try: data_type = D.get("type", "")
    except: data_type = ""
    if data_type == "":
        print(Fore.RED + "shiftAxis(): Argument D must be a dopey dict." + Fore.RESET); return D
    try: axis = axis.lower()
    except:
        print(Fore.BLUE + "shiftAxis(): Argument axis must be a string. Axes found is this data dict are:")
        for a in ["x", "y", "z"]:
            if a in D.keys(): print(Fore.BLUE + f"             {a}" + Fore.RESET)
        return D
    try: Axis = D.get(axis, np.array([]))
    except: Axis = np.array([])
    if len(Axis) == 0:
        print(Fore.RED + f"shiftAxis(): Axis '{axis}' does not exist in this data dict. Existing axes:")
        for a in ["x", "y", "z"]:
            if a in D.keys(): print(Fore.BLUE + f"             {a}" + Fore.RESET)
        return D
    try: shift = float(shift)
    except:
        print(Fore.RED + "shiftAxis(): The argument shift must be a scalar value." + Fore.RESET); return D 
    #
    DD = copy.deepcopy(D)
    DD.update({axis: Axis + shift})
    return DD



# ============================================================================================ 
# ============================================================================================
# ============================================================================================

def getIntensity(D = {}, shup = True):
    """
    """
    try: typ = D["type"]
    except:
        print(Fore.RED + "getIntensity(): Argument D must be a dopey dict." + Fore.RESET); return {}
    #
    intensity = D["intensity"]
    #
    if typ in ["XPS", "ARPES"]:
        return {"total": intensity.sum(),
                "min": intensity.min(),
                "max": intensity.max()}
    
    elif typ in ["fermi_map"]:
        return {"total": intensity.sum(),
                "min": intensity.min(),
                "max": intensity.max()}
    
    elif typ in ["spin_edc"]:
        DD = {}
        return {}






# ============================================================================================ 
# ============================================================================================
# ============================================================================================


def align(D = {}, shup = False, **kwargs):
    """
    """
    if not type(D) is dict: D = {}
    typ = D.get("type", "")
    if not typ == "fermi_map":
        print(Fore.RED + "align(): Argument D must be a dopy dict containing a Fermi map." + Fore.RESET); return
    #
    cmap = kwargs.get("cmap", "bone_r")
    #
    ENERGY, ANGLEX, ANGLEY = D.get("x", np.array([])), D.get("z", np.array([])), D.get("y", np.array([]))
    DE = (ENERGY[-1] - ENERGY[0]) / (len(ENERGY) -1)
    DAX = (ANGLEX[-1] - ANGLEX[0]) / (len(ANGLEX) -1)
    DAY = (ANGLEY[-1] - ANGLEY[0]) / (len(ANGLEY) -1)

    SliderE = ipw.FloatSlider(min=ENERGY[0], max=ENERGY[-1], step = DE, description = 'Energy', value = ENERGY.mean(), readout_format = ".3f")
    SliderDE = ipw.FloatSlider(min=0, max=20*DE, step = DE, description = 'dE', value = 1*DE, readout_format = ".3f")
    extent = [ANGLEX[0], ANGLEX[-1], ANGLEY[-1], ANGLEY[0]]

    SliderVmin = ipw.FloatSlider(min=0, max=D["intensity"].max(), step = D["intensity"].max()/20, description = 'Imin', value = 0, readout_format = ".1f")
    SliderVmax = ipw.FloatSlider(min=0, max=D["intensity"].max(), step = D["intensity"].max()/20, description = 'Imax', value = D["intensity"].max(), readout_format = ".1f")

    DropdownFigure = ipw.Dropdown(options = ["Cross", "Square", "Rectangle", "Hexagon", "Ellipse", "Circle"], value = "Hexagon", description = "Shape")
    SliderX = ipw.FloatSlider(min = ANGLEX[0], max = ANGLEX[-1], step = DAX, description = 'X', value = ANGLEX.mean(), readout_format = ".2f")
    SliderY = ipw.FloatSlider(min = ANGLEY[0], max = ANGLEY[-1], step = DAY, description = 'Y', value = ANGLEY.mean(), readout_format = ".2f")
    SliderA = ipw.FloatSlider(min = -90, max = 90, step = 1, description = 'Angle', value = 0, readout_format = ".1f")
    SliderS = ipw.FloatSlider(min = 0, max = 15, step = 0.1, description = 'Size', value = 5, readout_format = ".1f")
    SliderS2 = ipw.FloatSlider(min = 0, max = 15, step = 0.1, description = 'Size2', value = 5, readout_format = ".1f")

    vbox1 = ipw.VBox([SliderE, SliderDE])
    vbox2 = ipw.VBox([DropdownFigure, SliderX, SliderY, SliderA, SliderS, SliderS2])
    vbox3 = ipw.VBox([SliderVmin, SliderVmax])
    vbox = ipw.VBox([vbox1, vbox2, vbox3])
    

    def plot(E, DE, VMIN, VMAX, X, Y, A, S, S2, Figure):
        fig, ax = plt.subplots(figsize = (7,7))
        plt.tight_layout()
        #
        if VMIN > VMAX: VMIN = VMAX
        #
        XY = compact(D = subArray(D = D, axis = "x", v1 = E-DE/2, v2 = E+DE/2, shup = True), axis = 'x', shup = True)
        _ = ax.imshow(XY['intensity'].transpose(), extent = extent, aspect = 'equal', cmap = cmap, vmin = VMIN, vmax = VMAX)
        #
        #slider_vmin = np.min([XY["intensity"].min(), YE["intensity"].min(), XE["intensity"].min()])
        #slider_vmax = np.min([XY["intensity"].max(), YE["intensity"].max(), XE["intensity"].max()])
        #SliderVmin.min, SliderVmin.max = slider_vmin, slider_vmax
        #SliderVmax.min, SliderVmax.max = slider_vmin, slider_vmax
        #
        #if VMIN > VMAX: VMIN = VMAX
        #VMIN, VMAX = None, None
        ax.invert_yaxis()

        if Figure == "Cross":
            x1, y1 = X + S * np.sin(np.deg2rad(A)), Y + S * np.cos(np.deg2rad(A))
            x2, y2 = X - S * np.sin(np.deg2rad(A)), Y - S * np.cos(np.deg2rad(A))
            ax.plot([x1, x2], [y1, y2], color = "tab:red")
            x1, y1 = X + S2 * np.sin(np.deg2rad(A+90)), Y + S2 * np.cos(np.deg2rad(A+90))
            x2, y2 = X - S2 * np.sin(np.deg2rad(A+90)), Y - S2 * np.cos(np.deg2rad(A+90))
            ax.plot([x1, x2], [y1, y2], color = "tab:red")
        elif Figure == "Square":
            polygon = RegularPolygon((X, Y), numVertices=4, radius=S, orientation = -np.deg2rad(A+45), alpha=0.2, edgecolor='k', facecolor = "tab:red")
            ax.add_patch(polygon)
        elif Figure == "Rectangle":
            polygon = Rectangle((X, Y), width = 2*S, height = 2*S2, angle = -A, alpha=0.2, edgecolor='k', facecolor = "tab:red")
            ax.add_patch(polygon)
        elif Figure == "Hexagon":
            polygon = RegularPolygon((X, Y), numVertices=6, radius=S, orientation = -np.deg2rad(A+30), alpha=0.2, edgecolor='k', facecolor = "tab:red")
            ax.add_patch(polygon)
        elif Figure == "Ellipse":
            ellipse = Ellipse((X, Y), width = 2*S, height = 2*S2, angle = -A, alpha=0.2, edgecolor='k', facecolor = "tab:red")
            ax.add_patch(ellipse)
        elif Figure == "Circle":
            circle = Circle((X, Y), radius=S, alpha=0.2, edgecolor='k', facecolor = "tab:red")
            ax.add_patch(circle)
        
        s = 0.5
        x1, y1 = X + s * np.sin(np.deg2rad(A)), Y + s * np.cos(np.deg2rad(A))
        x2, y2 = X - s * np.sin(np.deg2rad(A)), Y - s * np.cos(np.deg2rad(A))
        ax.plot([x1, x2], [y1, y2], color = "tab:red", linewidth = 0.5)
        x1, y1 = X + s * np.sin(np.deg2rad(A+90)), Y + s * np.cos(np.deg2rad(A+90))
        x2, y2 = X - s * np.sin(np.deg2rad(A+90)), Y - s * np.cos(np.deg2rad(A+90))
        ax.plot([x1, x2], [y1, y2], color = "tab:red", linewidth = 0.5)


        #
        ax.set_xlabel('X (°)')
        ax.set_ylabel('Y (°)')
        #
        ax.set_title("ID {0}".format(D.get('experiment', {}).get('Spectrum_ID', '')))
        fig.tight_layout()
    
    Interact = ipw.interactive_output(plot, {'E': SliderE, 
                                             'DE': SliderDE, 
                                             "VMIN": SliderVmin,
                                             "VMAX": SliderVmax,
                                             "X": SliderX,
                                             "Y": SliderY,
                                             "A": SliderA,
                                             "S": SliderS,
                                             "S2": SliderS2,
                                             "Figure": DropdownFigure})
    
    box_out = ipw.HBox([Interact, vbox])
    box_out.layout = ipw.Layout(border="solid 1px gray", margin="5px", padding="2")
    display(box_out)



# ============================================================================================ 
# ============================================================================================
# ============================================================================================



def gaussianSmooth(D = None, sigma = None, shup = False, **kwargs):
    """
    """
    if type(D) is dict:
        if D.get("type", "") == "":
            print(Fore.RED + "gaussianSmooth(): Argument D must be a dopey dict or array." + Fore.RESET); return D
        return _gaussianSmooth_dopeyDict(D = D, sigma = sigma, shup = shup, **kwargs)
    elif type(D) is np.ndarray:
        if len(D) == 0:
            print(Fore.RED + "gaussianSmooth(): Argument D must be a dopey dict or array (of non-zero size!)." + Fore.RESET); return D
        return _gaussianSmooth_array(D = D, sigma = sigma, shup = shup, **kwargs)
    else:
        print(Fore.RED + "gaussianSmooth(): Argument D must be a dopey dict or array." + Fore.RESET); return D


def _gaussianSmooth_array(D = None, sigma = None, shup = False, **kwargs):
    """"""
    if not (type(sigma) is list or type(sigma) is np.ndarray):
        try: sigma = np.array([float(sigma)])
        except:
            print(Fore.MAGENTA + "gaussianSmooth(): Argument sigma must be a scalar or list of scalars." + Fore.RESET)
            print(Fore.MAGENTA + "                  Setting sigma = 3." + Fore.RESET)
            sigma = np.array([3])
    for s in sigma:
        try: s = float(s)
        except:
            print(Fore.MAGENTA + "gaussianSmooth(): Argument sigma must be a scalar or list of scalars." + Fore.RESET)
            print(Fore.MAGENTA + "                  Setting sigma = 3." + Fore.RESET)
            sigma = np.array([3])
    if len(sigma) > 1:
        if not len(sigma) == np.len(np.shape(D)):
            print(Fore.MAGENTA + "gaussianSmooth(): Argument sigma, when passed as a list, must have the same number of " + Fore.RESET)
            print(Fore.MAGENTA + "                  elements as the array dimension. Setting sigma = 3." + Fore.RESET)
            sigma = np.array(3)
    if len(sigma) == 1: sigma = sigma[0]
    return sp.ndimage.filters.gaussian_filter(D, sigma, mode = 'constant')
    
    

def _gaussianSmooth_dopeyDict(D = None, sigma = None, shup = False, **kwargs):
    """"""
    if "result" in D.get("type", ""):
         print(Fore.RED + "gaussianSmooth(): This method is not ready for result dicts. Work in progress." + Fore.RESET); return D
    else: TYPE = D.get("type", "")
    if TYPE == "":
        print(Fore.RED + "gaussianSmooth(): Could not determine what kind of dopey data this is. Sorry." + Fore.RESET); return D
    #
    if not "spin" in TYPE:
        intensity = _gaussianSmooth_array(D = D["intensity"], sigma = sigma, shup = shup, **kwargs)
        newD = copy.deepcopy(D)
        newD.update({"intensity": intensity})
    else:
        newD = copy.deepcopy(D)
        IntensitiesM, IntensitiesP = [], []
        for intensity in D["intensity"][0]: IntensitiesM.append( _gaussianSmooth_array(D = intensity, sigma = sigma, shup = shup, **kwargs) )
        for intensity in D["intensity"][0]: IntensitiesP.append( _gaussianSmooth_array(D = intensity, sigma = sigma, shup = shup, **kwargs) )
        IntensitiesM, IntensitiesP = np.array(IntensitiesM), np.array(IntensitiesP)
        newD.update({"intensity": [IntensitiesM, IntensitiesP]})
        newD.update({"intensity_mean": [np.mean(IntensitiesM, axis = 0), np.mean(IntensitiesP, axis = 0)]})
    return newD

    








# ============================================================================================ 
# ============================================================================================
# ============================================================================================
# ============================================================================================ 
# ============================================================================================
# ============================================================================================


# ====================================================== Gaussians

def gaussian(x = np.linspace(-1,1,100), *p):
    """
    p[0] * np.exp( -(x-p[1])**2 / (2*p[2]**2)) + p[3]*x + p[4]
    """
    try:
        A, mu, s, k, m = p
    except:
        print(Fore.RED + "gaussian(x = 0, *p): Expected 5 parameters." + Fore.RESET)
        print(Fore.RED + "                     p0 * np.exp( -(x-p1)**2 / (2*p2**2)) + p3*x + p4" + Fore.RESET)
        print(Fore.RED + "                     p1 being µ and p2 being the standard deviation and p3 and p4 a linear background." + Fore.RESET)
        print(Fore.RED + "                     Setting the parameters to default 1, 0, 0.1, 0, 0" + Fore.RESET)
        A, mu, s, k, m = 1., 0., 0.1, 0., 0.
    return A * np.exp( -(x-mu)**2 / (2*s**2)) + k*x + m


def gaussian2(x = np.linspace(-1,1,100), *p):
    """
    p0 * np.exp( -(x-p1)**2 / (2*p2**2)) + p3 * np.exp( -(x-p4)**2 / (2*p5**2)) + p6*x + p7
    """
    try:
        A1, mu1, s1, A2, mu2, s2, k, m = p
    except:
        print(Fore.RED + "gaussian2(x = 0, *p): Expected 8 parameters." + Fore.RESET)
        print(Fore.RED + "                      p0 * np.exp( -(x-p1)**2 / (2*p2**2)) + p3 * np.exp( -(x-p4)**2 / (2*p5**2)) + p6*x + p7" + Fore.RESET)
        print(Fore.RED + "                      p1 and p2 being µ and standard deviation for peak one, and p4 and p5 dito for peak two," + Fore.RESET)
        print(Fore.RED + "                      and p6 and p7 a linear background." + Fore.RESET)
        print(Fore.RED + "                      Setting the parameters to default 1, -0.5, 0.1, 1, 0.5, 0.1, 0, 0" + Fore.RESET)
        A1, mu1, s1, A2, mu2, s2, k, m = 1, -0.5, 0.1, 1, 0.5, 0.1, 0, 0
    return A1 * np.exp( -(x-mu1)**2 / (2*s1**2)) + A2 * np.exp( -(x-mu2)**2 / (2*s2**2)) + k*x + m


def fitGaussian(x = None, y = None, *p):
    """
    """
    res = {"x": np.array([]),
           "y": np.array([]),
           "yfit": np.array([]),
           "par": (np.NaN, np.NaN, np.NaN, np.NaN, np.NaN),
           "cov": (),
           "function": gaussian
           }
    if type(x) is type(None) or type(y) is type(None):
        print(Fore.RED + "fitGaussian(): Pass x and y as arrays." + Fore.RESET); return res
    if not (type(x) is np.ndarray or type(x) is list or type(y) is list or type(y) is np.ndarray):
        print(Fore.RED + "fitGaussian(): Pass x and y as arrays." + Fore.RESET); return res
    x, y = np.array(x), np.array(y)
    if not len(x) == len(y):
        print(Fore.RED + "fitGaussian(): The x array and the y array must have the same size." + Fore.RESET); return res
    if len(x) == 0:
        print(Fore.RED + "fitGaussian(): The x array and the y array can't be of length 0." + Fore.RESET); return res
    #
    par, cov = curve_fit(gaussian, x, y, p0 = p)
    yfit = gaussian(x, *par)
    res.update({"x": x, "y": y, "yfit": yfit, "par": tuple(par), "cov": cov})
    return res


def fitGaussian2(x = None, y = None, *p):
    """
    Argument x and y are arrays. 
    """
    res = {
            "type": "fit_gaussian2",
            "x": np.array([]),
            "y": np.array([]),
            "yfit": np.array([]),
            "par": (np.NaN, np.NaN, np.NaN, np.NaN, np.NaN),
            "cov": (),
            "function": gaussian2
            }
    if type(x) is type(None) or type(y) is type(None):
        print(Fore.RED + "fitGaussian2(): Pass x and y as arrays." + Fore.RESET); return res
    if not (type(x) is np.ndarray or type(x) is list or type(y) is list or type(y) is np.ndarray):
        print(Fore.RED + "fitGaussian2(): Pass x and y as arrays." + Fore.RESET); return res
    x, y = np.array(x), np.array(y)
    if not len(x) == len(y):
        print(Fore.RED + "fitGaussian2(): The x array and the y array must have the same size." + Fore.RESET); return res
    if len(x) == 0:
        print(Fore.RED + "fitGaussian2(): The x array and the y array can't be of length 0." + Fore.RESET); return res
    #
    par, cov = curve_fit(gaussian2, x, y, p0 = p)
    yfit = gaussian(x, *par)
    res.update({"x": x, "y": y, "yfit": yfit, "par": tuple(par), "cov": cov})
    return res




# ====================================================== 


def fermi(E = None, T = None, Ef = None, A = None):
    """
    Pass E as an array, Ef, T, and A as scalars. Returns an array (intensity).
    """
    kb = 8.6173e-5 # Boltzmann k in eV/K
    #
    if not type(E) is np.ndarray:
        print(Fore.RED + "fermi(): Pass argument E as an energy axis (array, eV)." + Fore.RESET)
        return None
    try: T = abs(float(T))
    except:
        print(Fore.RED + "fermi(): Pass argument T as the temperature (scalar, K)." + Fore.RESET)
        return np.zeros(len(E)) * np.NaN
    try: Ef = abs(float(Ef))
    except:
        print(Fore.RED + "fermi(): Pass argument Ef as the Fermi level energy (scalar, kinetic, eV)." + Fore.RESET)
        return np.zeros(len(E)) * np.NaN
    try: A = abs(float(A))
    except:
        print(Fore.RED + "fermi(): Pass argument A as the amplitude (scalar, intensity, a.u.)." + Fore.RESET)
        return np.zeros(len(E)) * np.NaN
    #
    return A * (1.0 / (np.exp((E - Ef)/(kb*T)) + 1))




    
 




