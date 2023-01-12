Time series
===========


Dates and times
---------------


Generate series of time
^^^^^^^^^^^^^^^^^^^^^^^

A series of time can be generated using 'date\_range' command. In below code, 'periods' is the total number of samples; whereas freq = 'M' represents that series must be generated based on 'Month'. 

* By default, pandas consider 'M' as end of the month. Use 'MS' for start of the month. Similarly, other options are also available for day ('D'), business days ('B')  and hours ('H') etc. 

.. code-block:: python
    
    >>> import pandas as pd 
    >>> import numpy as np 
    >>> rng = pd.date_range('2011-03-01 10:15', periods = 10, freq = 'M') 
    >>> rng 
    DatetimeIndex(['2011-03-31 10:15:00', '2011-04-30 10:15:00',
                   '2011-05-31 10:15:00', '2011-06-30 10:15:00',
                   '2011-07-31 10:15:00', '2011-08-31 10:15:00',
                   '2011-09-30 10:15:00', '2011-10-31 10:15:00',
                   '2011-11-30 10:15:00', '2011-12-31 10:15:00'],
                  dtype='datetime64[ns]', freq='M')

    >>> rng = pd.date_range('2015 Jul 2 10:15', periods = 10, freq = 'M')
    >>> rng 
    DatetimeIndex(['2015-07-31 10:15:00', '2015-08-31 10:15:00',
                   '2015-09-30 10:15:00', '2015-10-31 10:15:00',
                   '2015-11-30 10:15:00', '2015-12-31 10:15:00',
                   '2016-01-31 10:15:00', '2016-02-29 10:15:00',
                   '2016-03-31 10:15:00', '2016-04-30 10:15:00'],
                  dtype='datetime64[ns]', freq='M')

* Similarly, we can generate the time series using 'start' and 'end' parameters as below, 

.. code-block:: python

    >>> rng = pd.date_range(start = '2015 Jul 2 10:15', end = '2015 July 12', freq = '12H')
    >>> rng 
    DatetimeIndex(['2015-07-02 10:15:00', '2015-07-02 22:15:00',
                   '2015-07-03 10:15:00', '2015-07-03 22:15:00',
                   '2015-07-04 10:15:00', '2015-07-04 22:15:00',
                   '2015-07-05 10:15:00', '2015-07-05 22:15:00',
                   '2015-07-06 10:15:00', '2015-07-06 22:15:00',
                   '2015-07-07 10:15:00', '2015-07-07 22:15:00',
                   '2015-07-08 10:15:00', '2015-07-08 22:15:00',
                   '2015-07-09 10:15:00', '2015-07-09 22:15:00',
                   '2015-07-10 10:15:00', '2015-07-10 22:15:00',
                   '2015-07-11 10:15:00', '2015-07-11 22:15:00'],
                  dtype='datetime64[ns]', freq='12H')
    >>> len(rng)
    20

* Time zone can be specified for generating the series, 

 .. code-block:: python

    >>> rng = pd.date_range(start = '2015 Jul 2 10:15', end = '2015 July 12', freq = '12H', tz='Asia/Kolkata')
    >>> rng
    DatetimeIndex(['2015-07-02 10:15:00+05:30', '2015-07-02 22:15:00+05:30',
                   '2015-07-03 10:15:00+05:30', '2015-07-03 22:15:00+05:30',
                   '2015-07-04 10:15:00+05:30', '2015-07-04 22:15:00+05:30',
                   '2015-07-05 10:15:00+05:30', '2015-07-05 22:15:00+05:30',
                   '2015-07-06 10:15:00+05:30', '2015-07-06 22:15:00+05:30',
                   '2015-07-07 10:15:00+05:30', '2015-07-07 22:15:00+05:30',
                   '2015-07-08 10:15:00+05:30', '2015-07-08 22:15:00+05:30',
                   '2015-07-09 10:15:00+05:30', '2015-07-09 22:15:00+05:30',
                   '2015-07-10 10:15:00+05:30', '2015-07-10 22:15:00+05:30',
                   '2015-07-11 10:15:00+05:30', '2015-07-11 22:15:00+05:30'],
                  dtype='datetime64[ns, Asia/Kolkata]', freq='12H')
     >>> 

