import numpy as np

def get_index(a, b):

    """
    Returns the index of the given elements in the list.

    Args:
        a (list or float): Elements to be searched.
        b (list): List for searching.

    Returns:
        inx (list or int): The index of the given elements in the list b.
        inx_converse (list or int): The index of the given elements in the list a.
    """


    inx = []
    inx_converse = []
    # Check the type of the given element, whether it is a single one or several items.
    if isinstance(a, list) | isinstance(a, np.ndarray):
        for x in a:
            try:
                inx.append(b.index(x))
                inx_converse.append(a.index(x))
            except ValueError:
                pass
        return inx, inx_converse
    else:
        try:
            inx.append(b.index(a))
        except ValueError:
            pass
        return inx