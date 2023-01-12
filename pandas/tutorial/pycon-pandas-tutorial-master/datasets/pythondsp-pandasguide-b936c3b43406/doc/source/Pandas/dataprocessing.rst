Data processing 
===============

Most of programming work in data analysis and modeling is spent on data preparation e.g. loading, cleaning and rearranging the data etc. Pandas along with python libraries gives us provide us a high performance, flexible and high level environment for processing the data. 

In chapter 1, we saw basics of pandas; then various examples are shown in chapter 2 for better understanding of pandas; whereas chapter 3 presented some basics of numpy. In this chapter, we will see some more functionality of pandas to process the data effectively.


Hierarchical indexing
---------------------

Hierarchical indexing is an important feature of pandas that enable us to have multiple index levels. We already see an example of it in Section :ref:`multipleindex`. In this section, we will learn more about indexing and access to data with these indexing.  

Creating multiple index
^^^^^^^^^^^^^^^^^^^^^^^

* Following is an example of series with multiple index, 

.. code-block:: python

    >>> import pandas as pd 
    >>> data = pd.Series([10, 20, 30, 40, 15, 25, 35, 25], index = [['a', 'a',
    ... 'a', 'a', 'b', 'b', 'b', 'b'], ['obj1', 'obj2', 'obj3', 'obj4', 'obj1',
    ... 'obj2', 'obj3', 'obj4']]) 
    >>> data 
    a  obj1    10
       obj2    20
       obj3    30
       obj4    40
    b  obj1    15
       obj2    25
       obj3    35
       obj4    25
    dtype: int64


* There are two level of index here i.e. (a, b) and (obj1, ..., obj4). The index can be seen using 'index' command as shown below,  

.. code-block:: python

    >>> data.index 
    MultiIndex(levels=[['a', 'b'], ['obj1', 'obj2', 'obj3', 'obj4']],
               labels=[[0, 0, 0, 0, 1, 1, 1, 1], [0, 1, 2, 3, 0, 1, 2, 3]])

Partial indexing
^^^^^^^^^^^^^^^^

Choosing a particular index from a hierarchical indexing is known as partial indexing.

* In the below code, index 'b' is extracted from the data, 

.. code-block:: python

    >>> data['b'] 
    obj1    15
    obj2    25
    obj3    35
    obj4    25
    dtype: int64

* Further, the data can be extracted based on inner level i.e. 'obj'. Below result shows the two available values for 'obj2' in the Series. 

.. code-block:: python

    >>> data[:, 'obj2']
    a    20
    b    25
    dtype: int64
    >>>

.. _unstackDataMorePanda:

Unstack the data
^^^^^^^^^^^^^^^^

 We saw the use of unstack operation in the Section :ref:`unstackEx1`. Unstack changes the row header to column header. Since the row index is changed to column index, therefore the Series will become the DataFrame in this case. Following are the some more example of unstacking the data, 

.. code-block:: python

    >>> # unstack based on first level i.e. a, b
    >>> # note that data row-labels are a and b
    >>> data.unstack(0) 
           a   b
    obj1  10  15
    obj2  20  25
    obj3  30  35
    obj4  40  25

    >>> # unstack based on second level i.e. 'obj' 
    >>> data.unstack(1) 
       obj1  obj2  obj3  obj4
    a    10    20    30    40
    b    15    25    35    25
    >>>

    >>> # by default innermost level is used for unstacking
    >>> d = data.unstack()
    >>> d
       obj1  obj2  obj3  obj4
    a    10    20    30    40
    b    15    25    35    25

* 'stack()' operation converts the column index to row index again. In above code, DataFrame 'd' has 'obj' as column index, this can be converted into row index using 'stack' operation, 

.. code-block:: python

    >>> d.stack() 
    a  obj1    10
       obj2    20
       obj3    30
       obj4    40
    b  obj1    15
       obj2    25
       obj3    35
       obj4    25
    dtype: int64

Column indexing
^^^^^^^^^^^^^^^

Remember that, the column indexing is possible for DataFrame only (not for Series), because column-indexing require two dimensional data. Let's create a new DataFrame as below for understanding the columns with multiple index,  

