#coding=utf-8
import numpy as np
class Node(object):
    """节点类"""
    def __init__(self, elem=-1, lchild=None, rchild=None):
        self.elem = elem
        self.lchild = lchild
        self.rchild = rchild

class Tree(object):
    def __init__(self,root=0):
        self.root = root

def huffman_tree(arr):
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

def huffman_dict(mytree,i):
    nodes0 = []
    codes0 = []
    if mytree.lchild == None and mytree.rchild == None:
        nodes0.append([mytree.elem])
        codes0.append([i])
    else:
        nodes0,codes0 = huffman_dict(mytree.lchild,0)
        nodes1,codes1 = huffman_dict(mytree.rchild,1)
        nodes0.extend(nodes1)
        codes0.extend(codes1)
        for u in range(len(codes0)):
            codes0[u].insert(0,i)
    return nodes0,codes0

arr = [1,4,7,11,20]
huff_tree = huffman_tree(arr)
sample,codec = huffman_dict(huff_tree,1)
print(sample)
print(codec)