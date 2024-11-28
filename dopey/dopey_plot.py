__version__ = "24.11.22"
__author__  = "Mats Leandersson"

print(f"{__name__}, {__version__}")

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from colorama import Fore

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


# --------------- globals ----------------
_axtype = "<class 'matplotlib.axes._subplots.AxesSubplot'>"






# ==================================================================================================
# ==================================================================================================
# ==================================================================================================

def plot(D = {}, ax = None, shup = False, **kwargs):
    """
    A generic plot method for all dopey dicts (from load(), quickSpin(), or whatever).
    It uses a range of sub methods depending on the kind of data.
    """
    if not type(D) is dict:
        print(Fore.RED + "plot(): Argument D must be a dopey dict." + Fore.RESET); return ax
    #
    if not shup:
        print(Fore.BLUE + f"plot(): Valid arguments are D, ax, shup, and keyword arguments." + Fore.RESET)
    #
    Typ, Knd = D.get("type", "NONE"), D.get("kind", "NONE")
    #
    #if not (type(ax) is mpl.axes._axes.Axes or type(ax) is mpl.axes._subplots.AxesSubplot):
    #    if not type(ax) is type(None): print(Fore.MAGENTA + "plot(): Argument ax, if passed, must be a matplotlib Axes." + Fore.RESET)
    #    ax = None
    #
    if Typ in ["arpes", "xps"]: return _plotARPES(D = D, ax = ax, shup = shup, **kwargs)
    #
    elif Typ == "spin_edc": return _plotSpinEDC(D = D, ax = ax, shup = shup, **kwargs)
    #
    elif Typ == "spin_mdc": return _plotSpinMDC(D = D, ax = ax, shup = shup, **kwargs)
    #
    elif Typ == "spin_map": return _plotSpinMap(D = D, ax = ax, shup = shup, **kwargs)
    #
    elif Typ == "fermi_map": return _plotFermiMap(D = D, ax = ax, shup = shup, **kwargs)
    #
    elif Typ == "spin_arpes": return _plotSpinARPES(D = D, ax = ax, shup = shup, **kwargs)
    #
    elif Typ == "1d": return _plot1d(D = D, ax = ax, shup = shup, **kwargs)
    #
    elif Typ.startswith("2d"): return _plot2d(D = D, ax = ax, shup = shup, **kwargs)
    #
    elif Typ == "target_scattering_spectrum": return _plotTarget(D = D, ax = ax, shup = shup, **kwargs)
    #
    elif Typ == "result" and Knd == "spin_edc":
        return _plotResultsSpinEDC(D = D, ax = ax, shup = shup, **kwargs)
    #
    elif Typ == "result" and Knd == "spin_mdc":
        if not "y" in D: return _plotResultsSpinMDC_FE(D = D, ax = ax, shup = shup, **kwargs)
        else: return _plotResultsSpinMDC_FAT(D = D, ax = ax, shup = shup, **kwargs)
    #
    elif Typ == "result" and Knd == "spin_map":
        # The structure of result spin_map fata (FE) is the same as for result spin_mdc (FAT) 
        # so I use the same plot method for this.
        return _plotResultsSpinMDC_FAT(D = D, ax = ax, shup = shup, **kwargs)
    #
    elif Typ == "result" and Knd == "spin_edc_polarization":
        return _plotResultsSpinEDCpolarization(D = D, ax = ax, shup = shup, **kwargs)
    #
    elif Typ == "dichroism":
        return _plotDichroism(D = D, ax = ax, shup = shup, **kwargs)
    #
    elif Typ == "NONE":
        print(Fore.MAGENTA + "plot(): This is probably not any kind of dopey dict." + Fore.RESET)
        return None
        
    else:
        print(Fore.MAGENTA + f"plot(): the method is not yet updated to accept dopey dicts of e.g. type: {Typ} {D.get('kind','')}." + Fore.RESET)
        return None




# ==================================================================================================

def _plotARPES(D = {}, ax = None, shup = False, **kwargs):
    """"""
    accepted_kwargs = ["rotate", "figsize", "xlim", "ylim", "vmin", "vmax", "aspect", "cmap", "title", "fontsize"]
    if not shup:
        print(Fore.BLUE + f"plot(): Valid keyword arguments {accepted_kwargs}" + Fore.RESET)
    #
    if type(ax) is type(None):
        figsize = kwargs.get("figsize", (5,3))
        fig, ax = plt.subplots(figsize = figsize)
    else:
        fig = None
    #
    aspect = kwargs.get("aspect", "auto")
    xlim = kwargs.get("xlim", (None, None))
    ylim = kwargs.get("ylim", (None, None))
    cmap = kwargs.get("cmap", "bone_r")
    vmin = kwargs.get("vmin", None)
    vmax = kwargs.get("vmax", None)
    fontsize = kwargs.get("fontsize", 10)
    title = kwargs.get("title", "NONE")
    rotate = kwargs.get("rotate", False)
    #
    xaxis, xlabel = D.get("x", []), D.get("labels", {}).get("x", "")
    yaxis, ylabel = D.get("y", []), D.get("labels", {}).get("y", "")
    #print(f'{np.shape(xaxis) = }, {np.shape(yaxis) = }')
    intensity = D.get("intensity", [])
    if rotate:
        xaxis, yaxis = yaxis, xaxis
        xlabel, ylabel = ylabel, xlabel
        intensity = intensity.T
    #
    extent = [xaxis[0], xaxis[-1], yaxis[-1], yaxis[0]]
    ax.imshow(intensity, extent = extent, cmap = cmap, aspect = aspect, vmin = vmin, vmax = vmax)
    ax.invert_yaxis()
    ax.set_xlabel(xlabel, fontsize = fontsize - 1)
    ax.set_ylabel(ylabel, fontsize = fontsize - 1)
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    if title == "NONE":
        ax.set_title(f'id {D.get("spectrum_id", -1)}', fontsize = fontsize)
    else:
        if not title == "": ax.set_title(title, fontsize = fontsize)
    #
    if not type(fig) is type(None): fig.tight_layout()
    return ax



# ==================================================================================================

