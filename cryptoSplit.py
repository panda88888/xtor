# Need to add logic to pad all segments to same size

from sys import argv
from sys import getsizeof
from os.path import exists
from os.path import isfile
from os.path import getsize
from Crypto.Cipher import AES

script, inFileName = argv

chunkSize = 64 * 1024 #64kB chunk size
print "Chunck size is %d" % chunkSize
key = '0123456789ABCDEF'
iv = 'This is an IV456'
cipher = AES.new(key, AES.MODE_CBC, iv)

# Check if input file exists
if not exists(inFileName):
    print "ERROR: Cannot find input file: %r" % inFileName
    quit()

# Check if input file is a file
if not isfile(inFileName):
    print "ERROR: Input file %r is not a file." % inFileName
    quit()  # input file does not exist or is not a file

numChunks = getsize(inFileName) / chunkSize + 1

inFile = open(inFileName, 'rb')

for n in range(0, numChunks):
    outFileName = "%s.%03d" % (inFileName, n)
    if exists(outFileName):
        print "ERROR: output file %r already exists." % outFileName
        quit()
    print "Writing file: %r" % outFileName
    outPlainData = inFile.read(chunkSize)
    
    # Pad the chunk to 64kB if not correct chunk size
    if len(outPlainData) < chunkSize:
        outPlainData += '\0' * (chunkSize - len(outPlainData))
    outCipherData = cipher.encrypt(outPlainData)
    outFile = open(outFileName, 'wb')
    outFile.write(outCipherData)
    outFile.close()

inFile.close()