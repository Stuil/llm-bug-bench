from buggy import TreeNode, inorder_traversal

def test_empty():
    assert inorder_traversal(None) == []

def test_single():
    root = TreeNode(5)
    assert inorder_traversal(root) == [5]

def test_left_heavy():
    root = TreeNode(3, TreeNode(2, TreeNode(1)))
    assert inorder_traversal(root) == [1, 2, 3]

def test_full_tree():
    root = TreeNode(4,
        TreeNode(2, TreeNode(1), TreeNode(3)),
        TreeNode(6, TreeNode(5), TreeNode(7))
    )
    assert inorder_traversal(root) == [1, 2, 3, 4, 5, 6, 7]