* Further, we can change the time zone of the data for various comparison, 

.. code-block:: python

    >>> rng.tz_convert('Australia/Sydney')DatetimeIndex(['2015-07-02 14:45:00+10:00', '2015-07-03 02:45:00+10:00',
                   '2015-07-03 14:45:00+10:00', '2015-07-04 02:45:00+10:00',
                   '2015-07-04 14:45:00+10:00', '2015-07-05 02:45:00+10:00',
                   '2015-07-05 14:45:00+10:00', '2015-07-06 02:45:00+10:00',
                   '2015-07-06 14:45:00+10:00', '2015-07-07 02:45:00+10:00',
                   '2015-07-07 14:45:00+10:00', '2015-07-08 02:45:00+10:00',
                   '2015-07-08 14:45:00+10:00', '2015-07-09 02:45:00+10:00',
                   '2015-07-09 14:45:00+10:00', '2015-07-10 02:45:00+10:00',
                   '2015-07-10 14:45:00+10:00', '2015-07-11 02:45:00+10:00',
                   '2015-07-11 14:45:00+10:00', '2015-07-12 02:45:00+10:00'],
                  dtype='datetime64[ns, Australia/Sydney]', freq='12H')


* Note that types of these dates are Timestamp, 

.. code-block:: python

    >>> type(rng[0]) 
    <class 'pandas.tslib.Timestamp'>
    >>>


Convert string to dates
^^^^^^^^^^^^^^^^^^^^^^^

Dates in string formats can be converted into time stamp using 'to_datetime' option as below, 


.. code-block:: python

    >>> dd = ['07/07/2015', '08/12/2015', '12/04/2015'] 
    >>> dd 
    ['07/07/2015', '08/12/2015', '12/04/2015']
    >>> type(dd[0])
    <class 'str'>

    >>> # American style 
    >>> list(pd.to_datetime(dd)) 
    [Timestamp('2015-07-07 00:00:00'), Timestamp('2015-08-12 00:00:00'), Timestamp('2015-12-04 00:00:00')]

    >>> # European format 
    >>> d = list(pd.to_datetime(dd, dayfirst=True))
    >>> d 
    [Timestamp('2015-07-07 00:00:00'), Timestamp('2015-12-08 00:00:00'), Timestamp('2015-04-12 00:00:00')]
    >>> type(d[0]) 
    <class 'pandas.tslib.Timestamp'>
    >>>

Periods
^^^^^^^

Periods represents the time span e.g. days, years, quarter or month etc. Period class in pandas allows us to convert the frequency easily. 

Generating periods and frequency conversion
"""""""""""""""""""""""""""""""""""""""""""

In following code, period is generated using 'Period' command with frequency 'M'. Note that, when we use 'asfreq' operation with 'start' operation the date is '01' where as it is '31' with 'end' option. 


.. code-block:: python

    >>> pr = pd.Period('2012', freq='M') 
    >>> pr.asfreq('D', 'start') 
    Period('2012-01-01', 'D')
    >>> pr.asfreq('D', 'end')
    Period('2012-01-31', 'D')
    >>>

Period arithmetic
"""""""""""""""""

We can perform various arithmetic operation on periods. All the operations will be performed based on 'freq', 

.. code-block:: python

    >>> pr = pd.Period('2012', freq='A')  # Annual 
    >>> pr 
    Period('2012', 'A-DEC')
    >>> pr + 1 
    Period('2013', 'A-DEC')

    >>> # Year to month conversion 
    >>> prMonth = pr.asfreq('M') 
    >>> prMonth 
    Period('2012-12', 'M')
    >>> prMonth - 1 
    Period('2012-11', 'M')
    >>>

Creating period range
"""""""""""""""""""""

A range of periods can be created using 'period_range' command, 

.. code-block:: python

    >>> prg = pd.period_range('2010', '2015', freq='A') 
    >>> prg 
    PeriodIndex(['2010', '2011', '2012', '2013', '2014', '2015'], dtype='int64', freq='A-DEC')

    >>> # create a series with index as 'prg'
    >>> data = pd.Series(np.random.rand(len(prg)), index=prg) 
    >>> data 
    2010    0.785453
    2011    0.606939
    2012    0.558619
    2013    0.321185
    2014    0.224793
    2015    0.561374
    Freq: A-DEC, dtype: float64
    >>>

