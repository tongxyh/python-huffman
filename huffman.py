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
def sort_nodes(nodelist):
    #fast
    length = len(nodelist)
    if nodelist[0].elem > nodelist[length-1].elem:
        nodelist.insert(0,nodelist[length-1])
        nodelist.pop()
        print [x.elem for x in nodelist]
        return nodelist
    for i in range(length):
        if i == len(nodelist)-1 or (nodelist[i].elem <= nodelist[length-1].elem and nodelist[i+1].elem > nodelist[length-1].elem):
            nodelist.insert(i,nodelist[length-1])
            nodelist.pop()
            print [x.elem for x in nodelist]
            return nodelist

def huffman_tree(arr):
    arr = np.sort(arr)
    length = len(arr)
    nodes = []
    if length < 1:
        raise ValueError('check whether the input is empty')
    else:
        for x in arr:
            nodes.append(Node(x))

        i = 0
        while(len(nodes) > 1):
            root = Node(nodes[0].elem + nodes[1].elem)
            root.lchild = nodes[1]
            root.rchild = nodes[0]
            del(nodes[1])
            del(nodes[0])
            nodes.append(root)
            if len(nodes) > 1:
                nodes = sort_nodes(nodes)
        return nodes[0]

def huffman_dict(mytree,i):
    nodes0 = []
    codes0 = []
    if mytree.lchild == None and mytree.rchild == None:
        nodes0.append([mytree.elem])
        codes0.append([i])
    else:
        nodes0,codes0 = huffman_dict(mytree.lchild,1)
        nodes1,codes1 = huffman_dict(mytree.rchild,0)
        nodes0.extend(nodes1)
        codes0.extend(codes1)
        for u in range(len(codes0)):
            codes0[u].insert(0,i)
    return nodes0,codes0

arr = [1,4,7,11,111]
huff_tree = huffman_tree(arr)
sample0,codec0 = huffman_dict(huff_tree.lchild,1)
sample1,codec1 = huffman_dict(huff_tree.rchild,0)
sample0.extend(sample1)
codec0.extend(codec1)
print(sample0)
print(codec0)