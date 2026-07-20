import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import streamlit as st

def truncate_single_emission(emission, excitation_wl):
    """
    Returns the truncated emission spectrum for a single excitation wavelength.
    """

    truncated_emission = emission[1].copy()

    # Remove anti-Stokes emission
    truncated_emission[emission[0] < excitation_wl] = 0

    return truncated_emission

def spectral_trunc(absorption, emission):
    """
    Generates the complete LightTools emission lookup table.
    """

    excitation_wls = np.copy(absorption[0])

    excitation_spectra = np.zeros((len(absorption[0]), len(emission[0])))

    for i, exc_wl in enumerate(excitation_wls):
        excitation_spectra[i] = truncate_single_emission(emission,exc_wl)

    return excitation_wls, excitation_spectra

def terminate_with_zero(spectrum):
    """
    Terminates given spectra with 0 on either end, if not aleady the case.
    """
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

def writeOutput(excitation_wls, excitation_spectra, emission):
    """
    Generates the LightTools lookup table as a text string.
    """

    output = ""
    output += "dfat version 1.0\n"
    output += "dataname: Emission Spectra\n"
    output += "DATAPAIRS: wv inten\n"
    output += f"DATASETS: {len(excitation_wls)}\n"

    # Header with excitation wavelengths
    output += "\t" + "\t".join(str(int(excitation_wl)) for excitation_wl in excitation_wls) + "\n"

    # Emission data
    for i, em_wl in enumerate(emission[0]):
        row = [f"{em_wl:.0f}"]
        row.extend(f"{spec[i]:.10f}" for spec in excitation_spectra)
        output += "\t".join(row) + "\n"

    return output

plt.style.use('dark_background')

st.title("spectraLTrunc")
st.write("**:chart_with_upwards_trend: A useful tool for generating truncated emission spectra :chart_with_downwards_trend:**")
st.subheader("Description", divider = "gray")
st.markdown(
    """
    :orange[LightTools] treats absorption and emission events independently, where the wavelength of the emitted photon is chosen based on the full emission spectrum of the luminescent particle regardless of the wavelength of the absorbed photon. For luminescent species with spectral overlap, this can lead to the emission of a photon with higher energy than was initially absorbed (anti-Stokes). This results in unphysical results when the particle has significant spectral overlap, or experiences considerable irradiation within the overlapping region.

    :orange[LightTools] features a look-up table-style property for the emission spectrum of phosphor particles, which allows the user to specify the emission spectrum at discrete excitation (or absorption) wavelengths. :blue[**SpectraLTrunc**] aims to utilize this feature by truncating the emission spectrum for all wavelengths shorter than the excitation wavelength.

    :blue[**SpectraLTrunc**] requires two input parameters, the absorption and emission spectrum, and provides a look-up table as output. This file includes all necessary metadata to ensure compatibility with :orange[LightTools] and allow the user to import the truncated spectra directly into their :orange[LightTools] particle using the 'Load File' feature.
    """
)

# Function to convert Streamlit table into spectrum arrays
def table_to_spectrum(table):
    # Remove completely empty rows
    table = table.dropna()

    if len(table) == 0:
        return np.empty((2,0))

    # Convert to numeric values
    wavelength = pd.to_numeric(table["Wavelength (nm)"], errors = "coerce")
    intensity = pd.to_numeric(table["Intensity"], errors = "coerce")

    # Remove rows where conversion failed
    mask = wavelength.notna() & intensity.notna()

    # Convert to numpy arrays
    wavelength = np.array(wavelength[mask], dtype=float)
    intensity = np.array(intensity[mask], dtype=float)

    # Force negative intensities to zero
    intensity[intensity < 0] = 0

    # Sort in ascending order of wavelength
    idx = np.argsort(wavelength)
    wavelength = wavelength[idx]
    intensity = intensity[idx]

    # Combine into one spectrum
    spectrum = np.array([wavelength, intensity])

    # Terminate either end of spectrum by zero if not already
    spectrum = terminate_with_zero(spectrum)

    return spectrum

def plot_spectra(absorption, emission):

    is_empty_abs = len(absorption[0]) <= 0
    is_empty_ems = len(emission[0]) <= 0

    if is_empty_abs and is_empty_ems:
        st.info("Enter absorption and/or emission spectrum data to display plot.")
        return
    
    fig, ax = plt.subplots(figsize=(10, 7))

    if not is_empty_abs:
        ax.plot(absorption[0], absorption[1], linestyle = "-", label="Absorption")
    
    if not is_empty_ems:
        ax.plot(emission[0], emission[1], linestyle = "--", label="Emission")

    ax.set(
        xlabel = "Wavelength (nm)",
        ylabel = "Intensity (a.u.)"
    )

    # Determine wavelength range based on available spectra
    wavelengths = []

    if not is_empty_abs:
        wavelengths.extend(absorption[0])

    if not is_empty_ems:
        wavelengths.extend(emission[0])

    ax.set(
        xlim=(np.min(wavelengths), np.max(wavelengths)),
        ylim=(0, None)
    )

    ax.legend()

    # Beautiful custom grid
    ax.grid(True, which='major', linestyle='-', linewidth=0.75, alpha=0.25)
    ax.minorticks_on()
    ax.grid(True, which='minor', linestyle='-', linewidth=0.25, alpha=0.15)

    st.pyplot(fig)

