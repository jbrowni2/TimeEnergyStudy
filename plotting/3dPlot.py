import numpy as np
import pandas as pd
import csv
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv(r'../time_study.csv')


ax = plt.axes(projection='3d')
ax.scatter3D(df["True_Energy"]*0.0408625 -0.16892, df["True_T"]*8, df["delta_t"]*8, cmap='Greens')
ax.set_xlabel("Energy [keV]")
ax.set_ylabel("True Rise Time [ns]")
ax.set_zlabel("Delta T [ns]")
plt.show()