__version__ = "25.02.05"
__author__  = "Mats Leandersson"

print(f"{__name__}, {__version__} (Zip loader by Craig Polley)")


try:	import zipfile
except ImportError: print("\tWarning: Couldn't import the zipfile module. You will not be able to work with SES .zip files")

try:	import tempfile
except ImportError: print("\tWarning: Couldn't import the tempfile module. You will not be able to work with SES .zip files")

import numpy as np




def ses_zip_load(file_name = '', shup = False, **kwargs):
	"""
	This meathod loads zip data from SES. It is heavily dependent on Craig Polley's SES_zip.py.
	The data is loaded by _ses_zip_load() into a pesto dics and then rearranged into dopey format.
	"""
	region_index = kwargs.get("regio_index", 0)
	ses = _ses_zip_load(fileName = file_name, regionIndex = region_index)
	#
	for key in ['Metadata', 'Axis', 'AxisLabel', 'AxisUnits', 'data']:
		if not key in ses:
			print("zip_load(): missing keys in the data dict loaded by pesto.")
			return {}
	#
	retdict = {"file_name": file_name, "spectrum_id": 99999, "experiment": {}, "type": "fermi_map"}
	retdict.update({"x": ses["Axis"][0], "y": ses["Axis"][1], "z": ses["Axis"][2]})
	retdict.update({"intensity": np.array([]), "labels": {"x": ses["AxisLabel"][0], "y": ses["AxisLabel"][1], "z": ses["AxisLabel"][2], "intensity": "?"}})
	#
	shp = np.shape(ses["data"])
	new_data = np.zeros([shp[2], shp[1], shp[0]])
	for i3 in range(shp[2]):
		new_data[i3] = ses["data"][:,:,i3].T
	retdict.update({"intensity": new_data})
	#
	experiment = {"Version": "Scienta " + ses["Metadata"]["Instrument"]}
	experiment.update({"Energy_Axis": ses["Metadata"]["Energy Unit"], "Count_Rate": "?", "Spectrum_ID": retdict["spectrum_id"]})
	experiment.update({"Analysis_Method": "N/A", "Analyzer": "PhoibosCCD", "Lens_Mode": ses["Metadata"]["Lens Mode"], "Scan_Mode": ses["Metadata"]["Acquisition Mode"]})
	experiment.update({"Ek": np.NaN, "Ep": ses["Metadata"]["Pass Energy"]})
	retdict.update({"experiment": experiment})
	retdict.update({"ses": ses["Metadata"]})
	#
	return retdict
	
	
	
	
		
	
	





