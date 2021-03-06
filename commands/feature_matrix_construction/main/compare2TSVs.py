# -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

import miscIO
import tsvIO

import math
import sys


# -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

NA_VALUE = -999999

# -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#


def lookAtHeaderTokens(aTokens):

    patientList = []
    typeDict = {}

    for a in aTokens:
        if (a.upper().startswith("TCGA-")):
            patientID = a[8:12].upper()
            if (patientID not in patientList):
                patientList += [patientID]
            if (len(a) >= 15):
                typeID = a[13:15]
                if (typeID not in typeDict.keys()):
                    typeDict[typeID] = 0
                typeDict[typeID] += 1
            else:
                print " WARNING : no typeID ??? <%s> " % a

    if (len(patientList) > 0):
        print " "
        print " # of unique patients : ", len(patientList)
        print " sample type counts   : ", typeDict
        print " "
        print " "


# -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

def lookAtLine(aLine):

    if (1):
        print len(aLine)

        numTab = 0
        numLF = 0
        numCR = 0
        numSpace = 0
        numDigit = 0
        numLetter = 0

        numLinesOut = 0

        i1 = 0
        for ii in range(len(aLine)):
            ordVal = ord(aLine[ii])
            if (1):
                if (ordVal == 9):
                    # this is a tab ...
                    numTab += 1
                elif (ordVal == 10):
                    numLF += 1
                elif (ordVal == 13):
                    numCR += 1
                elif (ordVal == 32):
                    numSpace += 1
                elif ((ordVal >= 48 and ordVal <= 57) or (ordVal == 46)):
                    numDigit += 1
                elif ((ordVal >= 65 and ordVal <= 90) or (ordVal >= 97 and ordVal <= 122)):
                    numLetter += 1
                elif (ordVal < 32 or ordVal > 126):
                    print " %6d     %3d " % (ii, ordVal)
                else:

                    # print " %6d <%s> %3d " % ( ii, aLine[ii], ord ( aLine[ii]
                    # ) )
                    doNothing = 1
            if (ordVal == 13):
                i2 = ii
                # print " --> writing out from %d to %d " % ( i1, i2 )
                # print " <%s> " % aLine[i1:i2]
                numLinesOut += 1
                ## if ( numLinesOut == 5 ): sys.exit(-1)
                ## fhOut.write ( "%s\n" % aLine[i1:i2] )
                i1 = i2 + 1

        print numTab, numLF, numCR, numSpace, numDigit, numLetter
        print numLinesOut

    sys.exit(-1)

# -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#


def findIndex(rowLabels, aLabel):

    ## print " in findIndex ... ", aLabel
    ## print rowLabels[:5]

    if ( aLabel[1]==':' and aLabel[6]==':' ):
        if ( aLabel[2:6].lower()=="clin"  or  aLabel[2:6].lower()=="samp" ):
            aLabel2 = aLabel[6:].lower()
        else:
            aLabel2 = aLabel.lower()
    else:
        aLabel2 = aLabel.lower()

    for ii in range(len(rowLabels)):

        rLabel = rowLabels[ii]
        if ( rLabel[1]==':' and rLabel[6]==':' ):
            if ( rLabel[2:6].lower()=="clin"  or  rLabel[2:6].lower()=="samp" ):
                rLabel2 = rLabel[6:].lower()
            else:
                rLabel2 = rLabel.lower()
        else:
            rLabel2 = rLabel.lower()

        ## print "         comparing <%s> and <%s> " % ( rLabel2, aLabel2 )
        if ( rLabel2 == aLabel2 ):
            return (ii)

    if (0):
        print " ??? not found ??? ", aLabel
        print rowLabels[:5]
        print rowLabels[-5:]
    return (-1)

# -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