Converting string-dates to period
"""""""""""""""""""""""""""""""""

Conversion of string-dates to period is the two step process, i.e. first we need to convert the string to date format and then convert the dates in periods as shown below, 

.. code-block:: python

    >>> # dates as string
    >>> dates = ['2013-02-02', '2012-02-02', '2013-02-02'] 
    
    >>> # convert string to date format
    >>> d = pd.to_datetime(dates)  
    >>> d 
    DatetimeIndex(['2013-02-02', '2012-02-02', '2013-02-02'], dtype='datetime64[ns]', freq=None)

    >>> # create PeriodIndex from DatetimeIndex
    >>> prd = d.to_period(freq='M') 
    >>> prd 
    PeriodIndex(['2013-02', '2012-02', '2013-02'], dtype='int64', freq='M')

    >>> # change frequency type
    >>> prd.asfreq('D') 
    PeriodIndex(['2013-02-28', '2012-02-29', '2013-02-28'], dtype='int64', freq='D')
    >>> prd.asfreq('Y') 
    PeriodIndex(['2013', '2012', '2013'], dtype='int64', freq='A-DEC')

Convert periods to timestamps 
"""""""""""""""""""""""""""""

Periods can be converted back to timestamps using 'to_timestamp' command, 

.. code-block:: python

    >>> prd 
    PeriodIndex(['2013-02', '2012-02', '2013-02'], dtype='int64', freq='M')
    >>> prd.to_timestamp() 
    DatetimeIndex(['2013-02-01', '2012-02-01', '2013-02-01'], dtype='datetime64[ns]', freq=None)
    >>> prd.to_timestamp(how='end')
    DatetimeIndex(['2013-02-28', '2012-02-29', '2013-02-28'], dtype='datetime64[ns]', freq=None)
    >>>


Time offsets
^^^^^^^^^^^^

Time offset can be defined as follows. Further we can perform various operations on time as as well e.g. adding and subtracting etc. 

.. code-block:: python

    >>> # generate time offset
    >>> pd.Timedelta('3 days') 
    Timedelta('3 days 00:00:00')
    >>> pd.Timedelta('3M')
    Timedelta('0 days 00:03:00')
    >>> pd.Timedelta('4 days 3M')
    Timedelta('4 days 00:03:00')
    >>>

    >>> # adding Timedelta to time
    >>> pd.Timestamp('9 July 2016 12:00') + pd.Timedelta('1 day 3 min') 
    Timestamp('2016-07-10 12:03:00')
    >>>

    >>> # add Timedelta to complete rng
    >>> rng + pd.Timedelta('1 day') 
    DatetimeIndex(['2015-07-03 10:15:00+05:30', '2015-07-03 22:15:00+05:30',
                   '2015-07-04 10:15:00+05:30', '2015-07-04 22:15:00+05:30',
                   '2015-07-05 10:15:00+05:30', '2015-07-05 22:15:00+05:30',
                   '2015-07-06 10:15:00+05:30', '2015-07-06 22:15:00+05:30',
                   '2015-07-07 10:15:00+05:30', '2015-07-07 22:15:00+05:30',
                   '2015-07-08 10:15:00+05:30', '2015-07-08 22:15:00+05:30',
                   '2015-07-09 10:15:00+05:30', '2015-07-09 22:15:00+05:30',
                   '2015-07-10 10:15:00+05:30', '2015-07-10 22:15:00+05:30',
                   '2015-07-11 10:15:00+05:30', '2015-07-11 22:15:00+05:30',
                   '2015-07-12 10:15:00+05:30', '2015-07-12 22:15:00+05:30'],
                  dtype='datetime64[ns, Asia/Kolkata]', freq='12H')
    >>> 


Index data with time
^^^^^^^^^^^^^^^^^^^^

In this section, time is used as index for Series and DataFrame; and then various operations are performed on these data structures. 

* First, create a time series using 'date\_range' option as below. 

