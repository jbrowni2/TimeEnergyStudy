import numpy as np
import pandas as pd
import csv
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv(r'../timeVsSig.csv')

plt.errorbar(df["True_T"]*8, df["mean"]*8, yerr=df["mean_error"]*8, fmt='b.')
#plt.xlim(0,5)
plt.xlabel("True Rise Time [ns]")
plt.ylabel("Mean of ABS(Calculated Rise Time - True Rise Time) [ns]")
plt.title("Mean of ABS(Calculated Rise Time - True Rise Time) Vs True Rise Time w/ Energy = 2.4 KeV")
plt.show()