import util.analysis as ana
import pprint as pt
import pandas as pd
from datetime import datetime
import copy
import csv
import util.date_util as date_util


workdir = './data/coinbase/2018/proc/'
## test the new column
tx_file = workdir+'bchTx.csv'
txData = pd.read_csv(tx_file)
txBuy = ana.get_buy(txData)
txSell = ana.get_sell(txData)
## set adjust price (with washsale) as the orig price
txBuy['adj_price'] = txBuy['Price']
buy_list =  list(txBuy.itertuples(index=False))
sell_list=  list(txSell.itertuples(index=False))
# test filter out by date
last_day = '2018-01-31 23:59:59'
first_day = '2018-01-01 00:00:00'
print(date_util.is_in_range( '2018-01-30 23:59:59', first_day, last_day))
print(date_util.is_in_range( '2018-02-13 23:59:59', first_day, last_day))
print(date_util.is_in_range( '2017-01-30 23:59:59', first_day, last_day))
exit()

sell_list = list(filter(lambda s : date_util.earlier_than(s.Datetime, last_day) , sell_list))
for index in range(len(sell_list)):
    print('cur sell on {}. earlier than last day {}'.format(sell_list[index].Datetime, last_day))


exit()



for index in range(len(sell_list)):
    if date_util.earlier_than(sell_list[index].Datetime, last_day):
        print('cur sell on {}. earlier than last day {}'.format(sell_list[index].Datetime, last_day))


exit()

ana.save_list_csv(buy_list, './tmp/t.csv',  with_idx=False)
exit()
df = pd.DataFrame(buy_list)
df.to_csv('./testrem.csv',index=False)
exit()

#keys = 'Product, Amount, Tx, 'Datetime', 'Usd', 'Price', 'adj_price']
print(keys)
for index in range(len(buy_list)):
    print(index, buy_list[index])
    if index > 10:
        break


keys = ['idx', 'Product', 'Amount', 'Tx', 'Datetime', 'Usd', 'Price', 'adj_price']
with open('test.csv', 'wb') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(buy_list)

exit()

match = {
'product':'bch',
'sell_time':'2018-02-21 01:26:16',
'sell_tx':111,
'amount':2.0,
'buy_price':10.0,
'sell_price':5.0,
'profit':-10.0,
'disallowed':0.0,
'buy_tx':11,
'buy_time':'2017-12-15 01:28:16',
'wash_to_buy_tx':'0',
'wash_to_buy_time':'1900-01-01 00:00:00'
}

wsh_idx = 0
print(match)
for index in range(len(buy_list)):
    sell_time = ana.extract_time(match['sell_time'])
    wash_buy_time = ana.extract_time(buy_list[index].Datetime)
    if (ana.is_in_wash_range(sell_time, wash_buy_time)):
        print('find wash for sell at {}, buy at {}'.format(sell_time, wash_buy_time))
        print(index, buy_list[index])
        # update the wash sale data
        match['disallowed'] = -match['profit']
        match['wash_to_buy_tx'] = buy_list[index].Tx
        match['wash_to_buy_time'] = buy_list[index].Datetime
        wash_buy = copy.deepcopy(buy_list[index])
        ana.printOneLine()
        print('wash buy after copy')
        print(wash_buy)
        adj_amt = match['disallowed']/wash_buy.Amount + wash_buy.adj_price
        print(adj_amt)
        wash_buy = wash_buy._replace(adj_price = adj_amt)
        ana.printOneLine()
        print('wash buy updated to:')
        print(wash_buy)
        print('update buy list to wash_buy')
        buy_list[index] = wash_buy
        print("after adj price ")
        print(index, buy_list[index])
        wsh_idx = index
        break
ana.printOneLine()
print('updated match')
print(match)
ana.printTwoLine()
print(buy_list[wsh_idx])
exit()

## test the datetime convert


print(match)

date1 = datetime.strptime(match['sell_time'], "%Y-%m-%d %H:%M:%S")
date2 = datetime.strptime(match['buy_time'], "%Y-%m-%d %H:%M:%S")
print(ana.diff_dates(date1, date2))