def _plotSpinEDC(D = {}, ax = None, shup = False, **kwargs):
    """"""
    accepted_kwargs = ["figsize", "xlim", "ylim", "legend", "linewidth", "title", "fontsize", "intensity"]
    intkwargs = ["all", "all_minus", "all_plus", "mean", "mean_minus", "mean_plus"]
    if not shup:
        print(Fore.BLUE + f"plot(): Valid keyword arguments {accepted_kwargs}" + Fore.RESET)
        print(Fore.BLUE + f"        The keyword 'intensity' must be one of: {intkwargs}" + Fore.RESET)
    #
    if type(ax) is type(None):
        figsize = kwargs.get("figsize", (5,3))
        fig, ax = plt.subplots(figsize = figsize)
    else:
        fig = None
    #
    xlim = kwargs.get("xlim", (None, None))
    ylim = kwargs.get("ylim", (None, None))
    fontsize = kwargs.get("fontsize", 10)
    title = kwargs.get("title", "NONE")
    legend = kwargs.get("legend", True)
    linewidth = kwargs.get("linewidth", 0.8)
    #
    what_to_plot = kwargs.get("intensity", intkwargs[0])
    if not type(what_to_plot) is str: what_to_plot = intkwargs[0]
    else: what_to_plot = what_to_plot.lower()
    if not what_to_plot in intkwargs:
        print(Fore.RED + f"plot(): Unknown value for keyword argument 'intensity'.")
        print(f"        Setting intensity = '{intkwargs[0]}'"+ Fore.RESET)
        what_to_plot = intkwargs[0]
    #
    if what_to_plot == "all":
        for i, edc in enumerate(D.get("intensity")[0]):
            M = ""
            if i == 0: M = "(M-)"
            ax.plot(D.get("x"), edc, color = "red", linewidth = linewidth, label = f"i = {i} {M}")
        for i, edc in enumerate(D.get("intensity")[1]):
            M = ""
            if i == 0: M = "(M+)"
            ax.plot(D.get("x"), edc, color = "blue", linewidth = linewidth, label = f"i = {i} {M}")
        if legend: ax.legend(fontsize = fontsize - 2)
        if title == "NONE":
            ax.set_title(f'id {D.get("experiment", {}).get("Spectrum_ID", "?")}, individual edcs', fontsize = fontsize)
        else:
            if not title == "": ax.set_title(title, fontsize = fontsize)
    
    elif what_to_plot == "all_minus" or what_to_plot == "all_plus":
        if what_to_plot == "all_minus": im, color = 0, "red"
        else: im, color = 1, "blue"
        for i, edc in enumerate(D.get("intensity")[im]):
            ax.plot(D.get("x"), edc, linewidth = linewidth, label = f"i = {i}")
        if legend: ax.legend(fontsize = fontsize - 2)
        if title == "NONE":
            ax.set_title(f'id {D.get("experiment", {}).get("Spectrum_ID", "?")}, individual edcs ({what_to_plot[-3:]}. polarity)', fontsize = fontsize)
        else:
            if not title == "": ax.set_title(title, fontsize = fontsize)
    
    elif what_to_plot in ["mean", "mean_minus", "mean_plus"]:
        if what_to_plot in ["mean", "mean_minus"]:
            ax.plot(D.get("x"), D.get("intensity_mean")[0], color = "red", linewidth = linewidth, label = "M-")
        if what_to_plot in ["mean", "mean_plus"]:   
            ax.plot(D.get("x"), D.get("intensity_mean")[1], color = "blue", linewidth = linewidth, label = "M+")
        if legend: ax.legend(fontsize = fontsize - 2)
        if title == "NONE":
            ax.set_title(f'id {D.get("experiment", {}).get("Spectrum_ID", "?")}, average edc', fontsize = fontsize)
        else:
            if not title == "": ax.set_title(title, fontsize = fontsize)

    ax.set_xlabel(D.get("labels", {}).get("x", "x-axis"), fontsize = fontsize - 1)
    ax.set_ylabel(D.get("labels", {}).get("intensity", "y-axis"), fontsize = fontsize - 1)
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    
    if not type(fig) is type(None): fig.tight_layout()
    return ax




# ========================================================================================================================

def _plotSpinMDC(D = {}, ax = None, shup = False, **kwargs):
    """"""
    if type(ax) is type(None):
        figsize = kwargs.get("figsize", (5,3))
        fig, ax = plt.subplots(figsize = figsize)
    else:
        fig = None
    #
    xlim = kwargs.get("xlim", (None, None))
    ylim = kwargs.get("ylim", (None, None))
    vmin = kwargs.get("vmin", None)
    vmax = kwargs.get("vmax", None)
    cmap = kwargs.get("cmap", "bone_r")
    aspect = kwargs.get("aspect", "auto")
    fontsize = kwargs.get("fontsize", 10)
    title = kwargs.get("title", "NONE")
    legend = kwargs.get("legend", True)
    linewidth = kwargs.get("linewidth", 0.8)
    step = kwargs.get("step", -1)

    # ---

    if D.get("experiment", {}).get("Scan_Mode") == "FixedEnergies":
        #
        accepted_kwargs = ["figsize", "xlim", "ylim", "legend", "linewidth", "title", "fontsize", "intensity"]
        intkwargs = ["all", "all_minus", "all_plus", "mean", "mean_minus", "mean_plus"]
        if not shup:
            print(Fore.BLUE + f"plot(): Valid keyword arguments {accepted_kwargs}" + Fore.RESET)
            print(Fore.BLUE + f"        The keyword 'intensity' must be one of: {intkwargs}" + Fore.RESET)
        #
        xlim = kwargs.get("xlim", (None, None))
        ylim = kwargs.get("ylim", (None, None))
        fontsize = kwargs.get("fontsize", 10)
        title = kwargs.get("title", "NONE")
        legend = kwargs.get("legend", True)
        linewidth = kwargs.get("linewidth", 0.8)
        #
        what_to_plot = kwargs.get("intensity", intkwargs[0])
        if not type(what_to_plot) is str: what_to_plot = intkwargs[0]
        else: what_to_plot = what_to_plot.lower()
        if not what_to_plot in intkwargs:
            print(Fore.RED + "plot(): Unknown value for keyword argument 'intensity'.")
            print(f"        Setting intensity = '{intkwargs[0]}'"+ Fore.RESET)
            what_to_plot = intkwargs[0]
        #
        if what_to_plot == "all":
            for i, curve in enumerate(D.get("intensity")[0]):
                M = ""
                if i == 0: M = " (M-)"
                ax.plot(D.get("y"), curve, color = "red", linewidth = linewidth, label = f"i = {i}{M}")
            for i, curve in enumerate(D.get("intensity")[1]):
                M = ""
                if i == 0: M = " (M+)"
                ax.plot(D.get("y"), curve, color = "blue", linewidth = linewidth, label = f"i = {i}{M}")
            if legend: ax.legend(fontsize = fontsize - 2)
            if title == "NONE":
                ax.set_title(f'id {D.get("experiment", {}).get("Spectrum_ID", "?")}, individual edcs', fontsize = fontsize)
            else:
                if not title == "": ax.set_title(title, fontsize = fontsize)
        
        elif what_to_plot == "all_minus" or what_to_plot == "all_plus":
            if what_to_plot == "all_minus": im, color, MM = 0, "red", "M-"
            else: im, color, MM = 1, "blue", "M+"
            for i, curve in enumerate(D.get("intensity")[im]):
                M = ""
                if i == 0: M = f"({MM})"
                ax.plot(D.get("y"), curve, color = color, linewidth = linewidth, label = f"i = {i} {M}")
            if legend: ax.legend(fontsize = fontsize - 2)
            if title == "NONE":
                ax.set_title(f'id {D.get("experiment", {}).get("Spectrum_ID", "?")}, individual edcs ({what_to_plot[-3:]}. polarity)', fontsize = fontsize)
            else:
                if not title == "": ax.set_title(title, fontsize = fontsize)
        
        elif what_to_plot in ["mean", "mean_minus", "mean_plus"]:
            if what_to_plot in ["mean", "mean_minus"]:
                ax.plot(D.get("y"), D.get("intensity_mean")[0], color = "red", linewidth = linewidth, label = "M-")
            if what_to_plot in ["mean", "mean_plus"]:   
                ax.plot(D.get("y"), D.get("intensity_mean")[1], color = "blue", linewidth = linewidth, label = "M+")
            if legend: ax.legend(fontsize = fontsize - 2)
            if title == "NONE":
                ax.set_title(f'id {D.get("experiment", {}).get("Spectrum_ID", "?")}, mean edc', fontsize = fontsize)
            else:
                if not title == "": ax.set_title(title, fontsize = fontsize)
        
        ax.set_xlabel(D.get("labels", {}).get("y", "?"), fontsize = fontsize - 1)
        ax.set_ylabel(D.get("labels", {}).get("intensity", "?"), fontsize = fontsize - 1)
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
        if not type(fig) is type(None): fig.tight_layout()
        return ax
    
    if D.get("experiment", {}).get("Scan_Mode") == "FixedAnalyzerTransmission":
        #
        accepted_kwargs = ["figsize", "xlim", "ylim", "vmin", "vmax", "cmap", "aspect", "title", "fontsize", "intensity"]
        intkwargs = ["mean_minus", "mean_plus"]
        if not shup:
            print(Fore.BLUE + f"plot(): Valid keyword arguments {accepted_kwargs}" + Fore.RESET)
            print(Fore.BLUE + f"        The keyword 'intensity' must be one of: {intkwargs}" + Fore.RESET)
        #
        what_to_plot = kwargs.get("intensity", intkwargs[0])
        if not type(what_to_plot) is str: what_to_plot = intkwargs[0]
        else: what_to_plot = what_to_plot.lower()
        if not what_to_plot in intkwargs:
            print(Fore.RED + "plot(): Unknown value for keyword argument 'intensity'.")
            print(f"        Setting intensity = '{intkwargs[0]}'"+ Fore.RESET)
            what_to_plot = intkwargs[0]
        
        if what_to_plot in intkwargs:
            if what_to_plot == "mean_minus":
                map = D["intensity_mean"][0]
            else:
                map = D["intensity_mean"][1]
            extent = [D["x"][0], D["x"][-1], D["y"][-1], D["y"][0]]
            ax.imshow(map, extent = extent, cmap = cmap, vmin = vmin, vmax = vmax, aspect = aspect)
            ax.invert_yaxis()

            if title == "NONE":
                ax.set_title(f'id {D.get("experiment", {}).get("Spectrum_ID", "?")}, average intensity (polarity {what_to_plot[-5:].strip("_")})', fontsize = fontsize)
            else:
                if not title == "": ax.set_title(title, fontsize = fontsize)

            ax.set_ylabel(D.get("labels", {}).get("y", "?"), fontsize = fontsize - 1)
            ax.set_xlabel(D.get("labels", {}).get("x", "?"), fontsize = fontsize - 1)
            ax.set_xlim(xlim)
            ax.set_ylim(ylim)
        if not type(fig) is type(None): fig.tight_layout()
        return ax