def _ses_zip_load(fileName,**kwargs):
	"""
	FROM CRAIG POLLEY'S SES_zip.py
	"""

	beQuiet=kwargs.get('beQuiet')
	regionIndex=kwargs.get('regionIndex')


	regionNames=[]

	with zipfile.ZipFile(fileName) as z:
		for filename in z.namelist():
			if filename.startswith('Spectrum_') and filename.endswith('.bin'):
				regionNames.append(filename.replace("Spectrum_","").replace(".bin",""))

		if regionIndex>len(regionNames):
			if len(regionNames)==1: assert False, "This zip file contains only a single region, with index 1. You asked for region #{}, which doesn't exist.".format(regionIndex)
			else: assert False, "This zip file contains regions with indices spanning (1..{}). You asked for region #{}, which doesn't exist.".format(len(regionNames)-1,regionIndex)
			return 

		loadedSpectrum={}
		loadedSpectrum['Metadata']={}
		loadedSpectrum['Axis']=[[],[],[]]
		loadedSpectrum['AxisLabel']=["","",""]
		loadedSpectrum['AxisUnits']=["","",""]

		filename = 'Spectrum_'+regionNames[regionIndex-1]+'.ini'     
		
		with z.open(filename) as f: 

			for l in f:
				line=l.decode()
				
				#---- Energy axis ----
				if line.startswith("widthoffset="): loadedSpectrum['Metadata']['Low Energy']=float(line.replace("widthoffset=","").rstrip('\n').replace(",","."))
				if line.startswith("width="): numEnergyPoints=int(line.replace("width=","").rstrip('\n').replace(",","."))
				if line.startswith("widthdelta="): loadedSpectrum['Metadata']['Energy Step']=float(line.replace("widthdelta=","").rstrip('\n').replace(",",".")) 
				
				#-------------------
				
				#---- Analyzer slit axis ----
				if line.startswith("heightoffset="): loadedSpectrum['Metadata']['Low Analyzer Angle']=float(line.replace("heightoffset=","").rstrip('\n').replace(",","."))
				if line.startswith("height="): numAnalyzerAnglePoints=int(line.replace("height=","").rstrip('\n').replace(",","."))
				if line.startswith("heightdelta="): loadedSpectrum['Metadata']['Analyzer Angle Step']=float(line.replace("heightdelta=","").rstrip('\n').replace(",",".")) 
				#-------------------

				#---- Deflector axis ----
				if line.startswith("depthoffset="): loadedSpectrum['Metadata']['Low Deflector Angle']=float(line.replace("depthoffset=","").rstrip('\n').replace(",","."))
				if line.startswith("depth="): numDeflectorAnglePoints=int(line.replace("depth=","").rstrip('\n').replace(",","."))
				if line.startswith("depthdelta="): loadedSpectrum['Metadata']['Deflector Angle Step']=float(line.replace("depthdelta=","").rstrip('\n').replace(",",".")) 
				#-------------------

		filename = regionNames[regionIndex-1]+'.ini' 
		with z.open(filename) as f:
			for lineNumber, l in enumerate(f):
				line=l.decode()
				if line.startswith("Region Name="): loadedSpectrum['Metadata']['Region Name']=line.replace("Region Name=","").rstrip('\r\n')
				if line.startswith("Lens Mode="): loadedSpectrum['Metadata']['Lens Mode']=line.replace("Lens Mode=","").rstrip('\r\n')
				if line.startswith("Pass Energy="): loadedSpectrum['Metadata']['Pass Energy']=int(line.replace("Pass Energy=","").rstrip('\r\n'))
				if line.startswith("Number of Sweeps="): loadedSpectrum['Metadata']['Number of Sweeps']=int(line.replace("Number of Sweeps=","").rstrip('\r\n'))
				if line.startswith("Excitation Energy="): loadedSpectrum['Metadata']['Excitation Energy']=float(line.replace("Excitation Energy=","").rstrip('\r\n').replace(",","."))
				if line.startswith("Energy Scale="): loadedSpectrum['Metadata']['Energy Scale']=line.replace("Energy Scale=","").rstrip('\r\n')
				if line.startswith("Acquisition Mode="): loadedSpectrum['Metadata']['Acquisition Mode']=line.replace("Acquisition Mode=","").rstrip('\r\n')
				if line.startswith("Energy Unit="): loadedSpectrum['Metadata']['Energy Unit']=line.replace("Energy Unit=","").rstrip('\r\n')
				if line.startswith("Step Time="): loadedSpectrum['Metadata']['Step Time']=float(line.replace("Step Time=","").rstrip('\r\n').replace(",","."))
				if line.startswith("Detector First X-Channel="): loadedSpectrum['Metadata']['Detector First X-Channel']=int(line.replace("Detector First X-Channel=","").rstrip('\r\n'))
				if line.startswith("Detector Last X-Channel="): loadedSpectrum['Metadata']['Detector Last X-Channel']=int(line.replace("Detector Last X-Channel=","").rstrip('\r\n'))
				if line.startswith("Detector First Y-Channel="): loadedSpectrum['Metadata']['Detector First Y-Channel']=int(line.replace("Detector First Y-Channel=","").rstrip('\r\n'))
				if line.startswith("Detector Last Y-Channel="): loadedSpectrum['Metadata']['Detector Last Y-Channel']=int(line.replace("Detector Last Y-Channel=","").rstrip('\r\n'))
				if line.startswith("Number of Slices="): loadedSpectrum['Metadata']['Number of Slices']=int(line.replace("Number of Slices=","").rstrip('\r\n'))
				if line.startswith("File="): 
					path = line.replace("File=","").rstrip('\n').replace("\\\\","\\")
					loadedSpectrum['Metadata']['File Path']= path[:path.rindex('\\')+1] + fileName          
				if line.startswith("Sequence="): loadedSpectrum['Metadata']['Sequence']=line.replace("Sequence=","").rstrip('\r\n').replace("\\\\","\\")
				if line.startswith("Spectrum Name="): loadedSpectrum['Metadata']['Spectrum Name']=line.replace("Spectrum Name=","").rstrip('\r\n')
				if line.startswith("Instrument="): loadedSpectrum['Metadata']['Instrument']=line.replace("Instrument=","").rstrip('\r\n')
				if line.startswith("Location="): loadedSpectrum['Metadata']['Location']=line.replace("Location=","").rstrip('\r\n')
				if line.startswith("User="): loadedSpectrum['Metadata']['User']=line.replace("User=","").rstrip('\r\n')
				if line.startswith("Sample="): loadedSpectrum['Metadata']['Sample']=line.replace("Sample=","").rstrip('\r\n')
				if line.startswith("Comments="): loadedSpectrum['Metadata']['Comments']=line.replace("Comments=","").rstrip('\r\n')
				if line.startswith("Date="): loadedSpectrum['Metadata']['Date']=line.replace("Date=","").rstrip('\r\n')
				if line.startswith("Time="): loadedSpectrum['Metadata']['Time']=line.replace("Time=","").rstrip('\r\n')
				if line.startswith("Time per Spectrum Channel="): loadedSpectrum['Metadata']['Time per Spectrum Channel']=float(line.replace("Time per Spectrum Channel=","").rstrip('\r\n').replace(",","."))
				if line.startswith("DetectorMode="): loadedSpectrum['Metadata']['DetectorMode']=line.replace("DetectorMode=","").rstrip('\r\n')
				if line.startswith("A="): loadedSpectrum['Metadata']['Manipulator Azimuth']=float(line.replace("A=","").rstrip('\r\n').replace(",","."))
				if line.startswith("P="): loadedSpectrum['Metadata']['Manipulator Polar']=float(line.replace("P=","").rstrip('\r\n').replace(",","."))
				if line.startswith("T="): loadedSpectrum['Metadata']['Manipulator Tilt']=float(line.replace("T=","").rstrip('\r\n').replace(",","."))
				if line.startswith("X="): loadedSpectrum['Metadata']['Manipulator X']=float(line.replace("X=","").rstrip('\r\n').replace(",","."))
				if line.startswith("Y="): loadedSpectrum['Metadata']['Manipulator Y']=float(line.replace("Y=","").rstrip('\r\n').replace(",","."))
				if line.startswith("Z="): loadedSpectrum['Metadata']['Manipulator Z']=float(line.replace("Z=","").rstrip('\r\n').replace(",","."))




		angleStart=loadedSpectrum['Metadata']['Low Analyzer Angle']
		angleStep=loadedSpectrum['Metadata']['Analyzer Angle Step']
		angleEnd=loadedSpectrum['Metadata']['Low Analyzer Angle']+(numAnalyzerAnglePoints-1)*angleStep
		




		energyStart=loadedSpectrum['Metadata']['Low Energy']
		energyStep=loadedSpectrum['Metadata']['Energy Step']
		energyEnd=loadedSpectrum['Metadata']['Low Energy']+(numEnergyPoints-1)*energyStep
		#loadedSpectrum['yAxis']=np.linspace(energyStart,energyEnd,numEnergyPoints)
		#if loadedSpectrum['Metadata']['Energy Scale'].startswith("Kinetic"):loadedSpectrum['yAxisLabel']="Kinetic energy (eV)"
		#else: loadedSpectrum['yAxisLabel']="Binding energy (eV)"
		#loadedSpectrum['yAxisLabel']="Energy (eV)" 

		loadedSpectrum['Axis'][0]=np.linspace(energyStart,energyEnd,numEnergyPoints)
		if loadedSpectrum['Metadata']['Energy Scale'].startswith("Kinetic"):
			loadedSpectrum['AxisLabel'][0]="Kinetic energy"
		else: loadedSpectrum['AxisLabel'][0]="Binding energy"
		loadedSpectrum['AxisUnits'][0]="eV" 

		loadedSpectrum['Axis'][1]=np.linspace(angleStart,angleEnd,numAnalyzerAnglePoints)
		loadedSpectrum['AxisLabel'][1]="Analyzer angle" 
		loadedSpectrum['AxisUnits'][1]="$\degree$" 


		angleStart=loadedSpectrum['Metadata']['Low Deflector Angle']
		angleStep=loadedSpectrum['Metadata']['Deflector Angle Step']
		angleEnd=loadedSpectrum['Metadata']['Low Deflector Angle']+(numDeflectorAnglePoints-1)*angleStep
		loadedSpectrum['Axis'][2]=np.linspace(angleStart,angleEnd,num=numDeflectorAnglePoints,endpoint=True)
		loadedSpectrum['AxisLabel'][2]="Deflector angle" 
		loadedSpectrum['AxisUnits'][2]="$\degree$" 

		#---------- Load the data matrix ----------

		filename = 'Spectrum_'+regionNames[regionIndex-1]+'.bin' 	
		tempDirectory=tempfile.TemporaryDirectory()	
		z.extract(filename,tempDirectory.name)

		x=loadedSpectrum['Axis'][1]			
		y=loadedSpectrum['Axis'][0]
		z=loadedSpectrum['Axis'][2]

		with open(tempDirectory.name+"/"+filename, "r") as f:
			binaryBlob=np.fromfile(f,dtype=np.float32) 

		loadedSpectrum['data']=np.zeros((len(x),len(y),len(z)),np.float32)

		for jj in range(len(x)):
			precalc1 = jj*len(y)
			for kk in range(len(z)): 
				index=(kk*len(x)*len(y)) + precalc1  
				loadedSpectrum['data'][jj,:,kk]=binaryBlob[index:index+len(y)]
	loadedSpectrum['data']=loadedSpectrum['data'].transpose(1,0,2)	
	if beQuiet==False: 
		if len(z)==1: print("Single frame acquired at {:.2f} deg".format(z[0]))
		else: print("Deflected from {:.2f} deg to {:.2f} deg with stepsize {:.2f}".format(z[0],z[-1],abs(z[1]-z[0])))
	return loadedSpectrum






