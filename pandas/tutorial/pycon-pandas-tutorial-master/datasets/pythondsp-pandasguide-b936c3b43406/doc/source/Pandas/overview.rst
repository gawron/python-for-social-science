Overview
========

In this chapter, various functionalities of pandas are shown with examples, which are explained in later chapters as well.

.. note:: 

    CSV files can be downloaded from below link, 

        https://bitbucket.org/pythondsp/pandasguide/downloads/


Reading files
-------------

 In this section, two data files are used i.e. ‘titles.csv’ and ‘cast.csv’. The ‘titles.csv’ file contains the list of movies with the releasing year; whereas ‘cast.csv’ file has five columns which store the title of movie, releasing year, star-casts, type(actor/actress), characters and ratings for actors, as shown below,

.. code-block:: python

    >>> import pandas as pd 

    >>> casts = pd.read_csv('cast.csv', index_col=None)
    >>> casts.head() 
                      title  year      name   type                character     n
    0        Closet Monster  2015  Buffy #1  actor                  Buffy 4  31.0
    1       Suuri illusioni  1985    Homo $  actor                   Guests  22.0
    2   Battle of the Sexes  2017   $hutter  actor          Bobby Riggs Fan  10.0
    3  Secret in Their Eyes  2015   $hutter  actor          2002 Dodger Fan   NaN
    4            Steve Jobs  2015   $hutter  actor  1988 Opera House Patron   NaN

    >>> titles = pd.read_csv('titles.csv', index_col =None)
    >>> titles.tail() 
                          title  year
    49995                 Rebel  1970
    49996               Suzanne  1996
    49997                 Bomba  2013
    49998  Aao Jao Ghar Tumhara  1984
    49999            Mrs. Munck  1995


* **read_csv** : read the data from the csv file.
* **index_col = None** : there is no index i.e. first column is data
* **head()** : show only first five elements of the DataFrame 
* **tail()** : show only last five elements of the DataFrame 

If there is some error while reading the file due to encoding, then try for following option as well, 

.. code-block:: python 

   titles = pd.read_csv('titles.csv', index_col=None, encoding='utf-8') 

If we simply type the name of the DataFrame (i.e. cast in below code), then it will show the first thirty and last twenty rows of the file along with complete list of columns. This can be limited using ‘set_options’ as below. Further, at the end of the table total number of rows and columns will be displayed. 

.. code-block:: python

    >>> pd.set_option('max_rows', 10, 'max_columns', 10) 
    >>> titles 
                             title  year
    0               The Rising Son  1990
    1      The Thousand Plane Raid  1969
    2             Crucea de piatra  1993
    3                      Country  2000
    4                   Gaiking II  2011
    ...                        ...   ...
    49995                    Rebel  1970
    49996                  Suzanne  1996
    49997                    Bomba  2013
    49998     Aao Jao Ghar Tumhara  1984
    49999               Mrs. Munck  1995

    [50000 rows x 2 columns]

* **len** : ‘len’ commmand can be used to see the total number of rows in the file, 

.. code-block:: python

    >>> len(titles) 
    50000

.. note::
   
    head() and tail() commands can be used for remind ourselves about the header and contents of the file. These two commands will show the first and last 5 lines respectively of the file. Further, we can change the total number of lines to be displayed by these commands, 

    >>> titles.head(3) 
                         title  year
    0           The Rising Son  1990
    1  The Thousand Plane Raid  1969
    2         Crucea de piatra  1993


Data operations
---------------

In this section, various useful data operations for DataFrame are shown. 

Row and column selection
^^^^^^^^^^^^^^^^^^^^^^^^

Any row or column of the DataFrame can be selected by passing the name of the column or rows. After selecting one from DataFrame, it becomes one-dimensional therefore it is considered as Series. 

* **ix** : use 'ix' command to select a row from the DataFrame. 

.. code-block:: python

    >>> t = titles['title'] 

    >>> type(t) 
    <class 'pandas.core.series.Series'>

    >>> t.head() 
    0             The Rising Son
    1    The Thousand Plane Raid
    2           Crucea de piatra
    3                    Country
    4                 Gaiking II
    Name: title, dtype: object
    >>>

    >>> titles.ix[0] 
    title    The Rising Son
    year               1990
    Name: 0, dtype: object
    >>>

Filter Data
^^^^^^^^^^^

Data can be filtered by providing some boolean expression in DataFrame. For example, in below code, movies which released after 1985 are filtered out from the DataFrame 'titles' and stored in a new DataFrame i.e. after85. 

.. code-block:: python

    >>> # movies after 1985
    >>> after85 = titles[titles['year'] > 1985] 
    >>> after85.head() 
                   title  year
     0    The Rising Son  1990
     2  Crucea de piatra  1993
     3           Country  2000
     4        Gaiking II  2011
     5       Medusa (IV)  2015
    >>>  

.. note::

    When we pass the boolean results to DataFrame, then panda will show all the results which corresponds to True (rather than displaying True and False), as shown in above code. Further, ‘& (and)’ and ‘| (or)’ can be used for joining two conditions as shown below,**

In below code all the movies in decade 1990 (i.e. 1900-1999) are selected. Also 't = titles' is used for simplicity purpose only. 

.. code-block:: python

    >>> # display movie in years 1990 - 1999
    >>> t = titles 
    >>> movies90 = t[ (t['year']>=1990) & (t['year']<2000) ] 
    >>> movies90.head() 
                           title  year
    0             The Rising Son  1990
    2           Crucea de piatra  1993
    12  Poka Makorer Ghar Bosoti  1996
    19          Maa Durga Shakti  1999
    24      Conflict of Interest  1993
    >>>


Sorting 
^^^^^^^

Sorting can be performed using ‘sort_index’ or ‘sort_values’ keywords,

.. code-block:: python

    >>> # find all movies named as 'Macbeth'
    >>> t = titles 
    >>> macbeth = t[ t['title'] == 'Macbeth'] 
    >>> macbeth.head() 
             title  year
    4226   Macbeth  1913
    9322   Macbeth  2006
    11722  Macbeth  2013
    17166  Macbeth  1997
    25847  Macbeth  1998


Note that in above filtering operation, the data is sorted by index i.e. by default 'sort_index' operation is used as shown below, 

.. code-block:: python

    >>> # by default, sort by index i.e. row header
    >>> macbeth = t[ t['title'] == 'Macbeth'].sort_index() 
    >>> macbeth.head() 
             title  year
    4226   Macbeth  1913
    9322   Macbeth  2006
    11722  Macbeth  2013
    17166  Macbeth  1997
    25847  Macbeth  1998
    >>>

To sort the data by values, the 'sort_value' option can be used. In below code, data is sorted by year now, 