# ========================================================================================================================

def _plotSpinMap(D = {}, ax = None, shup = False, **kwargs):
    """"""
    if not D.get("experiment", {}).get("Scan_Mode", "") == "FixedEnergies":
        print(Fore.MAGENTA + "plot(): Plotting is not prepared for spin map data acquired in FixedAnalyzerTransmission,")
        print("        only FixedEnergies. It will be updated. Stay tuned." + Fore.RESET)
        return ax
    #
    accepted_kwargs = ["figsize", "xlim", "ylim", "vmin", "vmax", "cmap", "aspect", "title", "fontsize", "intensity"]
    intkwargs = ["mean_minus", "mean_plus"]
    if not shup:
        print(Fore.BLUE + f"plot(): Valid keyword arguments {accepted_kwargs}" + Fore.RESET)
        print(Fore.BLUE + f"        The keyword 'intensity' must be one of: {intkwargs}" + Fore.RESET)
    #
    if type(ax) is type(None):
        figsize = kwargs.get("figsize", (5,3))
        fig, ax = plt.subplots(figsize = figsize)
    else:
        fig = None
    #
    xlim = kwargs.get("xlim", (None, None))
    ylim = kwargs.get("ylim", (None, None))
    vmin = kwargs.get("vmin", None)
    vmax = kwargs.get("vmax", None)
    cmap = kwargs.get("cmap", "bone_r")
    aspect = kwargs.get("aspect", "auto")
    fontsize = kwargs.get("fontsize", 10)
    title = kwargs.get("title", "NONE")
    #
    what_to_plot = kwargs.get("intensity", intkwargs[0])
    if not type(what_to_plot) is str: what_to_plot = intkwargs[0]
    else: what_to_plot = what_to_plot.lower()
    if not what_to_plot in intkwargs:
        print(Fore.RED + "plot(): Unknown value for keyword argument 'intensity'.")
        print(f"        Setting intensity = '{intkwargs[0]}'"+ Fore.RESET)
        what_to_plot = intkwargs[0]
    #
    if what_to_plot in intkwargs:   
        if what_to_plot == "mean_minus":
            map = D["intensity_mean"][0]
        else:
            map = D["intensity_mean"][1]
        extent = [D["y"][0], D["y"][-1], D["z"][-1], D["z"][0]]
        ax.imshow(map, extent = extent, cmap = cmap, vmin = vmin, vmax = vmax, aspect = aspect)
        ax.invert_yaxis()

        if title == "NONE":
            ax.set_title(f'id {D.get("experiment", {}).get("Spectrum_ID", "?")}, mean intensity (polarity {what_to_plot[-5:].strip("_")})', fontsize = fontsize)
        else:
            if not title == "": ax.set_title(title, fontsize = fontsize)

        ax.set_ylabel(D.get("labels", {}).get("z", "?"), fontsize = fontsize - 1)
        ax.set_xlabel(D.get("labels", {}).get("y", "?"), fontsize = fontsize - 1)
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
        if not type(fig) is type(None): fig.tight_layout()
        return ax



# ==================================================================================================

def _plotSpinARPES(D = {}, ax = None, shup = False, **kwargs):
    """
    The data stucture for spin_arpes is the same as for arpes so let's just reuse the same 
    method, i.e. _plotARPES(D = {}, ax = None, shup = False, **kwargs)
    """
    return _plotARPES(D = D, ax = ax, shup = shup, **kwargs)
    



# ========================================================================================================================

def _plot1d(D = {}, ax = None, shup = False, **kwargs):
    """
    """
    accepted_kwargs = ["figsize", "xlim", "ylim", "title", "fontsize"]
    if not shup:
        print(Fore.BLUE + f"plot(): Valid keyword arguments {accepted_kwargs}" + Fore.RESET)
    if type(ax) is type(None):
        figsize = kwargs.get("figsize", (5,3))
        fig, ax = plt.subplots(figsize = figsize)
    else:
        fig = None
    #
    xlim = kwargs.get("xlim", (None, None))
    ylim = kwargs.get("ylim", (None, None))
    fontsize = kwargs.get("fontsize", 10)
    linewidth = kwargs.get("linewidth", 0.8)
    title = kwargs.get("title", "NONE")
    #
    ax.plot(D["x"], D["intensity"], color = "k", linewidth = linewidth)
    #
    if title == "NONE":
        ax.set_title(f'Data from spectrum id {D.get("experiment", {}).get("Spectrum_ID", "?")}', fontsize = fontsize)
    else:
        if not title == "": ax.set_title(title, fontsize = fontsize)

    ax.set_xlabel(D.get("labels", {}).get("x", "?"), fontsize = fontsize - 1)
    ax.set_ylabel(D.get("labels", {}).get("intensity", "?"), fontsize = fontsize - 1)
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    #
    if not type(fig) is type(None): fig.tight_layout()
    return ax




# ========================================================================================================================