.. code-block:: python

    >>> import numpy as np 
    >>> df = pd.DataFrame(np.arange(12).reshape(4, 3), 
    ...     index = [['a', 'a', 'b', 'b'], ['one', 'two', 'three', 'four']], 
    ...     columns = [['num1', 'num2', 'num3'], ['red', 'green', 'red']] 
    ... ) 
    >>>  
    >>> df 
            num1  num2 num3
             red green  red
    a one      0     1    2
      two      3     4    5
    b three    6     7    8
      four     9    10   11
    >>>

    >>> # display row index 
    >>> df.index 
    MultiIndex(levels=[['a', 'b'], ['four', 'one', 'three', 'two']],
               labels=[[0, 0, 1, 1], [1, 3, 2, 0]])

    >>> # display column index
    >>> df.columns 
    MultiIndex(levels=[['num1', 'num2', 'num3'], ['green', 'red']],
               labels=[[0, 1, 2], [1, 0, 1]])

* Note that, in previous section, we used the numbers for stack and unstack operation e.g. unstack(0) etc. We can give name to index as well as below, 

.. code-block:: python

    >>> df.index.names=['key1', 'key2'] 
    >>> df.columns.names=['n', 'color'] 
    >>> df 
    n          num1  num2 num3
    color       red green  red
    key1 key2                 
    a    one      0     1    2
         two      3     4    5
    b    three    6     7    8
         four     9    10   11
   
* Now, we can perform the partial indexing operations. In following code, various ways to access the data in a DataFrame are shown, 

.. code-block:: python

    >>> # accessing the column for num1
    >>> df['num1']  #  df.ix[:, 'num1'] 
    color       red
    key1 key2      
    a    one      0
         two      3
    b    three    6
         four     9
    
    >>> # accessing the column for a
    >>> df.ix['a'] 
    n     num1  num2 num3
    color  red green  red
    key2                 
    one      0     1    2
    two      3     4    5

    >>> # access row 0 only
    >>> df.ix[0]
    n     color
    num1  red      0
    num2  green    1
    num3  red      2
    Name: (a, one), dtype: int32

Swap and sort level
^^^^^^^^^^^^^^^^^^^

We can swap the index level using 'swaplevel' command, which takes two level-numbers as input, 

.. code-block:: python

    >>> df.swaplevel('key1', 'key2') 
    n          num1  num2 num3
    color       red green  red
    key2  key1                
    one   a       0     1    2
    two   a       3     4    5
    three b       6     7    8
    four  b       9    10   11
    >>>

Levels can be sorted using 'sort_index' command. In below code, data is sorted by 'key2' names i.e. key2 is arranged alphabatically, 

.. code-block:: python

    >>> df.sort_index(level='key2')
    n          num1  num2 num3
    color       red green  red
    key1 key2                 
    b    four     9    10   11
    a    one      0     1    2
    b    three    6     7    8
    a    two      3     4    5
    >>>


Summary statistics by level
^^^^^^^^^^^^^^^^^^^^^^^^^^^

We saw the example of groupby command in Section :ref:`groupbyEx1`. Pandas provides some easier ways to perform those operations using 'level' shown below, 

.. code-block:: python

    >>> # add all rows with similar key1 name 
    >>> df.sum(level = 'key1') 
    n     num1  num2 num3
    color  red green  red
    key1                 
    a        3     5    7
    b       15    17   19
    >>>

    >>> # add all the columns based on similar color
    >>> df.sum(level= 'color', axis=1)
    color       green  red
    key1 key2             
    a    one        1    2
         two        4    8
    b    three      7   14
         four      10   20


File operations
---------------

In this section, various methods for reading and writing the files are discussed. 

Reading files
^^^^^^^^^^^^^

Pandas supports various types of file format e.g. csv, text, excel and different database etc. Files are often stored in different formats as well e.g. files may or may not contain header, footer and comments etc.; therefore we need to process the content of file. Pandas provides various features which can process some of the common processing while reading the file. Some of these processing are shown in this section. 

* Files can be read using 'read\_csv', 'read\_table' or 'DataFrame.from\_csv' options, as shown below. Note that, the output of all these methods are same, but we need to provide different parameters to read the file correctly. 

Following are the contents of 'ex1.csv' file,  

.. code-block:: shell
    
    $ cat ex1.csv 
    a,b,c,d,message
    1,2,3,4,hello
    5,6,7,8,world
    9,10,11,12,foo

Below are the outputs of different file reading methods. 'read\_csv' is general purpose method for reading the files, hence this method is used for rest of the tutorial, 

