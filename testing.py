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
wave = waves[52][0:15000]

energy = 60
time = 120
rise = 6
flat = 0.8


wf_sub = proc.sub_wave(wave[0:15000])
pulse, true_time = proc.get_pulse(energy, time, int(len(wave[0:15000])))
wp = pulse + wf_sub
    
w_trap, trap_energy, trap_time = proc.apply_trap(wp, rise, flat)

max = np.mean(wp[trap_time::])
m90 = max*0.9
m10 = max*0.1
m50 = max*0.5
imax51 = proc.find_idx(wp, m50, trap_time)
imax9 = proc.find_idxr(wp, m90, imax51)
imax1 = proc.find_idx(wp, m10, imax51)
    
    
rise_cal = imax9 - imax1
delT = abs(rise_cal - true_time)

print(delT)
print(true_time)
print(rise_cal)

plt.plot(wp)
plt.axvline(imax51)
plt.axvline(imax9)
plt.axvline(imax1)
plt.show()