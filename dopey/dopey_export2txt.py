
__version__ = "24.11.30"
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
    elif TYPE == "spin_mdc" and D.get("experiment", {}).get("Scan_Mode", "") == "FixedAnalyzerTransmission": _export2txt_SpinMDC_FAT(D = D, fn = fn, shup = shup, **kwargs)
    elif TYPE == "spin_map" and D.get("experiment", {}).get("Scan_Mode", "") == "FixedEnergies": _export2txt_SpinMap_FE(D = D, fn = fn, shup = shup, **kwargs)
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
    accepted_kwargs = ["data"]
    accepted_data = ["scans", "mean"]
    if not shup:
        print(Fore.BLUE + f'export2txt(): Accepted keyword arguments are {accepted_kwargs}.' + Fore.RESET)
        print(Fore.BLUE + f'export2txt(): Accepted values for keyword argument data are {accepted_data}.' + Fore.RESET)
    #
    data = kwargs.get("data", "scans").lower()
    if not data in accepted_data:
        print(Fore.RED + 'export2txt(): Unknown value for the keyword argument data. Setting it to default "scans".' + Fore.RESET)
        data = "all"
    #
    file = open(fn, "w")
    file.write(f'# Type              : {D["type"]}\n')
    experiment_keys = ["Spectrum_ID", "Lens_Mode", "Scan_Mode", "Ep", "Excitation_Energy", "Dwell_Time"]
    for key in experiment_keys: file.write(f'# {key:<18}: {D["experiment"][key]}\n')
    file.write(f'# Energy            : {D["experiment"]["Energy_Axis"]}\n')
    file.write(f'# Intensity         : {D["experiment"]["Count_Rate"]}\n')
    n = np.shape(D["intensity"])[1]
    #
    if data == "scans": 
        file.write("#\n# data              : intensity per scan\n")
        file.write(f"# columns           : energy, {n} x negative polarity, {n} x positive polarity\n")
    else: 
        file.write("#\n# data              : average intensities\n")
        file.write("# columns           : energy, negative polarity, positive polarity\n")
    #
    for i, energy in enumerate(D["x"]):
        row = f"{energy:7.3f}"
        if data == "mean":
            row = f'{row}\t{D["intensity_avg"][0][i]:.5e}\t{D["intensity_avg"][0][i]:.5e}\n'
        elif data == "scans":
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
    accepted_kwargs = ["data"]
    accepted_data = ["scans", "mean"]
    if not shup:
        print(Fore.BLUE + f'export2txt(): Accepted keyword arguments are {accepted_kwargs}.' + Fore.RESET)
        print(Fore.BLUE + f'export2txt(): Accepted values for keyword argument data are {accepted_data}.' + Fore.RESET)
    #

    data = kwargs.get("data", "mean").lower()
    if not data in accepted_data:
        print(Fore.RED + 'export2txt(): Unknown value for the keyword argument data. Setting it to default "mean".' + Fore.RESET)
        data = "mean"
    #
    NE = kwargs.get("NE", 0)  # This is used by _save2txt_SpinMDC_FAT() to select which energy to save.
    #
    file = open(fn, "w")
    file.write(f'# Type              : {D["type"]}\n')
    experiment_keys = ["Spectrum_ID", "Lens_Mode", "Scan_Mode", "Ep", "Excitation_Energy", "Dwell_Time"]
    for key in experiment_keys: file.write(f'# {key:<18}: {D["experiment"][key]}\n')
    file.write(f'# Energy axis       : {D["experiment"]["Energy_Axis"]}\n')
    file.write(f'# Intensity         : {D["experiment"]["Count_Rate"]}\n')
    file.write(f'# Deflector         : {D["labels"]["y"]}\n')
    file.write(f'# Energy            : {D["x"][0]}\n')
    n = np.shape(D["intensity"])[1]
    file.write(f'# MDCs_per_polarity : {n}\n')
    #
    if data == "scans": 
        file.write("#\n# data              : intensity per scan\n")
        file.write(f"# columns           : deflector, {n} x negative polarity, {n} x positive polarity\n")
    else: 
        file.write("#\n# data              : average intensities\n")
        file.write("# columns           : deflector, negative polarity, positive polarity\n")
    #
    for i, deflector in enumerate(D["y"]):
        row = f"{deflector:6.2f} "
        if data == "mean":
            row = f'{row} {D["intensity_mean"][0][i][NE]:.5e} {D["intensity_mean"][1][i][NE]:.5e}\n'
        elif data == "scans":
            for j in range(n):
                row = f'{row} {D["intensity"][0][j][i][NE]:.5e}'
            for j in range(n):
                row = f'{row} {D["intensity"][1][j][i][NE]:.5e}'
            row = row + "\n"
        file.write(row)
    #
    file.close()
    if not shup: print(Fore.BLUE + f"export2txt(): Data saved to {fn}")