.. code-block:: python

    
    >>> import pandas as pd 
    
    >>> # DataFrame.from_csv
    >>> df = pd.DataFrame.from_csv('ex1.csv', index_col=None)
    >>> df 
       a   b   c   d message
    0  1   2   3   4   hello
    1  5   6   7   8   world
    2  9  10  11  12     foo

    >>> # read_csv
    >>> df = pd.read_csv('ex1.csv') 
    >>> df 
       a   b   c   d message
    0  1   2   3   4   hello
    1  5   6   7   8   world
    2  9  10  11  12     foo

    >>> # read_table
    >>> df = pd.read_table('ex1.csv', sep=',')
    >>> df 
       a   b   c   d message
    0  1   2   3   4   hello
    1  5   6   7   8   world
    2  9  10  11  12     foo
    >>>

* Note that, in above outputs, the headers are added from the file; but not all the files contain header. In this case, we need to explicitly define the header as below, 

Following are the contents of 'ex2.csv' file, 

.. code-block:: shell

    $ cat ex2.csv  
    1,2,3,4,hello
    5,6,7,8,world
    9,10,11,12,food

Since header is not present in above file, therefore we need to provide  the "header" argument explicitly. 

.. code-block:: python

    >>> import pandas as pd 

    >>> # set header as none, default values will be used as header 
    >>> pd.read_csv('ex2.csv', header=None) 
       0   1   2   3      4
    0  1   2   3   4  hello
    1  5   6   7   8  world
    2  9  10  11  12    foo

    >>> # specify the header using 'names'
    >>> pd.read_csv('ex2.csv', names=['a', 'b', 'c', 'd', 'message']) 
       a   b   c   d message
    0  1   2   3   4   hello
    1  5   6   7   8   world
    2  9  10  11  12     foo
    
    >>> # specify the row and column header both
    >>> pd.read_csv('ex2.csv', names=['a', 'b', 'c', 'd', 'message'], index_col='message')
             a   b   c   d
    message               
    hello    1   2   3   4
    world    5   6   7   8
    foo      9  10  11  12
    >>>


* Hierarchical index can be created by providing a list to 'index_col' argument,  

Following are the contents of 'csv_mindex.csv' file, 

.. code-block:: shell

    $ cat csv_mindex.csv 
    key1,key2,value1,value2
    one,a,1,2
    one,b,3,4
    one,c,5,6
    one,d,7,8
    two,a,9,10
    two,b,11,12
    two,c,13,14
    two,d,15,16

The hierarchical index can be created with 'key' values as below, 

.. code-block:: python

    >>> pd.read_csv('csv_mindex.csv', index_col=['key1', 'key2']) 
                  value1  value2
    key1 key2                
    one     a          1       2
            b          3       4
            c          5       6
            d          7       8
    two     a          9      10
            b         11      12
            c         13      14
            d         15      16
    >>> 

* Some files may contain additional information or comments, therefore we need to remove these information for processing the data. This can be done by using 'skiprows' command, 

Following are the content of 'ex4.csv' file, 

.. code-block:: shell

    $ cat ex4.csv 
    # hey!
    a,b,c,d,message
    # just wanted to make things more difficult for you
    # who reads CSV files with computers, anyway?
    1,2,3,4,hello
    5,6,7,8,world
    9,10,11,12,foodh

In above results, lines 0, 2 and 3 contains some comments. These can be removed as follows, 

.. code-block:: python 

    >>> d = pd.read_csv('ex4.csv', skiprows=[0,2,3])
    >>> d
        a   b   c   d message
     0  1   2   3   4   hello
     1  5   6   7   8   world
     2  9  10  11  12     foo

Writing data to a file
^^^^^^^^^^^^^^^^^^^^^^

The 'to\_csv' command is used to save the file. In following code, previous data 'd' is saved in two files i.e. d\_out.csv and d\_out2.csv with and without index respectively, 

.. code-block:: python

    >>> d.to_csv('d_out.csv')

    >>> # save without headers
    >>> d.to_csv('d_out2.csv', header=False, index=False)

Contents of above two files are shown below, 

.. code-block:: shell
    
    $ cat d_out.csv 
    ,a,b,c,d,message
    0,1,2,3,4,hello
    1,5,6,7,8,world
    2,9,10,11,12,foo

    $ cat d_out2.csv 
    0,1,2,3,4,hello
    1,5,6,7,8,world
    2,9,10,11,12,foo


Merge
-----

Merge or joins operations combine the data sets by liking rows using one or more keys. The 'merge' function is the main entry point for using these algorithms on the data. Let's understand this by following examples,

