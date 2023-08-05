""" 
Author:		 Muhammad Tahir Rafique
Date:		 2022-11-10 11:34:33
Project:	 File Explorer Lib
Description: Provide function to perform sorting.
"""


def argsort(seq):
    return sorted(range(len(seq)), key=seq.__getitem__)

def sort_files(sort_array, array_to_sort, mode='a'):
    """Sort the second list accoring to first list.
    mode: a (assending), d (decending)
    """
    # GETTING SORTING IDX
    sort_idx = argsort(sort_array)
    if mode == 'd':
        sort_idx = sort_idx[::-1]

    # LOOPING THROUGH TO MAKE NEW LIST
    new_list = []
    for idx in sort_idx:
        new_list.append(array_to_sort[idx])
    return new_list