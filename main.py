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


#multiprocessing dictionaries
manager = mp.Manager()
true_energy_dict = manager.dict()
delta_t_dict = manager.dict()
true_t_dict = manager.dict()
trap_energy_dict = manager.dict()
wavefrom_energy_dict = manager.dict()



def run(energy, time, wave, rise, flat, n):
    wf_sub = proc.sub_wave(wave)
    pulse, true_time = proc.get_pulse(energy, time, int(len(wave)))
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
    deltat = abs(rise_cal - true_time)


    true_energy_dict[n] = energy
    delta_t_dict[n] = deltat
    true_t_dict[n] = true_time
    trap_energy_dict[n] = trap_energy
    wavefrom_energy_dict[n] = np.max(wp)






#Getting the waveforms that have been filtered
path = "/home/jlb1694/data/raw/opt/Run1.lh5"
waves = proc.getWaves(path)
print(len(waves))

#Setting constants
tStart = 30 #starting rise time in clks
tEnd = 120 #ends rise time in clks
tStep = 31
times = np.linspace(tStart,tEnd, int(tStep))

Estart = 5
Eend = 100
Estep = 21
Energy_Lis = np.linspace(Estart, Eend, int(Estep))

rise = 6
flat = 0.8

n=0
for i,energy in enumerate(Energy_Lis):
    for j, time in enumerate(times):
        for l in range(0,20):
            print((n)/(len(Energy_Lis)*len(times)*4))
            m = rand.randint(0,len(waves)-1)
            p1 = mp.Process(target=run, args=(int(Energy_Lis[i]), int(times[j]), waves[m][0:15000], rise, flat, n))
            p1.start()
            n+=1
            p2 = mp.Process(target=run, args=(int(Energy_Lis[i]), int(times[j]), waves[m][0:15000], rise, flat, n))
            p2.start()
            n+=1
            p3 = mp.Process(target=run, args=(int(Energy_Lis[i]), int(times[j]), waves[m][0:15000], rise, flat, n))
            p3.start()
            n+=1
            p4 = mp.Process(target=run, args=(int(Energy_Lis[i]), int(times[j]), waves[m][0:15000], rise, flat, n))
            p4.start()
            n+=1
            p1.join()
            p2.join()
            p3.join()
            p4.join()


df = pd.DataFrame({"True_Energy":pd.Series(true_energy_dict), "delta_t":pd.Series(delta_t_dict),
"True_T":pd.Series(true_t_dict), "Trap_Energy":pd.Series(trap_energy_dict), "Waveform_Energy":pd.Series(wavefrom_energy_dict)})

df.to_csv(r'time_study.csv', index=False, header=True)