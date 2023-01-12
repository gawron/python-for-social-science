Numpy
=====

Numerical Python (Numpy) is used for performing various numerical computation in python. Calculations using Numpy arrays are faster than the normal python array. Further, pandas are build over numpy array, therefore better understanding of python can help us to use pandas more effectively. 

Creating Arrays
---------------

Defining multidimensional arrays are very easy in numpy as shown in below examples, 


.. code-block:: python

    >>> import numpy as np 

    >>> # 1-D array
    >>> d = np.array([1, 2, 3]) 
    >>> type(d) 
    <class 'numpy.ndarray'>
    >>> d 
    array([1, 2, 3])
    >>>

    >>> # multi dimensional array
    >>> nd = np.array([[1, 2, 3], [3, 4, 5], [10, 11, 12]])
    >>> type(nd) 
    <class 'numpy.ndarray'>
    >>> nd 
    array([[ 1,  2,  3],
           [ 3,  4,  5],
           [10, 11, 12]])
    >>> nd.shape  #  shape of array 
    (3, 3)
    >>> nd.dtype  #  data type  
    dtype('int32')
    >>> 

    >>> #  define zero matrix
    >>> np.zeros(3) 
    array([ 0.,  0.,  0.])
    >>> np.zeros([3, 2])
    array([[ 0.,  0.],
           [ 0.,  0.],
           [ 0.,  0.]])

    >>> # diagonal matrix
    >>> e = np.eye(3)
    array([[ 1.,  0.,  0.],
           [ 0.,  1.,  0.],
           [ 0.,  0.,  1.]])

    >>> # add 2 to e
    >>> e2 = e + 2 
    >>> e2 
    array([[ 3.,  2.,  2.],
           [ 2.,  3.,  2.],
           [ 2.,  2.,  3.]])


    >>> # create matrix with all entries as 1 and size as 'e2'
    >>> o = np.ones_like(e2)
    >>> o 
    array([[ 1.,  1.,  1.],
           [ 1.,  1.,  1.],
           [ 1.,  1.,  1.]])

    >>> # changing data type
    >>> o = np.ones_like(e2) 
    >>> o.dtype 
    dtype('float64')
    >>> oi = o.astype(np.int32)
    >>> oi 
    array([[1, 1, 1],
           [1, 1, 1],
           [1, 1, 1]])
    >>> oi.dtype 
    dtype('int32')
    >>>

    >>> # convert string-list to float
    >>> a = ['1', '2', '3'] 
    >>> a_arr = np.array(a, dtype=np.string_)  # convert list to ndarray
    >>> af = a_arr.astype(float)  # change ndarray type
    >>> af 
    array([ 1.,  2.,  3.])
    >>> af.dtype 
    dtype('float64')

Boolean indexing
----------------

Boolean indexing is very important feature of numpy, which is frequently used in pandas, 

.. code-block:: python

    >>> # accessing data with boolean indexing
    >>> data = np.random.randn(5, 3) 
    >>> data 
    array([[ 0.96174001,  1.49352768, -0.31277422],
           [ 0.25044202,  2.35367396,  0.5697222 ],
           [-1.21536074,  0.82088599, -1.85503026],
           [-1.31492648,  1.24546252,  0.27972961],
           [ 0.23487862, -0.20627825,  0.41470205]])
    >>> name = np.array(['a', 'b', 'c', 'a', 'b']) 
    >>> name=='a' 
    array([ True, False, False,  True, False], dtype=bool)
    >>> data[name=='a'] 
    array([[ 0.96174001,  1.49352768, -0.31277422],
           [-1.31492648,  1.24546252,  0.27972961]])

    >>> data[name != 'a'] 
    array([[ 0.25044202,  2.35367396,  0.5697222 ],
           [-1.21536074,  0.82088599, -1.85503026],
           [ 0.23487862, -0.20627825,  0.41470205]])
    >>> data[(name == 'b')  |  (name=='c')] 
    array([[ 0.25044202,  2.35367396,  0.5697222 ],
           [-1.21536074,  0.82088599, -1.85503026],
           [ 0.23487862, -0.20627825,  0.41470205]])

    >>> data[ (data > 1) & (data < 2) ]
    array([ 1.49352768,  1.24546252])
        

Reshaping arrays
----------------

.. code-block:: python

    >>> a = np.arange(0, 20) 
    >>> a 
    array([ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16,
           17, 18, 19])

    >>> # reshape array a 
    >>> a45 = a.reshape(4, 5) 
    >>> a45 
    array([[ 0,  1,  2,  3,  4],
           [ 5,  6,  7,  8,  9],
           [10, 11, 12, 13, 14],
           [15, 16, 17, 18, 19]])
    
    >>> # select row 2, 0 and 1 from a45 and store in b
    >>> b = a45[ [2, 0, 1] ] 
    >>> b 
    array([[10, 11, 12, 13, 14],
           [ 0,  1,  2,  3,  4],
           [ 5,  6,  7,  8,  9]])
    
    >>> # transpose array b
    >>> b.T 
    array([[10,  0,  5],
           [11,  1,  6],
           [12,  2,  7],
           [13,  3,  8],
           [14,  4,  9]])


Concatenating the data
----------------------

We can combine the data to two arrays using 'concatenate' command, 

.. code-block:: python

    >>> arr = np.arange(12).reshape(3,4) 
    >>> rn = np.random.randn(3, 4) 
    >>> arr 
    array([[ 0,  1,  2,  3],
           [ 4,  5,  6,  7],
           [ 8,  9, 10, 11]])
    >>> rn 
    array([[-0.25178434,  0.98443663, -0.99723191, -0.64737102],
           [ 1.29179768, -0.88437251, -1.25608884, -1.60265896],
           [-0.60085171,  0.8569506 ,  0.62657649,  1.43647342]])

    >>> # merge data of rn below the arr
    >>> np.concatenate([arr, rn])
    array([[  0.        ,   1.        ,   2.        ,   3.        ],
           [  4.        ,   5.        ,   6.        ,   7.        ],
           [  8.        ,   9.        ,  10.        ,  11.        ],
           [ -0.25178434,   0.98443663,  -0.99723191,  -0.64737102],
           [  1.29179768,  -0.88437251,  -1.25608884,  -1.60265896],
           [ -0.60085171,   0.8569506 ,   0.62657649,   1.43647342]])

    >>> # merge dataof rn on the right side of the arr
    >>> np.concatenate([arr, rn], axis=1)
    array([[  0.        ,   1.        ,   2.        ,   3.        ,
             -0.25178434,   0.98443663,  -0.99723191,  -0.64737102],
           [  4.        ,   5.        ,   6.        ,   7.        ,
              1.29179768,  -0.88437251,  -1.25608884,  -1.60265896],
           [  8.        ,   9.        ,  10.        ,  11.        ,
             -0.60085171,   0.8569506 ,   0.62657649,   1.43647342]])
    >>>


