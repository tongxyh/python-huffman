#coding=utf-8
import numpy as np
class Node(object):
    """节点类"""
    def __init__(self, elem=-1, cod = None, lchild=None, rchild=None):
        self.elem = elem
        self.cod = cod
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
        #print [x.elem for x in nodelist]
        return nodelist
    for i in range(length):
        if i == len(nodelist)-1 or (nodelist[i].elem <= nodelist[length-1].elem and nodelist[i+1].elem > nodelist[length-1].elem):
            nodelist.insert(i,nodelist[length-1])
            nodelist.pop()
            #print [x.elem for x in nodelist]
            return nodelist

def sort_nodes_all(nodelist):
    #fast
    length = len(nodelist)
    a = []
    b = []
    for i in range(1,length):
        if nodelist[i].elem < nodelist[0].elem:
            a.append(nodelist[i])
        else:
            b.append(nodelist[i])
    if len(a) > 1:
        a = sort_nodes_all(a)
    if len(b) > 1:
        b = sort_nodes_all(b)
    a.append(nodelist[0])
    a.extend(b)
    return a

def sort_bond(node_a,node_b):
    length = len(node_a)
    a_before = []
    a_after = []
    b_before = []
    b_after = []
    for i in range(1,length):
        if node_a[i] < node_a[0]:
            a_before.append(node_a[i])
            b_before.append(node_b[i])
        else:
            a_after.append(node_a[i])
            b_after.append(node_b[i])
    if len(a_before) > 1:
        a_before,b_before = sort_bond(a_before,b_before)
    if len(a_after) > 1:
        a_after,b_after = sort_bond(a_after,b_after)
    a_before.append(node_a[0])
    a_before.extend(a_after)
    b_before.append(node_b[0])
    b_before.extend(b_after)
    return a_before,b_before

def huffman_tree(arr,code_list):
    length = len(arr)
    nodes = []
    if length < 1:
        raise ValueError('check whether the input is empty')
    else:
        for x,y in zip(arr,code_list):
            nodes.append(Node(x,y))
            #print(x,y)
        if len(nodes) > 1:
            nodes = sort_nodes_all(nodes)
            #print [(x.elem,x.cod) for x in nodes]
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
        nodes0.append([mytree.cod])
        codes0.append([i])
    else:
        nodes0,codes0 = huffman_dict(mytree.lchild,1)
        nodes1,codes1 = huffman_dict(mytree.rchild,0)
        nodes0.extend(nodes1)
        codes0.extend(codes1)
        for u in range(len(codes0)):
            codes0[u].insert(0,i)
    return nodes0,codes0

def cal_distrib(arr,numbeg,numend):
    freq = []
    for i in range(numbeg,numend+1):
        freq.append(np.sum(arr == i))
    return freq

def cal_avgbits(arr,codec):
    a = 0
    for i in range(len(arr)):
        a = len(codec[i]) * arr[i] + a
    return a
inp = [1,2,3,4,5,1,3,4,2,5,1,1,1,4,2,1,3,4,5,2,1,3,4,4,2,2,2,1,4,1,3,1,1,3,1,1,5,1,3,2,1,1,3,4,5,3,4,5,5,3,2,1,3,2,3,2,1,2]
inp = np.array(inp)
arr = cal_distrib(inp,1,5)
arr = arr/np.double(np.sum(arr))
print(arr)
arr_list = [x for x in range(1,6)]

huff_tree = huffman_tree(arr,arr_list)

sample0,codec0 = huffman_dict(huff_tree.lchild,1)
sample1,codec1 = huffman_dict(huff_tree.rchild,0)
sample0.extend(sample1)
codec0.extend(codec1)
sample,codec = sort_bond(sample0,codec0)

print(sample)
print(codec)

a = cal_avgbits(arr,codec)
print a