__version__ = "24.12.17"
__author__  = "Mats Leandersson"

print(f"{__name__}, {__version__}")



from colorama import Fore
import numpy as np

try: 
    from dopey.dopey_constants import CCD_ANALYZERS, SPIN_ANALYZERS, DEFLECTOR_X, DEFLECTOR_Y, DEFLECTORS
    DEFLECTORX, DEFLECTORY = DEFLECTORS[0], DEFLECTORS[1] # remove this when fixed everywhere
except:
    try:
        from dopey_constants import CCD_ANALYZERS, SPIN_ANALYZERS, DEFLECTOR_X, DEFLECTOR_Y, DELFECTORS
        DEFLECTORX, DEFLECTORY = DEFLECTORS[0], DEFLECTORS[1] # remove this when fixed everywhere
    except: 
        print(Fore.RED + "dopey_loader.py: coluld not import from dopey_constants.py" + Fore.RESET)
        DEFLECTORX, DEFLECTORY = "", ""








# ==================================================================================================
# ==================================================================================================
# ==================================================================================================



def load(file_name = '', shup = False, keep_raw_data = False):
    """
    """
    #
    if not type(shup) is bool: shup = False
    #
    retd = {}           # The dict to be returned.
    experiment = {}     # Sub dict, add to dict retd
    parameters = []     # Array, add to dict Experiment
    #
    if not type(file_name) is str:
        print(Fore.RED + "load(): The argument file_name must be a string." + Fore.RESET)
        return {}
    if file_name == '':
        print(Fore.RED + "load(): The argument file_name can not be an empty string." + Fore.RESET)
        return {}
    if not file_name.split(".")[-1].lower() == "xy":
        print(Fore.RED + "load(): The loader only accepts .xy files (the file HAS to have extention .xy)." + Fore.RESET)
        return {}
    try:
        f = open(file_name, 'r')
        f.close()
    except:
        print(Fore.RED + 'load(): Could not find/open the file.' + Fore.RESET)
        return {}
    
    retd.update({"file_name": file_name, "spectrum_id": -1, "experiment": {},
                 "type": "unidentified", "raw_data": {}})

    data_start_row = -1

    with open(file_name, 'rb') as f:
        ReadHeader = True
        
        for i, row_ in enumerate(f):
            row = row_.decode(errors='ignore')
            row = row.replace('\r', '').replace('\n', '')

            if ReadHeader:
                if row.startswith('# Created by'):
                    experiment.update({'Version': row.split(",")[1].replace(' ','').strip('Version')})
                if row.startswith('#   Energy Axis'):
                    experiment.update({'Energy_Axis': row.split(":")[1].replace(' ','')})
                if row.startswith('#   Count Rate'):
                    experiment.update({'Count_Rate': row.split(": ")[1].replace(' ','').replace('per','/')})
                if row.startswith('# Spectrum ID:'):
                    experiment.update({'Spectrum_ID': int(row.split(":")[1].replace(' ',''))})
                    retd.update({"spectrum_id": experiment["Spectrum_ID"]})
                if row.startswith("# Analysis Method"):   
                    experiment.update({'Analysis_Method': row.split(":")[1].replace(' ','')})
                if row.startswith("# Analyzer:"):   
                    experiment.update({'Analyzer': row.split(":")[1].replace(' ','')})
                if row.startswith("# Analyzer Lens:"):   
                    experiment.update({'Lens_Mode': row.split(":")[1].replace(' ','')})
                if row.startswith("# Scan Mode:"):                                          
                    experiment.update({'Scan_Mode': row.split(":")[1].replace(' ','')})
                if row.startswith("# Curves/Scan:"): 
                    experiment.update({'Curves_Per_Scan': int(row.split(":")[1])})
                if row.startswith("# Values/Curve:"): 
                    experiment.update({'Values_Per_Curve': int(row.split(":")[1])})
                if row.startswith("# Dwell Time:"): 
                    experiment.update({'Dwell_Time': float(row.split(":")[1])})
                if row.startswith("# Excitation Energy:"):
                    experiment.update({'Excitation_Energy': float(row.split(":")[1].replace(' ',''))})
                if row.startswith("# Kinetic Energy:"):   
                    experiment.update({'Ek': float(row.split(":")[1])})
                if row.startswith("# Pass Energy"): 
                    experiment.update({'Ep': float(row.split(":")[1])})
                if row.startswith("# OrdinateRange"):
                    tmp = row.split(":")[1].strip(' ').strip('[').strip(']').split(',')
                    experiment.update({'Ordinate_Range': [float(tmp[0]), float(tmp[1])]})
                if row.startswith("# Parameter:"):
                    par = row.split(":")[1].split('=')[0].replace('" ', '').replace(' "', '')
                    parameters.append(par)
                if row.startswith("# Number of Scans:"):     ### <<<<<<<<<< ------------------ No leading # ???
                    experiment.update({'Number_of_scans': int(row.split(':')[1])})
                if row.startswith("# Comment"):
                    comment = row.split(":")[1].lstrip(" ")
                    experiment.update({"Comment": comment})
                if row == '# Cycle: 0':
                    data_start_row = i
                if row.startswith('# ColumnLabels'):
                    try:
                        column_labels = row.split(':')[1][17:].split(' ')
                    except:
                        column_labels = ['?', '?']
                    ReadHeader = False
            else:
                f.close()
                break
        experiment.update({'parameters': parameters})
        experiment.update({'Column_labels': column_labels})    
    
    # fix some stuff -----
    if experiment.get('Energy_Axis', '') == 'KineticEnergy': experiment.update({'Energy_Axis': 'Kinetic energy (eV)'})
    if experiment.get('Count_Rate', '') == 'Counts/Second': experiment.update({'Count_Rate': 'Intensity (counts/s)'})
    
    if data_start_row == -1:
        print(Fore.RED + "load(): I could not find the start row of the data. Sorry." + Fore.RESET); return {}
    
    # -------- Prepare arrays
    parameter_values = []
    for i in range(len(parameters)): parameter_values.append([])
    # This has created an list of empty lists, one list for each parameter and one for the parameter Step. Eg. [[], [], []]
    cycle = []
    non_energy_ordinate = []
    column1, column2 = [], []

    # -------- For convenience...
    cups = experiment["Curves_Per_Scan"]
    
    # Start loading
    with open(file_name, 'rb') as f:
        for i, row_ in enumerate(f):
            if i >= data_start_row:
                row = row_.decode(errors = 'ignore')
                row = row.replace('\r', '').replace('\n', '')
                
                if "Cycle" in row and not "Curve" in row:
                    cycle.append( int( row.split(":")[1] ) )
                
                if "Parameter" in row:
                    row_parts = row.split(": ")[-1].split(" = ")
                    par_name = row_parts[0].strip('"')
                    par_value = row_parts[-1].lower()
                    for j, p in enumerate(parameters):
                        if par_name == p:
                            if par_name == "NegativePolarity":   # This to translate strings to scalars.
                                if "off" in par_value.lower(): parameter_values[j].append(1)
                                else: parameter_values[j].append(-1)
                            else:
                                parameter_values[j].append(par_value)
                
                if "NonEnergyOrdinate" in row:
                    non_energy_ordinate.append(float(row.split(":")[-1]))
                
                if not row.startswith("#") and len(row) > 0:
                    row_parts = row.split("  ")
                    column1.append(float(row_parts[0]))
                    column2.append(float(row_parts[1]))

    cycle = np.array(cycle)
    #parameter_values = np.asfarray(parameter_values)    # np.asfarray was removed from numpy 2.0. Realized by Sven Schemmelmann. 
    parameter_values = np.asarray(parameter_values, dtype = np.float64)
    non_energy_ordinate = np.unique(non_energy_ordinate)
    column1, column2 = np.array(column1), np.array(column2)

    if len(cycle) == 0:
        column1 = column1.reshape(cups, int(len(column1)/cups))
        column2 = column2.reshape(cups, int(len(column2)/cups))
    else:
        column1 = column1.reshape(len(cycle), cups, int(len(column1)/cups/len(cycle)))
        column2 = column2.reshape(len(cycle), cups, int(len(column2)/cups/len(cycle)))
    
    experiment.update({"parameters": parameters})
    retd.update({"experiment": experiment})
    rawd = {"cycle": cycle, "parameters": parameters, "parameter_values": parameter_values,  
            "non_energy_ordinate": non_energy_ordinate, "column1": column1, "column2": column2}
        
    del cups, cycle, parameter_values, non_energy_ordinate, column1, column2
    
    # for covenience...
    analyzer = experiment["Analyzer"]

    # ---------- XPS or ARPES
    if len(parameters) == 0 and analyzer in CCD_ANALYZERS:
        ordinate_range = experiment.get("Ordinate_Range", [0,0])
        if abs(ordinate_range[0]) <= 1 and abs(ordinate_range[1]) <=1:      #XPS
            retd.update({"type": "xps"})
        else:
            retd.update({"type": "arpes"})
    
    # ---------- Fermi MAP
    elif len(parameters) == 1 and DEFLECTORX in parameters and analyzer in CCD_ANALYZERS:
        retd.update({"type": "fermi_map"})
    
    # ---------- Spin EDC
    elif len(parameters) == 2 and 'NegativePolarity' in parameters and analyzer in SPIN_ANALYZERS:
        retd.update({"type": "spin_edc"})
    
    # ---------- Spin MDC
    elif len(parameters) == 3 and ((DEFLECTORX in parameters) ^ (DEFLECTORY in parameters)) and analyzer in SPIN_ANALYZERS:  # ^ is the xor operator
        retd.update({"type": "spin_mdc"})
    
    # ---------- Spin map
    elif len(parameters) == 4 and analyzer in SPIN_ANALYZERS and DEFLECTORX in parameters and DEFLECTORY in parameters:
        retd.update({"type": "spin_map"})
    
    # ---------- Target scattering spectrum
    elif len(parameters) == 6 and "ScatteringEnergy [V]" in parameters and analyzer in SPIN_ANALYZERS:
        retd.update({"type": "target_scattering_spectrum"})
    
    # ---------- ARPES with spin detector
    elif len(parameters) == 1 and (DEFLECTOR_X in parameters or DEFLECTOR_Y in parameters) and analyzer in SPIN_ANALYZERS:
        retd.update({"type": "spin_arpes"})

    
    # -----------------------------------  

    # for covenience...
    vpc = experiment["Values_Per_Curve"]  

    if not shup:
        if retd["type"] == "unidentified":
            print(Fore.MAGENTA + "load(): The structure of the loaded data is not immediately recognized but that can" + Fore.RESET)
            print(Fore.MAGENTA + "        be fixed so no worries. Let me know. Alternatively, the semi-sorted data is " + Fore.RESET)
            print(Fore.MAGENTA + "        accessible in the returned dict (key raw_data)." + Fore.RESET)
            return retd
        else:
            #print(Fore.BLUE + f'load(): This was identified as {retd["type"]} data.' + Fore.RESET)
            pass
    
    if retd["type"] in ["arpes", "xps"]:    # =========== ARPES / XPS
        retd.update({"x": rawd["column1"][0][0]})
        labels = {"x": experiment["Energy_Axis"]}
        retd.update({"y": rawd["non_energy_ordinate"]})
        if experiment.get("Ordinate_Range", [0,0])[1] > 1: labels.update({"y": "Angle (deg.)"})
        else: labels.update({"y": "Detector y-range"})
        retd.update({"intensity": rawd["column2"][0]})
        labels.update({"intensity": experiment["Count_Rate"]})
        retd.update({"labels": labels})
    
    elif retd["type"] == "fermi_map":       # =========== Fermi map
        retd.update({"x": rawd["column1"][0][0]})
        labels = {"x": experiment["Energy_Axis"]}
        retd.update({"y": rawd["non_energy_ordinate"]})
        if experiment.get("Ordinate_Range", [0,0])[0] > -1: labels.update({"y": "Angle (deg.)"})
        else: labels.update({"y": "Detector y-range"})
        retd.update({"z": rawd["parameter_values"][0]})
        labels.update({"z": "X-Deflector (deg.)"})
        retd.update({"intensity": rawd["column2"]})
        labels.update({"intensity": experiment["Count_Rate"]})
        retd.update({"labels": labels})
    
    elif retd["type"] == "spin_edc":        # =========== Spin EDC
        polarity_index = rawd["parameters"].index("NegativePolarity")
        polarity = rawd["parameter_values"][polarity_index]
        intensity_plus, intensity_minus = [], []
        for i, p in enumerate(polarity):
            #if "off" in polarity[i].lower(): intensity_plus.append(rawd["column2"][i,0,:])
            if polarity[i] == 1: intensity_plus.append(rawd["column2"][i,0,:])
            else: intensity_minus.append(rawd["column2"][i,0,:])
        retd.update({"x": rawd["column1"][0][0],
                     "polarity": np.array([-1,1]),
                     "intensity": [np.array(intensity_minus), np.array(intensity_plus)],
                     "intensity_mean": [np.mean(intensity_minus, axis = 0), np.mean(intensity_plus, axis = 0)]})
        labels = {"x": experiment["Energy_Axis"],
                  "polarity": "Magnetization direction",
                  "intensity": experiment["Count_Rate"],
                  "intensity_mean": experiment["Count_Rate"]}
        retd.update({"labels": labels})
        #
        # ------- if scans are saved separately to the .xy file
        #                 Note that the number of curves per scan is saved as 1 even if it was not like that!!!
        length = np.shape(rawd["column1"])[-1]
        if length > vpc:
            curves_per_scan = int(length/vpc)
            new_intensity_minus, new_intensity_plus = [], []
            for curve in intensity_minus:
                curves = curve.reshape(curves_per_scan, vpc)
                for c in curves: new_intensity_minus.append(c)
            for curve in intensity_plus:
                curves = curve.reshape(curves_per_scan, vpc)
                for c in curves: new_intensity_plus.append(c)
            new_intensity_minus, new_intensity_plus = np.array(new_intensity_minus), np.array(new_intensity_plus)
            retd.update({"intensity": [new_intensity_minus, new_intensity_plus]})
            retd.update({"intensity_mean": [np.mean(new_intensity_minus, axis = 0), np.mean(new_intensity_plus, axis = 0)]})
            retd.update({"x": retd["x"][:vpc]})

    
    elif retd["type"] == "spin_mdc":        # =========== Spin MDC
        polarity = rawd["parameter_values"][ rawd["parameters"].index("NegativePolarity") ]
        #
        if DEFLECTORX in parameters: DEFL = DEFLECTORX
        else: DEFL = DEFLECTORY
        deflector = rawd["parameter_values"][ rawd["parameters"].index(DEFL) ]
        un_deflector = np.unique(deflector)
        #
        step = rawd["parameter_values"][ rawd["parameters"].index("Step") ]
        un_step = np.unique(step)
        #
        step2polarity = []
        for s in un_step:
            indx = np.argwhere(step == s)[0][0]
            step2polarity.append(polarity[indx])
        #
        intensity_sorted_plus = np.zeros([len(un_step), len(un_deflector), vpc])*np.NaN
        intensity_sorted_minus = np.zeros([len(un_step), len(un_deflector), vpc])*np.NaN
        for i, arr in enumerate(rawd["column2"]):
            sindex = abs(un_step - step[i]).argmin()
            dindex = abs(un_deflector - deflector[i]).argmin()
            if step2polarity[sindex] == 1:
                intensity_sorted_plus[sindex][dindex] = arr[0]
            else:
                intensity_sorted_minus[sindex][dindex] = arr[0]
        # The plus and minus polarities are now in two separate arrays. Next, remove the nans:
        intensity_sorted_minus_clean, intensity_sorted_plus_clean = [], []
        for arr in intensity_sorted_plus:
            if not np.nansum(arr) == 0: intensity_sorted_plus_clean.append(arr)
        for arr in intensity_sorted_minus:
            if not np.nansum(arr) == 0: intensity_sorted_minus_clean.append(arr)
        #
        retd.update({"x": rawd["column1"][0][0],
                     "y": un_deflector,
                     "polarity": np.array([-1,1]),
                     "intensity": [np.array(intensity_sorted_minus_clean), np.array(intensity_sorted_plus_clean)],
                     "intensity_mean": [np.mean(intensity_sorted_minus_clean, axis = 0), np.mean(intensity_sorted_plus_clean, axis = 0)]})
        labels = {"x": experiment["Energy_Axis"],
                  "y": DEFL,
                  "polarity": "Magnetization direction",
                  "intensity": experiment["Count_Rate"],
                  "intensity_mean": experiment["Count_Rate"]}
        retd.update({"labels": labels})
        # Fix the energy axis in case of FE:
        if len(retd["x"]) == 1: retd.update({"x": np.array([retd.get("experiment", {}).get("Ek", -1)])})
        
    
    elif retd["type"] == "spin_map":        # =========== Spin map
        polarity = rawd["parameter_values"][ rawd["parameters"].index("NegativePolarity") ]
        #
        deflectorx = rawd["parameter_values"][ rawd["parameters"].index(DEFLECTORX) ]
        un_deflectorx = np.unique(deflectorx)
        #
        deflectory = rawd["parameter_values"][ rawd["parameters"].index(DEFLECTORY) ]
        un_deflectory = np.unique(deflectory)
        #
        step = rawd["parameter_values"][ rawd["parameters"].index("Step") ]
        un_step = np.unique(step)
        #
        step2polarity = []
        for s in un_step:
            indx = np.argwhere(step == s)[0][0]
            step2polarity.append(polarity[indx])
        #
        intensity_sorted_plus = np.zeros([len(un_step), len(un_deflectory), len(un_deflectorx), vpc])*np.NaN
        intensity_sorted_minus = np.zeros([len(un_step), len(un_deflectory), len(un_deflectorx), vpc])*np.NaN
        for i, arr in enumerate(rawd["column2"]):
            sindex = abs(un_step - step[i]).argmin()
            dxindex = abs(un_deflectorx - deflectorx[i]).argmin()
            dyindex = abs(un_deflectory - deflectory[i]).argmin()
            if step2polarity[sindex] == 1:
                intensity_sorted_plus[sindex][dyindex][dxindex] = arr[0]
            else:
                intensity_sorted_minus[sindex][dyindex][dxindex] = arr[0]
        # The plus and minus polarities are now in two separate arrays. Next, remove the nans:
        intensity_sorted_minus_clean, intensity_sorted_plus_clean = [], []
        for arr in intensity_sorted_plus:
            if not np.nansum(arr) == 0: intensity_sorted_plus_clean.append(arr)
        for arr in intensity_sorted_minus:
            if not np.nansum(arr) == 0: intensity_sorted_minus_clean.append(arr)
        #
        retd.update({"x": rawd["column1"][0][0],
                     "y": un_deflectorx,
                     "z": un_deflectory,
                     "polarity": np.array([-1,1]),
                     "intensity": [np.array(intensity_sorted_minus_clean), np.array(intensity_sorted_plus_clean)],
                     "intensity_mean": [np.mean(intensity_sorted_minus_clean, axis = 0), np.mean(intensity_sorted_plus_clean, axis = 0)]})
        labels = {"x": experiment["Energy_Axis"],
                  "y": DEFLECTOR_X,
                  "z": DEFLECTOR_Y,
                  "polarity": "Magnetization direction",
                  "intensity": experiment["Count_Rate"],
                  "intensity_mean": experiment["Count_Rate"]}
        retd.update({"labels": labels})
        # Fix the energy axis in case of FE:
        if len(retd["x"]) == 1: retd.update({"x": np.array([retd.get("experiment", {}).get("Ek", -1)])})
    
    elif retd["type"] == "spin_arpes":        # =========== Spin ARPES
        retd.update({"x": rawd["column1"][0][0]})
        labels = {"x": experiment["Energy_Axis"]}
        if DEFLECTOR_X in parameters: DEFL = DEFLECTOR_X
        else: DEFL = DEFLECTOR_Y
        deflector = rawd["parameter_values"][ rawd["parameters"].index(DEFL) ]
        un_deflector = np.unique(deflector)
        retd.update({"y": un_deflector})
        labels = {"y": DEFL}
        #
        I = np.zeros([np.shape(rawd["column2"])[0], np.shape(rawd["column2"])[2]])
        for i, mp in enumerate(rawd["column2"]): I[i] = mp[0]
        retd.update({"intensity": I})
        labels.update({"intensity": experiment["Count_Rate"]})
        retd.update({"labels": labels})


    elif retd["type"] == "target_scattering_spectrum":        # =========== Target scattering spectrum
        par_index = rawd["parameters"].index("ScatteringEnergy [V]")
        energy = rawd["parameter_values"][par_index]
        intensity = rawd["column2"].sum(axis = 2).T.flatten()
        retd.update({"x": energy,
                     "intensity": intensity})
        labels = {"x": "Scattering energy (eV)",
                  "intensity": experiment["Count_Rate"]}
        retd.update({"labels": labels})

    if keep_raw_data: retd.update({"raw_data": rawd})
    else: del retd["raw_data"]

    if not shup:
        dataInfo(retd)
    return retd