def _plot2d(D = {}, ax = None, shup = False, **kwargs):
    """
    """
    accepted_kwargs = ["figsize", "xlim", "ylim", "vmin", "vmax", "cmap", "aspect", "title", "fontsize", "intensity"]
    if not shup:
        print(Fore.BLUE + f"plot(): Valid keyword arguments {accepted_kwargs}" + Fore.RESET)
    #
    if type(ax) is type(None):
        figsize = kwargs.get("figsize", (5,3))
        fig, ax = plt.subplots(figsize = figsize)
    else:
        fig = None
    #
    xlim = kwargs.get("xlim", (None, None))
    ylim = kwargs.get("ylim", (None, None))
    vmin = kwargs.get("vmin", None)
    vmax = kwargs.get("vmax", None)
    cmap = kwargs.get("cmap", "bone_r")
    aspect = kwargs.get("aspect", "auto")
    fontsize = kwargs.get("fontsize", 10)
    title = kwargs.get("title", "NONE")
    rotate = kwargs.get("rotate", False)
    #
    xaxis, xlabel = D.get("x", []), D.get("labels", {}).get("x", "")
    yaxis, ylabel = D.get("y", []), D.get("labels", {}).get("y", "")
    intensity = D.get("intensity", [])
    if rotate:
        xaxis, yaxis = yaxis, xaxis
        xlabel, ylabel = ylabel, xlabel
        intensity = intensity.T
    #
    extent = [xaxis[0], xaxis[-1], yaxis[-1], yaxis[0]]
    ax.imshow(intensity, extent = extent, cmap = cmap, aspect = aspect, vmin = vmin, vmax = vmax)
    ax.invert_yaxis()
    ax.set_xlabel(xlabel, fontsize = fontsize - 1)
    ax.set_ylabel(ylabel, fontsize = fontsize - 1)
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    if title == "NONE":
        ax.set_title(f'Data from id {D.get("experiment", {}).get("Spectrum_ID", "?")}', fontsize = fontsize)
    else:
        if not title == "": ax.set_title(title, fontsize = fontsize)
    #
    if not type(fig) is type(None): fig.tight_layout()
    return ax




# ========================================================================================================================

# Could've used _quickView1d() for this but since it's a dedicated data format...

def _plotTarget(D = {}, ax = None, shup = False, **kwargs):
    """"""
    accepted_kwargs = ["figsize", "xlim", "ylim", "title", "fontsize"]
    if not shup:
        print(Fore.BLUE + f"plot(): Valid keyword arguments {accepted_kwargs}" + Fore.RESET)
    #
    if type(ax) is type(None):
        figsize = kwargs.get("figsize", (5,3))
        fig, ax = plt.subplots(figsize = figsize)
    else:
        fig = None
    #
    xlim = kwargs.get("xlim", (None, None))
    ylim = kwargs.get("ylim", (None, None))
    fontsize = kwargs.get("fontsize", 10)
    linewidth = kwargs.get("linewidth", 0.8)
    title = kwargs.get("title", "NONE")
    #
    ax.plot(D["x"], D["intensity"], color = "k", linewidth = linewidth)
    #
    if title == "NONE":
        ax.set_title(f'id {D.get("experiment", {}).get("Spectrum_ID", "?")}, target scattering spectrum', fontsize = fontsize)
    else:
        if not title == "": ax.set_title(title, fontsize = fontsize)

    ax.set_ylabel(D.get("labels", {}).get("x", "?"), fontsize = fontsize - 1)
    ax.set_xlabel(D.get("labels", {}).get("intensity", "?"), fontsize = fontsize - 1)
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    #
    if not type(fig) is type(None): fig.tight_layout()
    return ax




# ========================================================================================================================

def _plotDichroism(D = {}, ax = None, shup = False, **kwargs):
    """
    """
    accepted_kwargs = ["figsize", "xlim", "ylim", "title", "fontsize", "cmap", "vmin", "vmax", "aspect", "rotate"]
    if not shup:
        print(Fore.BLUE + f"plot(): Valid keyword arguments {accepted_kwargs}" + Fore.RESET)
    #
    if type(ax) is type(None):
        figsize = kwargs.get("figsize", (5,3))
        fig, ax = plt.subplots(figsize = figsize)
    else:
        fig = None
    #
    xlim = kwargs.get("xlim", (None, None))
    ylim = kwargs.get("ylim", (None, None))
    fontsize = kwargs.get("fontsize", 10)
    title = kwargs.get("title", "")
    cmap = kwargs.get("cmap", "bwr")
    vmin = kwargs.get("vmin", None)
    vmax = kwargs.get("vmax", None)
    aspect = kwargs.get("aspect", "equal")
    rotate = kwargs.get("rotate", False)
    #
    xaxis, xlabel = D.get("x", []), D.get("labels", {}).get("x", "")
    yaxis, ylabel = D.get("y", []), D.get("labels", {}).get("y", "")
    intensity = D.get("intensity", np.array([]))
    if rotate:
        xaxis, yaxis = yaxis, xaxis
        xlabel, ylabel = ylabel, xlabel
        intensity = intensity.T
    #
    extent = [xaxis[0], xaxis[-1], yaxis[-1], yaxis[0]]
    ax.imshow(intensity, extent = extent, cmap = cmap, aspect = aspect, vmin = vmin, vmax = vmax)
    ax.invert_yaxis()
    ax.set_xlabel(xlabel, fontsize = fontsize - 1)
    ax.set_ylabel(ylabel, fontsize = fontsize - 1)
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_title(title, fontsize = fontsize)
    #
    if not type(fig) is type(None): fig.tight_layout()
    return ax





# ========================================================================================================================
# ========================================================================================================================
# ========================================================================================================================

def _plotFermiMap(D = {}, ax = None, shup = False, **kwargs):
    """"""
    if not shup:
        print(Fore.BLUE + "plot(): Pass argument cut as True to plot xy, xz, or yz cuts. Default cut = False opens an interactive 3d view." + Fore.RESET)
    cut = kwargs.get("cut", False)
    if cut:
        return _plotFermiMapCut(D = D, ax = ax, shup = shup, **kwargs)
    else:
        print(Fore.MAGENTA + "plot(): The intensity sliders are not active. Working on it." + Fore.RESET)
        _ = fermiMapInteractive(D = D, shup = shup, **kwargs)



# ------- interactive

