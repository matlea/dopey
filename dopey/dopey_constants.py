__version__ = "24.09.18"
__author__  = "Mats Leandersson"

print(f"{__name__}, {__version__}")

CCD_ANALYZERS = ["PhoibosCCD", "AnalyzerCCD"]
SPIN_ANALYZERS = ["PhoibosSpin"]
SHERMAN = 0.29
DEFLECTORS = ['ShiftX [a.u.]', 'ShiftY [a.u.]']
DEFLECTOR_X, DEFLECTOR_Y = DEFLECTORS[0], DEFLECTORS[1]

DATA_AXES = ["x", "y", "z"]
DATA_INTENSITIES = ["intensity", "intensity_mean"]

MEASUREMENT_TYPES = ["xps", "arpes", "fermi_map", "spin_edc", "spin_mdc", "spin_map", "spin_arpes", "target_scattering_spectrum"]