.. code-block:: python

    >>> dates = pd.date_range('2015-01-12', '2015-06-14', freq = 'M')  
    >>> dates 
    DatetimeIndex(['2015-01-31', '2015-02-28', '2015-03-31', '2015-04-30',
                   '2015-05-31'],
                  dtype='datetime64[ns]', freq='M')
    >>> len(dates)
    5

* Next, create a Series of temperature of length same as dates, 

.. code-block:: python

    >>> atemp = pd.Series([100.2, 98, 93, 98, 100], index=dates) 
    >>> atemp 
    2015-01-31    100.2
    2015-02-28     98.0
    2015-03-31     93.0
    2015-04-30     98.0
    2015-05-31    100.0
    Freq: M, dtype: float64
    >>>


* Now, time index can be used to access the temperatures as below, 

.. code-block:: python

    >>> idx = atemp.index[3] 
    >>> idx 
    Timestamp('2015-04-30 00:00:00', offset='M')
    >>> atemp[idx] 
    98.0
    >>>

* Next, make another temperature series 'stemp' and create a DataFrame using 'stemp' and 'atemp' as below, 

.. code-block:: python

    >>> stemp = pd.Series([89, 98, 100, 88, 89], index=dates) 
    >>> stemp 
    2015-01-31     89
    2015-02-28     98
    2015-03-31    100
    2015-04-30     88
    2015-05-31     89
    Freq: M, dtype: int64
    >>>

    >>> # create DataFrame
    >>> temps = pd.DataFrame({'Auckland':atemp, 'Delhi':stemp}) 
    >>> temps 
                Auckland  Delhi
    2015-01-31     100.2     89
    2015-02-28      98.0     98
    2015-03-31      93.0    100
    2015-04-30      98.0     88
    2015-05-31     100.0     89
    >>>

    >>> # check the temperature of Auckland
    >>> temps['Auckland']  # or temps.Auckland
    2015-01-31    100.2
    2015-02-28     98.0
    2015-03-31     93.0
    2015-04-30     98.0
    2015-05-31    100.0
    Freq: M, Name: Auckland, dtype: float64
    >>>

* We can add one more column to DataFrame 'temp' which shows the temperature differences between these two cities, 

.. code-block:: python

    >>> temps['Diff'] = temps['Auckland'] - temps['Delhi']
    >>> temps 
                Auckland  Delhi  Diff
    2015-01-31     100.2     89  11.2
    2015-02-28      98.0     98   0.0
    2015-03-31      93.0    100  -7.0
    2015-04-30      98.0     88  10.0
    2015-05-31     100.0     89  11.0
    >>>

    >>> # delete the temp['Diff']
    >>> del temps['Diff']
    >>> temps 
                Auckland  Delhi
    2015-01-31     100.2     89
    2015-02-28      98.0     98
    2015-03-31      93.0    100
    2015-04-30      98.0     88
    2015-05-31     100.0     89
    >>>

Application
-----------

In previous section, we saw some basics of time series. In this section, we will learn some usage of time series with an example, 

Basics
^^^^^^

* First, load the stocks.csv file as below, 

.. code-block:: python

    >>> import pandas as pd
    >>> df = pd.read_csv('stocks.csv') 
    >>> df.head() 
                      date    AA    GE    IBM  MSFT
    0  1990-02-01 00:00:00  4.98  2.87  16.79  0.51
    1  1990-02-02 00:00:00  5.04  2.87  16.89  0.51
    2  1990-02-05 00:00:00  5.07  2.87  17.32  0.51
    3  1990-02-06 00:00:00  5.01  2.88  17.56  0.51
    4  1990-02-07 00:00:00  5.04  2.91  17.93  0.51
    >>>

* If we check the format of 'date' column, we will find that it is string (not the date), 

.. code-block:: python

    >>> d = df.date[0]
    >>> d 
    '1990-02-01 00:00:00'
    >>> type(d) 
    <class 'str'>
    >>>

* To import 'date' as time stamp, 'parse_dates' option can be used as below, 

.. code-block:: python
    
    >>> df = pd.DataFrame.from_csv('stocks.csv', parse_dates=['date'])
    >>> d = df.date[0] 
    >>> d 
    Timestamp('1990-02-01 00:00:00')
    >>> type(d) 
    <class 'pandas.tslib.Timestamp'>
    >>>

    >>> df.head() 
            date    AA    GE    IBM  MSFT
    0 1990-02-01  4.98  2.87  16.79  0.51
    1 1990-02-02  5.04  2.87  16.89  0.51
    2 1990-02-05  5.07  2.87  17.32  0.51
    3 1990-02-06  5.01  2.88  17.56  0.51
    4 1990-02-07  5.04  2.91  17.93  0.51

