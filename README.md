# SpectraLTrunc

A web application for generating **LightTools-compatible emission spectrum lookup tables** from absorption and emission spectra.

🌐 **Launch the application:** [https://spectraltrunc.streamlit.app/](https://spectraltrunc-app.streamlit.app/)

---

## Description

LightTools treats absorption and emission events independently, where the wavelength of the emitted photon is chosen based on the full emission spectrum of the luminescent particle regardless of the wavelength of the absorbed photon. For luminescent species with spectral overlap, this can lead to the emission of a photon with higher energy than was initially absorbed (anti-Stokes). This results in unphysical results when the particle has significant spectral overlap, or experiences considerable irradiation within the overlapping region.

LightTools features a look-up table-style property for the emission spectrum of phosphor particles, which allows the user to specify the emission spectrum at discrete excitation (or absorption) wavelengths. SpectraLTrunc aims to utilize this feature by truncating the emission spectrum for all wavelengths shorter than the excitation wavelength.

SpectraLTrunc requires two input parameters, the absorption and emission spectrum, and provides a look-up table as output. This file includes all necessary metadata to ensure compatibility with LightTools and allow the user to import the truncated spectra directly into their LightTools particle using the 'Load File' feature.

---

## Features

- Paste absorption and emission spectra directly from Excel
- Automatic sorting of wavelength data
- Automatic termination of spectra with zero intensity at both boundaries
- Automatic correction of negative intensity values
- Interactive preview of the input spectra
- Interactive preview of the truncated emission spectrum
- One-click generation and download of a LightTools-compatible lookup table

---

## Running locally

Clone the repository and install the required packages:

```bash
pip install -r requirements.txt
```

Launch the Streamlit application:

```bash
streamlit run main.py
```

---

## Example

An example absorption and emission spectrum of **Lumogen F Red 305** is included. This luminophore exhibits significant spectral overlap and serves as an illustrative example of the truncation procedure.

---

## License

MIT License