.. code-block:: python

    >>> df1 = pd.DataFrame({ 'key' : ['b', 'b', 'a', 'c', 'a', 'a', 'b'],  
    ...                     'data1' : range(7)}) 

    >>> df2 = pd.DataFrame({ 'key' : ['a', 'b', 'd'],  
    ...                      'data2' : range(3)}) 

    >>> df1 
       data1 key
    0      0   b
    1      1   b
    2      2   a
    3      3   c
    4      4   a
    5      5   a
    6      6   b
    
    >>> df2 = pd.DataFrame({ 'key' : ['a', 'b', 'd', 'b'],  
    ...                      'data2' : range(4)})
    >>> df2 
       data2 key
    0      0   a
    1      1   b
    2      2   d
    3      3   b
    >>>
   
Many to one 
^^^^^^^^^^^


* 'Many to one' merge joins the Cartesian product of the rows, e.g. df1 and df2 has total 3 and 2 rows of 'b' respectively, therefore join will result in total 6 rows. Further, it is better to define 'on' keyword while using the joins, as it makes code more readable,

.. code-block:: python

    >>> pd.merge(df1, df2)  # or pd.merge(df1, df2, on='key') 
        data1 key  data2
     0      0   b      1
     1      0   b      3
     2      1   b      1
     3      1   b      3
     4      6   b      1
     5      6   b      3
     6      2   a      0
     7      4   a      0
     8      5   a      0
     >>>

* In previous case, both the DataFrame have the same header 'key'. In the following example data are joined based on different keys using 'left_on' and 'right_on' keywords,

.. code-block:: python

    >>> # data is same as previous, only 'key' is replaces with 'key1' and 'key2'
    >>> df1 = pd.DataFrame({ 'key1' : ['b', 'b', 'a', 'c', 'a', 'a', 'b'], 
    ...                     'data1' : range(7)}) 
    >>> df2 = pd.DataFrame({ 'key2' : ['a', 'b', 'd', 'b'],   
    ...                     'data1' : range(4)})

    >>> pd.merge(df1, df2, left_on='key1', right_on='key2') 
       data1_x key1  data1_y key2
    0        0    b        1    b
    1        0    b        3    b
    2        1    b        1    b
    3        1    b        3    b
    4        6    b        1    b
    5        6    b        3    b
    6        2    a        0    a
    7        4    a        0    a
    8        5    a        0    a
    >>>


Inner and outer join
^^^^^^^^^^^^^^^^^^^^

In previous example, we can see that uncommon entries in DataFrame 'df1' and 'df2' are missing from the merge e.g. 'd' is not in the merged data. This is an example of 'inner join' where only common keys are merged together. 
By default, pandas perform the inner join. To perform outer join, we need to use 'how' keyword which can have 3 different values i.e. 'left', 'right' and 'outer'. 'left' option takes the left DataFrame and merge all it's entries with other DataFrame. Similarly, 'right' option merge the entries of the right DataFrame with left DataFrame. Lastly, the 'outer' option merge all the entries from both the DataFrame, as shown below. Note that, the missing entries after joining the table are represented as 'NaN'. 

.. code-block:: python

    >>> # left join
    >>> pd.merge(df1, df2, left_on='key1', right_on='key2', how="left") 
       data1_x key1  data1_y key2
    0        0    b      1.0    b
    1        0    b      3.0    b
    2        1    b      1.0    b
    3        1    b      3.0    b
    4        2    a      0.0    a
    5        3    c      NaN  NaN
    6        4    a      0.0    a
    7        5    a      0.0    a
    8        6    b      1.0    b
    9        6    b      3.0    b

    >>> # right join
    >>> pd.merge(df1, df2, left_on='key1', right_on='key2', how="right")
        data1_x key1  data1_y key2
    0      0.0    b        1    b
    1      1.0    b        1    b
    2      6.0    b        1    b
    3      0.0    b        3    b
    4      1.0    b        3    b
    5      6.0    b        3    b
    6      2.0    a        0    a
    7      4.0    a        0    a
    8      5.0    a        0    a
    9      NaN  NaN        2    d

    >>> # outer join
    >>> pd.merge(df1, df2, left_on='key1', right_on='key2', how="outer")
        data1_x key1  data1_y key2
    0       0.0    b      1.0    b
    1       0.0    b      3.0    b
    2       1.0    b      1.0    b
    3       1.0    b      3.0    b
    4       6.0    b      1.0    b
    5       6.0    b      3.0    b
    6       2.0    a      0.0    a
    7       4.0    a      0.0    a
    8       5.0    a      0.0    a
    9       3.0    c      NaN  NaN
    10      NaN  NaN      2.0    d


