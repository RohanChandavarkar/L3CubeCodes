#! /usr/bin/python

import os
import sys
import stat
import md5 

GroupFilesBySize = {}

def gothrough(argument, dirname, files):
    d = os.getcwd() #THE CURRENT WORKING DIRECTORY IS STORED IN dir
    os.chdir(dirname) #CHANGE THE DIRECTORY TO THE ONE SPECIFIED AS PARAMETERS
    try:
        files.remove('Thumbs') #THIS WILL REMOVE ALL THUMB TYPE FILES (TEMPORARY FILES NOT CONSIDERED)
    except ValueError:
        pass
    for f in files:
        if not os.path.isfile(f):
            continue #IF NOT A FILE THAT MEANS IF ITS A DIRECTORY THE GO BACK TO FOR LOOP
        filesize = os.stat(f)[stat.ST_SIZE] #GET THE FILE SIZE
        if filesize < 100:
            continue #IGNORE FILES LESS THAN 100 BYTES IN SIZE
        if filesize in GroupFilesBySize:
            temparray = GroupFilesBySize[filesize]
        else:
            temparray = []
            GroupFilesBySize[filesize] = temparray
        temparray.append(os.path.join(dirname,f))
        '''
        THE CODE FROM LINES 23 TO 28 WILL CREATE AN ARRAY LIKE
        {SIZE IN BYTES(KEY):[LIST OF FILES HAVING THAT SIZE](VALUE)}
        THAT IS KEY-VALUE PAIR
        FOR EXAMPLE - 
        {150:["/home/user/folder1/hello.txt","/home/user/folder2/hello.txt"] & SO ON....}
        '''
    os.chdir(d) #CHANGE BACK TO THE CURRENT WORKING DIRECTORY STORED IN dir

for var in sys.argv[1:]:
    #SCAN THROUGH ALL FILES & SUB FOLDERS IN THE GIVE DIRECTORY SPECIFIED BY sys.argv[1]
    print 'SCANNING THE DIRECTORY "%s".....' % var
    os.path.walk(var,gothrough,GroupFilesBySize)

#THUS TILL HERE WE HAVE CLASSIFIED FILES BASED ON THEIR SIZE
#THAT MEANS ALL FILES HAVING SAME SIZE WILL BE GROUPED TOGETHER

#NOW WE WILL FIND POTENTIAL DUPLICATES BY HASHING JUST FIRST 1024 BYTES OF EACH FILE
#FILES HAVING SIMILAR HASH VALUE WILL BE GROUPED TOGETHER

print 'FINDING POTENTIAL DUPLICATES.......'
possibleDuplicates = []
possibleDuplicatesCount = 0
trueType = type(True) #BOOLEAN VARIABLE HAVING VALUE TRUE
SizeArr = GroupFilesBySize.keys() #ALL THE KEYS (i.e.) FILE SIZE VALUES ARE NOW STORED IN SizeArr
SizeArr.sort() #SIZES ARE SORTED IN ASCENDING ORDER