* Since, we want to used the date as index, therefore load it as index, 

.. code-block:: python

    >>> df = pd.DataFrame.from_csv('stocks.csv', parse_dates=['date'], index_col='date') 
    >>> df.head() 
                Unnamed: 0    AA    GE    IBM  MSFT
    date                                           
    1990-02-01           0  4.98  2.87  16.79  0.51
    1990-02-02           1  5.04  2.87  16.89  0.51
    1990-02-05           2  5.07  2.87  17.32  0.51
    1990-02-06           3  5.01  2.88  17.56  0.51
    1990-02-07           4  5.04  2.91  17.93  0.51
  
* Since, 'Unnamed: 0' is not a useful column, therefore we can remove it as below, 

.. code-block:: python

    >>> del df['Unnamed: 0']
    >>> df.head() 
                  AA    GE    IBM  MSFT
    date                               
    1990-02-01  4.98  2.87  16.79  0.51
    1990-02-02  5.04  2.87  16.89  0.51
    1990-02-05  5.07  2.87  17.32  0.51
    1990-02-06  5.01  2.88  17.56  0.51
    1990-02-07  5.04  2.91  17.93  0.51
    >>>

* Before going further, let's check the name of the index as it will be used at various places along with plotting the data, where index will be used automatically for plots. **Note that, data is used as columns as well as index by using 'drop' keyword.**

.. code-block:: python

    >>> # check the name of the index
    >>> df.index.name 
    'date'
    >>>

* Let's redo all the above steps in different ways, 

.. code-block:: python

    >>> # load and display first file line of the file
    >>> stocks = pd.DataFrame.from_csv('stocks.csv', parse_dates=['date']) 
    >>> stocks.head() 
            date    AA    GE    IBM  MSFT
    0 1990-02-01  4.98  2.87  16.79  0.51
    1 1990-02-02  5.04  2.87  16.89  0.51
    2 1990-02-05  5.07  2.87  17.32  0.51
    3 1990-02-06  5.01  2.88  17.56  0.51
    4 1990-02-07  5.04  2.91  17.93  0.51
    
    >>> stocks.index.name  # nothing is set as index 
    >>> # set date as index but do not remove it from column
    >>> stocks = stocks.set_index('date', drop=False)
    >>> stocks.index.name 
    'date'
    >>> stocks.head() 
                     date    AA    GE    IBM  MSFT
    date                                          
    1990-02-01 1990-02-01  4.98  2.87  16.79  0.51
    1990-02-02 1990-02-02  5.04  2.87  16.89  0.51
    1990-02-05 1990-02-05  5.07  2.87  17.32  0.51
    1990-02-06 1990-02-06  5.01  2.88  17.56  0.51
    1990-02-07 1990-02-07  5.04  2.91  17.93  0.51
    >>>

    >>> # check the type of date  
    >>> type(stocks.date[0])
    <class 'pandas.tslib.Timestamp'>
    >>>

* Data can be accessed by providing the date in any valid format, as shown below, 

.. code-block:: python

    >>> # all four commands have same results
    >>> # stocks.ix['1990, 02, 01']
    >>> # stocks.ix['1990-02-01']
    >>> # stocks.ix['1990/02/01']
    >>> stocks.ix['1990-Feb-01']
    date    1990-02-01 00:00:00
    AA                     4.98
    GE                     2.87
    IBM                   16.79
    MSFT                   0.51
    Name: 1990-02-01 00:00:00, dtype: object
    >>>

* We can display the results in between some range with slice operation e.g. from 01/Feb/90 to 06/Feb/90. Note that, last date of the slice is included in the results, 

