#coding=utf-8

chars = [chr(i) for i in xrange(97,123)]
total_map = dict()
map(lambda x:total_map.setdefault(x[0], 0), chars)

def decodeme(decodebase, contents):
    pass

def codeme(encodebase, contents):
    pass

def analyze(contents):
    contents = contents.lower()
    for i in contents:
        total_map[i] += 1
    return sorted(total_map.items(), key=lambda d: d[1], reverse=True)

def assign(contents):
    pass

def main():
    # read the code from input
    codebook = input("Please enter the codebook: ")
    print(codebook)
    freq = analyze(codebook)
    printFreq(freq)
    encode, decode = assign(freq)
    print("Encode:")
    print(encode)
    print("Decode:")
    print(decode)
    while (True):
        enc = input("Please enter a message to encode: ")
        print(enc)
        if enc == "EXIT":
            break
        if enc != "SKIP":
            coded = codeme(encode, enc)
            print(coded)
        dec = input("Please enter a message to decode: ")
        print(dec)
        if dec == "EXIT":
            break
        if dec != "SKIP":
            coded = decodeme(decode, dec)
            print(coded)
    print("This program will self destruct in 10 seconds...")
#main()
print analyze('accd')