# ==================================================================================================
# ==================================================================================================
# ==================================================================================================




def dictContents(D = None):
   """
   """
   if not type(D) is dict:
      print(Fore.RED + "dictContents(): As perhaps is indicated by the name this method takes a dict as an argument and shows its contents..." + Fore.RESET)
      return
   if len(D) == 0:
      print(Fore.BLUE + "This is an empy dict.")
      return
   #
   _dictContents(D = D, indent = 0)

def _dictContents(D = {}, indent = 0):
   for key, value in D.items():
      print('\t' * indent + Fore.BLUE + str(key) + Fore.RESET)
      if isinstance(value, dict):
         _dictContents(value, indent+1)
      else:
         tabs = '\t' * (indent+1)
         if isinstance(value, (list, tuple, np.ndarray)):
            print(f'{tabs}{Fore.GREEN}{type(value).__name__}{Fore.RESET}, shape = {np.shape(value)}')
         elif isinstance(value, str):
            print(f'{tabs}{Fore.GREEN}{type(value).__name__}{Fore.RESET}, value = "{value}"')
         elif isinstance(value, (int, float)):
            print(f'{tabs}{Fore.GREEN}{type(value).__name__}{Fore.RESET}, value = {value}')
         else:
            print(f'{tabs}{Fore.GREEN}{type(value).__name__}{Fore.RESET}')




