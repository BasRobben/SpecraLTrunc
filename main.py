import csv
import numpy as np

def spectrumReader(loc):
    with open(loc) as file:
        reader = csv.reader(file, delimiter='\t', quoting=csv.QUOTE_NONNUMERIC)
        rows = list(reader)
        
    wavelengths = [row[0] for row in rows]
    intensities = [row[1] for row in rows]
        
    return np.array([wavelengths, intensities])

def terminateWithZero(spectrum):
    
    term_spectrum = [spectrum[0].copy(), spectrum[1].copy()]
    
    # Check lower wavelength boundary
    if term_spectrum[1][0] != 0:
        term_spectrum[0] = np.insert(term_spectrum[0], 0, term_spectrum[0][0] - (term_spectrum[0][1] - term_spectrum[0][0]))
        term_spectrum[1] = np.insert(term_spectrum[1], 0, 0)
    
    # Check upper wavelength boundary
    if term_spectrum[1][-1] != 0:
        term_spectrum[0] = np.append(term_spectrum[0], term_spectrum[0][-1] + (term_spectrum[0][-1] - term_spectrum[0][-2]))
        term_spectrum[1] = np.append(term_spectrum[1], 0)
         
    return np.array(term_spectrum)

absorption = terminateWithZero(spectrumReader("spectra/absorption.txt"))
emission = terminateWithZero(spectrumReader("spectra/emission.txt"))

# Truncation of emission spectrum for each excitation wavelength
excitation_wls = np.copy(absorption[0])
excitation_spectra = np.zeros((len(absorption[0]), len(emission[0])))

for i, exc_wl in enumerate(absorption[0]):
    excitation_spectrum = emission[1].copy()
    excitation_spectrum[emission[0] <= exc_wl] = 0
    excitation_spectra[i] = excitation_spectrum

# Formatting the output file with the required structure
with open("emission_adjusted_new.txt", "w") as f:
    f.write("dfat version 1.0\n")
    f.write("dataname: Emission Spectra\n")
    f.write("DATAPAIRS: wv inten\n")
    f.write(f"DATASETS: {len(excitation_wls)}\n")
    
    # Write header with excitation wavelengths
    f.write("\t" + "\t".join(str(int(excitation_wl)) for excitation_wl in excitation_wls) + "\n")

    # Write emission data
    for i, em_wl in enumerate(emission[0]):
        row = [f"{em_wl:.0f}"]
        row.extend(f"{spec[i]:.10f}" for spec in excitation_spectra)
        f.write("\t".join(row) + "\n")