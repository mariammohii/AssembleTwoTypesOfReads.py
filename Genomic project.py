#---------Function To Read File---------
def readSolution(fileName):
    b=open(fileName).readline().strip()
    return b

def readFiles (fileName):
    b = open(fileName).readlines()
    return b
#---------------------findpath---------------------------
def findstartPath(pairedDict):
    for key in pairedDict.items():
        found=False
        for value in pairedDict.items():
            if(value[1]==key[0]):
                found=True
                break
        if not found:
            start=key[0]
            break
    return start

def findendPath(pairedDict):
    for value in pairedDict.items():
        found=False
        for key in pairedDict.items():
            if(key[0]==value[1]):
                found=True
                break
        if not found:
            end=value[1]
            break
    return end
###############################check solution################################
def testcases(estimatedSequence,actualSequence):
    if estimatedSequence == actualSequence:
        print('Succeeded!! \nThe sequence is ', estimatedSequence)

    else:
        print('Failed!! \nThe actual Sequence is ', actualSequence,
              '\nThe estimated Sequence is ', estimatedSequence)
    return 0

#---------------------------------------------single functions-----------------------------------------------------------------------
def readRegularTextFilesingle(b):
    fline = int(b[0])
    content_list = [line.rstrip() for line in b[1:]]
    return fline, content_list
def getKmers(Contnt,fline):
    dict={}
    for i in (Contnt):
        prefix = i[:fline-1]
        suffix= i[1:]
        dict.setdefault(prefix, suffix)
    return dict

#---------Function concatenatesingle---------
def concatenateSingle(singleDict, start, end):
    path = start
    while(True):
        if(start != end):
            suff=singleDict.get(start)
            path += suff[-1]
            start = suff
        else:
            break
    return path
#---------Function single sequnce---------
def single_read():
    var = "SingleReadInput (2).txt"
    dict={}
    file= readFiles(var)
    firstLine,contentList=readRegularTextFilesingle(file)
    dict=getKmers(contentList,firstLine)
    #print(dict)
    start=findstartPath(dict)
    end=findendPath(dict)
    sequence=concatenateSingle(dict,start,end)
    return sequence
#----------------------------------------------paired functions----------------------------------------------------------------------------
def readRegularTextFilePaired(fileContent):
    firstLineContent = fileContent[0]
    firstLineContent= firstLineContent.split(" ")
    lengthOfReads = int(firstLineContent[0])
    gapValue = int(firstLineContent[1])
    return lengthOfReads,gapValue ,fileContent
#---------Function To getMers---------
def getMers(reads,lengthOfReads):
    length = lengthOfReads - 1
    mers = []
    for read in reads:
        for i in range(len(read) - length + 1):
            mers.append(read[i : length + i])
    return mers

def splitreads(fileContent):
    readsForward = []
    readsBackward = []
    for line in fileContent[1:]:
        lineContent = line.strip()
        lineContent=lineContent.split("|")
        forward=lineContent[0]
        readsForward.append(forward)
        back=lineContent[1]
        readsBackward.append(back)
    return  readsForward, readsBackward

def createPairedDict(forwardMers, backwardMers):
    pairedDict = {}
    length=len(forwardMers)
    for i in range(0, length, 2):
        pref=(forwardMers[i], backwardMers[i])
        suff=(forwardMers[i + 1], backwardMers[i + 1])
        pairedDict.setdefault(pref,suff)
    return pairedDict




#---------Function concatenatePaired---------

def concatenatePaired(start,pairedDict, index):
    seq = start[index]
    length=len(pairedDict)
    for i in range(length):
        suff=pairedDict.get(start)
        if suff != None:
            seq += suff[index][-1]
            start = suff
    return seq




#---------Function To assembly---------
def assembly(prefix, suffix, length, gap):
    cratria=len(suffix) - (length + gap)
    finalseq=prefix + suffix[cratria:]
    return finalseq

#---------Function To pairedReads---------
def pairedReads():
    fileName="ReadPairsInput.txt"

    file=readFiles(fileName)
    lengthOfReads, gapValue,fileContent = readRegularTextFilePaired(file)
    readsForward, readsBackward=splitreads(fileContent)


    forwardMers = getMers(readsForward,lengthOfReads)
    # print('Forward Mers: ', forwardMers)
    backwardMers = getMers(readsBackward,lengthOfReads)
    pairedDict = createPairedDict(forwardMers, backwardMers)
    #print('Graph: ', pairedDict)

    start= findstartPath(pairedDict)
    end = findendPath(pairedDict)
    # print('Start Node: ', start)
    # print('End Node: ', end)

    prefix = concatenatePaired(start,pairedDict, 0)
    suffix = concatenatePaired(start,pairedDict, 1)
    estimatedSequence = assembly(prefix, suffix, lengthOfReads, gapValue)
    return estimatedSequence





#------------main------------------
while(True):
    print("****************************************************welcome**********************************************************")
    print("please choose number for the method")
    print("1/ for single method\n2/ for paried method\n")
    choose = int(input("Enter your value: "))
    if(choose==1):
            solutionName = "SingleReadOutput.txt"
            actual = readSolution(solutionName)
            seq = single_read()
    elif(choose==2):
            solutionName = "ReadPairsOutput.txt"
            actual = readSolution(solutionName)
            seq =pairedReads()

    else:
        continue
    testcases(seq,actual)