def fermiMapInteractive(D = {}, shup = False, **kwargs):
    """
    Interactive plot of 3d data (energy, angle, x delflection).
    """
    figsize = kwargs.get("figsize", (8,4))
    cmap = kwargs.get("cmap", "bone_r")
    linewidth = 0.75

    ENERGY = D.get('x')
    ANGLEX = D.get('z')
    ANGLEY = D.get('y')
    dENERGY = (ENERGY[-1]-ENERGY[0])/len(ENERGY)
    dANGLEX = abs(ANGLEX[1]-ANGLEX[0])
    dANGLEY = abs(ANGLEY[1]-ANGLEY[0])

    estart = kwargs.get("estart", ENERGY.mean())
    xstart = kwargs.get("xstart", ANGLEX.mean())
    ystart = kwargs.get("xstart", ANGLEY.mean())
    if estart < ENERGY.min(): estart = ENERGY.min() + 5*dENERGY
    if estart > ENERGY.max(): estart = ENERGY.max() - 5*dENERGY
    if xstart < ANGLEX.min(): estart = ANGLEX.min() + dANGLEX
    if xstart > ANGLEX.max(): estart = ANGLEX.max() - dANGLEX
    if ystart < ANGLEY.min(): estart = ANGLEY.min() + 5*dANGLEY
    if ystart > ANGLEY.max(): estart = ANGLEY.max() - 5*dANGLEY
    accepted_kwargs = ["estart", "xstart", "ystart"]
    if not shup:
        print(Fore.BLUE + f"fermiMapInteractive(): The method accepts the following keyword arguments: {accepted_kwargs}" + Fore.RESET)

    SliderE = ipw.FloatSlider(min=ENERGY[0], max=ENERGY[-1], step = dENERGY, description = 'Energy', value = estart, readout_format = ".3f")
    SliderX = ipw.FloatSlider(min=ANGLEX.min(), max=ANGLEX.max(), step = dANGLEX, description = 'Deflection X', value = xstart, readout_format = ".2f")
    SliderY = ipw.FloatSlider(min=ANGLEY[0], max=ANGLEY[-1], step = dANGLEY, description = 'Angle Y', value = ystart, readout_format = ".2f")

    SliderDE = ipw.FloatSlider(min=0, max=(ENERGY[-1]-ENERGY[0]), step = dENERGY, description = 'dE', value = 1*dENERGY, readout_format = ".3f")
    SliderDX = ipw.FloatSlider(min=0, max=(ANGLEX.max()-ANGLEX.min()), step = dANGLEX, description = 'dX', value = dANGLEX, readout_format = ".2f")
    SliderDY = ipw.FloatSlider(min=0, max=(ANGLEY[-1]-ANGLEY[0]), step = dANGLEY, description = 'dX', value = 1*dANGLEY, readout_format = ".2f")

    box_sliders_x = ipw.HBox([SliderE, SliderX, SliderY])
    box_sliders_dx = ipw.HBox([SliderDE, SliderDX, SliderDY])
    box_sliders = ipw.VBox([box_sliders_x, box_sliders_dx])

    SliderVmin = ipw.FloatSlider(min=0, max=D["intensity"].max(), step = D["intensity"].max()/20, description = 'Imin', value = 0, readout_format = ".1f")
    SliderVmax = ipw.FloatSlider(min=0, max=D["intensity"].max(), step = D["intensity"].max()/20, description = 'Imax', value = D["intensity"].max(), readout_format = ".1f")

    box_sliders_2top = ipw.HBox([SliderVmin])
    box_sliders_2bot = ipw.HBox([SliderVmax])
    box_sliders_2 = ipw.VBox([box_sliders_2top, box_sliders_2bot])

    extentE = [ANGLEX[0], ANGLEX[-1], ANGLEY[-1], ANGLEY[0]] 
    extentX = [ANGLEY[0], ANGLEY[-1], ENERGY[-1], ENERGY[0]]
    extentY = [ANGLEX[0], ANGLEX[-1], ENERGY[-1], ENERGY[0]]

    def plot(X, Y, E, DX, DY, DE, VMIN, VMAX):
        fig, ax = plt.subplots(figsize = figsize, ncols = 3)
        plt.tight_layout()
        #
        XY = compact(D = subArray(D = D, axis = "x", v1 = E-DE/2, v2 = E+DE/2, shup = True), axis = 'x', shup = True)
        YE = compact(D = subArray(D = D, axis = "z", v1 = X-DX/2, v2 = X+DX/2, shup = True), axis = 'z', shup = True)
        XE = compact(D = subArray(D = D, axis = "y", v1 = Y-DY/2, v2 = Y+DY/2, shup = True), axis = 'y', shup = True)
        #
        #slider_vmin = np.min([XY["intensity"].min(), YE["intensity"].min(), XE["intensity"].min()])
        #slider_vmax = np.min([XY["intensity"].max(), YE["intensity"].max(), XE["intensity"].max()])
        #SliderVmin.min, SliderVmin.max = slider_vmin, slider_vmax
        #SliderVmax.min, SliderVmax.max = slider_vmin, slider_vmax
        #
        #if VMIN > VMAX: VMIN = VMAX
        VMIN, VMAX = None, None
        _ = ax[0].imshow(XY['intensity'].transpose(), extent = extentE, aspect = 'equal', cmap = cmap, vmin = VMIN, vmax = VMAX)
        _ = ax[1].imshow(YE['intensity'].transpose(), extent = extentX, aspect = 'auto',  cmap = cmap, vmin = VMIN, vmax = VMAX)
        _ = ax[2].imshow(XE['intensity'].transpose(), extent = extentY, aspect = 'auto',  cmap = cmap, vmin = VMIN, vmax = VMAX)
        for a in ax: a.invert_yaxis()
        #
        ax[0].axvline(x = X - DX/2, linewidth = linewidth, color = 'red')
        ax[0].axvline(x = X + DX/2, linewidth = linewidth, color = 'red')
        ax[0].axhline(y = Y - DY/2, linewidth = linewidth, color = 'red')
        ax[0].axhline(y = Y + DY/2, linewidth = linewidth, color = 'red')
        for i in [1,2]: 
            ax[i].axhline(y = E - DE/2, linewidth = linewidth, color = 'red')
            ax[i].axhline(y = E + DE/2, linewidth = linewidth, color = 'red')
        #
        ax[0].set_xlabel('X (°)')
        ax[0].set_ylabel('Y (°)')
        ax[1].set_xlabel('Y (°)')
        ax[2].set_xlabel('X (°)')
        #
        fig.suptitle("ID {0}".format(D.get('experiment', {}).get('Spectrum_ID', '')))
        fig.tight_layout()

    Interact = ipw.interactive_output(plot, {'X': SliderX, 
                                             'Y': SliderY, 
                                             'E': SliderE, 
                                             'DX': SliderDX,
                                             'DY': SliderDY, 
                                             'DE': SliderDE,
                                             "VMIN": SliderVmin,
                                             "VMAX": SliderVmax})

    box_out = ipw.VBox([box_sliders, Interact, box_sliders_2])
    box_out.layout = ipw.Layout(border="solid 1px gray", margin="5px", padding="2")
    display(box_out)


def _plotFermiMapCut(D = {}, ax = None, shup = False, **kwargs):
    """"""
    accepted_kwargs = ["rotate", "axis", "v1", "v2", "figsize", "xlim", "ylim", "vmin", "vmax", "cmap", "aspect", "title", "fontsize", "intensity"]
    if not shup:
        print(Fore.BLUE + f"plot(): Valid keyword arguments {accepted_kwargs}" + Fore.RESET)
    #
    fig = None
    if type(ax) is type(None):
        figsize = kwargs.get("figsize", (5,3))
        fig, ax = plt.subplots(figsize = figsize)
    else:
        fig = None
    axis = kwargs.get("axis", None)
    v1 = kwargs.get("v1", None)
    v2 = kwargs.get("v2", None)
    #
    if not type(axis) is str:
        print(Fore.MAGENTA + "plot(): When passing cut = True you have to pass keyword argument axis = 'x', 'y', or 'z'. Setting axis = 'x'." + Fore.RESET)
        axis = "x"
    axis = axis.lower()
    if not axis in ["x", "y", "z"]:
        print(Fore.MAGENTA + "plot(): The keyword argument axis must be 'x', 'y', or 'z'. Setting axis = 'x'." + Fore.RESET)
        axis = "x"
    #
    try: v1 = float(v1)
    except:
        v1 = D[axis].min()
        print(Fore.MAGENTA + f"plot(): When passing cut = True you have to pass keyword argument v1. Setting v1 = {v1}" + Fore.RESET)
    try: v2 = float(v2)
    except:
        v2 = D[axis].max()
        print(Fore.MAGENTA + f"plot(): When passing cut = True you have to pass keyword argument v2. Setting v2 = {v2}" + Fore.RESET)
    #
    newD = subArray(D, axis = axis, v1 = v1, v2 = v2, shup = True)
    newD = compact(newD, axis = axis, shup = True)
    print(newD["type"], np.shape(newD["intensity"]))
    if not type(fig) is type(None): fig.tight_layout()
    return plot(newD, ax = ax, shup = True, **kwargs)




# ========================================================================================================================
# ========================================================================================================================
# ========================================================================================================================


