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
wave = waves[1096][0:15000]

energy = 60
time = 60
rise = 6
flat = 0.8


wf_sub = proc.sub_wave(wave[0:15000])
pulse, true_time = proc.get_pulse(energy, time, int(len(wave[0:15000])))
wp = pulse + wf_sub
    
w_trap, trap_energy, trap_time = proc.apply_trap(wp, rise, flat)

m90 = trap_energy*0.9
m10 = trap_energy*0.1
m50 = trap_energy*0.5
imax51 = proc.find_idx(wp, m50, trap_time)
imax9 = proc.find_idxr(wp, m90, imax51)
imax1 = proc.find_idx(wp, m10, imax51)
    
    
rise_cal = imax9 - imax1
delT = abs(rise_cal - true_time)

print(delT)
print(true_time)
print(rise_cal)
print(trap_energy)
print(imax51)
print(trap_time)

plt.plot(wp)
plt.plot(w_trap)
plt.axvline(imax51, color = 'g')
plt.axvline(imax9, color = 'r')
plt.axvline(imax1, color = 'b')
plt.show()