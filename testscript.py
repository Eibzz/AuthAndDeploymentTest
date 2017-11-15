import sys, os, time

if __name__ == "__main__":
    testFilePath = sys.stdin.readline().strip()
    for line in sys.stdin.readlines():
        n = line.strip()
        if(n.strip() != ""):
            arg = "ID%s: Test message posted using Python script and Selenium." % n
            os.system("%s \"%s\"" % (testFilePath, arg))
            #sleep for 4 seconds
            time.sleep(4)
    