def _plotResultsSpinEDC(D = {}, ax = None, shup = False, **kwargs):
    # Note to self: if you improve this method then apply the same improvements to _plotResultsSpinMDC_FE() as it is
    # basically the same.
    """
    """
    accepted_kwargs = ["intensity", "figsize", "xlim", "ylim", "aylim", "cylim", "fontsize", "legend", "linewidth", "fontsize"]
    intkwargs = ["intensity", "asymmetry", "components"]
    if not shup:
        print(Fore.BLUE + f"plot(): Valid keyword arguments {accepted_kwargs}" + Fore.RESET)
        print(Fore.BLUE + f"        Pass keyword intensity to return a pyplot axis. Valid values: {intkwargs}" + Fore.RESET)
    #
    linewidth = kwargs.get("linewidth", 0.75)
    legend = kwargs.get("legend", True)
    fontsize = kwargs.get("fontsize", 10)
    xlim = kwargs.get("xlim", (None, None)) 
    ylim = kwargs.get("ylim", (None, None))   
    aylim = kwargs.get("aylim", (None, None))
    cylim = kwargs.get("aylim", (None, None))
    #
    def plot1(aX):
        aX.plot(D["x"], D["intensity"][1], color = "blue", linewidth = linewidth, label = "M+")
        aX.plot(D["x"], D["intensity"][0], color = "red", linewidth = linewidth, label = "M-")
        aX.set_title("Scattered intensity", fontsize = fontsize)
        aX.set_xlabel(D.get("labels", {}).get("x", "?"), fontsize = fontsize - 1)
        aX.set_ylabel(D.get("labels", {}).get("intensity", "?"), fontsize = fontsize - 1)
        aX.set_xlim(xlim)
        aX.set_ylim(ylim)
        if legend: aX.legend(fontsize = fontsize -2)
        return aX
    
    def plot2(aX):
        aX.plot(D["x"], D.get("asymmetry"), color = "k", linewidth = linewidth, label = "asymmetry")
        aX.set_xlabel(D.get("labels", {}).get("x", "?"), fontsize = fontsize - 1)
        aX.set_ylabel(D.get("labels", {}).get("asymmetry", "?"), fontsize = fontsize - 1)
        aX.set_title("Asymmetry", fontsize = fontsize)
        aX.set_xlim(xlim)
        aX.set_ylim(aylim)
        if legend: aX.legend(fontsize = fontsize -2)
        return aX
    
    def plot3(aX):
        aX.plot(D["x"], D["component"][1], color = "blue", linewidth = linewidth, label = "+")
        aX.plot(D["x"], D["component"][0], color = "red", linewidth = linewidth, label = "-")
        aX.set_title("Component intensity", fontsize = fontsize)
        aX.set_xlabel(D.get("labels", {}).get("x", "?"), fontsize = fontsize - 1)
        aX.set_ylabel(D.get("labels", {}).get("intensity", "?"), fontsize = fontsize - 1)
        aX.set_xlim(xlim)
        aX.set_ylim(cylim)
        if legend: aX.legend(fontsize = fontsize -2)
        return aX
    #
    what_to_plot = kwargs.get("intensity", intkwargs[0])
    fig = None
    if not type(what_to_plot) is str: what_to_plot = intkwargs[0]
    what_to_plot = what_to_plot.lower()
    if not what_to_plot in intkwargs:
        what_to_plot = intkwargs[0]
        print(Fore.MAGENTA + f"plot(): Valid values for the keyword argument intensity are: {intkwargs}. Setting default intensity = {intkwargs[0]}." + Fore.RESET)
    #if not type(ax) is mpl.axes._axes.Axes:
    if type(ax) is type(None):
        fig, ax = plt.subplots(figsize = kwargs.get("figsize", (5, 3)))
    if what_to_plot == "intensity": ax = plot1(ax)
    elif what_to_plot == "asymmetry": ax = plot2(ax)
    elif what_to_plot == "components": ax = plot3(ax)
    if not type(fig) is type(None): fig.tight_layout()
    return ax



def _plotResultsSpinMDC_FE(D = {}, ax = None, shup = False, **kwargs):
    # Note to self: This is more or less exactly the same as the _plotResultsSpinEDC except for the x-axis.
    # Keeping them separately anyway.
    """
    """
    accepted_kwargs = ["intensity", "figsize", "xlim", "ylim", "aylim", "cylim", "fontsize", "legend", "linewidth", "fontsize"]
    intkwargs = ["intensity", "asymmetry", "components"]
    if not shup:
        print(Fore.BLUE + f"plot(): Valid keyword arguments {accepted_kwargs}" + Fore.RESET)
        print(Fore.BLUE + f"        Pass keyword intensity to return a pyplot axis. Valid values: {intkwargs}" + Fore.RESET)
    #
    linewidth = kwargs.get("linewidth", 0.75)
    legend = kwargs.get("legend", True)
    fontsize = kwargs.get("fontsize", 10)
    xlim = kwargs.get("xlim", (None, None)) 
    ylim = kwargs.get("ylim", (None, None))   
    aylim = kwargs.get("aylim", (None, None))
    cylim = kwargs.get("aylim", (None, None))
    #
    def plot1(aX):
        aX.plot(D["x"], D["intensity"][1], color = "blue", linewidth = linewidth, label = "M+")
        aX.plot(D["x"], D["intensity"][0], color = "red", linewidth = linewidth, label = "M-")
        aX.set_title("Scattered intensity", fontsize = fontsize)
        aX.set_xlabel(D.get("labels", {}).get("x", "?"), fontsize = fontsize - 1)
        aX.set_ylabel(D.get("labels", {}).get("intensity", "?"), fontsize = fontsize - 1)
        aX.set_xlim(xlim)
        aX.set_ylim(ylim)
        if legend: aX.legend(fontsize = fontsize -2)
        return aX
    
    def plot2(aX):
        aX.plot(D["x"], D.get("asymmetry"), color = "k", linewidth = linewidth, label = "asymmetry")
        aX.set_xlabel(D.get("labels", {}).get("x", "?"), fontsize = fontsize - 1)
        aX.set_ylabel(D.get("labels", {}).get("asymmetry", "?"), fontsize = fontsize - 1)
        aX.set_title("Asymmetry", fontsize = fontsize)
        aX.set_xlim(xlim)
        aX.set_ylim(aylim)
        if legend: aX.legend(fontsize = fontsize -2)
        return aX
    
    def plot3(aX):
        aX.plot(D["x"], D["component"][1], color = "blue", linewidth = linewidth, label = "+")
        aX.plot(D["x"], D["component"][0], color = "red", linewidth = linewidth, label = "-")
        aX.set_title("Component intensity", fontsize = fontsize)
        aX.set_xlabel(D.get("labels", {}).get("x", "?"), fontsize = fontsize - 1)
        aX.set_ylabel(D.get("labels", {}).get("intensity", "?"), fontsize = fontsize - 1)
        aX.set_xlim(xlim)
        aX.set_ylim(cylim)
        if legend: aX.legend(fontsize = fontsize -2)
        return aX
    #

    what_to_plot = kwargs.get("intensity", "")
    fig = None
    if not type(what_to_plot) is str: what_to_plot = ""
    what_to_plot = what_to_plot.lower()
    if not what_to_plot in intkwargs:
        what_to_plot = intkwargs[0]
        print(Fore.MAGENTA + f"plot(): Valid values for the keyword argument intensity are: {intkwargs}. Setting default intensity = {intkwargs[0]}." + Fore.RESET)
    if not type(ax) is mpl.axes._axes.Axes:
        fig, ax = plt.subplots(figsize = kwargs.get("figsize", (5, 3)))
    if what_to_plot in "intensity": ax = plot1(ax)
    elif what_to_plot == "asymmetry": ax = plot2(ax)
    elif what_to_plot == "components": ax = plot3(ax)
    if not type(fig) is type(None): fig.tight_layout()
    return ax