def _export2txt_SpinMDC_FAT(D = {}, fn = "", shup = False, **kwargs):
    """
    """
    #
    print(Fore.LIGHTBLACK_EX + "export2txt(): This data format (spin MDC in Fixed Analyzer Transmission mode) is not yet ready for be written to text files." + Fore.RESET); return
    #
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



def _export2txt_SpinMap_FE(D = {}, fn = "", shup = False, **kwargs):
    """
    """
    #
    accepted_kwargs = ["data"]
    accepted_data = ["scans", "mean"]
    if not shup:
        print(Fore.BLUE + f'export2txt(): Accepted keyword arguments are {accepted_kwargs}.' + Fore.RESET)
        print(Fore.BLUE + f'export2txt(): Accepted values for keyword argument data are {accepted_data}.' + Fore.RESET)
    #
    data = kwargs.get("data", "mean").lower()
    if not data in accepted_data:
        print(Fore.RED + f'export2txt(): Unknown value for the format keyword argument. Available values are: {accepted_data}. Setting it to default "scans".' + Fore.RESET)
        data = "scans"
    #
    fn_base = fn.split(".")[0]
    fn_defl1, fn_defl2 = f"{fn_base}_defl1.dat", f"{fn_base}_defl2.dat"
    file1, file2 = open(fn_defl1, "w"), open(fn_defl2, "w")
    file1.write(f'# Deflector         : {D["labels"]["y"]}\n')
    file2.write(f'# Deflector         : {D["labels"]["z"]}\n')
    for defl in D["y"]: file1.write(f"{defl:6.2f}\n")
    for defl in D["z"]: file2.write(f"{defl:6.2f}\n")
    file1.close(); file2.close()
    if not shup:
        print(Fore.BLUE + f'export2txt(): The deflector axes are written to files {fn_defl1} and {fn_defl2}.' + Fore.RESET)
    #
    fn_plus, fn_minus = f"{fn_base}_plus.dat", f"{fn_base}_minus.dat"
    file1, file2 = open(fn_plus, "w"), open(fn_minus, "w")
    for file in [file1, file2]:
        file.write(f'# Type              : {D["type"]}\n')
    file1.write(f'# Polarity          : minus\n'); file2.write(f'# Polarity          : minus\n')
    for file in [file1, file2]:
        experiment_keys = ["Spectrum_ID", "Lens_Mode", "Scan_Mode", "Ep", "Excitation_Energy", "Dwell_Time"]
        for key in experiment_keys: file.write(f'# {key:<18}: {D["experiment"][key]}\n')
        file.write(f'# Energy axis       : {D["experiment"]["Energy_Axis"]}\n')
        file.write(f'# Intensity         : {D["experiment"]["Count_Rate"]}\n')
        file.write(f'# Deflector1        : {D["labels"]["y"]}\n')
        file.write(f'# Deflector2        : {D["labels"]["z"]}\n')
        file.write(f'# Energy            : {D["x"][0]}\n')
    #
    if data == "mean":
        for row in D["intensity_mean"][1]:
            wrow = ""
            for r in row: wrow += f"{r[0]:.5e}\t"
            file1.write(wrow + "\n")
        for row in D["intensity_mean"][0]:
            wrow = ""
            for r in row: wrow += f"{r[0]:.5e}\t"
            file2.write(wrow + "\n")
        if not shup:
            print(Fore.BLUE + f'export2txt(): The mean intensities are written to files {fn_plus} and {fn_minus}.' + Fore.RESET)
    #
    elif data == "scans":
        for file in [file1, file2]: file.write("#\n")
        for i, scan in enumerate(D["intensity"][1]):
            file1.write(f"# Scan: {i}\n")
            for row in scan:
                wrow = ""
                for r in row: wrow += f"{r[0]:.5e}\t"
                file1.write(wrow + "\n")
        for i, scan in enumerate(D["intensity"][0]):
            file2.write(f"# Scan: {i}\n")
            for row in scan:
                wrow = ""
                for r in row: wrow += f"{r[0]:.5e}\t"
                file2.write(wrow + "\n")
        if not shup:
            print(Fore.BLUE + f'export2txt(): The intensities for the individual scans are written to files {fn_plus} and {fn_minus}.' + Fore.RESET)
    #
    file1.close(); file2.close()


    
    
