#coding=utf-8
"""
参考leveldb中的bloom filter
"""

class BloomFilter(object):
    def __init__(self, bits_per_key):
        self.bits_per_key_ = bits_per_key
        self.key_num_ = int(bits_per_key * 0.69) #log2
        self.hash_seed = 0xbc9f1d34

    @staticmethod
    def DecodeFixed32(input_str):
        """
        字符串是大端存储，需要转成小端转换成数字
        """
        h = 0
        index = 0
        for i in xrange(len(input_str)):
            h |= ord(input_str[i]) << index * 8
            index += 1
        return h

    @staticmethod
    def BloomHash(input_str, seed):
        #similar to murmur hash
        m = 0xc6a4a793
        r = 24
        h = seed ^ (len(input_str) * m)
        index = 0
        while index + 4 <= len(input_str):
            w = BloomFilter.DecodeFixed32(input_str[index:4])
            index += 4
            h += w
            h *= m
            h ^= (h >> 16)
        flag = len(input_str) - index
        while flag > 0:
            h += ord(input_str[index + flag - 1]) << ((flag - 1) * 8)
            flag -= 1
        h *= m
        h ^= (h >> r)
        return h

    def CreateFilter(self, input_str):
        bits = self.bits_per_key_ * len(input_str)
        if bits < 64:
            bits = 64
        #占用字节数
        tbytes = (bits + 7) / 8
        #真是占用空间
        bits = tbytes * 8
        dst = [0 for i in xrange(tbytes)]
        dst.append(self.key_num_)
        for i in xrange(len(input_str)):
            h = BloomFilter.BloomHash(input_str[i], self.hash_seed)
            delta = (h >> 17) | (h << 15)
            for j in xrange(self.key_num_):
                bitpos = h % bits
                dst[bitpos / 8] |= (1 << (bitpos % 8))
                h += delta
        return dst #返回filter

    def KeyMayMatch(self, input_str, input_filter):
        if len(input_filter) < 2:
            return False
        bits = (len(input_filter) - 1) * 8
        if input_filter[-1] > 30:
            print "warn: hash key num is too large"
            return True
        for i in xrange(len(input_str)):
            h = BloomFilter.BloomHash(input_str[i], self.hash_seed)
            delta = (h >> 17) | (h << 15)
            for j in xrange(self.key_num_):
                bitpos = h % bits
                if (input_filter[bitpos / 8] & (1 << (bitpos % 8))) == 0:
                    return False
                h += delta
        return True

if __name__ == '__main__':
    s = ['this','is','test']
    bloom = BloomFilter(8)
    dt = bloom.CreateFilter(input_str=s)
    print bloom.KeyMayMatch(['test',], dt)
    #print BloomFilter(5).BloomHash(s[:1],0xbc9f1d34)
    #print BloomFilter(5).BloomHash(s[:2],0xbc9f1d34)
    #print BloomFilter(5).BloomHash(s[:3],0xbc9f1d34)
    #print BloomFilter(5).BloomHash(s[:4],0xbc9f1d34)
    #print BloomFilter(5).DecodeFixed32('this')
