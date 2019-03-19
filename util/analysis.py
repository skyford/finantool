# profit analysis

import pandas as pd
import util.loader as loader

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
    txSell =get_sell(txData)
    buy_list =  list(txBuy.itertuples(index=False))
    sell_list =  list(txSell.itertuples(index=False))
    result = tx_matcher(buy_list, sell_list)
    return result

def create_empty_match_frame_record():
    return pd.DataFrame(columns=['product', 'sell_time', 'amount', 'buy_price', 'sell_price', 'profit',  'sell_tx', 'buy_tx', 'buy_time'])

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
    'sell_price':sell.Price,
    'profit':(sell.Price - buy.Price)*tuple_amount,
    'sell_tx':sell.Tx,
    'buy_tx':buy.Tx,
    'buy_time':buy.Datetime
    }
    return result

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
            df = df.append(match_res,ignore_index=True);
            update_buy = cur_buy._replace(Amount = (cur_buy_amount - consumed_amount))
            print('After replace {} the buy[0].Amout is {}'.format(consumed_amount, update_buy.Amount))
            sell_amount -=  consumed_amount
            sell = sell._replace(Amount = -sell_amount)
            buy_list.pop(0);
            if update_buy.Amount > 0.00000001:
                buy_list.insert(0, update_buy);
            else:
                print('We fully consume this buy order, now buy_list size is {}.'.format(len(buy_list)))
            print('now buy_list size is {}'.format(len(buy_list)));
    return df

def gen_sum(match_res):
    product =  match_res.iloc[0]['product']
    total_profit = match_res['profit'].sum()
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
