import csv
import numpy as np
import matplotlib.pyplot as plt

# # Read data
# data_abs = pd.read_csv(
#     "spectra/absorption.txt",
#     sep=r"\s+",
#     header=None,
#     names=["wavelength", "absorption"]
# )

# data_ems = pd.read_csv(
#     "spectra/emission.txt",
#     sep=r"\s+",
#     header=None,
#     names=["wavelength", "emission"]
# )

def spectrumReader(loc):
    values = []
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

plt.plot(absorption[0], absorption[1])
plt.plot(emission[0], emission[1])

plt.show()


# excitation_wls = []

# lt_table = np.zeros_like(emission)
# lt_table[0] = emission[:, 0]
# print(lt_table)

# for i in range(len(absorption[:,0])):
#     excitation_wl = int(absorption[i][0])
    
#     print()
    
#     if absorption[i][1] > 0:
#         excitation_wls.append(excitation_wl)
#         truncated_emission = emission[:,1].copy()
#         mask = emission[:, 0] <= excitation_wl
#         truncated_emission[mask] = 0.0

# # Create a new DataFrame with emission wavelengths as rows
# columns = {'wavelength': data_ems['wavelength']}

# print(data_abs)

# with open("absorption.txt") as absorption_file:
    

# # Track excitation wavelengths for columns
# excitation_wls = []

# for i in range(data_abs.shape[0]):
#     excitation_wl = int(data_abs.at[i, 'wavelength'])  # Use integer for column names
    
#     if data_abs.at[i, 'absorption'] > 0:
#         excitation_wls.append(str(excitation_wl))  # Store excitation wavelength as a string
    
#         # Copy emission spectrum
#         adjusted_emission = data_ems['emission'].copy()
        
#         # Find indices where emission wavelength <= excitation wavelength
#         mask = data_ems['wavelength'] <= excitation_wl
        
#         # Set emission values before and including excitation wavelength to zero
#         adjusted_emission[mask] = 0.0
        
#         # Add column for this excitation wavelength
#         emission_df[str(excitation_wl)] = adjusted_emission

# # Formatting the output file with the required structure
# with open("emission_adjusted.txt", "w") as f:
#     f.write("dfat version 1.0\n")
#     f.write("dataname: Emission Spectra\n")
#     f.write("DATAPAIRS: wv inten\n")
#     f.write(f"DATASETS: {len(excitation_wls)}\n")
    
#     # Write header with excitation wavelengths
#     f.write("\t" + "\t".join(excitation_wls) + "\n")

#     # Write emission data
#     for i in range(emission_df.shape[0]):
#         row_values = [f"{emission_df.at[i, 'wavelength']:.0f}"]  # First column: emission wavelength
#         row_values += [f"{emission_df.at[i, wl]:.10f}" for wl in excitation_wls]  # Columns for each excitation wavelength
#         f.write("\t".join(row_values) + "\n")