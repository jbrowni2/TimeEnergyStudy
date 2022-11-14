import numpy as np
import pandas as pd
import csv
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv(r'../time_study.csv')


plt.scatter(df["True_Energy"]*0.0408625 -0.16892, df["True_T"]*8, c=df["delta_t"], cmap='Greens')
plt.xlim(0,5)
cbar = plt.colorbar()
cbar.set_label("delta T [ns]")
plt.xlabel("Energy [keV]")
plt.ylabel("True Rise Time [ns]")
plt.show()
plt.show()