def _plotResultsSpinMDC_FAT(D = {}, ax = None, shup = False, **kwargs):
    # Note to self: if you improve this method then apply the same improvements to _plotResultsSpinMap() as it is
    # basically the same.
    """"""
    accepted_kwargs = ["figsize", "fontsize", "xlim", "ylim", "vmin", "vmax", "avmin", "avmax", "cvmin", "cvmax", "aspect", "cmap", ]
    intkwargs = ["intensity+", "intensity-", "asymmetry", "component+", "component-", "presentation"]
    if not shup:
        print(Fore.BLUE + f"plot(): Valid keyword arguments {accepted_kwargs}" + Fore.RESET)
        print(Fore.BLUE + f"        Pass keyword intensity to return a pyplot axis. Valid values: {intkwargs}" + Fore.RESET)
    #
    figsize = kwargs.get("figsize", (8, 4.5))
    fontsize = kwargs.get("fontsize", 10)
    xlim = kwargs.get("xlim", (None, None)) 
    ylim = kwargs.get("ylim", (None, None))   
    vmin = kwargs.get("vmin", None)
    vmax = kwargs.get("vmax", None)
    avmin = kwargs.get("avmin", None)
    avmax = kwargs.get("avmax", None)
    cvmin = kwargs.get("cvmin", None)
    cvmax = kwargs.get("cvmax", None)
    aspect = kwargs.get("aspect", "auto")
    cmap = kwargs.get("cmap", "bone_r")
    #
    extent = [D["x"][0], D["x"][-1], D["y"][-1], D["y"][0]]
    
    def _plot(ax_, I_, extent_, aspect_, vmin_, vmax_, cmap_, xlim_, ylim_, ttl_):
        ax_.imshow(I_, extent = extent_, aspect = aspect_, vmin = vmin_, vmax = vmax_, cmap = cmap_)
        ax_.set_xlim(xlim_)
        ax_.set_ylim(ylim_)
        ax_.set_xlabel(D.get("labels", {}).get("x", "?"), fontsize = fontsize - 1)
        ax_.set_ylabel(D.get("labels", {}).get("y", "?"), fontsize = fontsize - 1)
        ax_.set_title(ttl_)
        ax_.invert_yaxis()
        return ax_
    #
    what_to_plot = kwargs.get("intensity", "")
    fig = None
    if not type(what_to_plot) is str: what_to_plot = ""
    what_to_plot = what_to_plot.lower()
    if not what_to_plot in intkwargs: what_to_plot = ""
    if what_to_plot == "":
        if str(type(ax)) == _axtype:
            print(Fore.MAGENTA + "plot(): A pyplot ax will not be returned unless you pass a valid value for the keyword argument intensity." + Fore.RESET)
        fig, ax = plt.subplots(nrows = 2, ncols = 3, figsize = kwargs.get("figsize", (10, 5)))
        ax[0][0] = _plot(ax[0][0], D["intensity"][1], extent, aspect, vmin, vmax, cmap, xlim, ylim, "Scattered intensity, $M+$")
        ax[1][0] = _plot(ax[1][0], D["intensity"][0], extent, aspect, vmin, vmax, cmap, xlim, ylim, "Scattered intensity, $M-$")
        ax[0][1] = _plot(ax[0][1], D["component"][1], extent, aspect, cvmin, cvmax, cmap, xlim, ylim, "Component intensity, $+$")
        ax[1][1] = _plot(ax[1][1], D["component"][0], extent, aspect, cvmin, cvmax, cmap, xlim, ylim, "Component intensity, $-$")
        ax[0][2] = _plot(ax[0][2], D["asymmetry"],    extent, aspect, avmin, avmax, cmap, xlim, ylim, "Asymmetry")
        ax[1][2] = _plot(ax[1][2], D["component"][1] - D["component"][0], extent, aspect, avmin, avmax, "bwr", xlim, ylim, "")
        fig.tight_layout()
    else:
        if not str(type(ax)) == _axtype:
            fig, ax = plt.subplots(figsize = kwargs.get("figsize", (5, 3)))
        if what_to_plot == "intensity+": ax = _plot(ax, D["intensity"][1], extent, aspect, vmin, vmax, cmap, xlim, ylim, "Scattered intensity, $M+$")
        elif what_to_plot == "intensity-": ax = _plot(ax, D["intensity"][0], extent, aspect, vmin, vmax, cmap, xlim, ylim, "Scattered intensity, $M-$")
        elif what_to_plot == "component+": ax = _plot(ax, D["component"][1], extent, aspect, cvmin, cvmax, cmap, xlim, ylim, "Component intensity, $+$")
        elif what_to_plot == "component-": ax = _plot(ax, D["component"][0], extent, aspect, cvmin, cvmax, cmap, xlim, ylim, "Component intensity, $-$")
        elif what_to_plot == "asymmetry": ax = _plot(ax, D["asymmetry"], extent, aspect, cvmin, cvmax, cmap, xlim, ylim, "Asymmetry")
        elif what_to_plot == "presentation": ax = _plot(ax, D["component"][1] - D["component"][0], extent, aspect, avmin, avmax, "bwr", xlim, ylim, "")
    return ax


