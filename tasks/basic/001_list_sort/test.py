from buggy import sort_list

def test_sort_ascending():
    assert sort_list([3, 1, 2]) == [1, 2, 3]

def test_sort_descending():
    assert sort_list([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]

def test_sort_with_duplicates():
    assert sort_list([3, 1, 2, 1]) == [1, 1, 2, 3]

def test_sort_empty():
    assert sort_list([]) == []

def test_sort_single():
    assert sort_list([42]) == [42]

def test_sort_all_same():
    assert sort_list([7, 7, 7, 7]) == [7, 7, 7, 7]
