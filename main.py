import csv
import numpy as np
import streamlit as st

st.title("spectraLTrunc")
st.markdown(
    """
    **A useful tool for generating truncated emission spectra.**

    LightTools treats absorption and emission events independently, where the wavelength of the emitted photon is chosen based on the full emission spectrum of the luminescent particle regardless of the wavelength of the absorbed photon. For luminescent species with spectral overlap, this can lead to the emission of a photon with higher energy than was initially absorbed (anti-Stokes). This results in unphysical results when the particle has significant spectral overlap, or experiences considerable irradiation within the overlapping region.

    LightTools features a look-up table-style property for the emission spectrum of phosphor particles, which allows the user to specify the emission spectrum at discrete excitation (or absorption) wavelengths. SpectraLTrunc aims to utilize this feature by truncating the emission spectrum for all wavelengths shorter than the excitation wavelength.

    SpectraLTrunc requires two input parameters, the absorption and emission spectrum, and provides a look-up table as output. This file includes all necessary metadata to ensure compatibility with LightTools and allow the user to import the truncated spectra directly into their LightTools particle using the 'Upload File' feature.
    """
)

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