def _plotResultsSpinEDCpolarization(D = {}, ax = None, shup = False, **kwargs):
    """"""
    accepted_kwargs = ["intensity", "figsize", "xlim", "pylim", "cylim", "fontsize", "legend", "linewidth", "fontsize"]
    intkwargs = ["polarization", "components"]
    if not shup:
        print(Fore.BLUE + f"plot(): Valid keyword arguments {accepted_kwargs}" + Fore.RESET)
        print(Fore.BLUE + f"        Pass keyword intensity to return a pyplot axis. Valid values: {intkwargs}" + Fore.RESET)
    #
    linewidth = kwargs.get("linewidth", 0.75)
    legend = kwargs.get("legend", True)
    fontsize = kwargs.get("fontsize", 10)
    xlim = kwargs.get("xlim", (None, None)) 
    pylim = kwargs.get("pylim", (None, None))
    cylim = kwargs.get("cylim", (None, None))

    def plot1(aX):
        try: aX.plot(D["x"], D["px"], color = "blue", linewidth = linewidth, label = "$P_x$")
        except: pass
        try: aX.plot(D["x"], D["py"], color = "green", linewidth = linewidth, label = "$P_y$")
        except: pass
        try: aX.plot(D["x"], D["pz"], color = "red", linewidth = linewidth, label = "$P_z$")
        except: pass
        aX.set_title("Polarization", fontsize = fontsize)
        aX.set_xlabel(D.get("labels", {}).get("x", "?"), fontsize = fontsize - 1)
        try: aX.set_ylabel(D.get("labels", {})["px"], fontsize = fontsize - 1)
        except:
            try: aX.set_ylabel(D.get("labels", {})["py"], fontsize = fontsize - 1)
            except:
                try: aX.set_ylabel(D.get("labels", {})["py"], fontsize = fontsize - 1)
                except: pass
        aX.set_xlim(xlim)
        aX.set_ylim(pylim)
        if legend: aX.legend(fontsize = fontsize -2)
        return aX
    
    def plot2(aX):
        try: 
            aX.plot(D["x"], D["component_intensity_px"][1], color = "blue", linewidth = linewidth, label = "$x+$")
            aX.plot(D["x"], D["component_intensity_px"][0], color = "blue", linewidth = linewidth, label = "$x-$", linestyle = "--")
        except: pass
        try: 
            aX.plot(D["x"], D["component_intensity_py"][1], color = "green", linewidth = linewidth, label = "$y+$")
            aX.plot(D["x"], D["component_intensity_py"][0], color = "green", linewidth = linewidth, label = "$y-$", linestyle = "--")
        except: pass
        try: 
            aX.plot(D["x"], D["component_intensity_pz"][1], color = "red", linewidth = linewidth, label = "$z+$")
            aX.plot(D["x"], D["component_intensity_pz"][0], color = "red", linewidth = linewidth, label = "$z-$", linestyle = "--")
        except: pass
        aX.set_title("Component intensity", fontsize = fontsize)
        aX.set_xlabel(D.get("labels", {}).get("x", "?"), fontsize = fontsize - 1)
        try: aX.set_ylabel(D.get("labels", {})["component_intensity_px"], fontsize = fontsize - 1)
        except:
            try: aX.set_ylabel(D.get("labels", {})["component_intensity_py"], fontsize = fontsize - 1)
            except:
                try: aX.set_ylabel(D.get("labels", {})["component_intensity_pz"], fontsize = fontsize - 1)
                except: pass
        aX.set_xlim(xlim)
        aX.set_ylim(cylim)
        if legend: aX.legend(fontsize = fontsize -2)
        return aX
    
    what_to_plot = kwargs.get("intensity", "")
    fig = None
    if not type(what_to_plot) is str: what_to_plot = ""
    what_to_plot = what_to_plot.lower()
    if not what_to_plot in intkwargs: what_to_plot = ""
    if what_to_plot == "":
        if str(type(ax)) == _axtype:
            print(Fore.MAGENTA + "plot(): A pyplot ax will not be returned unless you pass a valid value for keywork argument intensity." + Fore.RESET)
        fig, ax = plt.subplots(ncols = 2, figsize = kwargs.get("figsize", (6, 2.5)))
        ax[0] = plot1(ax[0])
        ax[1] = plot2(ax[1])
        fig.tight_layout()
    else:
        if not str(type(ax)) == _axtype:
            fig, ax = plt.subplots(figsize = kwargs.get("figsize", (5, 3)))
        if what_to_plot in "polarization": ax = plot1(ax)
        elif what_to_plot == "components": ax = plot2(ax)
        fig.tight_layout()
    return ax






# ========================================================================================================================
# ========================================================================================================================
# ========================================================================================================================

def waterfallPlot(D = {}, ax = None, shup = False, **kwargs):
    """
    Arguments:  D   a dopey dict of appropiate type
                ax  a pyplot axis
    
    Keyword arguments:  figsize     tuple
                        bunch       integer     add up a 'bunch' number of curves to one. default 0.
                        rotate      bool        default True.
                        separation  float       default 0.
                        fontsize    integer     default 10.
                        color       bool        default True.
                        yticks      bool        default True.
                        xlabel      string      
                        ylabel      string      
    """
    #
    #
    accepted_types = ["dichroism", "arpes", "2d_xy", "2d_xz", "2d_yz"]
    accepted_kwargs = ["figsize", "bunch", "rotate", "separation", "fontsize", "color", "yticks", "xlabel", "ylabel"]
    try: typ = D.get("type", "")
    except:
        print(Fore.RED + "waterfallPlot(): Argument D must be a dopey dict." + Fore.RESET); return ax
    if not typ in accepted_types:
        print(Fore.RED + f"waterfallPlot(): Argument D must be a dopey dict of type: {accepted_types}. More types will be added later on." + Fore.RESET); return ax
    #
    if not shup:
        print(Fore.BLUE + f"waterfallPlot(): Arguments D (appropiate dopey dict), ax (pyplot axis), keywork arguments {accepted_kwargs}." + Fore.RESET)
    #
    xaxis, yaxis = D.get("x", np.array([])), D.get("y", np.array([]))
    intensity = D.get("intensity", np.array([]))
    xlabel, ylabel = D.get("labels", {}).get("x", ""), D.get("labels", {}).get("y", "")
    #
    rotate = kwargs.get("rotate", True)
    if not type(rotate) is bool:
        rotate = True
        print(Fore.MAGENTA + f"waterfallPlot(): Keyword argument rotate must be a bool. Setting it to default True." + Fore.RESET)
    if rotate:
        xaxis, yaxis = yaxis, xaxis
        xlabel, ylabel = ylabel, xlabel
        intensity = intensity.transpose()
    #
    figsize = kwargs.get("figsize", (3,5))
    #
    fig = None
    if type(ax) is type(None): fig, ax = plt.subplots(figsize = figsize)
    #
    _, bunch_default = np.shape(intensity)
    bunch_default = int(bunch_default/10)
    bunch = kwargs.get("bunch", bunch_default)
    try: bunch = abs(int(bunch))
    except:
        bunch = bunch_default
        print(Fore.MAGENTA + f"waterfallPlot(): Keyword argument bunch must be an integer. Setting it to default 1." + Fore.RESET)
    #
    shx, shy = np.shape(intensity)
    shy2 = int(shy/bunch)
    new_intensity = np.zeros([shy2, shx]) * np.NaN
    i = 0
    for j in range(shy2):
        curve = np.zeros(shx)
        for k in range(bunch):
            curve += intensity[i]
            i += 1
        new_intensity[j] = curve
    #
    separation = kwargs.get("separation", 0)
    try: separation = float(separation)
    except:
        separation = 0
        print(Fore.MAGENTA + f"waterfallPlot(): Keyword argument separation must be a float. Setting it to default 0." + Fore.RESET)
    color = kwargs.get("color", True)
    if not type(color) is bool:
        color = True
        print(Fore.MAGENTA + f"waterfallPlot(): Keyword argument color must be a bool. Setting it to default True." + Fore.RESET)
    for i, curve in enumerate(new_intensity):
        if color: ax.plot(xaxis, curve + i*separation)
        else: ax.plot(xaxis, curve + i*separation, color = "k")
    fontsize = kwargs.get("fontsize", 10)
    try: fontsize = abs(int(fontsize))
    except:
        fontsize = 10
        print(Fore.MAGENTA + f"waterfallPlot(): Keyword argument fontsize must be an integer. Setting it to default 10." + Fore.RESET)
    #
    yticks = kwargs.get("yticks", True)
    if not type(yticks) is bool:
        yticks = True
        print(Fore.MAGENTA + f"waterfallPlot(): Keyword argument yticks must be a bool. Setting it to default True." + Fore.RESET)
    if not yticks: ax.set_yticks([])
    #
    xlabel2 = kwargs.get("xlabel", xlabel)
    if not type(xlabel2) is str:
        xlabel2 = xlabel
        print(Fore.MAGENTA + f"waterfallPlot(): Keyword argument xlabel must be a string. Setting it to default '{xlabel}'." + Fore.RESET)
    ax.set_xlabel(xlabel2, fontsize = fontsize)
    #
    ylabel2 = kwargs.get("ylabel", "")
    if not type(ylabel2) is str:
        ylabel2 = ""
        print(Fore.MAGENTA + f"waterfallPlot(): Keyword argument ylabel must be a string. Setting it to default ''." + Fore.RESET)
    ax.set_ylabel(ylabel2, fontsize = fontsize)
    #
    if not type(fig) is type(None): fig.tight_layout()
    #
    return ax