.. code-block:: python

    >>> # sort by year  
    >>> macbeth = t[ t['title'] == 'Macbeth'].sort_values('year')
    >>> macbeth.head() 
             title  year
    4226   Macbeth  1913
    17166  Macbeth  1997
    25847  Macbeth  1998
    9322   Macbeth  2006
    11722  Macbeth  2013
    >>>

Null values
^^^^^^^^^^^


Note that, various columns may contains no values, which are usually filled as NaN. For example, rows 3-4 of casts are NaN as shown below, 

.. code-block:: python

    >>> casts.ix[3:4] 
                      title  year     name   type                character   n
    3  Secret in Their Eyes  2015  $hutter  actor          2002 Dodger Fan NaN
    4            Steve Jobs  2015  $hutter  actor  1988 Opera House Patron NaN


These null values can be easily selected, unselected or contents can be replaced by any other values e.g. empty strings or 0 etc. Various examples of null values are shown in this section. 

* **'isnull'** command returns the true value if any row of has null values. Since the rows 3-4 has NaN value, therefore, these are displayed as True.  

.. code-block:: python

    >>> c = casts 
    >>> c['n'].isnull().head() 
    0    False
    1    False
    2    False
    3     True
    4     True
    Name: n, dtype: bool

* **'notnull'** is opposite of isnull, it returns true for not null values, 

.. code-block:: python

    >>> c['n'].notnull().head()
    0     True
    1     True
    2     True
    3    False
    4    False
    Name: n, dtype: bool

* To display the rows with null values, the condition must be passed in the DataFrame,

.. code-block:: python

    >>> c[c['n'].isnull()].head(3)
                        title  year     name   type                character   n
    3    Secret in Their Eyes  2015  $hutter  actor          2002 Dodger Fan NaN
    4              Steve Jobs  2015  $hutter  actor  1988 Opera House Patron NaN
    5   Straight Outta Compton 2015  $hutter  actor              Club Patron NaN
    >>> 

* NaN values can be fill by using **fillna**, **ffill(forward fill)**, and **bfill(backward fill)** etc. In below code, 'NaN' values are replace by NA. Further, example of ffill and bfill are shown in later part of the tutorial,  

.. code-block:: python

     >>> c_fill = c[c['n'].isnull()].fillna('NA')
     >>> c_fill.head(2) 
                       title  year     name   type                character   n
     3  Secret in Their Eyes  2015  $hutter  actor          2002 Dodger Fan  NA
     4            Steve Jobs  2015  $hutter  actor  1988 Opera House Patron  NA


String operations
^^^^^^^^^^^^^^^^^

Various string operations can be performed using **'.str.'** option. Let's search for the movie "Maa" first, 

.. code-block:: python

    >>> t = titles 
    >>> t[t['title'] == 'Maa'] 
          title  year
    38880   Maa  1968
    >>>

There is only one movie in the list. Now, we want to search all the movies which starts with 'Maa'. The '.str.' option is required for such queries as shown below, 

.. code-block:: python

    >>> t[t['title'].str.startswith("Maa ")].head(3) 
                      title  year
    19     Maa Durga Shakti  1999
    3046      Maa Aur Mamta  1970
    7470  Maa Vaibhav Laxmi  1989
    >>>

.. _countvalues:

Count Values
^^^^^^^^^^^^

Total number of occurrences can be counted using **'value_counts()'** option. In following code, total number of movies are displayed base on years.

.. code-block:: python

    >>> t['year'].value_counts().head() 
    2016    2363
    2017    2138
    2015    1849
    2014    1701
    2013    1609
    Name: year, dtype: int64


Plots
^^^^^

Pandas supports the matplotlib library and can be used to plot the data as well. In previous section, the total numbers of movies/year were filtered out from the DataFrame. In the below code, those values are saved in new DataFrame and then plotted using panda, 

.. code-block:: python

    >>> import matplotlib.pyplot as plt 
    >>> t = titles 
    >>> p = t['year'].value_counts() 
    >>> p.plot() 
    <matplotlib.axes._subplots.AxesSubplot object at 0xaf18df6c>
    >>> plt.show() 


Following plot will be generated from above code, which does not provide any useful information.

.. image:: example1/plot1.png
    :width: 70%

It's better to sort the years (i.e. index) first and then plot the data as below. Here, the plot shows that number of movies are increasing every year.

.. code-block:: python

    >>> p.sort_index().plot() 
    <matplotlib.axes._subplots.AxesSubplot object at 0xa9cd134c>
    >>> plt.show() 
   
.. image:: example1/plot2.png
    :width: 70%
  
Now, the graph provide some useful information i.e. number of movies are increasing each year. 


.. _groupbyEx1:
    
Groupby
-------

Data can be grouped by columns-headers. Further, custom formats can be defined to group the various elements of the DataFrame. 

Groupby with column-names
^^^^^^^^^^^^^^^^^^^^^^^^^

In Section :ref:`countvalues`, the value of movies/year were counted using 'count_values()' method. Same can be achieve by 'groupby' method as well. The 'groupby' command return an object, and we need to an additional functionality to it to get some results. For example, in below code, data is grouped by 'year' and then size() command is used. The **size()** option counts the total number for rows for each year; therefore the result of below code is same as 'count_values()' command. 

.. code-block:: python

    >>> cg = c.groupby(['year']).size()
    >>> cg.plot() 
    <matplotlib.axes._subplots.AxesSubplot object at 0xa9f14b4c>
    >>> plt.show() 
    >>>

.. image:: example1/plot2.png
    :width: 70%


* Further, groupby option can take multiple parameters for grouping. For example, we want to group the movies of the actor 'Aaron Abrams' based on year, 

.. code-block:: python

    >>> c = casts 
    >>> cf = c[c['name'] == 'Aaron Abrams'] 
    >>> cf.groupby(['year']).size().head() 
    year
    2003    2
    2004    2
    2005    2
    2006    1
    2007    2
    dtype: int64
    >>> 

Above list shows that year-2003 is found in two rows with name-entry as 'Aaron Abrams'. In the other word, he did 2 movies in 2003. 

* Next, we want to see the list of movies as well, then we can pass two parameters in the list as shown below,

.. code-block:: python

    >>> cf.groupby(['year', 'title']).size().head()
    year  title                               
    2003  The In-Laws                             1
          The Visual Bible: The Gospel of John    1
    2004  Resident Evil: Apocalypse               1
          Siblings                                1
    2005  Cinderella Man                          1
    dtype: int64
    >>>

In above code, the groupby operation is performed on the 'year' first and then on 'title'. In the other word, first all the movies are grouped by year. After that, the result of this groupby is again grouped based on titles. Note that, first group command arranged the year in order i.e. 2003, 2004 and 2005 etc.; then next group command arranged the title in alphabetical order. 


