#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: florence
"""
# Installable package for use in clinical settings as a clinical recommendation
# for doseage of radioactive tracers injected for PET scans and time between
# injection and scan to minimize exposure to radiation by optimizing dosage
# and time
# Assumptions made to simplify the module

#PET_Dosage
#├── LICENSE
#├── pyproject.toml
#├── README.md
#├── src/
#│   └── PET_Dosage_florence
#│       ├── __init__.py
#│       └── PET_Dosage.py
#└── tests/

#%% Installs

import numpy as np
import pandas as pd

#%% Main Function

def main():
    
    # user input
    # prompted user inputs 
    # (currently only for full body PET/CT scans or PET brain scans)
    # dosage not based on everything being intravenous (only volume of region of focus)
    
    use_case = float(input('1 for manual input, 0 for uplaoding excel file: '))
    
    if use_case == 1:
        mass = float(input('patient mass in kg: '))
        height = float(input('patient height in m: '))
        location = int(input('enter 0 if full body or 1 if brain: '))
        sex = int(input('enter patient biological sex [0 for male, 1 for female]: ')) # brains different sizes
    else:
        filename = input("Please enter a file name in the form of 'filename.xlsx': \n")
        file = pd.read_excel(filename)
        print(file)
        file_np = file.to_numpy()
        inputs = file_np[:, 1]
        mass = inputs[0]
        height = inputs[1]
        location = inputs[2]
        sex = inputs[3]
    
    # Finding volume based on user inputs
    volume = finding_volume(mass, location, sex)
    
    # Finding radioactivity
    necessary_radioactivity_mCi = 1 # mCi
    disintegrations = 3.7e7
    Bq = necessary_radioactivity_mCi * 3.7e7
    radioactivity_manual = Bq * (1/(1e-6))
    conversion_cm_to_m = 1e-6
    
    radioactivity = finding_radioactivity_from_curies(necessary_radioactivity_mCi, disintegrations, conversion_cm_to_m)
    
    # Finding moles
    AN = 6.022e23
    
    moles = finding_moles(volume, radioactivity, AN)

    print('moles of F18-FDG: ', moles)
    
    # Finding time
    desired_percentage = 0.7545
    t_half = 109.7 # minutes
    
    t = Time_of_scan(t_half, desired_percentage)
    
    print("time between injection and scan based on radiotracer: ", t)
       

#%% Finding Volume

def finding_volume(mass, location, sex):

    density = 985 # kg/m^3

    patient_body_volume = mass / density # rough approximation for now

    if location == 1:
        volume = patient_body_volume
    else:
        if sex == 0:
            volume = 0.001273 # m^3
        else:
            volume = 0.001131 # m^3 values from allen institute
            
    return volume
            
#%% Radioactivity

# 30 seconds for blood to fully circulate body (Cleaveland clinic)
# optimal time between injection and scan 30-40 min

# Patients were injected with an activity of 18F-FDG ranging from 2.23 to 15.21 MBq/kg
# (Everaert et al., 2003)

# using desired molarity and volume of desired region, find desired dose

# Necessary radioactivity per unit volume ~ 1 mCi/mL (Chao et al., 2017)
# 1 mCi is 3.70x10^7 disintegrations per second
# Becquerel is IUPAC unit of measure for radioactivity
# number of atoms inside a source that decay per second
# 1 Bq = the quantity of material in which one nucleus decays per second
# 1 mCi = 37 MBq
# 37 MBq/mL therefore 37 MBq/cm^3
# 37 (MBq/cm^3) * (1/1e-6)(cm^3/m^3) = 3.7e13 Bq/m^3

def finding_radioactivity_from_curies(necessary_radioactivity_mCi, disintegrations, conversion):

    radioactivity = (necessary_radioactivity_mCi * disintegrations)/conversion
    
    return radioactivity

#%% Mole calculations

def finding_moles(volume, radioactivity, AN):

    number_of_atoms = volume * radioactivity
    moles = number_of_atoms / AN
    
    return moles

#%% Time

# Halflife equaiton N(t) = N_0(1/2)^(t/(t_(1/2)))
# optimal scan at 30 min after (0.826) or 60 min after (0.683)
# middle is 0.7545

# finding optimal time (based on radiotracer used)

# desired_percentage * moles = moles * (1/2)^(t/(t_half))
# solving for t

def Time_of_scan(t_half, desired_percentage):
    t = (t_half * np.log10(desired_percentage)) / (-np.log10(2))
    
    return t
