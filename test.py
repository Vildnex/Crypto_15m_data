import os.path
from os import listdir
from os.path import isfile, join

import numpy as np
import pandas_ta
from scipy.stats import linregress

import pandas as pd
import swifter

FILE_PATH = "Data"


def get_files_ohlc(path: str):
    return [f for f in listdir(path) if isfile(join(path, f))]


def get_slope(array):
    y = np.array(array)
    x = np.arange(len(y))
    slope, intercept, r_value, p_value, std_err = linregress(x, y)
    return slope


def add_slop_indicator(ohlc: pd.DataFrame, ind: str, candles_back: int):
    ohlc[f'slope_{val}_{days}'] = ohlc[ind].swifter.rolling(window=candles_back, min_periods=candles_back).apply(
        get_slope, raw=True)


if __name__ == '__main__':
    files = get_files_ohlc(FILE_PATH)
    dicts = {}

    for file in files:
        name_pair = file.split("_")[0]
        dicts[name_pair] = pd.read_json(os.path.join(FILE_PATH, file))
        dicts[name_pair].rename({0: 'date',
                                 1: 'open',
                                 2: 'high',
                                 3: 'low',
                                 4: 'close',
                                 5: 'volume'}, axis=1, inplace=True)
        dicts[name_pair]['date'] = dicts[name_pair]['date'].values.astype(dtype='datetime64[ms]')
        for val in range(20, 100):
            dicts[name_pair].ta.ema(length=val, append=True)

        print(f"END_{name_pair}")
        for val in range(20, 100):
            for days in range(5, 100):
                add_slop_indicator(dicts[name_pair], f"EMA_{val}", days)
        print(f"DONE {name_pair}")