def info(D = {}, **kwargs): dataInfo(D = D, **kwargs)

def dataInfo(D = {}, **kwargs):
    """"""
    if not type(D) is dict:
        print(Fore.RED + "dataInfo(): The argument  (D)must be a dopey dict from dopey.load()." + Fore.RESET)
        return
    #
    if D.get("type", "NONE") == "NONE":
        print(Fore.RED + "dataInfo(): The argument (D) must be a dopey dict from dopey.load()." + Fore.RESET)
        return
    #
    if len(kwargs) > 0:
        print(Fore.MAGENTA + "dataInfo(): The method takes only one argument, and that is D (a dopey dict). Nothing else" + Fore.RESET)
    #
    FNAME, SID, TYPE, KIND = D.get("file_name", ""), D.get("spectrum_id", -1), D.get("type"), D.get("kind", "")
    EXP, LAB = D.get("experiment", {}), D.get("labels")
    fBLA, fBLU, fRES = Fore.BLACK, Fore.BLUE, Fore.RESET
    print(f"{fBLA}==========================={fRES}")
    print(f"{fBLA}Data info:{fRES}")
    if not FNAME == "":
        print(f"  {fBLA}File name:      {fBLU}{FNAME}{fRES}")
        print(f"  {fBLA}Spectrum id:    {fBLU}{SID}{fRES}")
    if  len(EXP) > 1:
        print(f"  {fBLA}Lens mode:      {fBLU}{EXP.get('Lens_Mode', '?')}{fRES}")
        print(f"  {fBLA}Scan mode:      {fBLU}{EXP.get('Scan_Mode', '?')}{fRES}")
    try:
        Ek, Ep = EXP.get("Ek", "-"), EXP.get("Ep", "-")
        print(f"  {fBLA}Ep, Ek:         {fBLU}{Ep:.2f} eV, {Ek:.2f} eV{fRES}")
    except: pass
    print(f"  {fBLA}Type of data:   {fBLU}{TYPE}{fRES}")
    if not KIND == "":
        print(f"  {fBLA}Kind of result: {fBLU}{KIND}{fRES}")
    print(f"{fBLA}Axes:{fRES}")
    for ax in ["x", "y", "z"]:
        if ax in D:
            a = D.get(ax, [])
            lena = len(a)
            lab = LAB.get(ax, "?")
            print(f"  {fBLA}{ax}:              {fBLU}{lena} points, {lab}, from {a[0]} to {a[-1]}{fRES}")
    print(f"{fBLA}Intensity:{fRES}")
    print(f"  {fBLA}intensity:      {fBLU}{np.shape(D.get('intensity', []))}{fRES}")
    if "intensity_mean" in D:
        print(f"  {fBLA}intensity_mean: {fBLU}{np.shape(D.get('intensity_mean', []))}{fRES}")
    #
    if not EXP.get("Comment", "") == "":
        print(f"{fBLA}Comment:{fRES}")
        print(f"{fBLU}{EXP.get('Comment', '')}{fRES}")
    print(f"{fBLA}==========================={fRES}")



    
