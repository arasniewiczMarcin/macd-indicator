import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def show_chart(x, y, xlabel, ylabel, title, x2=None, y2=None):

    plt.plot(x, y)
    if x2 is not None and y2 is not None:
        plt.plot(x2, y2, "r")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(rotation=30)
    plt.xticks(np.arange(0, len(x), step=len(x) // 6))
    plt.tight_layout()
    plt.show()


def show_stock_chart(x, y, xlabel, ylabel, title):
    show_chart(x, y, xlabel, ylabel, title)


def count_ema(i, N, alpha, stock_values):
    counter = 0
    denominator = 0
    power = 0
    for j in range(i, i - N, -1):
        if j < 0:
            break
        counter += stock_values[j] * (1 - alpha) ** power
        denominator += (1 - alpha) ** power
        power += 1

    return counter, denominator

def create_macd_signal_plot(stock_values, dates):
    macd = []

    for i in range(len(stock_values)):
        #count 26 EMA
        EMA26 = 0
        EMA12 = 0
        for k in range(12, 27, 14):
            N = k
            alpha = 2 / (N + 1)
            counter, denominator = count_ema(i, N, alpha, stock_values)

            if k == 12:
                EMA12 = counter / denominator
            else:
                EMA26 = counter / denominator
        macd.append(EMA12 - EMA26)

    signal = []
    N = 9
    alpha = 2 / (N + 1)
    for i in range(len(macd)):
        counter, denominator = count_ema(i, N, alpha, macd)
        signal.append(counter/denominator)

    show_chart(dates, macd, "Date", "MACD values", "MACD-Signal", dates, signal)


def main():
    wig20 = pd.read_csv('wig20_w.csv')

    stock_values = wig20["Otwarcie"]
    dates = wig20["Data"]
    show_stock_chart(dates, stock_values, "Date", "Values [zł]", "WIG20- prices over time")

    create_macd_signal_plot(stock_values, dates)


if __name__ == "__main__":
    main()