def chopOneFeat ( aLabel, labelTokens ):

    aType = labelTokens[1].lower()

    if ( aType == "gexp" ):
        return ( labelTokens[0] + ":" + labelTokens[1] + ":" + labelTokens[2] + ":::::" + labelTokens[7] )

    if ( aType == "gnab" ):
        return ( labelTokens[0] + ":" + labelTokens[1] + ":" + labelTokens[2] + ":::::" + labelTokens[7] )

    if ( aType == "mirn" ):
        return ( labelTokens[0] + ":" + labelTokens[1] + ":" + labelTokens[2] + ":::::" + labelTokens[7] )

    if ( aType == "cnvr" ):
        return ( labelTokens[0] + ":" + labelTokens[1] + "::" + labelTokens[3] + ":" \
               + labelTokens[4] + ":" + labelTokens[5] + "::" + labelTokens[7] )

    if ( aType == "meth" ):
        try:
            splitLast = labelTokens[7].split('_')
        except:
            splitLast = [ '' ]
        return ( labelTokens[0] + ":" + labelTokens[1] + "::::::" + splitLast[0] )

    if ( aType == "rppa" ):
        return ( labelTokens[0] + ":" + labelTokens[1] + "::::::" + labelTokens[7] )

    if ( aType == "clin" ):
        return ( labelTokens[0] + "::" + labelTokens[2] + ":::::" + labelTokens[7] )

    if ( aType == "samp" ):
        return ( labelTokens[0] + "::" + labelTokens[2] + ":::::" + labelTokens[7] )

    print " in chopOneFeat ... ", aLabel
    print labelTokens
    sys.exit(-1)

# -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