* Next, we want to do grouping based on maximum ratings in a year; i.e. we want to group the items by year and see the maximum rating in those years, 

.. code-block:: python

    >>> c.groupby(['year']).n.max().head() 
    year
    1912     6.0
    1913    14.0
    1914    39.0
    1915    14.0
    1916    35.0
    Name: n, dtype: float64

Above results show that the maximum rating in year 1912 is 6 for Aaron Abrams. 

* Similarly, we can check for the minimum rating, 

.. code-block:: python

    >>> c.groupby(['year']).n.min().head()
    year
    1912    6.0
    1913    1.0
    1914    1.0
    1915    1.0
    1916    1.0
    Name: n, dtype: float64

* Lastly, we want to check the mean rating each year, 

.. code-block:: python

    >>> c.groupby(['year']).n.mean().head()
    year
    1912    6.000000
    1913    4.142857
    1914    7.085106
    1915    4.236111
    1916    5.037736
    Name: n, dtype: float64

Groupby with custom field
^^^^^^^^^^^^^^^^^^^^^^^^^


Suppose we want to group the data based on decades, then we need to create a custom groupby field, 

.. code-block:: python

    >>> # decade conversion : 1985//10 = 198, 198*10 = 1980
    >>> decade = c['year']//10*10 
    >>> c_dec = c.groupby(decade).n.size() 
    >>> 
    >>> c_dec.head() 
    year
    1910     669
    1920    1121
    1930    3448
    1940    3997
    1950    3892
    dtype: int64
      
Above results shows the total number of movies in each decade.


.. _unstackEx1:

Unstack
-------

Before understanding the unstack, let's consider one case from cast.csv file. In following code, the data is grouped by decade and type i.e. actor and actress. 