Concatenating the data
^^^^^^^^^^^^^^^^^^^^^^

We saw concatenation of data in Numpy. Pandas concatenation is more generalized than Numpy. It allows concatenation based on union or intersection of data along with labeling to visualize the grouping as shown in this section, 

.. code-block:: python

    
    >>> s1 = pd.Series([0, 1], index=['a', 'b']) 
    >>> s2 = pd.Series([2, 1, 3], index=['c', 'd', 'e'])
    >>> s3 = pd.Series([4, 7], index=['a', 'e']) 

    >>> s1 
    a    0
    b    1
    dtype: int64
    
    >>> s2 
    c    2
    d    1
    e    3
    dtype: int64
    
    >>> s3 
    a    4
    e    7
    dtype: int64

    >>> # concatenate s1 and s2
    >>> pd.concat([s1, s2])
    a    0
    b    1
    c    2
    d    1
    e    3
    dtype: int64

    >>> # join on axis 1
    >>> pd.concat([s1, s2], axis=1)
         0    1
    a  0.0  NaN
    b  1.0  NaN
    c  NaN  2.0
    d  NaN  1.0
    e  NaN  3.0

* In above results , it is difficult to identify the different pieces of concatenate operation. We can provide 'keys' to make the operation identifiable, 

.. code-block:: python

    >>> pd.concat([s1, s2, s3], keys=['one', 'two', 'three'])
    one    a    0
           b    1
    two    c    2
           d    1
           e    3
    three  a    4
           e    7
    dtype: int64

.. note::

    Above concatenate operation are the union of two data set i.e. it is outer join. We can use "join='inner'" for intersection of data. 

.. code-block:: python

    >>> pd.concat([s1, s3], join='inner', axis=1)
        0  1
     a  0  4

* Concatenating the DataFrame is same as above. Following is the example of the concatenation of DataFrame. Note that 'df1' and 'df2' are defined at the beginning of this section. 

.. code-block:: python

    >>> pd.concat([df1, df2], join='inner', axis=1, keys=['one', 'two'])
        one        two     
      data1 key1 data1 key2
    0     0    b     0    a
    1     1    b     1    b
    2     2    a     2    d
    3     3    c     3    b

* We can pass the DataFrame as dictionary as well for the concatenation operation. In this case, the keys of the dictionary will be used as 'keys' for the operation, 

.. code-block:: python

    >>> pd.concat({ 'level1':df1, 'level2':df2}, axis=1, join='inner') 
        level1      level2     
         data1 key1  data1 key2
      0      0    b      0    a
      1      1    b      1    b
      2      2    a      2    d
      3      3    c      3    b
      >>>


Data transformation
-------------------

In previous section, we saw various operations to join the various data. Next, important step is the data transformation i.e. cleaning and filtering the data e.g. removing the duplicate entries and replacing the NaN values etc. 

Removing duplicates
^^^^^^^^^^^^^^^^^^^

* Removing duplicate entries are quite easy with 'drop_duplicates' command. Also, 'duplicate()' command can be used to check the duplicate entries as shown below, 

.. code-block:: python

    >>> # create DataFrame with duplicate entries
    >>> df = pd.DataFrame({'k1':['one']*3 + ['two']*4,  
    ...                     'k2':[1,1,2,3,3,4,4]}) 
    >>> df 
        k1  k2
    0  one   1
    1  one   1
    2  one   2
    3  two   3
    4  two   3
    5  two   4
    6  two   4

    >>> # see the duplicate entries
    >>> df.duplicated() 
    0    false
    1     true
    2    false
    3    false
    4     true
    5    false
    6     true
    dtype: bool

    >>> # drop the duplicate entries
    >>> df.drop_duplicates() 
        k1  k2
    0  one   1
    2  one   2
    3  two   3
    5  two   4


* Currently, last entry is removed by drop_duplicates commnad. If we want to keep the last entry, then 'keep' keyword can be used, 

.. code-block:: python

    >>> df.drop_duplicates(keep="last")
        k1  k2
    1  one   1
    2  one   2
    4  two   3
    6  two   4
    >>>

* We can drop all the duplicate values from based on the specific columns as well, 

