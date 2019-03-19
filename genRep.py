import util.analysis as ana
import pprint as pt
import pandas as pd

workdir = './data/coinbase/2018/proc/'

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
