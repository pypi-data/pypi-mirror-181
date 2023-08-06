"""Array sorting"""

import numpy as np

__all__ = ['sort_by_counting', ]

def sort_by_counting(array):
    """Sorts an array by counting

    >>> sort_by_counting([3, 1, 1, 2])
    [1, 1, 2, 3]

    >>> sort_by_counting([3, -1, 2, 2])
    Traceback (most recent call last):
        ...
    ValueError: Array must consist of positive numbers

    >>> sort_by_counting([3, 1.2, 2, 2])
    Traceback (most recent call last):
        ...
    TypeError: Array must consist of integers

    >>> sort_by_counting([3, '1', 2, 2])
    Traceback (most recent call last):
        ...
    TypeError: Array must consist of integers
    """

    for i in array:
        if isinstance(i, (float, str)):
            raise TypeError('Array must consist of integers')
        if i < 0 :
            raise ValueError('Array must consist of positive numbers')

    count_array = np.zeros(max(array) + 1, dtype='int32')
    for i in array:
        count_array[i] += 1
    array = np.array([], dtype='int32')
    count_array = list(count_array)
    for value, counts in enumerate(count_array):
        if counts:
            array = np.append(array, [value] * counts)
    return list(array)

if __name__ == '__main__':
    import doctest
    print(doctest.testmod())