.. code-block:: python

    >>> # drop duplicate entries based on k1 only
    >>> df.drop_duplicates(['k1'])
        k1  k2
    0  one   1
    3  two   3
    
    >>> # drop if k1 and k2 column matched
    >>> df.drop_duplicates(['k1', 'k2'])
        k1  k2
    0  one   1
    2  one   2
    3  two   3
    5  two   4
    >>>

Replacing values
^^^^^^^^^^^^^^^^

Replacing value is very easy using pandas as below, 

.. code-block:: python

    >>> # replace 'one' with 'One'
    >>> df.replace('one', 'One') 
        k1  k2
    0  One   1
    1  One   1
    2  One   2
    3  two   3
    4  two   3
    5  two   4
    6  two   4

    >>> # replace 'one'->'One'  and 3->30
    >>> df.replace(['one', 3], ['One', '30'])
        k1  k2
    0  One   1
    1  One   1
    2  One   2
    3  two  30
    4  two  30
    5  two   4
    6  two   4
    >>>

* Arguments can be passed as dictionary as well, 

.. code-block:: python

    >>> df.replace({'one':'One', 3:30})
        k1  k2
    0  One   1
    1  One   1
    2  One   2
    3  two  30
    4  two  30
    5  two   4
    6  two   4

Groupby and data aggregation
----------------------------

Basics
^^^^^^


We saw various groupby operation in Section :ref:`groupbyEx1`. Here, some more features of gropby operations are discussed. 

Let's create a DataFrame first, 

.. code-block:: python

    >>> df = pd.DataFrame({'k1':['a', 'a', 'b', 'b', 'a'], 
    ...                     'k2':['one', 'two', 'one', 'two', 'one'],  
    ...                     'data1': [2, 3, 3, 2, 4], 
    ...                     'data2': [5, 5, 5, 5, 10]}) 
    >>> df 
       data1  data2 k1   k2
    0      2      5  a  one
    1      3      5  a  two
    2      3      5  b  one
    3      2      5  b  two
    4      4     10  a  one


* Now, create a group based on 'k1' and find the mean value as below. In the following code, rows (0, 1, 4) and (2, 3) are grouped together. Therefore mean values are 3 and 2.5.

.. code-block:: python

    >>> gp1 = df['data1'].groupby(df['k1']) 
    >>> gp1 
    <pandas.core.groupby.SeriesGroupBy object at 0xb21f6bcc>
    >>> gp1.mean() 
    k1
    a    3.0
    b    2.5
    Name: data1, dtype: float64

* We can pass multiple parameters for grouping as well, 

.. code-block:: python

    >>> gp2 = df['data1'].groupby([df['k1'], df['k2']]) 
    >>> mean = gp2.mean() 
    >>> mean
    k1  k2 
    a   one    3
        two    3
    b   one    3
        two    2
    Name: data1, dtype: int64
    >>>

Iterating over group
^^^^^^^^^^^^^^^^^^^^

* The groupby operation supports iteration which generates the tuple with two values i.e. group-name and data. 

.. code-block:: python

    >>> for name, group in gp1: 
    ...     print(name) 
    ...     print(group) 
    ...  
    a
    0    2
    1    3
    4    4
    Name: data1, dtype: int64
    b
    2    3
    3    2
    Name: data1, dtype: int64


* If groupby operation is performed based on multiple keys, then it will generate a tuple for keys as well, 

.. code-block:: python

    >>> for name, group in gp2: 
    ...     print(name) 
    ...     print(group) 
    ...  
    ('a', 'one')
    0    2
    4    4
    Name: data1, dtype: int64
    ('a', 'two')
    1    3
    Name: data1, dtype: int64
    ('b', 'one')
    2    3
    Name: data1, dtype: int64
    ('b', 'two')
    3    2
    Name: data1, dtype: int64


    >>> # seperate key values as well
    >>> for (k1, k2), group in gp2: 
    ...     print(k1, k2)
    ...     print(group) 
    ...  
    a one
    0    2
    4    4
    Name: data1, dtype: int64
    a two
    1    3
    Name: data1, dtype: int64
    b one
    2    3
    Name: data1, dtype: int64
    b two
    3    2
    Name: data1, dtype: int64
    >>>

Data aggregation
^^^^^^^^^^^^^^^^

We can perform various aggregation operation on the grouped data as well, 

.. code-block:: python

    >>> gp1.max() 
    k1
    a    4
    b    3
    Name: data1, dtype: int64
    >>> gp2.min()
    k1  k2 
    a   one    2
        two    3
    b   one    3
        two    2
    Name: data1, dtype: int64