.. code-block:: python

    >>> c = casts 
    >>> c.groupby( [c['year']//10*10, 'type'] ).size().head(8)
    year  type   
    1910  actor       384
          actress     285
    1920  actor       710
          actress     411
    1930  actor      2628
          actress     820
    1940  actor      3014
          actress     983
    dtype: int64
    >>>

.. note::

    Unstack is discussed in Section :ref:`unstackDataMorePanda` in detail. 

Now we want to compare and plot the total number of actors and actresses in each decade. One solution to this problem is to grab even and odd rows separately and plot the data, which is quite complicated operation if types has more varieties e.g. new-actor, new-actress and teen-actors etc. A simple solution to such problem is the **'unstack'**, which allows to create a new DataFrame based on the grouped Dataframe, as shown below. 

* Since we want a plot based on actors and actress, therefore first we need to group the data based on 'type' as below, 

.. code-block:: python

    >>> c = casts 
    >>> c_decade = c.groupby( ['type', c['year']//10*10] ).size() 
    >>> c_decade 
    type     year
    actor    1910      384
             1920      710
             1930     2628
             [...]
    actress  1910      285
             1920      411
             1930      820
             [...]
    dtype: int64
    >>>

* Now we can create a new DataFrame using 'unstack' command. The 'unstack' command creates a new DataFrame based on index, 

.. code-block:: python

    >>> c_decade.unstack() 
    year     1910  1920  1930  1940  1950  1960  1970  1980  1990  [...]
    type                                                                          
    actor     384   710  2628  3014  2877  2775  3044  3565  5108  [...]
    actress   285   411   820   983  1015   968  1299  1989  2544  [...]

* Use following commands to plot the above data, 

 .. code-block:: python

    >>> c_decade.unstack().plot() 
    <matplotlib.axes._subplots.AxesSubplot object at 0xb1cec56c>
    >>> plt.show() 
    >>> c_decade.unstack().plot(kind='bar')
    <matplotlib.axes._subplots.AxesSubplot object at 0xa8bf778c>
    >>> plt.show() 


Below figure will be generated from above command. Note that in the plot, actor and actress are plot separately in the groups.  

.. image:: example1/plot4.png
    :width: 70%


* To plot the data side by side, use unstack(0) option as shown below (by default unstack(-1) is used),

.. code-block:: python

    >>> c_decade.unstack(0) 
    type  actor  actress
    year                
    1910    384      285
    1920    710      411
    1930   2628      820
    1940   3014      983
    1950   2877     1015
    1960   2775      968
    1970   3044     1299
    1980   3565     1989
    1990   5108     2544
    2000  10368     5831
    2010  15523     8853
    2020      4        3

    >>> c_decade.unstack(0).plot(kind='bar')
    <matplotlib.axes._subplots.AxesSubplot object at 0xb1d218cc>
    >>> plt.show() 

.. image:: example1/plot5.png
    :width: 70%
 


Merge
-----

Usually, different data of same project are available in various files. To get the useful information from these files, we need to combine these files. Also, we need to merge to different data in the same file to get some specific information. In this section, we will understand these two merges i.e. merge with different file and merge with same file. 

Merge with different files
^^^^^^^^^^^^^^^^^^^^^^^^^^

In this section, we will merge the data of two table i.e. 'release_dates.csv' and 'cast.csv'. The 'release_dates.csv' file contains the release date of movies in different countries. 


* First, load the 'release_dates.csv' file, which contains the release dates of some of the movies, listed in 'cast.csv'. Following are the content of 'release_dates.csv' file,


.. code-block:: python

    >>> release = pd.read_csv('release_dates.csv', index_col=None) 
    >>> release.head() 
                        title  year      country        date
    0   #73, Shaanthi Nivaasa  2007        India  2007-06-15
    1                 #Beings  2015      Romania  2015-01-29
    2               #Declimax  2018  Netherlands  2018-01-21
    3  #Ewankosau saranghaeyo  2015  Philippines  2015-01-21
    4                 #Horror  2015          USA  2015-11-20


    >>> casts.head() 
                      title  year      name   type                character     n
    0        Closet Monster  2015  Buffy #1  actor                  Buffy 4  31.0
    1       Suuri illusioni  1985    Homo $  actor                   Guests  22.0
    2   Battle of the Sexes  2017   $hutter  actor          Bobby Riggs Fan  10.0
    3  Secret in Their Eyes  2015   $hutter  actor          2002 Dodger Fan   NaN
    4            Steve Jobs  2015   $hutter  actor  1988 Opera House Patron   NaN


* Let's we want to see the release date of the movie 'Amelia'. For this first, filter out the Amelia from the DataFrame 'cast' as below. There are only two entries for the movie Amelia. 

.. code-block:: python

    >>> c_amelia = casts[ casts['title'] == 'Amelia']
    >>> c_amelia.head() 
            title  year            name   type    character     n
    5767   Amelia  2009    Aaron Abrams  actor  Slim Gordon   8.0
    23319  Amelia  2009  Jeremy Akerman  actor      Sheriff  19.0
    >>>


* Next, we will see the entries of movie 'Amelia' in release dates as below. In the below result, we can see that there are two different release years for the movie i.e. 1966 and 2009. 

.. code-block:: python

    >>> release [ release['title'] == 'Amelia' ].head() 
            title  year    country        date
    20543  Amelia  1966     Mexico  1966-03-10
    20544  Amelia  2009     Canada  2009-10-23
    20545  Amelia  2009        USA  2009-10-23
    20546  Amelia  2009  Australia  2009-11-12
    20547  Amelia  2009  Singapore  2009-11-12
    >>>

* Since there is not entry for Amelia-1966 in casts DataFrame, therefore merge command will not merge the Amelia-1966 release dates. In following results, we can see that only Amelia 2009 release dates are merges with casts DataFrame. 

.. code-block:: python

    >>> c_amelia.merge(release).head() 
        title  year          name   type    character    n    country        date
    0  Amelia  2009  Aaron Abrams  actor  Slim Gordon  8.0     Canada  2009-10-23
    1  Amelia  2009  Aaron Abrams  actor  Slim Gordon  8.0        USA  2009-10-23
    2  Amelia  2009  Aaron Abrams  actor  Slim Gordon  8.0  Australia  2009-11-12
    3  Amelia  2009  Aaron Abrams  actor  Slim Gordon  8.0  Singapore  2009-11-12
    4  Amelia  2009  Aaron Abrams  actor  Slim Gordon  8.0    Ireland  2009-11-13

 
Merge table with itself
^^^^^^^^^^^^^^^^^^^^^^^

Suppose, we want see the list of co-actors in the movies. For this, we need to merge the table with itself based on the title and year, as shown below. In the below code, co-star for actor 'Aaron Abrams' are displayed,

* First, filter out the results for 'Aaron Abrams', 

  .. code-block:: python

    >>> c = casts[ casts['name']=='Aaron Abrams' ] 
    >>> c.head(2) 
                       title  year          name   type       character    n
    5765       #FromJennifer  2017  Aaron Abrams  actor  Ralph Sinclair  NaN
    5766  388 Arletta Avenue  2011  Aaron Abrams  actor            Alex  4.0
    >>>

* Next, to find the co-stars, merge the DataFrame with itself based on 'title' and 'year' i.e. for being a co-star, the name of the movie and the year must be same, 

* Note that 'casts' is used inside the bracket instead of c.

.. code-block:: python

    c.merge(casts, on=['title', 'year']).head()

.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>title</th>
          <th>year</th>
          <th>name_x</th>
          <th>type_x</th>
          <th>character_x</th>
          <th>n_x</th>
          <th>name_y</th>
          <th>type_y</th>
          <th>character_y</th>
          <th>n_y</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>#FromJennifer</td>
          <td>2017</td>
          <td>Aaron Abrams</td>
          <td>actor</td>
          <td>Ralph Sinclair</td>
          <td>NaN</td>
          <td>Aaron Abrams</td>
          <td>actor</td>
          <td>Ralph Sinclair</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>1</th>
          <td>#FromJennifer</td>
          <td>2017</td>
          <td>Aaron Abrams</td>
          <td>actor</td>
          <td>Ralph Sinclair</td>
          <td>NaN</td>
          <td>Christian Ackerman</td>
          <td>actor</td>
          <td>Simon</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2</th>
          <td>388 Arletta Avenue</td>
          <td>2011</td>
          <td>Aaron Abrams</td>
          <td>actor</td>
          <td>Alex</td>
          <td>4.0</td>
          <td>Graham Abbey</td>
          <td>actor</td>
          <td>Officer #2</td>
          <td>8.0</td>
        </tr>
        <tr>
          <th>3</th>
          <td>388 Arletta Avenue</td>
          <td>2011</td>
          <td>Aaron Abrams</td>
          <td>actor</td>
          <td>Alex</td>
          <td>4.0</td>
          <td>Aaron Abrams</td>
          <td>actor</td>
          <td>Alex</td>
          <td>4.0</td>
        </tr>
        <tr>
          <th>4</th>
          <td>Amelia</td>
          <td>2009</td>
          <td>Aaron Abrams</td>
          <td>actor</td>
          <td>Slim Gordon</td>
          <td>8.0</td>
          <td>Aaron Abrams</td>
          <td>actor</td>
          <td>Slim Gordon</td>
          <td>8.0</td>
        </tr>
      </tbody>
    </table>
    </div>


The problem with above joining is that it displays the 'Aaron Abrams' as
his co-actor as well (see first row). This problem can be avoided as
below,

.. code-block:: python

    c_costar = c.merge (casts, on=['title', 'year'])
    c_costar = c_costar[c_costar['name_y'] != 'Aaron Abrams']
    c_costar.head()

.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>title</th>
          <th>year</th>
          <th>name_x</th>
          <th>type_x</th>
          <th>character_x</th>
          <th>n_x</th>
          <th>name_y</th>
          <th>type_y</th>
          <th>character_y</th>
          <th>n_y</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>1</th>
          <td>#FromJennifer</td>
          <td>2017</td>
          <td>Aaron Abrams</td>
          <td>actor</td>
          <td>Ralph Sinclair</td>
          <td>NaN</td>
          <td>Christian Ackerman</td>
          <td>actor</td>
          <td>Simon</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2</th>
          <td>388 Arletta Avenue</td>
          <td>2011</td>
          <td>Aaron Abrams</td>
          <td>actor</td>
          <td>Alex</td>
          <td>4.0</td>
          <td>Graham Abbey</td>
          <td>actor</td>
          <td>Officer #2</td>
          <td>8.0</td>
        </tr>
        <tr>
          <th>5</th>
          <td>Amelia</td>
          <td>2009</td>
          <td>Aaron Abrams</td>
          <td>actor</td>
          <td>Slim Gordon</td>
          <td>8.0</td>
          <td>Jeremy Akerman</td>
          <td>actor</td>
          <td>Sheriff</td>
          <td>19.0</td>
        </tr>
        <tr>
          <th>8</th>
          <td>Cinderella Man</td>
          <td>2005</td>
          <td>Aaron Abrams</td>
          <td>actor</td>
          <td>1928 Fan</td>
          <td>67.0</td>
          <td>Nick Alachiotis</td>
          <td>actor</td>
          <td>Baer Cornerman</td>
          <td>38.0</td>
        </tr>
        <tr>
          <th>9</th>
          <td>Cinderella Man</td>
          <td>2005</td>
          <td>Aaron Abrams</td>
          <td>actor</td>
          <td>1928 Fan</td>
          <td>67.0</td>
          <td>Nick Alachiotis</td>
          <td>actor</td>
          <td>Undercard Boxer - Feldman</td>
          <td>38.0</td>
        </tr>
      </tbody>
    </table>
    </div>



Index
-----

In the previous section, we saw some uses of index for sorting and plotting the data. In this section, index are discussed in detail.

Index is very important tool in pandas. It is used to organize the data and to provide us fast access to data. In this section, time for data-access are compared for the data with and without indexing. For this section, Jupyter notebook is used as '%%timeit' is very easy to use in it to compare the time required for various access-operations.

Creating index
^^^^^^^^^^^^^^

.. code-block:: python
    
    import pandas as pd
    cast = pd.read_csv('cast.csv', index_col=None)
    cast.head()


.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>title</th>
          <th>year</th>
          <th>name</th>
          <th>type</th>
          <th>character</th>
          <th>n</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>Closet Monster</td>
          <td>2015</td>
          <td>Buffy #1</td>
          <td>actor</td>
          <td>Buffy 4</td>
          <td>31.0</td>
        </tr>
        <tr>
          <th>1</th>
          <td>Suuri illusioni</td>
          <td>1985</td>
          <td>Homo $</td>
          <td>actor</td>
          <td>Guests</td>
          <td>22.0</td>
        </tr>
        <tr>
          <th>2</th>
          <td>Macbeth</td>
          <td>1916</td>
          <td>USA</td>
          <td>1916-06-04</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>3</th>
          <td>Macbeth</td>
          <td>1916</td>
          <td>Japan</td>
          <td>1917-02-26</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>4</th>
          <td>Macbeth</td>
          <td>1948</td>
          <td>France</td>
          <td>1950-06-23</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
      </tbody>
    </table>
    </div>

.. code-block:: python

    %%time
    
    # data access without indexing
    cast[cast['title']=='Macbeth']


.. parsed-literal::

    CPU times: user 8 ms, sys: 4 ms, total: 12 ms
    Wall time: 13.8 ms

.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>title</th>
          <th>year</th>
          <th>name</th>
          <th>type</th>
          <th>character</th>
          <th>n</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>2</th>
          <td>Macbeth</td>
          <td>1916</td>
          <td>USA</td>
          <td>1916-06-04</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>3</th>
          <td>Macbeth</td>
          <td>1916</td>
          <td>Japan</td>
          <td>1917-02-26</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>4</th>
          <td>Macbeth</td>
          <td>1948</td>
          <td>France</td>
          <td>1950-06-23</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>5</th>
          <td>Macbeth</td>
          <td>1948</td>
          <td>West Germany</td>
          <td>1950-06-28</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>6</th>
          <td>Macbeth</td>
          <td>1948</td>
          <td>Finland</td>
          <td>1950-09-22</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>...</th>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
        </tr>
        <tr>
          <th>27046</th>
          <td>Macbeth</td>
          <td>2016</td>
          <td>John Albasiny</td>
          <td>actor</td>
          <td>Doctor</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>38146</th>
          <td>Macbeth</td>
          <td>1948</td>
          <td>William Alland</td>
          <td>actor</td>
          <td>Second Murderer</td>
          <td>18.0</td>
        </tr>
        <tr>
          <th>40695</th>
          <td>Macbeth</td>
          <td>1997</td>
          <td>Stevie Allen</td>
          <td>actor</td>
          <td>Murderer</td>
          <td>21.0</td>
        </tr>
        <tr>
          <th>60599</th>
          <td>Macbeth</td>
          <td>2014</td>
          <td>Moyo Akand?</td>
          <td>actress</td>
          <td>Witch</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>63832</th>
          <td>Macbeth</td>
          <td>1916</td>
          <td>Mary Alden</td>
          <td>actress</td>
          <td>Lady Macduff</td>
          <td>6.0</td>
        </tr>
      </tbody>
    </table>
    <p>63 rows × 6 columns</p>
    </div>



'%%timeit' can be used for more precise results as it run the shell
various times and display the average time; but it will not show the
output of the shell,

.. code-block:: python

    %%timeit
    
    # data access without indexing
    cast[cast['title']=='Macbeth']


.. parsed-literal::

    100 loops, best of 3: 9.85 ms per loop


**'set\_index'** can be used to create an index for the data. Note that, in below code, 'title' is set at index, therefore index-numbers are replaced by 'title' (see the first column).

.. code-block:: python

    # below line will not work for multiple index
    # c = cast.set_index('title')  
    
    c = cast.set_index(['title'])
    c.head(4)


.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>year</th>
          <th>name</th>
          <th>type</th>
          <th>character</th>
          <th>n</th>
        </tr>
        <tr>
          <th>title</th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>Closet Monster</th>
          <td>2015</td>
          <td>Buffy #1</td>
          <td>actor</td>
          <td>Buffy 4</td>
          <td>31.0</td>
        </tr>
        <tr>
          <th>Suuri illusioni</th>
          <td>1985</td>
          <td>Homo $</td>
          <td>actor</td>
          <td>Guests</td>
          <td>22.0</td>
        </tr>
        <tr>
          <th>Macbeth</th>
          <td>1916</td>
          <td>USA</td>
          <td>1916-06-04</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>Macbeth</th>
          <td>1916</td>
          <td>Japan</td>
          <td>1917-02-26</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
      </tbody>
    </table>
    </div>



To use the above indexing, **'.loc'** should be used for fast
operations,

.. code-block:: python

    %%time
    
    # data access with indexing
    # note that there is minor performance improvement
    c.loc['Macbeth']


.. parsed-literal::

    CPU times: user 36 ms, sys: 0 ns, total: 36 ms
    Wall time: 36.2 ms




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>year</th>
          <th>name</th>
          <th>type</th>
          <th>character</th>
          <th>n</th>
        </tr>
        <tr>
          <th>title</th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>Macbeth</th>
          <td>1916</td>
          <td>USA</td>
          <td>1916-06-04</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>Macbeth</th>
          <td>1916</td>
          <td>Japan</td>
          <td>1917-02-26</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>Macbeth</th>
          <td>1948</td>
          <td>France</td>
          <td>1950-06-23</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>Macbeth</th>
          <td>1948</td>
          <td>West Germany</td>
          <td>1950-06-28</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>Macbeth</th>
          <td>1948</td>
          <td>Finland</td>
          <td>1950-09-22</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>...</th>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
        </tr>
        <tr>
          <th>Macbeth</th>
          <td>2016</td>
          <td>John Albasiny</td>
          <td>actor</td>
          <td>Doctor</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>Macbeth</th>
          <td>1948</td>
          <td>William Alland</td>
          <td>actor</td>
          <td>Second Murderer</td>
          <td>18.0</td>
        </tr>
        <tr>
          <th>Macbeth</th>
          <td>1997</td>
          <td>Stevie Allen</td>
          <td>actor</td>
          <td>Murderer</td>
          <td>21.0</td>
        </tr>
        <tr>
          <th>Macbeth</th>
          <td>2014</td>
          <td>Moyo Akand?</td>
          <td>actress</td>
          <td>Witch</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>Macbeth</th>
          <td>1916</td>
          <td>Mary Alden</td>
          <td>actress</td>
          <td>Lady Macduff</td>
          <td>6.0</td>
        </tr>
      </tbody>
    </table>
    <p>63 rows × 5 columns</p>
    </div>



.. code-block:: python

    %%timeit
    
    # data access with indexing
    # note that there is minor performance improvement
    c.loc['Macbeth']


.. parsed-literal::

    100 loops, best of 3: 5.64 ms per loop


\*\* We can see that, there is performance improvement (i.e. 11ms to
6ms) using indexing, because speed will increase further if the index
are in sorted order. \*\*

Next, we will sort the index and perform the filter operation,

.. code-block:: python

    cs = cast.set_index(['title']).sort_index()
    cs.tail(4)




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>year</th>
          <th>name</th>
          <th>type</th>
          <th>character</th>
          <th>n</th>
        </tr>
        <tr>
          <th>title</th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>xXx: Return of Xander Cage</th>
          <td>2017</td>
          <td>Julie Abcede</td>
          <td>actor</td>
          <td>Catwalk Partiers</td>
          <td>84.0</td>
        </tr>
        <tr>
          <th>xXx: Return of Xander Cage</th>
          <td>2017</td>
          <td>Jeimi Abila</td>
          <td>actress</td>
          <td>Lazarus' Girls</td>
          <td>64.0</td>
        </tr>
        <tr>
          <th>xXx: Return of Xander Cage</th>
          <td>2017</td>
          <td>Wayne Ambrose</td>
          <td>actor</td>
          <td>Choir Members</td>
          <td>34.0</td>
        </tr>
        <tr>
          <th>xXx: State of the Union</th>
          <td>2005</td>
          <td>Robert Alonzo</td>
          <td>actor</td>
          <td>Guard</td>
          <td>NaN</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code-block:: python

    %%time
    
    # data access with indexing
    # note that there is huge performance improvement
    cs.loc['Macbeth']


.. parsed-literal::

    CPU times: user 36 ms, sys: 0 ns, total: 36 ms
    Wall time: 38.8 ms




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>year</th>
          <th>name</th>
          <th>type</th>
          <th>character</th>
          <th>n</th>
        </tr>
        <tr>
          <th>title</th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>Macbeth</th>
          <td>2015</td>
          <td>Darren Adamson</td>
          <td>actor</td>
          <td>Soldier</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>Macbeth</th>
          <td>2015</td>
          <td>Estonia</td>
          <td>2015-12-25</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>Macbeth</th>
          <td>1948</td>
          <td>Robert Alan</td>
          <td>actor</td>
          <td>Third Murderer</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>Macbeth</th>
          <td>1948</td>
          <td>West Germany</td>
          <td>1950-06-28</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>Macbeth</th>
          <td>2015</td>
          <td>Bulgaria</td>
          <td>2015-12-11</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>...</th>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
        </tr>
        <tr>
          <th>Macbeth</th>
          <td>2015</td>
          <td>Argentina</td>
          <td>2015-12-17</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>Macbeth</th>
          <td>2009</td>
          <td>USA</td>
          <td>2009-11-17</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>Macbeth</th>
          <td>1997</td>
          <td>UK</td>
          <td>1997-05-16</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>Macbeth</th>
          <td>2015</td>
          <td>Germany</td>
          <td>2015-10-29</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>Macbeth</th>
          <td>1916</td>
          <td>Mary Alden</td>
          <td>actress</td>
          <td>Lady Macduff</td>
          <td>6.0</td>
        </tr>
      </tbody>
    </table>
    <p>63 rows × 5 columns</p>
    </div>



Now, filtering is completing in around '0.5 ms' (rather than 4 ms), as
shown by below results,

.. code-block:: python

    %%timeit
    
    # data access with indexing
    # note that there huge performance improvement
    cs.loc['Macbeth']


.. parsed-literal::

    1000 loops, best of 3: 480 µs per loop

.. _multipleindex:

Multiple index
^^^^^^^^^^^^^^

Further, we can have multiple indexes in the data,

.. code-block:: python

    # data with two index i.e. title and n
    cm = cast.set_index(['title', 'n']).sort_index()
    cm.tail(30)




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th></th>
          <th>year</th>
          <th>name</th>
          <th>type</th>
          <th>character</th>
        </tr>
        <tr>
          <th>title</th>
          <th>n</th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>Zwei in einem Anzug</th>
          <th>2.0</th>
          <td>1950</td>
          <td>Wolf Albach-Retty</td>
          <td>actor</td>
          <td>Otto Vogel</td>
        </tr>
        <tr>
          <th>Zwei in einem Auto</th>
          <th>2.0</th>
          <td>1951</td>
          <td>Wolf Albach-Retty</td>
          <td>actor</td>
          <td>Georg Schmittlein</td>
        </tr>
        <tr>
          <th>Zweimal zwei im Himmelbett</th>
          <th>1.0</th>
          <td>1937</td>
          <td>Georg Alexander</td>
          <td>actor</td>
          <td>Arnd Krusemark</td>
        </tr>
        <tr>
          <th>Zwischen Lachen und Weinen</th>
          <th>NaN</th>
          <td>1919</td>
          <td>Georg Alexander</td>
          <td>actor</td>
          <td>Hans</td>
        </tr>
        <tr>
          <th>Zwischen Pankow und Zehlendorf</th>
          <th>NaN</th>
          <td>1991</td>
          <td>Eugen Albert</td>
          <td>actor</td>
          <td>Soldat</td>
        </tr>
        <tr>
          <th>...</th>
          <th>...</th>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
        </tr>
        <tr>
          <th>w Delta z</th>
          <th>8.0</th>
          <td>2007</td>
          <td>Barbara Adair</td>
          <td>actress</td>
          <td>Alice Jackson</td>
        </tr>
        <tr>
          <th rowspan="3" valign="top">xXx: Return of Xander Cage</th>
          <th>34.0</th>
          <td>2017</td>
          <td>Wayne Ambrose</td>
          <td>actor</td>
          <td>Choir Members</td>
        </tr>
        <tr>
          <th>64.0</th>
          <td>2017</td>
          <td>Jeimi Abila</td>
          <td>actress</td>
          <td>Lazarus' Girls</td>
        </tr>
        <tr>
          <th>84.0</th>
          <td>2017</td>
          <td>Julie Abcede</td>
          <td>actor</td>
          <td>Catwalk Partiers</td>
        </tr>
        <tr>
          <th>xXx: State of the Union</th>
          <th>NaN</th>
          <td>2005</td>
          <td>Robert Alonzo</td>
          <td>actor</td>
          <td>Guard</td>
        </tr>
      </tbody>
    </table>
    <p>30 rows × 4 columns</p>
    </div>



.. code-block:: python


    >>> cm.loc['Macbeth']
           year                 name     type        character
    n                                                         
     4.0   1916  Spottiswoode Aitken    actor           Duncan
     6.0   1916           Mary Alden  actress     Lady Macduff
     18.0  1948       William Alland    actor  Second Murderer
     21.0  1997         Stevie Allen    actor         Murderer
    NaN    2015       Darren Adamson    actor          Soldier
    NaN    1948          Robert Alan    actor   Third Murderer
    NaN    2016        John Albasiny    actor           Doctor
    NaN    2014          Moyo Akand?  actress            Witch









In above result, 'title' is removed from the index list, which
represents that there is one more level of index, which can be used for
filtering. Lets filter the data again with second index as well,

.. code-block:: python

    # show Macbeth with ranking 4-18
    cm.loc['Macbeth'].loc[4:18]




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>year</th>
          <th>name</th>
          <th>type</th>
          <th>character</th>
        </tr>
        <tr>
          <th>n</th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>4.0</th>
          <td>1916</td>
          <td>Spottiswoode Aitken</td>
          <td>actor</td>
          <td>Duncan</td>
        </tr>
        <tr>
          <th>6.0</th>
          <td>1916</td>
          <td>Mary Alden</td>
          <td>actress</td>
          <td>Lady Macduff</td>
        </tr>
        <tr>
          <th>18.0</th>
          <td>1948</td>
          <td>William Alland</td>
          <td>actor</td>
          <td>Second Murderer</td>
        </tr>
      </tbody>
    </table>
    </div>



If there is only one match data, then Series will return (instead of
DataFrame),

.. code-block:: python

    # show Macbeth with ranking 4
    cm.loc['Macbeth'].loc[4]




.. parsed-literal::

    year                        1916
    name         Spottiswoode Aitken
    type                       actor
    character                 Duncan
    Name: 4.0, dtype: object



Reset index
^^^^^^^^^^^

Index can be reset using **'reset\_index**' command. Let's look at the
'cm' DataFrame again.

.. code-block:: python

    cm.head(2)




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th></th>
          <th>year</th>
          <th>name</th>
          <th>type</th>
          <th>character</th>
        </tr>
        <tr>
          <th>title</th>
          <th>n</th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>#1 Serial Killer</th>
          <th>17.0</th>
          <td>2013</td>
          <td>Michael Alton</td>
          <td>actor</td>
          <td>Detective Roberts</td>
        </tr>
        <tr>
          <th>#DigitalLivesMatter</th>
          <th>NaN</th>
          <td>2016</td>
          <td>Rashan Ali</td>
          <td>actress</td>
          <td>News Reporter</td>
        </tr>
      </tbody>
    </table>
    </div>



In 'cm' DataFrame, there are two index; and one of these i.e. n is
removed using 'reset\_index' command.

.. code-block:: python

    # remove 'n' from index
    cm = cm.reset_index('n')
    cm.head(2)




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>n</th>
          <th>year</th>
          <th>name</th>
          <th>type</th>
          <th>character</th>
        </tr>
        <tr>
          <th>title</th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>#1 Serial Killer</th>
          <td>17.0</td>
          <td>2013</td>
          <td>Michael Alton</td>
          <td>actor</td>
          <td>Detective Roberts</td>
        </tr>
        <tr>
          <th>#DigitalLivesMatter</th>
          <td>NaN</td>
          <td>2016</td>
          <td>Rashan Ali</td>
          <td>actress</td>
          <td>News Reporter</td>
        </tr>
      </tbody>
    </table>
    </div>



Implement using Python-CSV library
----------------------------------

Note that, all the above logic can be implemented using python-csv library as well. In this section, some of the logics of above sections are re-implemented using python-csv library.  By looking at following examples, we can see that how easy is it to work with pandas as compare to python-csv library. However, we have more fun with python built-in libraries, 


Read the file
^^^^^^^^^^^^^

.. code-block:: python

    import csv
    titles = list(csv.DictReader(open('titles.csv')))
    titles[0:5]  # display first 5 rows

.. parsed-literal::

    [OrderedDict([('title', 'The Rising Son'), ('year', '1990')]), 
    OrderedDict([('title', 'The Thousand Plane Raid'), ('year', '1969')]), 
    OrderedDict([('title', 'Crucea de piatra'), ('year', '1993')]), 
    OrderedDict([('title', 'Country'), ('year', '2000')]), 
    OrderedDict([('title', 'Gaiking II'), ('year', '2011')])]


.. code-block:: python
    
    # display last 5 rows 
    titles[-5:]

.. parsed-literal::

    [OrderedDict([('title', 'Rebel'), ('year', '1970')]), 
    OrderedDict([('title', 'Suzanne'), ('year', '1996')]), 
    OrderedDict([('title', 'Bomba'), ('year', '2013')]), 
    OrderedDict([('title', 'Aao Jao Ghar Tumhara'), ('year', '1984')]), 
    OrderedDict([('title', 'Mrs. Munck'), ('year', '1995')])]



* Display title and year in separate row, 

.. code-block:: python

    for k, v in titles[0].items():
        print(k, ':',  v)


.. parsed-literal::

    title : The Rising Son
    year : 1990

Display movies according to year
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Display all movies in year 1985

.. code-block:: python

    year85 = [a for a in titles if a['year'] == '1985']
    year85[:5]

.. parsed-literal::

    [OrderedDict([('title', 'Insaaf Main Karoonga'), ('year', '1985')]), 
    OrderedDict([('title', 'Vivre pour survivre'), ('year', '1985')]), 
    OrderedDict([('title', 'Water'), ('year', '1985')]), 
    OrderedDict([('title', 'Doea tanda mata'), ('year', '1985')]), 
    OrderedDict([('title', 'Koritsia gia tsibima'), ('year', '1985')])]



* Movies in years 1990 - 1999, 

.. code-block:: python

    # movies from 1990 to 1999
    movies90 = [m for m in titles if (int(m['year']) < int('2000')) and (int(m['year']) > int('1989'))]
    movies90[:5]

.. parsed-literal::

    [OrderedDict([('title', 'The Rising Son'), ('year', '1990')]), 
    OrderedDict([('title', 'Crucea de piatra'), ('year', '1993')]), 
    OrderedDict([('title', 'Poka Makorer Ghar Bosoti'), ('year', '1996')]), 
    OrderedDict([('title', 'Maa Durga Shakti'), ('year', '1999')]), 
    OrderedDict([('title', 'Conflict of Interest'), ('year', '1993')])]


* Find all movies 'Macbeth', 

.. code-block:: python

    # find Macbeth movies
    macbeth = [m for m in titles if m['title']=='Macbeth']
    macbeth[:3]

.. parsed-literal::

    [OrderedDict([('title', 'Macbeth'), ('year', '1913')]), 
    OrderedDict([('title', 'Macbeth'), ('year', '2006')]), 
    OrderedDict([('title', 'Macbeth'), ('year', '2013')])]


operator.iemgetter
^^^^^^^^^^^^^^^^^^

* Sort movies by year, 

.. code-block:: python

    # sort based on year and display 3 
    from operator import itemgetter
    sorted(macbeth, key=itemgetter('year'))[:3]

.. parsed-literal::

    [OrderedDict([('title', 'Macbeth'), ('year', '1913')]), 
    OrderedDict([('title', 'Macbeth'), ('year', '1997')]), 
    OrderedDict([('title', 'Macbeth'), ('year', '1998')])]


Replace empty string with 0
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    casts = list(csv.DictReader(open('cast.csv')))

.. code-block:: python

    casts[3:5]

.. parsed-literal::

    [OrderedDict([('title', 'Secret in Their Eyes'), 
        ('year', '2015'), 
        ('name', '$hutter'), 
        ('type', 'actor'), 
        ('character', '2002 Dodger Fan'), 
        ('n', '')]), 
    OrderedDict([('title', 'Steve Jobs'), 
        ('year', '2015'), 
        ('name', '$hutter'), 
        ('type', 'actor'), 
        ('character', '1988 Opera House Patron'), 
        ('n', '')])]


.. code-block:: python

    # replace '' with 0
    cast0 = [{**c, 'n':c['n'].replace('', '0')} for c in casts]
    cast0[3:5]

.. parsed-literal::

    [{'title': 'Secret in Their Eyes', 
        'year': '2015', 'name': '$hutter', 
        'type': 'actor', 'character': '2002 Dodger Fan', 
        'n': '0'}, 
    {'title': 'Steve Jobs', 
    'year': '2015', 'name': '$hutter', 
    'type': 'actor', 'character': '1988 Opera House Patron', 
    'n': '0'}]


* Movies starts with 'Maa'

.. code-block:: python

    # Movies starts with Maa
    maa = [m for m in titles if m['title'].startswith('Maa')]
    maa[:3]


.. parsed-literal::

    [OrderedDict([('title', 'Maa Durga Shakti'), ('year', '1999')]), 
    OrderedDict([('title', 'Maarek hob'), ('year', '2004')]), 
    OrderedDict([('title', 'Maa Aur Mamta'), ('year', '1970')])]



collections.Counter
^^^^^^^^^^^^^^^^^^^

* Count movies by year, 

.. code-block:: python

    # Most release movies
    from collections import Counter
    by_year = Counter(t['year'] for t in titles)
    by_year.most_common(3)
    # by_year.elements # to see the complete dictionary


.. parsed-literal::

    ['1990', '1969', '1993', '2000', '2011']


* plot the data

.. code-block:: python

    import matplotlib.pyplot as plt
    data = by_year.most_common(len(titles))
    data = sorted(data)  # sort the data for proper axis
    x = [c[0] for c in data]  # extract year
    y = [c[1] for c in data]  # extract total number of movies
    plt.plot(x, y)
    plt.show()


.. image:: example1/plot6.png
    :width: 70%


collections.defaultdict
^^^^^^^^^^^^^^^^^^^^^^^

* append movies in dictionary by year, 

.. code-block:: python

    from collections import defaultdict

.. code-block:: python

    d = defaultdict(list)
    for row in titles:
        d[row['year']].append(row['title'])
    
    xx=[]
    yy=[]
    for k, v in d.items():
        xx.append(k)# = k
        yy.append(len(v))# = len(v)
    
    plt.plot(sorted(xx), yy)
    plt.show()


.. image:: example1/plot7.png
    :width: 70%

.. code-block:: python

    xx[:5]  # display content of xx

.. parsed-literal::

    ['1976', '1964', '1914', '1934', '1952']

.. code-block:: python

    yy[:5] # display content of yy 

.. parsed-literal::

    [515, 465, 437, 616, 1457]


* show all movies of Aaron Abrams

.. code-block:: python

    # show all movies of Aaron Abrams
    cf = [c for c in casts if c['name']=='Aaron Abrams']
    cf[:3]

.. parsed-literal::

    [OrderedDict([('title', '#FromJennifer'), ('year', '2017'), 
        ('name', 'Aaron Abrams'), ('type', 'actor'), 
        ('character', 'Ralph Sinclair'), ('n', '')]), 
    OrderedDict([('title', '388 Arletta Avenue'), ('year', '2011'), 
        ('name', 'Aaron Abrams'), ('type', 'actor'), 
        ('character', 'Alex'), ('n', '4')]), 
    OrderedDict([('title', 'Amelia'), ('year', '2009'), 
        ('name', 'Aaron Abrams'), ('type', 'actor'), 
        ('character', 'Slim Gordon'), ('n', '8')])]


* Collect all movies of Aaron Abrams by year, 

.. code-block:: python

    # Display movies of Aaron Abrams by year
    dcf = defaultdict(list)
    for row in cf:
        dcf[row['year']].append(row['title'])

    dcf


.. code-block:: text

    defaultdict(<class 'list'>, {
        '2017': ['#FromJennifer', 'The Go-Getters'], 
        '2011': ['388 Arletta Avenue', 'Jesus Henry Christ', 'Jesus Henry Christ', 'Take This Waltz', 'The Chicago 8'], '2009': ['Amelia', 'At Home by Myself... with You'], 
        '2005': ['Cinderella Man', 'Sabah'], 
        '2015': ['Closet Monster', 'Regression'], 
        '2018': ['Code 8'], '2007': ['Firehouse Dog', 'Young People Fucking'], 
        '2008': ['Flash of Genius'], '2013': ['It Was You Charlie'], 
        '2004': ['Resident Evil: Apocalypse', 'Siblings'], 
        '2003': ['The In-Laws', 'The Visual Bible: The Gospel of John'], 
        '2006': ['Zoom']})




