import numpy as np
#coding=utf-8
class Node(object):
    """节点类"""
    def __init__(self, elem=-1, lchild=None, rchild=None):
        self.elem = elem
        self.lchild = lchild
        self.rchild = rchild

class Tree(object):
    def __init__(self,root=0):
        self.root = root

def huffman_dict(arr):
    arr = np.sort(arr)
    length = len(arr)
    if length < 1:
        raise ValueError('check whether the input is empty')
    else:
        i = 0
        tree = Node(arr[0])
        for i in range(1,length):
            root = Node(tree.elem+arr[i])
            root.lchild = tree
            root.rchild = Node(arr[i])
            tree = root
        return tree

arr = [1,4,7,11,20]
huff_tree = huffman_dict(arr)
print(huff_tree.elem)