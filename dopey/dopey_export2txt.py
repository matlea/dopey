
__version__ = "24.05.28"
__author__  = "Mats Leandersson"

print(f"{__name__}, {__version__}")


from colorama import Fore
import numpy as np



def export2txt(D = {}, fn = None, shup = False, **kwargs):
    """
    """
    if not shup:
        print(Fore.BLUE + "export2txt(D, fn, shup, **kwargs):" + Fore.RESET)
        print(Fore.BLUE + "   D: dopey dict (data), fn: string (file name), shup: boolean (shut up)" + Fore.RESET) 
    if not type(D) is dict:
        print(Fore.RED + "export2txt(D, file_name, shup, **kwargs): Argument D must be a dopey dict." + Fore.RESET); return
    if D.get("type", "NONE") == "NONE":
        print(Fore.RED + "export2txt(D, file_name, shup, **kwargs): Argument D must be a dopey dict." + Fore.RESET); return
    #
    if not type(fn) is str: fn = "data.dat"
    if len(fn) == 0: fn = "data.dat"
    if len(fn.split(".")) == 1: fn = f"{fn}.dat"
    if not len(fn.split(".")[-1]) == 3: fn = f"{fn}.dat"
    if not fn.endswith(".dat"): fn = f"{fn}.dat"
    #
    TYPE = D.get("type", "")
    #
    if TYPE == "arpes": _export2txt_ARPES(D = D, fn = fn, shup = shup, **kwargs)
    elif TYPE == "spin_edc": _export2txt_SpinEDC(D = D, fn = fn, shup = shup, **kwargs)
    elif TYPE == "spin_mdc" and D.get("experiment", {}).get("Scan_Mode", "") == "FixedEnergies": _export2txt_SpinMDC_FE(D = D, fn = fn, shup = shup, **kwargs)
    #elif TYPE == "spin_mdc" and D.get("experiment", {}).get("Scan_Mode", "") == "FixedAnalyzerTransmission": _save2txt_SpinMDC_FAT(D = D, fn = fn, shup = shup, **kwargs)  # One version
    else:
        print(Fore.MAGENTA + "export2txt(): The method is not ready for this data type. A work in progress. The different types are added one by one." + Fore.RESET)





def _export2txt_ARPES(D = {}, fn = "", shup = False, **kwargs):
    """
    """
    if not shup:
        print(Fore.BLUE + 'export2txt(): ARPES data can be saved as columns data (format = "columns", default) or as an array (format = "array").' + Fore.RESET)
    frm = kwargs.get("format", "columns").lower()
    if not frm in ["columns", "array"]:
        print(Fore.RED + 'export2txt(): Unknown value for the format keyword argument. Setting it to default "columns".' + Fore.RESET)
        frm = "columns"
    #
    file = open(fn, "w")
    file.write(f'# Type              : {D["type"]}\n')
    experiment_keys = ["Spectrum_ID", "Lens_Mode", "Scan_Mode", "Ep", "Excitation_Energy", "Dwell_Time"]
    for key in experiment_keys: file.write(f'# {key:<18}: {D["experiment"][key]}\n')
    file.write(f'# Energy            : {D["experiment"]["Energy_Axis"]}\n')
    file.write(f'# Intensity         : {D["experiment"]["Count_Rate"]}\n')
    file.write(f'# Energy_start      : {D["x"][0]}\n')
    file.write(f'# Energy_stop       : {D["x"][-1]}\n')
    file.write(f'# Energy_values     : {len(D["x"])}\n')
    file.write(f'# Angle_start       : {D["y"][0]}\n')
    file.write(f'# Angle_stop        : {D["y"][-1]}\n')
    file.write(f'# Angle_values      : {len(D["y"])}\n')
    #
    if frm == "array":
        for I in D.get("intensity"):
            row = f"{I[0]:.5e}"
            for index, i in enumerate(I):
                if index> 0: row = f"{row}\t{i:.5e}"
            file.write(f"{row}\n")
    #
    elif frm == "columns":
        file.write('#\n# Columns           : angle, energy, intensity\n')
        for ia, angle in enumerate(D["y"]):
            for ie, energy in enumerate(D["x"]):
                file.write(f'{angle:8.4f}\t{energy:7.3f}\t{D["intensity"][ia][ie]}\n')
    #
    file.close()
    #
    if not shup: print(Fore.BLUE + f"export2txt(): Data saved to {fn}")
    

