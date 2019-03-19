import pandas as pd

def raw_tx_csv_loader(type, file):
    print('Loading  {} tx from file:{}'.format(type, file))
    data = pd.read_csv(file, sep = ' ')
    data_re = data[['Product','OP', 'Amount', 'Tx']]
    data_re['Datetime'] =  data[['Date','Time']].apply(lambda x : '{} {}'.format(x[0],x[1]), axis=1)
    data_re['Tx'] = data_re['Tx'].astype(str)
    return data_re