.. code-block:: python
    
    >>> stocks.ix['1990-Feb-01':'1990-Feb-06']
                     date    AA    GE    IBM  MSFT
    date                                          
    1990-02-01 1990-02-01  4.98  2.87  16.79  0.51
    1990-02-02 1990-02-02  5.04  2.87  16.89  0.51
    1990-02-05 1990-02-05  5.07  2.87  17.32  0.51
    1990-02-06 1990-02-06  5.01  2.88  17.56  0.51
    >>>

    >>> # select all from Feb-1990 and display first 5
    >>> stocks.ix['1990-Feb'].head() 
                    date    AA    GE    IBM  MSFT
    date                                          
    1990-02-01 1990-02-01  4.98  2.87  16.79  0.51
    1990-02-02 1990-02-02  5.04  2.87  16.89  0.51
    1990-02-05 1990-02-05  5.07  2.87  17.32  0.51
    1990-02-06 1990-02-06  5.01  2.88  17.56  0.51
    1990-02-07 1990-02-07  5.04  2.91  17.93  0.51
    >>>
    
    >>> # use python-timedelta or pandas-offset for defining range
    >>> from datetime import datetime, timedelta 
    >>> start = datetime(1990, 2, 1) 
    >>> # stocks.ix[start:start+timedelta(days=5)]  # python-timedelta
    >>> stocks.ix[start:start+pd.offsets.Day(5)]  # pandas-offset
                     date    AA    GE    IBM  MSFT
    date                                          
    1990-02-01 1990-02-01  4.98  2.87  16.79  0.51
    1990-02-02 1990-02-02  5.04  2.87  16.89  0.51
    1990-02-05 1990-02-05  5.07  2.87  17.32  0.51
    1990-02-06 1990-02-06  5.01  2.88  17.56  0.51
    >>>

.. note:: 

        Above slice operation works only if the dates are in sorted order. If dates are not sorted then we need to sort them first by using sort_index() command i.e. stocks.sort_index()


Resampling
^^^^^^^^^^

Resampling is the conversion of time series from one frequency to another. If we convert higher frequency data to lower frequency, then it is known as down-sampling; whereas if data is converted to low frequency to higher frequency, then  it is called up-sampling. 

* Suppose, we want to see the data at the end of each month only (not on daily basis), then we can use following resampling code, 

.. code-block:: python

    >>> stocks.ix[pd.date_range(stocks.index[0], stocks.index[-1], freq='M')].head()
                     date    AA    GE    IBM  MSFT
    1990-02-28 1990-02-28  5.22  2.89  18.06  0.54
    1990-03-31        NaT   NaN   NaN    NaN   NaN   # it is not business day i.e. sat/sun
    1990-04-30 1990-04-30  5.07  2.99  18.95  0.63
    1990-05-31 1990-05-31  5.39  3.24  21.10  0.80
    1990-06-30        NaT   NaN   NaN    NaN   NaN

    >>> # 'BM' can be used for 'business month' 
    >>> stocks.ix[pd.date_range(stocks.index[0], stocks.index[-1], freq='BM')].head()
                     date    AA    GE    IBM  MSFT
    1990-02-28 1990-02-28  5.22  2.89  18.06  0.54
    1990-03-30 1990-03-30  5.26  3.01  18.45  0.60
    1990-04-30 1990-04-30  5.07  2.99  18.95  0.63
    1990-05-31 1990-05-31  5.39  3.24  21.10  0.80
    1990-06-29 1990-06-29  5.21  3.26  20.66  0.83
    >>>

    >>> # confirm the entry on 1990-03-30
    >>> stocks.ix['1990-Mar-30']
    date    1990-03-30 00:00:00
    AA                     5.26
    GE                     3.01
    IBM                   18.45
    MSFT                    0.6
    Name: 1990-03-30 00:00:00, dtype: object


* Pandas provides easier way to write the above code i.e. using 'resampling'. Further, resampling provides various features e.g. resample the data and show the mean value of the resampled data or maximum value of the data etc.,  as shown below, 

.. rubric:: Downsampling

Following is the example of downsampling. 

