#coding=utf-8
import numpy as np
import huffman
import bitstring
import struct

def write_head(codec,f):
    file_object = f

    bytes = struct.pack('i',len(codec))     #  codec NUM
    offset = struct.calcsize('i')
    file_object.write(bytes)

    for i in codec:
        cod = ''
        for j in codec[i]:
            cod = cod + str(j)
        #codec_str.append(cod)
        bytes = struct.pack('ii%ds'%len(codec[i]),i,len(codec[i]),cod.encode('utf-8'))
        offset = struct.calcsize('ii%ds'%len(codec[i])) + offset

        #bytes = struct.pack("ii",1,2)
        #print struct.unpack("ii", bytes)
        file_object.write(bytes)

    offset = struct.calcsize('i') + offset
    #print('bits:',offset)
    #file_object.close()
    return offset*8

def read_head(file_object):

    #string = file_object.read(1)
    #print(string)
    codec_num = struct.unpack("i",file_object.read(4))[0]
    dict={}
    for i in range(codec_num):
        index, lens = struct.unpack("ii",file_object.read(8))
        #dict[index] = struct.unpack("%ds"%lens,file_object.read(lens))[0]
        str = struct.unpack("%ds"%lens,file_object.read(lens))[0]
        cod = []
        for j in str:
            cod.append(int(j))
        dict[index] = cod
        #print index,dict[index]
    lens_arr = struct.unpack("i",file_object.read(4))[0]
    #data= int(file_object.read().encode('hex'),16)
    #file_object.close()
    return lens_arr

#arr = [1,2,1,2,4,4,3,2,4,4,2,3,3,3,3,3,4,4,4,4]
#distri = [0.1,0.2,0.3,0.4]

np.random.seed()
cnt = 0
for _ in range(1000):

    arr = np.random.randint(1,6,[20])
    distri = [0.2,0.2,0.2,0.2,0.2]

    avgbits,codec = huffman.dict(distri,1,5)

    #write
    f = open('test.dat', 'wb')
    sizehead = write_head(codec,f)
    sizearr = huffman.encode(arr,codec,f)
    sizearr = int(np.ceil(sizearr/8.0)*8)
    f.close()
    #print('head:',sizehead,'bytes')
    #print('arr:',sizearr,'bytes')
    #print('file sum:',sizehead + sizearr,'bytes / ',(sizehead + sizearr)/8,'bits')
    #print 'head:',sizehead,'bits'
    #print 'arr:',sizearr,'bits'
    #print 'file sum:',sizehead + sizearr,'bits /',(sizehead + sizearr)/8,'bytes'

    #read
    file_object = open('test.dat', 'rb')
    lens_arr = read_head(file_object)
    #print(lens_arr)
    decoded = huffman.decode(lens_arr,codec,file_object)
    file_object.close()

    #print("decoded: ",decoded)
    #print "original data: ",arr
    #print "decoded data: ",decoded
    def list_compare(a,b):
        if len(a) == len(b):
            _flag = (a == b)
            for i in _flag:
                if i == False:
                    #print "FAIL"
                    return False
            #print "SUCCESS"
            return True
        else:
            #print "FAIL"
            return False
    r = list_compare(arr,decoded)
    if r == True:
        cnt += 1

print "TEST PASSED {}/{}".format(cnt,1000)
