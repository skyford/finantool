import util.analysis as ana
import pprint as pt
import pandas as pd
import util.date_util as date_util

workdir = './data/coinbase/2018/proc/'
first_day = '2018-01-01 00:00:00'
last_day = '2018-12-31 23:59:59'

def gen_coin_report(coin, workdir, first_day, last_day):
    rep, remaining_buy = ana.gen_report(coin, workdir+coin+'Tx.csv', last_day)
    rep.to_csv(workdir+coin+'Rep.csv',index=True)
    ana.save_list_csv(remaining_buy, workdir+coin+'RemBuy.csv',  with_idx=True)
    # make summary only with in range [first_day, last_day]
    #rep_in_range = rep[date_util.is_in_range(rep['sell_time'], first_day, last_day)]
    first_date = date_util.extract_time(first_day)
    rep_in_range = rep[rep['sell_time'] >= first_date]
    final_sum = ana.gen_sum(rep_in_range)
    final_sum.to_csv(workdir+coin+'Sum.csv',index=False)

gen_coin_report('btc', workdir, first_day, last_day)
gen_coin_report('bch', workdir, first_day, last_day)
gen_coin_report('eth', workdir, first_day, last_day)
gen_coin_report('ltc', workdir, first_day, last_day)
exit()

coin = 'btc'
rep = ana.gen_report(coin, workdir+coin+'Tx.csv')
rep.to_csv(workdir+coin+'Rep.csv',index=True)
final_sum = ana.gen_sum(rep)
final_sum.to_csv(workdir+coin+'Sum.csv',index=False)

coin = 'bch'
rep = ana.gen_report(coin, workdir+coin+'Tx.csv')
rep.to_csv(workdir+coin+'Rep.csv',index=True)
final_sum = ana.gen_sum(rep)
final_sum.to_csv(workdir+coin+'Sum.csv',index=False)

coin = 'eth'
rep = ana.gen_report(coin, workdir+coin+'Tx.csv')
rep.to_csv(workdir+coin+'Rep.csv',index=True)
final_sum = ana.gen_sum(rep)
final_sum.to_csv(workdir+coin+'Sum.csv',index=False)

coin = 'ltc'
rep = ana.gen_report(coin, workdir+coin+'Tx.csv')
rep.to_csv(workdir+coin+'Rep.csv',index=True)
final_sum = ana.gen_sum(rep)
final_sum.to_csv(workdir+coin+'Sum.csv',index=False)
