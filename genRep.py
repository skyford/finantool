import util.analysis as ana
import pprint as pt
import pandas as pd

workdir = './data/coinbase/2018/proc/'

def gen_coin_report(coin, workdir):
    rep, remaining_buy = ana.gen_report(coin, workdir+coin+'Tx.csv')
    rep.to_csv(workdir+coin+'Rep.csv',index=True)
    ana.save_list_csv(remaining_buy, workdir+coin+'RemBuy.csv',  with_idx=True)
    final_sum = ana.gen_sum(rep)
    final_sum.to_csv(workdir+coin+'Sum.csv',index=False)


gen_coin_report('bch', workdir)
gen_coin_report('btc', workdir)
gen_coin_report('eth', workdir)
gen_coin_report('ltc', workdir)
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
