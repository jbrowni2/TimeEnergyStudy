import numpy as np
import pandas as pd
import csv
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv(r'../time_study.csv')

df["True_Energy"] = df["True_Energy"]*0.0408625 -0.16892
df["True_Energy"] = df["True_Energy"].round(2)
df["True_T"] = df["True_T"]*8
df["sig"] = df["sig"]*8
df["sig"] = df["sig"].round(0)

pivotted = df.pivot("True_Energy", "True_T", "sig")


sns.heatmap(pivotted, cbar_kws={'label': 'Sigma of ABS(Calculated Rise Time - True Rise Time) [ns]'}, annot=True, fmt="g", linewidths=.5, cmap="Blues")
plt.title("Sigma ABS(Calculated Rise Time - True Rise Time) VS True Rise Time and True Energy")
plt.xlabel("True Rise Time [ns]")
plt.ylabel("True Energy [KeV]")
plt.show()