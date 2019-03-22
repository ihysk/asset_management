import pandas as pd
import pandas_datareader as pdr
import datetime
import json


class AssetCalulator:

    def load_stock_data(self, file_name):
        with open(file_name, 'r', encoding='utf-8') as f:
            json_data = json.load(f)

        self.stocks = pd.Series(json_data)

        end = datetime.date.today()
        start = datetime.datetime(2019, 1, 1)

        self.stock_data = pdr.tiingo.TiingoDailyReader(self.stocks.index, start, end).read()

    def get_current_appraised_amount(self):
        total = 0
        for item in self.stocks.index:
            df = self.stock_data.loc[(item,)]
            price = df.ix[[-1], ['close']]
            num = 0
            for stk in self.stocks[item]:
                num += stk['num']
            total += price * num
        return total.iat[0, 0]

    def get_original_amount(self):
        total = 0
        for item in self.stocks.index:
            num = 0
            for stk in self.stocks[item]:
                num += stk['num']
                total += stk['num'] * stk['price']
        return total


if __name__ == '__main__':
    calc = AssetCalulator()
    calc.load_stock_data('stocks.json')
    print(calc.get_original_amount())
    print(calc.get_current_appraised_amount())
