import util.analysis as ana
import pprint as pt
import pandas as pd

workdir = './data/coinbase/2018/proc/'
last_day = '2018-12-31 23:59:59'

def gen_coin_report(coin, workdir, last_day):
    rep, remaining_buy = ana.gen_report(coin, workdir+coin+'Tx.csv', last_day)
    rep.to_csv(workdir+coin+'Rep.csv',index=True)
    ana.save_list_csv(remaining_buy, workdir+coin+'RemBuy.csv',  with_idx=True)
    final_sum = ana.gen_sum(rep)
    final_sum.to_csv(workdir+coin+'Sum.csv',index=False)


gen_coin_report('bch', workdir, last_day)
gen_coin_report('btc', workdir, last_day)
gen_coin_report('eth', workdir, last_day)
gen_coin_report('ltc', workdir, last_day)
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
