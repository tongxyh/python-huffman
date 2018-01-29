import numpy as np
import huffman
arr = [1,2,1,2,4,4,3,2,4,4,2,3,3,3,3,3,4,4,4,4]
distri = [0.1,0.2,0.3,0.4]
avgbits,codec = huffman.dict(distri,1,10)
huffman.encode(arr,codec,'test')
decoded = huffman.decode(len(arr),codec,'test')
print(decoded)