if __name__ == "__main__":

    if (len(sys.argv) != 3):
        print ' Usage : %s <input TSV #1> <input TSV #2> ' % sys.argv[0]
        sys.exit(-1)

    inFileA = sys.argv[1]
    inFileB = sys.argv[2]

    try:
        fhA = file(inFileA, 'r')
        fhA.close()
        fhB = file(inFileB, 'r')
        fhB.close()
    except:
        print " one or the other file does not exist ??? "
        print inFileA
        print inFileB
        sys.exit(-1)

    print " "
    print " reading input files ... : "
    print "     file A : ", inFileA
    print "     file B : ", inFileB
    print " "

    dataA = tsvIO.readTSV(inFileA)
    dataB = tsvIO.readTSV(inFileB)

    if (len(dataA) == 0):
        print " input file A does not exist ??? "
        print inFileA
        sys.exit(-1)

    if (len(dataB) == 0):
        print inFileB
        print " input file B does not exist ??? "
        sys.exit(-1)

    # new approach to comparing feature names ... chop out certain
    # non-critical portions of the feature to allow for less
    # stringent matching ...
    chopFeat = 1

    # first take a look at the feature (row) labels ...

    rowLabelsA = []
    for aLabel in dataA['rowLabels']:
        aLabel = aLabel.lower()
        aTokens = aLabel.split(':')
        if ( len(aTokens) > 3 ):
            if ( chopFeat ):
                rowLabelsA += [ chopOneFeat ( aLabel, aTokens ) ]
            else:
                if ( aTokens[1]=="clin"  or  aTokens[1]=="samp" ):
                    rowLabelsA += [ aLabel[6:] ]
                else:
                    rowLabelsA += [ aLabel ]
        else:
            rowLabelsA += [ aLabel ]
    rowLabelsA.sort()

    rowLabelsB = []
    for bLabel in dataB['rowLabels']:
        bLabel = bLabel.lower()
        bTokens = bLabel.split(':')
        if ( len(bTokens) > 3 ):
            if ( chopFeat ):
                rowLabelsB += [ chopOneFeat ( bLabel, bTokens ) ]
            else:
                if ( bTokens[1]=="clin"  or  bTokens[1]=="samp" ):
                    rowLabelsB += [ bLabel[6:] ]
                else:
                    rowLabelsB += [ bLabel ]
        else:
            rowLabelsB += [ bLabel ]
    rowLabelsB.sort()

    ## print len(rowLabelsA), len(rowLabelsB)
    ## print rowLabelsA[:5], rowLabelsA[-5:]
    ## print rowLabelsB[:5], rowLabelsB[-5:]

    numAinB = 0
    featLabelsAnotB = []
    for aLabel in rowLabelsA:
        if (aLabel in rowLabelsB):
            numAinB += 1
        else:
            featLabelsAnotB += [aLabel]

    numBinA = 0
    featLabelsBnotA = []
    for aLabel in rowLabelsB:
        if (aLabel in rowLabelsA):
            numBinA += 1
        else:
            featLabelsBnotA += [aLabel]

    print " "
    print "     --> total # of features in each : %6d  %6d " % (len(rowLabelsA), len(rowLabelsB))
    print "         overlap counts              : %6d  %6d " % (numAinB, numBinA)

    featLabelsAnotB.sort()
    featLabelsBnotA.sort()

    ## print len(featLabelsAnotB), featLabelsAnotB[:5]
    ## print len(featLabelsBnotA), featLabelsBnotA[:5]

    print " "
    if (len(featLabelsAnotB) > 0):
        print " %d labels in A but not in B (string names have been arbitrarily forced to lower-case) : " % (len(featLabelsAnotB))
        for aLabel in featLabelsAnotB:
            print "     feat in A not B: ", aLabel
    else:
        print " NO labels in A but not in B (string names have been arbitrarily forced to lower-case) : "

    print " "
    if (len(featLabelsBnotA) > 0):
        print " %d labels in B but not in A (string names have been arbitrarily forced to lower-case) : " % (len(featLabelsBnotA))
        for aLabel in featLabelsBnotA:
            print "     feat in B not A: ", aLabel
    else:
        print " NO labels in B but not in A (string names have been arbitrarily forced to lower-case) : "

    # and next at the column (sample) labels ...

    # first check the sample ID lengths ...
    colLabelA_len = len(dataA['colLabels'][0])
    colLabelB_len = len(dataB['colLabels'][0])
    minLen = min(colLabelA_len, colLabelB_len)
    if (minLen < colLabelA_len):
        print " NOTE: sample IDs in A will be abbreviated ... eg from <%s> to <%s> " \
            % (dataA['colLabels'][0], dataA['colLabels'][0][:minLen])
    if (minLen < colLabelB_len):
        print " NOTE: sample IDs in B will be abbreviated ... eg from <%s> to <%s> " \
            % (dataB['colLabels'][0], dataB['colLabels'][0][:minLen])

    colLabelsA = []
    for aLabel in dataA['colLabels']:
        colLabelsA += [aLabel[:minLen].upper()]
    colLabelsB = []
    for aLabel in dataB['colLabels']:
        colLabelsB += [aLabel[:minLen].upper()]

    numAinB = 0
    samplesAnotB = []
    for aLabel in colLabelsA:
        if (aLabel in colLabelsB):
            numAinB += 1
        else:
            samplesAnotB += [aLabel]

    numBinA = 0
    samplesBnotA = []
    for aLabel in colLabelsB:
        if (aLabel in colLabelsA):
            numBinA += 1
        else:
            samplesBnotA += [aLabel]

    print " "
    print "     --> total # of samples in each  : %6d  %6d " % (len(colLabelsA), len(colLabelsB))
    print "         overlap counts              : %6d  %6d " % (numAinB, numBinA)

    samplesAnotB.sort()
    samplesBnotA.sort()

    print " "
    if (len(samplesAnotB) > 0):
        print " %d samples in A but not in B (string names have been arbitrarily forced to upper-case) : " % (len(samplesAnotB))
        for aLabel in samplesAnotB:
            print aLabel
    else:
        print " NO samples in A but not in B (string names have been arbitrarily forced to upper-case) : "

    print " "
    if (len(samplesBnotA) > 0):
        print " %d samples in B but not in A (string names have been arbitrarily forced to upper-case) : " % (len(samplesBnotA))
        for aLabel in samplesBnotA:
            print aLabel
    else:
        print " NO samples in B but not in A (string names have been arbitrarily forced to upper-case) : "

    # now, for the features that exist in both, compare the *data* values ...
    print " "
    print " "
    print " "
    print " now checking data values, feature by feature ... "
    print " (based on features in A that are also in B) "


    ## print rowLabelsA[:5]
    ## print featLabelsAnotB[:5]

    for aLabel in rowLabelsA:

        # skip this feature if it is in the A-not-B list ...
        if (aLabel in featLabelsAnotB):
            continue

        # skip binary indicator features since they are generated automatically
        # ...
        if (aLabel[6:9] == ":i("):
            continue

        # get the feature index for each matrix ...
        iA = findIndex(dataA['rowLabels'], aLabel)
        iB = findIndex(dataB['rowLabels'], aLabel)
        ## print " (a) ", aLabel, iA, iB

        # grab the data vector from each matrix ...
        dataVecA = dataA['dataMatrix'][iA]
        dataVecB = dataB['dataMatrix'][iB]
        # print dataVecA, dataVecB

        numDiff = 0
        numNotNA = 0

        sumDiff = 0.
        sumDiff2 = 0.
        sumN = 0

        # now loop over the individual data values for this feature
        ## print " looping jA over %d " % len(dataVecA)
        for jA in range(len(dataVecA)):
            sampleA = dataA['colLabels'][jA]
            ## print jA, sampleA, dataVecA[jA]

            if (str(dataVecA[jA]) == "NA" or str(dataVecA[jA]) == "-999999"):
                ## print " (NA) "
                continue

            else:
                numNotNA += 1

                jB = findIndex(dataB['colLabels'], sampleA)
                if (jB < 0):
                    ## print " sample <%s> not found in matrix B " % sampleA
                    if (str(dataVecA[jA]) == "NA"):
                        doNothing = 1
                    elif (str(dataVecA[jA]) == "-999999"):
                        doNothing = 1
                    else:
                        numDiff += 1
                else:
                    ## print jA, jB
                    ## print dataVecA[jA], dataVecB[jB]

                    if (str(dataVecB[jB]) == "NA" or str(dataVecB[jB]) == "-999999"):
                        doNothing = 1

                    elif (str(dataVecA[jA]).lower() != str(dataVecB[jB]).lower()):
                        # print " values are different for sample <%s> : <%s>
                        # vs <%s> " % ( sampleA, str(dataVecA[jA]),
                        # str(dataVecB[jB]) )
                        numDiff += 1
                        try:
                            diffVal = float (dataVecA[jA] ) - \
                                float(dataVecB[jB])
                            if (abs(diffVal) > 99999):
                                print " ERROR ??? using NA value ??? !!! ", jA, dataVecA[jA], jB, dataVecB[jB]
                            sumDiff += diffVal
                            sumDiff2 += (diffVal * diffVal)
                            sumN += 1
                        except:
                            doNothing = 1

        if (numDiff == 0):
            print " all %4d non-NA values are the same <%s> (%d) " % (numNotNA, aLabel, len(dataVecA))
        else:
            if (sumN > 3):
                meanDiff = float(sumDiff) / float(sumN)
                meanDiff2 = float(sumDiff2) / float(sumN)
                sigmDiff = math.sqrt(
                    max((meanDiff2 - (meanDiff * meanDiff)), 0.))
                if (abs(meanDiff) > 0.02 or sigmDiff > 0.02):
                    print " %4d out of %4d non-NA values are different <%s> (%d) [%d,%.2f,%.2f] " % \
                        (numDiff, numNotNA, aLabel,
                         len(dataVecA), sumN, meanDiff, sigmDiff)
                else:
                    print " %4d out of %4d non-NA values are different <%s> (%d) -- but not significantly [%d,%.2f,%.2f] " % \
                        (numDiff, numNotNA, aLabel,
                         len(dataVecA), sumN, meanDiff, sigmDiff)
            else:
                print " %4d out of %4d non-NA values are different <%s> (%d) " % (numDiff, numNotNA, aLabel, len(dataVecA))


    print " "
    print " FINISHED "
    print " "

# -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
