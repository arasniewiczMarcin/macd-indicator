import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def show_chart(x, y, xlabel, ylabel, title, x2 = [], y2 = []):

    plt.plot(x, y)
    if x2 and y2:
        plt.plot(x2, y2)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(rotation=30)
    plt.xticks(np.arange(0, len(dates), step=len(dates) // 6))
    plt.tight_layout()
    plt.show()

def show_stock_chart(x, y, xlabel, ylabel, title):
    show_chart(x, y, xlabel, ylabel, title)

#def count_EMA()

def create_MACD_SIGNAL_plot(stock_values, dates):
    macd = []
    signal = []
    for i in range(0, len(stock_values)):
        #count 26 EMA
        N = 0
        EMA26 = 0
        EMA12 = 0
        for k in range(12, 27, 14):
            N = k
            counter = 0
            denominator = 0
            alpha = 2 / (N + 1)
            power = 0
            for j in range(i, i - N, -1):
                if j < 0:
                    break
                counter += stock_values[j] * (1 - alpha)**power
                denominator += (1 - alpha)**power
                power += 1

            if k == 12:
                EMA12 = counter / denominator
            else:
                EMA26 = counter / denominator
        macd.append(EMA12 - EMA26)



    show_chart(dates, macd, "Date", "MACD values", "MACD-Signal")





if __name__ == "__main__":
    wig20 = pd.read_csv('wig20_w.csv')

    stock_values = wig20["Otwarcie"]
    dates = wig20["Data"]
    show_stock_chart(dates, stock_values, "Date", "Values [zł]", "WIG20- prices over time")

    create_MACD_SIGNAL_plot(stock_values, dates)