.. code-block:: python

    >>> # resample and find mean of each bin 
    >>> stocks.resample('BM').mean().head()
                     AA        GE        IBM      MSFT
    date                                               
    1990-02-28  5.043684  2.873158  17.781579  0.523158
    1990-03-30  5.362273  2.963636  18.466818  0.595000
    1990-04-30  5.141000  3.037500  18.767500  0.638500
    1990-05-31  5.278182  3.160000  20.121818  0.731364
    1990-06-29  5.399048  3.275714  20.933810  0.821429

    >>> # size() : total number of rows in each bin 
    >>> stocks.resample('BM').size().head(3)
    date
    1990-02-28    19  # total 19 business days in Feb-90
    1990-03-30    22
    1990-04-30    20
    Freq: BM, dtype: int64

    >>> # count total number of rows in each bin for each column
    >>> stocks.resample('BM').count().head(3)
                date  AA  GE  IBM  MSFT
    date                               
    1990-02-28    19  19  19   19    19
    1990-03-30    22  22  22   22    22
    1990-04-30    20  20  20   20    20
    >>>
       
    >>> # display last resample value from each bin
    >>> ds = stocks.resample('BM').asfreq().head() 
    >>> ds
                     date    AA    GE    IBM  MSFT
    date                                          
    1990-02-28 1990-02-28  5.22  2.89  18.06  0.54
    1990-03-30 1990-03-30  5.26  3.01  18.45  0.60
    1990-04-30 1990-04-30  5.07  2.99  18.95  0.63
    1990-05-31 1990-05-31  5.39  3.24  21.10  0.80
    1990-06-29 1990-06-29  5.21  3.26  20.66  0.83
    >>>

.. rubric:: Upsampling 

* When we upsample the data, the values are filled by NaN; therefore we need to use 'fillna' method to replace the NaN value with some other values,as shown below, 

.. code-block:: python

    >>> # blank places are filled by NaN
    >>> rs = ds.resample('B').asfreq() 
    >>> rs.head() 
                     date    AA    GE    IBM  MSFT
    date                                          
    1990-02-28 1990-02-28  5.22  2.89  18.06  0.54
    1990-03-01        NaT   NaN   NaN    NaN   NaN
    1990-03-02        NaT   NaN   NaN    NaN   NaN
    1990-03-05        NaT   NaN   NaN    NaN   NaN
    1990-03-06        NaT   NaN   NaN    NaN   NaN
    

    >>> # forward fill the NaN
    >>> rs = ds.resample('B').asfreq().fillna(method='ffill') 
    >>> rs.head() 
                     date    AA    GE    IBM  MSFT
    date                                          
    1990-02-28 1990-02-28  5.22  2.89  18.06  0.54
    1990-03-01 1990-02-28  5.22  2.89  18.06  0.54
    1990-03-02 1990-02-28  5.22  2.89  18.06  0.54
    1990-03-05 1990-02-28  5.22  2.89  18.06  0.54
    1990-03-06 1990-02-28  5.22  2.89  18.06  0.54
    >>>

Plotting the data
^^^^^^^^^^^^^^^^^

In this section, we will plot various data from the DataFrame 'stocks' for various time ranges,

* First, plot the data of 'AA' for complete range, 

.. code-block:: python

    >>> import matplotlib.pyplot as plt 
    >>> stocks.AA.plot() 
    <matplotlib.axes._subplots.AxesSubplot object at 0xa9c3060c>
    >>> plt.show() 
   

.. image:: timeseries/plot1.png
        :width: 70%


* We can plot various data in the same window, by selecting the column using 'ix', 

.. code-block:: python

    >>> stocks.ix['1990':'1995', ['AA', 'IBM', 'MSFT', 'GE']].plot()
    <matplotlib.axes._subplots.AxesSubplot object at 0xa9c2d2ac>
    >>> plt.show() 
    >>>

.. image:: timeseries/plot3.png
        :width: 70%


Moving windows functions
^^^^^^^^^^^^^^^^^^^^^^^^

Pandas provide the ways to analyze the data over a sliding window e.g. in below code the data of 'AA' is plotted aalong with the mean value over a window of length 250, 

.. code-block:: python

    >>> stocks.AA.plot() 
    <matplotlib.axes._subplots.AxesSubplot object at 0xa9c5f4ec>
    >>> stocks.AA.rolling(window=200,center=False).mean().plot()
    <matplotlib.axes._subplots.AxesSubplot object at 0xa9c5f4ec>
    >>> plt.show() 
    >>>

.. image:: timeseries/plot4.png
        :width: 70%
