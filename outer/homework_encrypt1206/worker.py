#coding=utf-8

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

if __name__ == '__main__':
    main()
