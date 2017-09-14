#coding=utf-8
import numpy as np
import bitstring
import struct

class Node(object):
    """节点类"""
    def __init__(self, distrib=-1, value=None, lchild=None, rchild=None):
        self.distrib = distrib #distribution
        self.value = value #value of sample
        self.lchild = lchild
        self.rchild = rchild

class Tree(object):
    def __init__(self,root=0):
        self.root = root

def sort_nodes(nodelist):
    #fast
    length = len(nodelist)
    if nodelist[0].distrib > nodelist[length-1].distrib:
        nodelist.insert(0,nodelist[length-1])
        nodelist.pop()
        #print [x.distrib for x in nodelist]
        return nodelist
    for i in range(length):
        if i == len(nodelist)-1 or (nodelist[i].distrib <= nodelist[length-1].distrib and nodelist[i+1].distrib > nodelist[length-1].distrib):
            nodelist.insert(i,nodelist[length-1])
            nodelist.pop()
            #print [x.distrib for x in nodelist]
            return nodelist

def sort_nodes_all(nodelist):
    #fast
    length = len(nodelist)
    a = []
    b = []
    for i in range(1,length):
        if nodelist[i].distrib < nodelist[0].distrib:
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

#calaulate the distribution of the data to be encoded
def cal_distrib(arr,begin_n = 0,end_n = 256):
    freq = []
    for i in range(begin_n,end_n+1):
        freq.append(np.sum(arr == i))
    return freq

#calaulate thr average bits of the data encoded by huffman
def cal_avgbits(arr,codec):
    a = 0
    for i in range(len(arr)):
        a = len(codec[i]) * arr[i] + a
    return a

#build the huffman tree
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
            #print [(x.distrib,x.value) for x in nodes]
        i = 0
        while(len(nodes) > 1):
            root = Node(nodes[0].distrib + nodes[1].distrib)
            root.lchild = nodes[1]
            root.rchild = nodes[0]
            del(nodes[1])
            del(nodes[0])
            nodes.append(root)
            if len(nodes) > 1:
                nodes = sort_nodes(nodes)
        return nodes[0]

#get the codec of the huffman tree
def huffman_search(mytree,i):
    nodes0 = []
    codes0 = []
    if mytree.lchild == None and mytree.rchild == None:
        nodes0.append(mytree.value)
        codes0.append([i])
    else:
        nodes0,codes0 = huffman_search(mytree.lchild,1)
        nodes1,codes1 = huffman_search(mytree.rchild,0)
        nodes0.extend(nodes1)
        codes0.extend(codes1)
        for u in range(len(codes0)):
            codes0[u].insert(0,i)
    return nodes0,codes0

def dict(arr,begin_n = 1,end_n = 10):
    #input: arr - distribution
    arr_list = [x for x in range(begin_n,end_n+1)]
    huff_tree = huffman_tree(arr,arr_list)
    sample0,codec0 = huffman_search(huff_tree.lchild,1)
    sample1,codec1 = huffman_search(huff_tree.rchild,0)
    sample0.extend(sample1)
    codec0.extend(codec1)
    sample,codec = sort_bond(sample0,codec0)
    avgbits = cal_avgbits(arr,codec)
    dict = {}
    for i in range(len(sample)):
         dict[sample[i]] = codec[i]
    #    print(sample[i])
    return avgbits,dict

def encode(arr,codec,filename):
    arr = arr.flatten()
    bin = ''
    file_object = open(filename + '.deepc', 'wb')

    #deal with codec
    #strb = b'BEG'
    #bytes = struct.pack('3s',strb)
    #file_object.write(bytes)
    codec_str = []
    for i in codec:
        #print(i)
        cod = ''
        for j in codec[i]:
            cod = cod + str(j)
        codec_str.append(cod)
        bytes = struct.pack('ii%ds'%len(codec[i]),i,len(codec[i]),codec_str[i].encode('utf-8'))
        file_object.write(bytes)

    for i in arr:
        for j in codec[i]:
            bin = bin + str(j)
    bitstring.Bits(bin=bin).tofile(file_object)

    file_object.close()

def decode(filename):
    f = open(filename + '.deepc', 'rb')