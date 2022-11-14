"""
This filter was written by Ryan B.
This filter takes in a processed pygama file and reduces it into a desired energy range.
"""

import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import h5py 
import json
import copy
from collections import OrderedDict
from lmfit import Model
import os

from pygama.pargen.dsp_optimize import run_one_dsp
from pygama.pargen.dsp_optimize import run_grid
from pygama.pargen.dsp_optimize import ParGrid
from pygama.lgdo.lh5_store import LH5Store
import pygama.math.histogram as pgh
import pygama.math.peak_fitting as pgf
import pywt
from statistics import median


sys.path.insert(1, '../analysis/')
import processes.foundation as fd
import processes.fitModel as fM
import processes.histogramAction as hA


def main():

    run = 9188
    data = fd.get_t1_data(run, "Card1")

    f_wfs = 'opt/Run1.lh5'


    cwd = os.getcwd()
    file = cwd + '/address.json'
    with open(file, 'r') as read_file:
        address = json.load(read_file)

    sto = LH5Store(address["tier1_dir"])

    waves = np.unique(data[0]["waveform"]["values"].nda, axis=0)

    filter_idx = np.zeros(len(waves), dtype=int)
    j = 0
    for i,wave in enumerate(waves):
        if wave[0] != 0:
            if wave[0] < wave[-1]:
                filter_idx[j] = int(i)
                j+=1
    
    filter_idx = np.unique(filter_idx)

    runstr = "Run"+str(run)+".lh5"

    tb_in = 'Card1'

    tb_wfs, nwfs = sto.read_object('Card1/',[runstr],idx=filter_idx)

    waves = tb_wfs["waveform"]["values"].nda


    for i in range(0,len(tb_wfs["waveform"]["values"].nda)):
        cDs = pywt.swt(tb_wfs["waveform"]["values"].nda[i], "haar", level=4)
        threshold = np.zeros_like([0,0,0,0])

        j = 0
        for cD in cDs:
            median_value = median(cD[1])
            median_average_deviation = median([abs(number-median_value) for number in cD[1]])
            sig1 = median_average_deviation/0.6745
            threshold[j] = sig1*np.sqrt(2*np.log(len(wave)))
            j+=1

        j = 0
        for cD in cDs:
            cD[1][abs(cD[1]) < threshold[j]] = 0.0
            j += 1

        tb_wfs["waveform"]["values"].nda[i] = pywt.iswt(cDs, "Haar")

    print(len(tb_wfs))
    
    sto.write_object(tb_wfs, f'{tb_in}', f_wfs,wo_mode='a')


if __name__ == "__main__":
    main()