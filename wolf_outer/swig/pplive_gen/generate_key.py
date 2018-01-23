import time,md5,pplive_key_generate

def generateOldKey():
    t = long(time.time())
    return pplive_key_generate.generateOldKey(t)
	
if __name__ == "__main__" :
    print("genrate old key :%s\n" % generateOldKey())