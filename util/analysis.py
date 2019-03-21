# profit analysis
import pandas as pd
import util.loader as loader
from datetime import datetime
import copy
import csv

def gen_tx(coin, coin_file, usd_match):
    coin_data = loader.raw_tx_csv_loader(coin,  coin_file)
    coinTx = pd.merge(coin_data[['Product', 'Amount', 'Tx', 'Datetime']], usd_match[['Usd', 'Tx']], on='Tx')
    coinTx['Price'] = -coinTx['Usd']/coinTx['Amount']
    return coinTx

def get_buy(df):
    return df[df['Amount'] > 0]

def get_sell(df):
    return df[df['Amount'] < 0]

def gen_report(product, tx_file):
    txData = pd.read_csv(tx_file)
    txBuy = get_buy(txData)
    txSell = get_sell(txData)
    ## set adjust price (with washsale) as the orig price
    txBuy['adj_price'] = txBuy['Price']
    buy_list =  list(txBuy.itertuples(index=False))
    sell_list =  list(txSell.itertuples(index=False))
    result = tx_matcher(buy_list, sell_list)
    return result, buy_list

def create_empty_match_frame_record():
    return pd.DataFrame(columns=['product', 'sell_time', 'amount', 'buy_price', 'sell_price', 'profit', 'disallowed', 'sell_tx', 'buy_tx', 'buy_time', 'wash_to_buy_tx', 'wash_to_buy_time'])

## create a raw match result, disallowed_wash is set to 0.0
def create_match(buy, sell):
    tuple_amount = -sell.Amount
    if tuple_amount > buy.Amount:
        tuple_amount = buy.Amount
    result = {
    'product':sell.Product,
    'sell_time':sell.Datetime,
    'sell_tx':sell.Tx,
    'amount':tuple_amount,
    'buy_price':buy.Price,
    'buy_adj_price':buy.adj_price,
    'sell_price':sell.Price,
    'profit':(sell.Price - buy.adj_price)*tuple_amount,
    'disallowed':0.0,
    'buy_tx':buy.Tx,
    'buy_time':buy.Datetime,
    'wash_to_buy_tx':'na',
    'wash_to_buy_time':'1900-01-01 00:00:00'
    }
    return result

def save_list_csv(list, file, with_idx):
    df = pd.DataFrame(list)
    df.to_csv(file,index=with_idx)

def printTwoLine():
    print('===================================================================')

def printOneLine():
    print('--------------------------------------------------------------------')

def tx_matcher(buy_list, sell_list):
    df = create_empty_match_frame_record()
    print("buy len {} ; sell len {}".format(len(buy_list), len(sell_list)))
    for sell in sell_list:
        printTwoLine()
        sell_amount = -sell.Amount;
        print("sell {} Amount {} at {}".format(sell.Product, sell_amount, sell.Price))
        while sell_amount > 0.0:
            # get curr ealiest buy
            cur_buy = buy_list[0];
            print("cur Buy {} Amount {} at {}".format(cur_buy.Product, cur_buy.Amount, cur_buy.Price))
            match_res = create_match(cur_buy, sell)
            print("match result amount {}".format(match_res['amount']))
            consumed_amount = match_res['amount']
            cur_buy_amount = cur_buy.Amount
            print('consumer amount {}, cur_buy_amount is {}'.format(consumed_amount, cur_buy_amount))
            update_buy = cur_buy._replace(Amount = (cur_buy_amount - consumed_amount))
            print('After replace {} the buy[0].Amout is {}'.format(consumed_amount, update_buy.Amount))
            sell_amount -=  consumed_amount
            sell = sell._replace(Amount = -sell_amount)
            buy_list.pop(0)
            ## Note, now the current used buy is out of the list
            if match_res['profit'] < 0:
                update_wash(match_res, buy_list)
            if update_buy.Amount > 0.00000001:
                buy_list.insert(0, update_buy);
            else:
                print('We fully consume this buy order, now buy_list size is {}.'.format(len(buy_list)))
            print('now buy_list size is {}'.format(len(buy_list)))
            df = df.append(match_res,ignore_index=True);
    return df

## try to find a wash_sale candidate if any, and update the result
def update_wash(match, buy_list):
    for index in range(len(buy_list)):
        sell_time = extract_time(match['sell_time'])
        wash_buy_time = extract_time(buy_list[index].Datetime)
        if (is_in_wash_range(sell_time, wash_buy_time)):
            print('find wash for sell at {}, buy at {}'.format(sell_time, wash_buy_time))
            print(index, buy_list[index])
            # update the wash sale data
            match['disallowed'] = -match['profit']
            match['wash_to_buy_tx'] = buy_list[index].Tx
            match['wash_to_buy_time'] = buy_list[index].Datetime
            wash_buy = copy.deepcopy(buy_list[index])
            adj_amt = match['disallowed']/wash_buy.Amount + wash_buy.adj_price
            wash_buy = wash_buy._replace(adj_price = adj_amt)
            buy_list[index] = wash_buy
            break
    return

def diff_dates(date1, date2):
    return abs(date2-date1).days

def extract_time(datestr):
    return datetime.strptime(datestr, "%Y-%m-%d %H:%M:%S")

def is_in_wash_range(date1, date2):
    if diff_dates(date1,date2) <= 30:
        return True
    else:
        return False

def gen_sum(match_res):
    product =  match_res.iloc[0]['product']
    total_profit = match_res['profit'].sum() + match_res['disallowed'].sum()
    total_match_pair = len(match_res)
    earliest = match_res.iloc[0]['buy_time']
    lastest = match_res.iloc[-1]['sell_time']
    res = pd.DataFrame(columns=['product', 'from', 'to', 'profit', 'match_pairs'])
    res = res.append({
    'product' : product,
    'from' : earliest,
    'to' : lastest,
    'profit' : total_profit,
    'match_pairs' : total_match_pair
    },ignore_index=True)
    return res;
