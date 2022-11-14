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


#multiprocessing dictionaries
manager = mp.Manager()
true_energy_dict = manager.dict()
sig_dict = manager.dict()
mean_dict = manager.dict()
sig_error_dict = manager.dict()
true_t_dict = manager.dict()
mean_error_dict = manager.dict()



def run(energy, time, waves, rise, flat, n):
    delArr = np.zeros(len(waves))
    for i,wave in enumerate(waves):
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
        delArr[i] = abs(rise_cal - true_time)

    sig, error = proc.cal_sig(delArr)


    true_energy_dict[n] = energy
    sig_dict[n] = sig
    true_t_dict[n] = true_time
    mean_dict[n] = np.mean(delArr)
    sig_error_dict[n] = error
    mean_error_dict[n] = sig/np.sqrt(len(delArr))






#Getting the waveforms that have been filtered
path = "/home/jlb1694/data/raw/opt/Run1.lh5"
waves = proc.getWaves(path)
print(len(waves))

#Setting constants
tStart = 30 #starting rise time in clks
tEnd = 120 #ends rise time in clks
tStep = 31
times = np.linspace(tStart,tEnd, int(tStep))

energy = 60

rise = 6
flat = 0.8

n=0
for n in np.arange(0,len(times),5):
    print(n/len(times))
    if n >= len(times)-6:
        break
    p1 = mp.Process(target=run, args=(int(energy), int(times[n]), waves, rise, flat, n))
    p1.start()
    n+=1
    p2 = mp.Process(target=run, args=(int(energy), int(times[n]), waves, rise, flat, n))
    p2.start()
    n+=1
    p3 = mp.Process(target=run, args=(int(energy), int(times[n]), waves, rise, flat, n))
    p3.start()
    n+=1
    p4 = mp.Process(target=run, args=(int(energy), int(times[n]), waves, rise, flat, n))
    p4.start()
    n+=1
    p1.join()
    p2.join()
    p3.join()
    p4.join()

df = pd.DataFrame({"True_Energy":pd.Series(true_energy_dict), "mean":pd.Series(mean_dict),
"mean_error":pd.Series(mean_error_dict),
"True_T":pd.Series(true_t_dict), "sig":pd.Series(sig_dict), "sig_error":pd.Series(sig_error_dict)})

df.to_csv(r'timeVsSig.csv', index=False, header=True)