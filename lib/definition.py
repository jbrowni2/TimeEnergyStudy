import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from scipy import stats
from scipy import signal
from math import exp
import processes.foundation as fd
from math import exp, sqrt, pi, erfc
from lmfit import Model
import csv
from scipy.optimize import curve_fit
import pywt
from statistics import median
import copy
from matplotlib import colors
import h5py


def getWaves(path):
    f = h5py.File(path, 'r')
    waves = np.asarray(f["Card1/waveform/values"])
    return waves


def get_pulse(energy, time, length):
    rise = time
    energy = energy



    pulse = np.zeros(length)
    x = np.linspace(-rise-40,rise+40,2*rise+81)
    y = energy/(1 + np.exp(-x/(0.3*rise)))

    pulse[10000: 10000+len(x)] = y
    pulse[10000+len(x)::] = y[-1]

    imax51 = find_idx(pulse, energy*0.5, length-1)
    imax9 = find_idxr(pulse, energy*0.9, imax51)
    imax1 = find_idx(pulse, energy*0.1, imax51)
    rise_cal = imax9 - imax1


    return pulse, rise_cal


def sub_wave(wave):
    mean = np.nan
    stdev = np.nan
    slope = np.nan
    intercept = np.nan


    sum_x = sum_x2 = sum_xy = sum_y = mean = stdev = 0
    isum = len(wave)

    for i in range(0, len(wave), 1):
    # the mean and standard deviation
        temp = wave[i] - mean
        mean += temp / (i + 1)
        stdev += temp * (wave[i] - mean)

        # linear regression
        sum_x += i
        sum_x2 += i * i
        sum_xy += wave[i] * i
        sum_y += wave[i]

    slope = (isum * sum_xy - sum_x * sum_y) / (isum * sum_x2 - sum_x * sum_x)
    intercept = (sum_y - sum_x * slope) / isum

    line = np.array([x * slope + intercept for x in range(0, len(wave))])
    wave_sub = wave - line

    return wave_sub


#rise and flat are in micro seconds
def apply_trap(wp, rise, flat):
    w_trap = np.zeros(len(wp))

    rise = int(rise/.008)
    flat = int(flat/.008)

    w_trap[0] = wp[0]/rise
    for i in range(1, rise, 1):
        w_trap[i] = w_trap[i - 1] + wp[i] / rise
    for i in range(rise, rise + flat, 1):
        w_trap[i] = w_trap[i - 1] + (wp[i] - wp[i - rise])/rise
    for i in range(rise + flat, 2 * rise + flat, 1):
        w_trap[i] = w_trap[i - 1] + (wp[i] - wp[i - rise] - wp[i - rise - flat])/rise
    for i in range(2 * rise + flat, len(wp), 1):
        w_trap[i] = (
        w_trap[i - 1]
        + (wp[i]
        - wp[i - rise]
        - wp[i - rise - flat]
        + wp[i - 2 * rise - flat])/rise
    )

    trap_time = find_idx(w_trap, 0.1*np.max(w_trap), np.argmax(w_trap))

    return w_trap, np.max(w_trap), trap_time




def find_idx(arr, val, idxBegin):
        for i in range(idxBegin, 0, -1):
            count = arr[i]
            if count <= val:
                break

        idx = i
        return idx

def find_idxr(arr, val, idxBegin):
        for i in range(idxBegin, len(arr)-1, 1):
            count = arr[i]
            if count >= val:
                break
        
        idx = i
        return idx


def cal_sig(arr):
    #Here is where I calculate the variance
    sig = np.std(arr)
    err = sig/(np.sqrt(2*len(arr)-2))

    return sig, err