# Input tables for absorption and emission spectra
st.subheader("Absorption spectrum", divider = "gray")
st.write("Enter the absorption spectrum in the table below.")
st.write("*Note that data from Excel can be directly copied into the table below.*")
absorption_table = st.data_editor(
    pd.DataFrame(columns=["Wavelength (nm)", "Intensity"]),
    num_rows="dynamic",
    key = "absorption_table"
)

st.subheader("Emission spectrum", divider = "gray")
st.write("Enter the emission spectrum in the table below.")
st.write("*Note that data from Excel can be directly copied into the table below.*")
emission_table = st.data_editor(
    pd.DataFrame(columns=["Wavelength (nm)", "Intensity"]),
    num_rows="dynamic",
    key = "emission_table"
)

# Convert tables to spectra
absorption = table_to_spectrum(absorption_table)
emission = table_to_spectrum(emission_table)

# Plotting spectrum
st.subheader("Preview spectral input", divider="gray")
plot_spectra(absorption, emission)


## Preview truncated emission spectrum
st.subheader("Preview truncated emission spectra", divider="gray")
if len(absorption[0]) > 0 and len(emission[0]) > 0:
    # Slider for excitation wavelength
    selected_excitation = st.slider(
        "User the slider below to select excitation wavelength (nm)",
        min_value=int(np.min(absorption[0])),
        max_value=int(np.max(absorption[0])),
        value=int(absorption[0][len(absorption[0])//2]),
        step=1
    )

    # Calculate only this spectrum
    truncated_emission = truncate_single_emission(emission, selected_excitation)

    fig, ax = plt.subplots(figsize=(10, 5))

    # Original emission
    ax.plot(emission[0], emission[1], linestyle="--", label="Original emission")

    # Truncated emission
    ax.plot(emission[0], truncated_emission, linestyle="-", label=f"Truncated emission ({selected_excitation} nm excitation)")

    # Explicitly show selected excitation wavelength
    ax.axvline(selected_excitation, linestyle=":", linewidth=1, label="Excitation wavelength")   

    ax.set(
        xlabel="Emission wavelength (nm)",
        ylabel="Intensity (a.u.)",
        ylim=(0, None)
    )

    ax.legend()

    # Beautiful custom grid
    ax.grid(True, which="major", linestyle="-", linewidth=0.75, alpha=0.25)
    ax.minorticks_on()
    ax.grid(True, which="minor", linestyle="-", linewidth=0.25, alpha=0.15)

    st.pyplot(fig)
else:
    st.info("Enter absorption and emission spectrum to generate truncated emission spectrum.")

## Compute full lookup table and cache result
@st.cache_data
def generate_output_file(absorption, emission):
    excitation_wls, excitation_spectra = spectral_trunc(absorption, emission)

    return writeOutput(excitation_wls, excitation_spectra, emission)

## Download output file
st.subheader("Download output", divider="gray")
if len(absorption[0]) > 0 and len(emission[0]) > 0:

    output_file = generate_output_file(absorption, emission)

    st.download_button(
        label="Download LightTools file",
        data=output_file,
        file_name="spectraltrunc_output.txt",
        mime="text/plain"
    )

else:
    st.info("Enter absorption and emission spectrum to download LightTools file.")

## How to use
st.subheader("How to Use", divider = "gray")
st.write("Enter your desired absorption and emission spectra into the :blue[**SpectraLTrunc**] tool presented above. Ensure that the preview absorption and emission spectra look as expect. A preview of a truncated emission spectrum may be shown by specifying an excitation wavelength using the slider. The :blue-background[Download LightTools file] button downloads a text file containing all relevant truncated emission spectra as a function of excitation wavelength. This file includes all necessary metadata to ensure compatibility with :orange[LightTools] and allow the user to import the truncated spectra directly into their :orange[LightTools] particle using the built-in 'Load File' feature. A basic description of adding particles and uploading the desired truncated emission file into :orange[LightTools] is provided below.")

st.write("Within :orange[LightTools], navigate to the :blue-background[Material Manager] and select your custom material. Add a luminescent particle by clicking :blue-background[Add Particle] and selecting :blue-background[Phosphor / Quantum Dot].")
st.image("images/add_particle.PNG")

st.write("Open the newly-added particle in the drop-down menu of the material. Click on :blue-background[Emission Spectra] in the navigation tab. Here you will find a default emission spectrum lookup table. To change this into the desired truncated emission spectrum, load the text file obtained above into the custom particle using the :blue-background[Load File] button and selecting the desired file. The default table should now have changed to the truncated emission spectra lookup table, where the first row represents the excitation wavelengths and correspond to the wavelengths specified in the input absorption spectrum. The wavelengths in the first column should correspond those in the input emission spectrum.")
st.image("images/load_file.PNG")