import lib.definition as proc
import numpy as np
import pandas as pd
import itertools
from lmfit import Model
import os, psutil
import gc
import multiprocessing as mp
import csv
import random as rand
from scipy.stats import sem
import matplotlib.pyplot as plt


path = "/home/jlb1694/data/raw/opt/Run1.lh5"
waves = proc.getWaves(path)


energy = 60
time = 30
rise = 6
flat = 0.8
delTArr = np.zeros(len(waves))

for i,wave in enumerate(waves):
    if i == 1093:
        continue
    elif i == 1096:
        continue
    elif i == 1102:
        continue
    print(i/len(waves))
    wf_sub = proc.sub_wave(wave[0:15000])
    pulse, true_time = proc.get_pulse(energy, time, int(len(wave[0:15000])))
    wp = pulse + wf_sub
    
    w_trap, trap_energy, trap_time = proc.apply_trap(wp, rise, flat)
    if trap_energy > 62:
        continue

    m90 = trap_energy*0.9
    m10 = trap_energy*0.1
    m50 = trap_energy*0.5
    imax51 = proc.find_idx(wp, m50, trap_time)
    imax9 = proc.find_idxr(wp, m90, imax51)
    imax1 = proc.find_idx(wp, m10, imax51)
    
    
    rise_cal = imax9 - imax1
    delTArr[i] = abs(rise_cal - true_time)

df = pd.DataFrame({"DeltaT per Wave":pd.Series(delTArr)})

df.to_csv(r'timeVsWave.csv', index=False, header=True)