def _export2txt_SpinEDC(D = {}, fn = "", shup = False, **kwargs):
    """
    """
    if not shup:
        print(Fore.BLUE + 'export2txt(): Spin EDC data is saved as columns, the first column being the energy values.' + Fore.RESET)
        print(Fore.BLUE + '              To save the mean intenities pass argument data = "mean", and to save' + Fore.RESET)
        print(Fore.BLUE + '              all intenity curves pass data = "all" (default).' + Fore.RESET)
    data = kwargs.get("data", "all").lower()
    if not data in ["all", "mean"]:
        print(Fore.RED + 'export2txt(): Unknown value for the format keyword argument. Setting it to default "all".' + Fore.RESET)
        data = "all"
    #
    file = open(fn, "w")
    file.write(f'# Type              : {D["type"]}\n')
    experiment_keys = ["Spectrum_ID", "Lens_Mode", "Scan_Mode", "Ep", "Excitation_Energy", "Dwell_Time"]
    for key in experiment_keys: file.write(f'# {key:<18}: {D["experiment"][key]}\n')
    file.write(f'# Energy            : {D["experiment"]["Energy_Axis"]}\n')
    file.write(f'# Intensity         : {D["experiment"]["Count_Rate"]}\n')
    n = np.shape(D["intensity"])[1]
    file.write(f'# EDCs_per_polarity : {n}\n')
    #
    if data == "all": 
        file.write("#\n# data              : intensity per scan\n")
        file.write(f"# columns           : energy, {n} x negative polarity, {n} x positive polarity\n")
    else: 
        file.write("#\n# data              : average intensities\n")
        file.write("# columns           : energy, negative polarity, positive polarity\n")
    #
    for i, energy in enumerate(D["x"]):
        row = f"{energy:7.3f}"
        if data == "average":
            row = f'{row}\t{D["intensity_avg"][0][i]:.5e}\t{D["intensity_avg"][0][i]:.5e}\n'
        elif data == "all":
            for j in range(n):
                row = f'{row}\t{D["intensity"][0][j][i]:.5e}'
            for j in range(n):
                row = f'{row}\t{D["intensity"][1][j][i]:.5e}'
            row = f'{row}\n'
        file.write(row)
    #
    file.close()
    if not shup: print(Fore.BLUE + f"export2txt(): Data saved to {fn}")



def _export2txt_SpinMDC_FE(D = {}, fn = "", shup = False, **kwargs):  # Note: this is almost identical to _save2txt_SpinEDC().
    """
    """
    if not shup:
        print(Fore.BLUE + 'export2txt(): Spin MDC data is saved as columns, the first column being the energy values.' + Fore.RESET)
        print(Fore.BLUE + '              To save the average intenities pass argument data = "average", and to save' + Fore.RESET)
        print(Fore.BLUE + '              all intenity curves pass data = "all" (default).' + Fore.RESET)
    data = kwargs.get("data", "all").lower()
    if not data in ["all", "average"]:
        print(Fore.RED + 'export2txt(): Unknown value for the format keyword argument. Setting it to default "all".' + Fore.RESET)
        data = "all"
    #
    NE = kwargs.get("NE", 0)  # This is used by _save2txt_SpinMDC_FAT() to select which energy to save.
    #
    file = open(fn, "w")
    file.write(f'# Type              : {D["type"]}\n')
    experiment_keys = ["Spectrum_ID", "Lens_Mode", "Scan_Mode", "Ep", "Excitation_Energy", "Dwell_Time"]
    for key in experiment_keys: file.write(f'# {key:<18}: {D["experiment"][key]}\n')
    file.write(f'# Energy            : {D["experiment"]["Energy_Axis"]}\n')
    file.write(f'# Intensity         : {D["experiment"]["Count_Rate"]}\n')
    file.write(f'# Deflector         : {D["labels"]["y"]}\n')
    n = np.shape(D["intensity"])[1]
    file.write(f'# MDCs_per_polarity : {n}\n')
    #
    if data == "all": 
        file.write("#\n# data              : intensity per scan\n")
        file.write(f"# columns           : deflector, {n} x negative polarity, {n} x positive polarity\n")
    else: 
        file.write("#\n# data              : average intensities\n")
        file.write("# columns           : deflector, negative polarity, positive polarity\n")
    #
    for i, deflector in enumerate(D["y"]):
        row = f"{deflector:7.3f}"
        if data == "average":
            row = f'{row}\t{D["intensity_mean"][0][i][NE]:.5e}\t{D["intensity_mean"][1][i][NE]:.5e}\n'
        elif data == "all":
            for j in range(n):
                row = f'{row}\t{D["intensity"][0][j][i][NE]:.5e}'
            for j in range(n):
                row = f'{row}\t{D["intensity"][1][j][i][NE]:.5e}'
            row = f'{row}\n'
        file.write(row)
    #
    file.close()
    if not shup: print(Fore.BLUE + f"export2txt(): Data saved to {fn}")



def _export2txt_SpinMDC_FAT(D = {}, fn = "", shup = False, **kwargs):
    """
    """
    if not shup:
        print(Fore.BLUE + 'export2txt(): Spin MDC data is saved as columns, the first column being the energy values.' + Fore.RESET)
        print(Fore.BLUE + '              To save the average intenities pass argument data = "mean", and to save' + Fore.RESET)
        print(Fore.BLUE + '              all intenity curves pass data = "all" (default).' + Fore.RESET + "\n")
        print(Fore.BLUE + '              Note that this MDC was reccorded in Fixed Analyzer Transmission mode so there' + Fore.RESET)
        print(Fore.BLUE + '              are several energy values (i.e. edcs) per deflector angle. The data for each' + Fore.RESET)
        print(Fore.BLUE + '              energy value will be saved to separate files.' + Fore.RESET)
    #
    data = kwargs.get("data", "all").lower()
    if not data in ["all", "mean"]:
        print(Fore.RED + 'export2txt(): Unknown value for the format keyword argument. Setting it to default "all".' + Fore.RESET)
        data = "mean"
    #
    for i, energy in enumerate(D["x"]):
        fn_ = f'{fn[:-4]}_E{i}={energy:.3f}eV{fn[-4:]}'
        _export2txt_SpinMDC_FE(D = D, fn = fn_, shup = True, data = data, NE = i)
    #