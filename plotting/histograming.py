import numpy as np
import pandas as pd
import csv
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv(r'../timeVsWave.csv')

plt.hist(df["DeltaT per Wave"]*8, bins=300)
plt.show()