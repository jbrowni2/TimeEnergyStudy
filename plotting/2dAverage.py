import numpy as np
import pandas as pd
import csv
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv(r'../time_study.csv')

df2 = df.groupby('True_Energy', as_index=False).mean()

plt.scatter(df2["True_Energy"]*0.0408625 -0.16892, df2["delta_t"]*8)
#plt.xlim(0,5)
plt.xlabel("Energy [keV]")
plt.ylabel("delta_T [ns]")
plt.show()
