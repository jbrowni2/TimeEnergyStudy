import numpy as np
import pandas as pd
import csv
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv(r'../timeVsSig.csv')

plt.scatter(df["True_T"]*8, df["sig"]*8)
#plt.xlim(0,5)
plt.xlabel("True T[ns]")
plt.ylabel("sig of deltaT [ns]")
plt.show()