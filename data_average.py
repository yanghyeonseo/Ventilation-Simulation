import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

FILE_NAME = 'Particle Count MAXFRAME5000 NUM10000 LENGTH10.0 VENT_SIZE1.0_'

df = pd.read_csv(FILE_NAME + str(1) + '.csv', index_col = 0)
for i in range(2, 11) :
    df += pd.read_csv(FILE_NAME + str(i) + '.csv', index_col = 0)
df /= 10

df.to_csv(FILE_NAME + 'avg.csv')

df.plot(linewidth = 1.0)
plt.legend(loc = 'best')
plt.savefig(FILE_NAME + 'avg.png')
plt.show()
