Reading multiple files
======================

In previous chapters, we used only one or two files to read the data. In this chapter, multiple files are concatenated to analyze the data. 


Example: Baby names trend
-------------------------

In this section, various operations are performed on the various text-files to gather the useful information from it. These text file contains the list to names of babies since 1880. Each record in the individual annual files has the format "name,sex,number," where name is 2 to 15 characters, sex is M (male) or F (female) and "number" is the number of occurrences of the name. Each file is sorted first on sex and then on number of occurrences in descending order. When there is a tie on the number of occurrences, names are listed in alphabetical order. Following is the list of files on which various operations will be performed. 

.. code-block:: shell 

    $ ls
    yob1880.txt  yob1882.txt  yob1884.txt  yob1886.txt
    yob1881.txt  yob1883.txt  yob1885.txt  yob1887.txt


Following are the first ten lines in the yob1880.txt file, 

.. code-block:: shell

    $ head -n 10 yob1980.txt 
    Jennifer,F,58375
    Amanda,F,35817
    Jessica,F,33914
    Melissa,F,31625
    Sarah,F,25737
    Heather,F,19965
    Nicole,F,19910
    Amy,F,19832
    Elizabeth,F,19523
    Michelle,F,19113


Total boys and girls in year 1880
---------------------------------

* First, we will read one file and then check to total number of rows in that file, 

.. code-block:: python

    >>> import pandas as pd 
    >>> names1880 = pd.read_csv('yob1880.txt', names=['name', 'gender', 'birthcount']) 
    >>> # total number of rows in yob1880.txt
    >>> len(names1880) 
    2000
    >>>
    >>> names1880.head() 
            name gender  birthcount
    0       Mary      F        7065
    1       Anna      F        2604
    2       Emma      F        2003
    3  Elizabeth      F        1939
    4     Minnie      F        1746
    >>>
    
* Note that, the file contains 2000 rows; and each row contains a name and total number of babies with that particular name along with the gender information. We can calculate the total number of boys and girls by adding the 'birthcount' based on gender; i.e. we need to group the data based on gender and then add the individual group's birthcount, 

.. code-block:: python

    >>> # total number of boys and girls in year 1880 
    >>> names1880.groupby('gender').birthcount.sum() 
    gender
    F     90993
    M    110493
    Name: birthcount, dtype: int64
    >>>

pivot_table
-----------

In previous chapters, we saw various examples of groupby and unstack operations. These two operations can be performed by a single operation as well i.e. pivot_table. In this section, we will calculate the total number of births in years 1880 to 1887 using pivot_table. For this first we need to merge the data from the files for these year.

.. code-block:: python

    >>> years = range(1880, 1887)
    >>> pieces = []
    >>> columns = ['name', 'gender', 'birthcount']
    >>> for year in years:
    ...     path = 'yob{}.txt'.format(year)
    ...     columns = ['name', 'gender', 'birthcount']
    ...     for year in years:
    ...             path =  'yob{}.txt'.format(year)
    ...             df = pd.read_csv(path, names=columns)
    ...             df['year']=year
    ...             pieces.append(df)
    ...             allData = pd.concat(pieces, ignore_index=True)
    ... 
    >>> 
    >>> len(allData)
    105903
    >>> 
    >>> allData.head(2)
       name gender  birthcount  year
    0  Mary      F        7065  1880
    1  Anna      F        2604  1880


* Total number of birth can be calculated using pivot_table, as shown below,

.. code-block:: python

    >>> import matplotlib.pyplot as plt
    >>> total_births = allData.pivot_table('birthcount', index=['year'], columns=['gender'], aggfunc=sum)
    >>> total_births.head(3)
    gender       F       M
    year                  
    1880    636951  773451
    1881    643685  705236
    1882    754957  795809


    >>> total_births.plot(kind='bar') 
    <matplotlib.axes._subplots.AxesSubplot object at 0xa580b44c>
    >>> plt.show() 
    >>>

.. image:: names/plot1.png
    :width: 70%

* Same can be achieved by using 'groupby' option as below, 

.. code-block:: python
    
    >>> allData.groupby(['year', 'gender']).sum().unstack('gender').head(3)
           birthcount        
    gender          F       M
    year                     
    1880       636951  773451
    1881       643685  705236
    1882       754957  795809


* Next, we want to check the ratio of the names with total number of names. For this, we can write a function, which calculates the ration and apply it to groupby option, 

.. code-block:: python

    >>> # calculate ratio
    ... def add_prop(group):
    ...     births = group.birthcount.astype(float)
    ...     group['prop'] = births/births.sum()  # add column prop
    ...     return group
    ... 
    >>> 
    >>> names = allData.groupby(['year', 'gender']).apply(add_prop)

    >>> names.head()
            name gender  birthcount  year      prop
    0       Mary      F        7065  1880  0.011092
    1       Anna      F        2604  1880  0.004088
    2       Emma      F        2003  1880  0.003145
    3  Elizabeth      F        1939  1880  0.003044
    4     Minnie      F        1746  1880  0.00274

