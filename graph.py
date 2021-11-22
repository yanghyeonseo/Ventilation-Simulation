import math
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt


FILE_NAME = 'Particle Count MAXFRAME5000 NUM10000 LENGTH10.0 VENT_SIZE1.0_avg.csv'


def func(t, C, D, x) :
    return (C / (math.pi * D * t) ** 0.5) * np.exp(-x ** 2 / (4 * D * t))


def difference_graphs(df) :
    t = np.arange(1, 5001)

    plt.cla()
    for vent_loc in range(-8, 9, 2) :
        data = list(df[str(vent_loc) + '.0'] - df['0.0'])
        plt.plot(t, data, linewidth = 1)
    plt.legend([-8.0, -6.0, -4.0, -2.0, 0.0, 2.0, 4.0, 6.0, 8.0], loc = (0.83, 0.46))
    plt.savefig('Difference graphs.png')


def inefficiency_graphs(df) :
    t = np.arange(1, 5001)

    plt.cla()
    for vent_loc in range(-8, 9, 2) :
        data = list(df[str(vent_loc) + '.0'] / df['0.0'])
        print(max(data), end = ' ')
        plt.plot(t, data, linewidth = 1)
    # plt.legend([-8.0, -6.0, -4.0, -2.0, 0.0, 2.0, 4.0, 6.0, 8.0], loc = (0.83, 0.46))
    # plt.savefig('Inefficiency graphs.png')


def fitting_graph(df) :
    t = np.arange(1, 5001)

    for vent_loc in range(-8, 9, 2) :
        if vent_loc == 0 :
            continue

        data = list(df[str(vent_loc) + '.0'] - df['0.0'])
        
        popt, pcov = curve_fit(func, t, data)

        residuals = data - func(t, *popt)
        ss_res = np.sum(residuals ** 2)
        ss_tot = np.sum((data - np.mean(data)) ** 2)
        r_squared = 1 - (ss_res / ss_tot)

        plt.cla()
        plt.plot(t, data, color = 'blue', linewidth = 1)
        plt.plot(t, func(t, *popt), color = 'red', linewidth = 1)
        plt.legend(['difference between ' + str(vent_loc) + '.0' + ' and 0.0', 'Fit curve'], loc = 'best')
        plt.savefig('VENT_LOC ' + str(vent_loc) + '.0 ' + '(C=' + str(popt[0]) + ' D=' + str(popt[1]) + ' R^2=' + str(r_squared) + ').png')


##### main #####

df = pd.read_csv(FILE_NAME, index_col = 0)

# difference_graphs(df)
inefficiency_graphs(df)
# fitting_graph(df)
