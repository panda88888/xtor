from sys import argv
from os.path import exists
from os.path import isfile
from Crypto.Cipher import AES

script, srcFileName = argv

chunkSize = 64 * 1024 #64kB chunk size
key = '0123456789ABCDEF'
iv = 'This is an IV456'
cipher = AES.new(key, AES.MODE_CBC, iv)

# Check if input file exists
if not exists(srcFileName):
    print "Cannot find input file: %r" % srcFileName
    quit()

# Check if input file is a file
if not isfile(srcFileName):
    print "Input file %r is not a file." % srcFileName
    quit()  # input file does not exist or is not a file

# Check if we are starting from segment 000
if srcFileName[-4:] != ".000":
    print "Not starting at file segment 000.  File extension must be '.000'"
    quit()

outFileName = srcFileName[:-4]  # Remove ".000" from the end
outFile = open(outFileName, 'wb')
outFile.seek(0)
currChunk = 0

while exists(srcFileName):
    srcFile = open(srcFileName, 'rb')
    srcData = srcFile.read()
    srcFile.close
    plaintextData = cipher.decrypt(srcData)
    outFile.write(plaintextData)
    currChunk += 1
    srcFileName = "%s.%03d" % (outFileName, currChunk)

outFile.close()