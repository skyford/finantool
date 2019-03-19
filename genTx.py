import util.loader as loader
import util.analysis as ana
import pprint as pt
import pandas as pd

# please remove the page info by : ^page [0-9][0-9][0-9] of
workdir = './data/coinbase/2018/proc/'

usdData = loader.raw_tx_csv_loader('USD', workdir+'usd.csv')
print usdData

usd_match = usdData[usdData['OP'].str.match('Match')]
usd_match.columns = ['Product', 'OP', 'Usd', 'Tx', 'Datetime']

usd_match.to_csv(workdir+'UsdTx.csv',index=False)

usd_fee = usdData[usdData['OP'].str.match('Fee')]
print usd_fee
usd_fee.to_csv(workdir+'UsdFee.csv',index=False)
usd_deposit = usdData[usdData['OP'].str.match('Deposit')]
print usd_deposit
usd_deposit.to_csv(workdir+'UsdDeposit.csv',index=False)

coin='btc'
res = ana.gen_tx(coin,workdir+coin+'.csv', usd_match)
res.to_csv(workdir+coin+'Tx.csv',index=False)

coin='bch'
res = ana.gen_tx(coin,workdir+coin+'.csv', usd_match)
res.to_csv(workdir+coin+'Tx.csv',index=False)

coin='eth'
res = ana.gen_tx(coin,workdir+coin+'.csv', usd_match)
res.to_csv(workdir+coin+'Tx.csv',index=False)

#ltcData = loader.raw_tx_csv_loader('LTC',  workdir+'ltc_t.csv')
#print bchData
#ltcTx = pd.merge(ltcData[['Product', 'Amount', 'Tx', 'Datetime']], usd_match[['Usd', 'Tx']], on='Tx')
#ltcTx['Price'] = -ltcTx['Usd']/ltcTx['Amount']

coin='ltc'
res = ana.gen_tx(coin,workdir+coin+'.csv', usd_match)
res.to_csv(workdir+coin+'Tx.csv',index=False)
