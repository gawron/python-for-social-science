# IPython log file

get_ipython().system('cat ex1.csv')
import pandas as pd
df = pd.DataFrame.from_csv('ex1.csv', index_col=None)
df
get_ipython().magic('save meher')
get_ipython().magic('pinfo %save')
get_ipython().magic('save meher.py')
get_ipython().magic('pinfo %logstsave')
get_ipython().magic('logon')
get_ipython().magic('logon meher')
get_ipython().magic('logstart')
a = 2
get_ipython().magic('save meher.py')
:q
