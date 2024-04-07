import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def show_charts(x, stock_values, y, xlabel, ylabel, title, y2, stocks):
    figure, axis = plt.subplots(2, 1)
    axis[0].plot(x, stock_values)
    axis[1].plot(x, y)
    for i in range(2):

        axis[i].set_xlabel(xlabel[i])
        axis[i].set_ylabel(ylabel[i])
        axis[i].set_title(title[i])
        axis[i].tick_params(axis='x', rotation=30)
        axis[i].set_xticks(np.arange(0, len(x), step=len(x) // 6))
        axis[i].set_xticklabels(x[np.arange(0, len(x), step=len(x) // 6)], rotation=30)

    axis[1].plot(x, y2, "r")
    for x, y, buy, index in stocks:
        if buy is True:
            axis[1].scatter(x, y, color='green')
        else:
            axis[1].scatter(x, y, color='red')

    plt.tight_layout()
    plt.show()


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


def simulate_buying_stocks(stocks_values, stocks):
    print(stocks_values[0])
    account_balance = stocks_values[0] * 1000
    start_balance = account_balance
    bid = account_balance / 10
    shares = 0.0
    print(f"Początkowy stan konta wynosi {account_balance}zł, a cena za akcje wynosi {stocks_values[0]}")

    for date, signal, buy, index in stocks:

        if buy is True:
            if account_balance >= bid:
                shares += bid / stocks_values[index]
                account_balance -= bid
                print(f"Kupuję akcje za {bid}zł. Stan konta wynosi: {account_balance}zł. Ilość posiadanych akcji wynosi {shares}.")
            elif account_balance > 0:
                price = account_balance
                shares += price / stocks_values[index]
                account_balance = 0
                print(f"Kupuję akcje za {price}zł. Stan konta wynosi: {account_balance}zł. Ilość posiadanych akcji wynosi {shares}.")
        else:
            sell = shares / 2
            shares /= 2
            account_balance += sell * stocks_values[index]
            print(f"Sprzedaje akcje za {sell * stocks_values[index]}. Stan konta wynosi: {account_balance}zł. Ilość posiadanych akcji wynosi {shares}.")

    sell = shares
    shares = 0
    account_balance += sell * stocks_values.tail(1).values[0]
    print(f"Sprzedaje wszystkie akcje za {sell * stocks_values.tail(1).values[0]}. Stan konta wynosi: {account_balance}zł. Ilość posiadanych akcji wynosi {shares}.")
    print(f"Roznica pieniedzy przed i po inwestowaniu wynosi {account_balance - start_balance}")



def create_macd_signal_plot(stock_values, dates, name):
    macd = []

    for i in range(len(stock_values)):
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
    stocks = []
    for i in range(len(macd)):
        counter, denominator = count_ema(i, N, alpha, macd)
        signal.append(counter/denominator)

        if i > 1:
            if macd[i] > signal[i] and macd[i - 1] < signal[i - 1]:
                stocks.append((dates[i], signal[i], False, i))
            elif macd[i] < signal[i] and macd[i - 1] > signal[i - 1]:
                stocks.append((dates[i], signal[i], True, i))

    simulate_buying_stocks(stock_values, stocks)
    show_charts(dates, stock_values, macd, ["Date", "Date"], ["Values [zł]", "MACD values"],
               [f"{name}- prices over time", "MACD-Signal"], signal, stocks)


def main():
    stocks = ['wig20_d.csv', 'wig20_w.csv', 'cmr_d.csv']
    names = ['wig20 days', 'wig20 weeks', 'comarch days', 'comarch weeks']
    for stock, name in zip(stocks, names):
        s = pd.read_csv(stock)

        stock_values = s["Zamkniecie"]
        dates = s["Data"]

        create_macd_signal_plot(stock_values, dates, name)


if __name__ == "__main__":
    main()