for k in SizeArr:
    InputFiles = GroupFilesBySize[k] #FILES HAVING SIMILAR SIZE WILL BE STORED IN InputFiles
    OutputFiles = [] #FILES HAVING SIMILAR HASH VALUES FOR FIRST 1024 BYTES WILL BE STORED IN OutputFiles
    HashValues = {}
    if len(InputFiles) is 1:
        continue #IGNORE IF ONLY 1 FILE FOUND HAVING PARTICULAR SIZE (i.e.) NO DUPLICATES FOUND
    print 'TESTING %d FILES OF SIZE %d BYTES ....' % (len(InputFiles),k)
    for subfiles in InputFiles:
        if not os.path.isfile(subfiles):
            continue #IF NOT A FILE THAT MEANS IF ITS A DIRECTORY THE GO BACK TO FOR LOOP
        fileHandle = file(subfiles,'r')
        HashObject = md5.new(fileHandle.read(1024)) #PERFORM HASHING USING MD5 FOR FIRST 1024 BYTES FOR THE FILES
        HashOpValue = HashObject.digest() #ALL HASHING VALUES OBTAINED ARE NOW STORED IN ARRAY
        if HashOpValue in HashValues:
            temparray1 = HashValues[HashOpValue]
            if type(temparray1) is not trueType:
                OutputFiles.append(HashValues[HashOpValue])
                HashValues[HashOpValue] = True
            OutputFiles.append(subfiles)
        else:
            HashValues[HashOpValue] = subfiles
        fileHandle.close()
    '''
    THIS WILL CREATE AN ARRAY NAMED OutputFiles THAT WILL STORE THE HASH VALUES AND CORRESPONDING FILES
    IT WILL LOOK LIKE
    {HASH VALUE(KEY):[LIST OF FILES HAVING SAME HASH VALUE FOR FIRST 1024 BYTES](VALUES)}
    '''
    if len(OutputFiles):
        possibleDuplicates.append(OutputFiles)
        possibleDuplicatesCount = possibleDuplicatesCount + len(OutputFiles)

del GroupFilesBySize

print 'FOUND %d SETS OF POTENTIAL DUPLICATE FILES' % possibleDuplicatesCount
print 'SCANNING FOR REAL DUPLICATES'

'''
NOW WE PERFORM THE FINAL PART
HERE WE WILL HASH THE ENTIRE FILE
AFTER THIS THE FINAL SET OF DUPLICATE FILES WILL BE DETERMINED
NOTE THAT FOR THIS WE MAKE USE OF POTENTIAL DUPLICATES
'''

realDuplicates = []
for subset in possibleDuplicates:
    RealOutputFiles = []
    TotalHashValue = {}
    for fileName in subset:
        print 'SCANNING FILE "%s" .....' % fileName
        RealFileHandle = file(fileName,'r')
        TotalHashObject = md5.new()
        while True:
            r = RealFileHandle.read(4096)
            if not len(r):
                break
            TotalHashObject.update(r)
        RealFileHandle.close()
        '''
        IN LINES 105 TO 112 WE PERFORM HASHING ON ENTIRE FILE
        WE DO THIS BY FIRST OPENING A FILE USING FILE fileHandle
        THEN WE HASH THE FIRST BLOCK OF 4096 BYTES FOR THE FILE
        AFTER THIS WE KEEP HASHING THE FOLLOWING BLOCKS OF 4096 BYTES AND SIMULTANEOUSLY UPDATE THE HASH VALUE OF THE FILE
        '''
        TotalHashOpValue = TotalHashObject.digest()
        if TotalHashValue.has_key(TotalHashOpValue):
            if not len(RealOutputFiles):
                RealOutputFiles.append(TotalHashValue[TotalHashOpValue])
            RealOutputFiles.append(fileName)
        else:
            TotalHashValue[TotalHashOpValue] = fileName
    if len(RealOutputFiles):
        realDuplicates.append(RealOutputFiles)

'''
NOW WE HAVE OBTAINED FINAL ARRAY THAT HAS THE SET OF ACTUAL DUPLICATE FILES
IT WILL LOOK LIKE THIS
{HASH VALUE(KEY):[LIST OF FILES HAVING SAME HASH VALUE FOR ENTIRE CONTENTS](VALUE)}
'''

'''
NOW WE DELETE THE DUPLICATE FILES
WE HAVE AN ARRAY THAT CONTAINS LIST OF DUPLICATE FILES 
SO WE SELECT THE FIRST ONE AS ORIGINAL AND THEN THE REMAINING ONES ARE CONSIDERED AS DUPLICATES
THESE DUPLICATES ARE THEN REMOVED
'''

i = 0
for d in realDuplicates:
    print 'ORIGINAL FILE IS %s' % d[0]
    for f in d[1:]:
        i = i + 1
        print 'DUPLICATE FILE IS %s' % f
        print 'DELETING DUPLICATE FILE'
        os.remove(f)
        print 'DUPLICATE FILE DELETED SUCCESSFULLY'
    print


            