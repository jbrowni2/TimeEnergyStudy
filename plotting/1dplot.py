import numpy as np
import pandas as pd
import csv
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv(r'../timeVsWave.csv')

plt.plot(df["DeltaT per Wave"]*8)
plt.title("DeltaT Vs Wave Number")
plt.xlabel("DeltaT [ns]")
plt.ylabel("Wave Number")
plt.show()