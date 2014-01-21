# -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

# these are system modules
import numpy
import sys

# these are my local ones
import tsvIO

# -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

NA_VALUE = -999999

# -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#


def cleanUpName(aName):

    bName = ''

    aName = aName.upper()

    ## ii = aName.find(" - Homo sapiens (human)")
    ii = aName.find(" - HOMO SAPIENS (HUMAN)")
    if (ii >= 0):
        aName = aName[:ii]
    aName = aName.strip()

    ii = aName.find("(")
    while (ii >= 0):
        jj = aName.find(")", ii)
        aName = aName[:ii] + aName[jj + 1:]
        ii = aName.find("(")
    aName = aName.strip()

    ii = aName.find("<")
    while (ii >= 0):
        jj = aName.find(">", ii)
        aName = aName[:ii] + aName[jj + 1:]
        ii = aName.find("<")
    aName = aName.strip()

    for ii in range(len(aName)):
        if (aName[ii] == ','):
            continue
        elif (aName[ii] == '('):
            bName += '_'
        elif (aName[ii] == ')'):
            bName += '_'
        elif (aName[ii] == '-'):
            bName += '_'
        elif (aName[ii] == '/'):
            bName += '_'
        elif (aName[ii] == ';'):
            bName += '_'
        elif (aName[ii] == '&'):
            continue
        elif (aName[ii] == '#'):
            continue
        elif (aName[ii] == ' '):
            bName += '_'
        else:
            bName += aName[ii].upper()

    ii = bName.find("__")
    while (ii >= 0):
        print "             ", ii, bName
        bName = bName[:ii] + bName[ii + 1:]
        print "             ", bName
        ii = bName.find("__")

    return (bName)

# -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#


def readPathways():

    ## fh = file ( "/users/sreynold/scratch/CPDB_pathways_genes.tab", 'r' )
    ## fh = file ( "/users/sreynold/scratch/CPDB_plus.tab", 'r' )
    ## fh = file ( "/proj/ilyalab/sreynold/TCGA/pathways/only_biocarta.tab", 'r' )
    ## fh = file ( "/proj/ilyalab/sreynold/TCGA/pathways/only_NCI_Nature.tab", 'r' )
    fh = file(
        "/proj/ilyalab/sreynold/TCGA/pathways/only_NCI_Nature_ver4.tab", 'r')

    pwDict = {}

    for aLine in fh:
        aLine = aLine.strip()
        aLine = aLine.upper()
        tokenList = aLine.split('\t')
        if (len(tokenList) != 3):
            continue
        if (tokenList[0] == "pathway"):
            continue

        longPathwayName = tokenList[0]
        shortPathwayName = tokenList[1]

        geneTokens = tokenList[2].strip()
        geneList = geneTokens.split(',')
        geneList.sort()

        if (len(geneList) > 0):
            while (geneList[0] == ''):
                geneList = geneList[1:]
                if (len(geneList) == 0):
                    continue

        if (len(geneList) == 0):
            continue

        pathwayName = cleanUpName(shortPathwayName)

        if (pathwayName not in pwDict.keys()):
            # print " adding pathway %s (%d) " % ( pathwayName, len(geneList) )
            pwDict[pathwayName] = geneList
        else:
            if (len(pwDict[pathwayName]) < len(geneList)):
                # print " substituting shorter list of genes for %s (%d) " % (
                # pathwayName, len(geneList) )
                pwDict[pathwayName] = geneList
            # else:
                # print " NOT substituing list for %s " % pathwayName

    fh.close()

    print " "
    print " have pathway dictionary with %d pathways " % len(pwDict)
    print "     --> now looking for duplicate pathways ... "
    pwList = pwDict.keys()
    pwList.sort()
    delList = []
    pairDict = {}

    for ii in range(len(pwList) - 1):
        iiName = pwList[ii]
        iiLen = len(pwDict[iiName])
        for jj in range(ii + 1, len(pwList)):
            jjName = pwList[jj]
            jjLen = len(pwDict[jjName])
            if (jjLen != iiLen):
                continue

            if (pwDict[iiName] == pwDict[jjName]):
                print "\n\n SAME !!! "
                print iiName, iiLen
                print pwDict[iiName]
                print jjName, jjLen
                print pwDict[jjName]

                iiSplit = iiName.split('__')
                jjSplit = jjName.split('__')

                if (iiSplit[1] <= jjSplit[1]):
                    pairNames = (iiSplit[1], jjSplit[1])
                else:
                    pairNames = (jjSplit[1], iiSplit[1])
                if (pairNames in pairDict.keys()):
                    pairDict[pairNames] += 1
                else:
                    pairDict[pairNames] = 1

                if (iiSplit[1] == jjSplit[1]):
                    if (len(iiName) <= len(jjName)):
                        delList += [jjName]
                    else:
                        delList += [iiName]

                else:

                    if (iiSplit[1] == "NCI-NATURE"):
                        delList += [jjName]
                    elif (jjSplit[1] == "NCI-NATURE"):
                        delList += [iiName]

                    elif (iiSplit[1] == "PID"):
                        delList += [jjName]
                    elif (jjSplit[1] == "PID"):
                        delList += [iiName]

                    elif (iiSplit[1] == "KEGG"):
                        delList += [jjName]
                    elif (jjSplit[1] == "KEGG"):
                        delList += [iiName]

                    elif (iiSplit[1] == "PWCOMMONS"):
                        delList += [jjName]
                    elif (jjSplit[1] == "PWCOMMONS"):
                        delList += [iiName]

                    elif (iiSplit[1] == "REACTOME"):
                        delList += [jjName]
                    elif (jjSplit[1] == "REACTOME"):
                        delList += [iiName]

                    elif (iiSplit[1] == "WIKIPATHWAYS"):
                        delList += [jjName]
                    elif (jjSplit[1] == "WIKIPATHWAYS"):
                        delList += [iiName]

                    elif (iiSplit[1] == "WIKIPW"):
                        delList += [jjName]
                    elif (jjSplit[1] == "WIKIPW"):
                        delList += [iiName]

                    elif (iiSplit[1] == "SMPDB"):
                        delList += [jjName]
                    elif (jjSplit[1] == "SMPDB"):
                        delList += [iiName]

                    elif (iiSplit[1] == "HUMANCYC"):
                        delList += [jjName]
                    elif (jjSplit[1] == "HUMANCYC"):
                        delList += [iiName]

                    else:
                        sys.exit(-1)

    for aName in delList:
        try:
            del pwDict[aName]
        except:
            doNothing = 1

    print " "
    print " returning pathway dictionary with %d pathways " % len(pwDict)
    print " "
    for aKey in pairDict.keys():
        print aKey, pairDict[aKey]
    print " "
    print " "

    return (pwDict)

# -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#


def setFeatBits(rowLabels, featPrefix, doesContain, notContain):

    numSet = 0

    numRow = len(rowLabels)
    bitVec = numpy.zeros(numRow, dtype=numpy.bool)
    for iR in range(numRow):
        if (featPrefix != ""):
            if (not rowLabels[iR].startswith(featPrefix)):
                continue
        if (doesContain != ""):
            if (rowLabels[iR].find(doesContain) < 0):
                continue
        if (notContain != ""):
            if (rowLabels[iR].find(notContain) >= 0):
                continue
        bitVec[iR] = 1
        numSet += 1

    print featPrefix, doesContain, notContain, numRow, numSet
    if (numSet == 0):
        print " numSet=0 ... this is probably a problem ... "
        # sys.exit(-1)

    return (bitVec)

# -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
# B:GNAB:ADAM7:chr8:24298509:24384483:+:y_n_somatic y_n y_del
# --> B:GNAB:ADAM7:chr8:24298509:24384483:+:y_del_somatic


def makeNewFeatureName(curFeatName, oldString, newString):

    i1 = curFeatName.find(oldString)
    if (i1 < 0 or len(oldString) < 2):
        print " ERROR in makeNewFeatureName ???? ", curFeatName, oldString, newString

    i2 = i1 + len(oldString)
    newFeatName = curFeatName[:i1] + newString + curFeatName[i2:]
    # print curFeatName, oldString, newString, newFeatName

    return (newFeatName)

# -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#


def chooseCountThreshold(dataD):

    rowLabels = dataD['rowLabels']
    dMat = dataD['dataMatrix']

    numBits = 0
    for ii in range(len(rowLabels)):
        if (numBits > 0):
            continue
        if (rowLabels[ii].find("B:GNAB:TP53:") >= 0):
            for jj in range(len(dMat[ii])):
                if (dMat[ii][jj] == 0):
                    numBits += 1
                elif (dMat[ii][jj] == 1):
                    numBits += 1

    print " number of bits found for TP53 mutation feature: ", numBits
    countThreshold = int(numBits / 11) - 1
    return (countThreshold)

# -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#


def pathwayGnab(dataD, pathways={}):

    print " "
    print " ************************************************************* "
    print " ************************************************************* "
    print " "
    print " in pathwayGnab ... "

    # check that the input feature matrix looks ok ...
    try:
        numRow = len(dataD['rowLabels'])
        numCol = len(dataD['colLabels'])
        rowLabels = dataD['rowLabels']
        print " %d rows x %d columns " % (numRow, numCol)
        # print rowLabels[:5]
        # print rowLabels[-5:]
    except:
        print " ERROR in pathwayGnab ??? bad data ??? "
        return (dataD)

    if (len(pathways) == 0):
        pathways = {}

        pathways[
            "TP53_pathway"] = ["E2F1", "TP53", "RB1", "CDK4", "TIMP3", "CDK2", "ATM",
                               "CCNE1", "CCND1", "CDKN1A", "BCL2", "BAX", "PCNA", "MDM2",
                               "APAF1", "GADD45A"]

        pathways[
            "PI3K_AKT_pathway"] = ["FRAP1", "LST8", "PDPK1", "NGF", "NR4A1", "FOXO1", "CHUK",
                                   "THEM4", "PTEN", "CREB1", "BAD", "RHOA", "TRIB3", "PHLPP",
                                   "CASP9", "AKT1S1", "MDM2", "RPS6KB2"]

        pathways[
            "Wnt_pathway"] = ["PPP2R5B", "PPP2R5A", "PPP2R5D", "BTRC", "WNT3A",
                              "PPP2R5C", "MMP7", "PRKX", "CTNNB1", "WNT2", "CSNK2A2", "MAP3K7", "PRKACG",
                              "WNT1", "WNT4", "WNT3", "CSNK2A1", "PRKACA", "PRKACB", "WNT6", "CUL1",
                              "WNT10A", "WNT10B", "VANGL1", "ROCK1", "ROCK2", "VANGL2", "CHP2", "SKP1",
                              "EP300", "JUN", "MAPK9", "PPP2R5E", "MAPK8", "LOC728622", "WNT5A", "WNT5B",
                              "CXXC4", "DAAM1", "DAAM2", "RBX1", "RAC2", "RAC3", "RAC1", "CACYBP",
                              "AXIN2", "AXIN1", "DVL2", "DVL3", "TCF7", "CREBBP", "SMAD4", "SMAD3",
                              "SMAD2", "PORCN", "DVL1", "SFRP5", "SFRP1", "PRICKLE1", "SFRP2", "SFRP4",
                              "PRICKLE2", "WIF1", "PPARD", "PLCB3", "PLCB4", "FRAT1", "RHOA", "FRAT2",
                              "SOX17", "PLCB1", "FOSL1", "MYC", "PLCB2", "PPP2R1B", "PRKCA", "PPP2R1A",
                              "TBL1XR1", "CTBP1", "CTBP2", "TP53", "LEF1", "PRKCG", "PRKCB", "CTNNBIP1",
                              "SENP2", "CCND1", "PSEN1", "CCND3", "CCND2", "WNT9B", "WNT11", "SIAH1",
                              "RUVBL1", "WNT9A", "CER1", "NKD1", "WNT16", "NKD2", "APC2", "CAMK2G",
                              "PPP3R1", "PPP3R2", "TCF7L2", "TCF7L1", "CHD8", "PPP2CA", "PPP2CB",
                              "PPP3CB", "NFAT5", "CAMK2D", "PPP3CC", "NFATC4", "CAMK2B", "CHP",
                              "PPP3CA", "NFATC2", "NFATC3", "FBXW11", "CAMK2A", "WNT8A", "WNT8B",
                              "APC", "NFATC1", "CSNK1A1", "FZD9", "FZD8", "NLK", "FZD1", "CSNK2B",
                              "CSNK1A1L", "FZD3", "FZD2", "MAPK10", "FZD5", "FZD4", "FZD7", "DKK4",
                              "WNT2B", "FZD6", "DKK2", "FZD10", "WNT7B", "DKK1", "CSNK1E", "GSK3B",
                              "LRP6", "TBL1X", "WNT7A", "LRP5", "TBL1Y"]

    print " "
    print " total number of pathways : ", len(pathways)
    print " "

    mutationTypes = [":y_n_somatic", ":nonsilent_somatic",
                     ":y_del_somatic", ":y_amp_somatic"]
    numTypes = len(mutationTypes)

    pathwayList = pathways.keys()
    pathwayList.sort()
    numPW = len(pathways)
    newNameVec = [0] * (numPW * numTypes)
    newDataMat = [0] * (numPW * numTypes)

    dMat = dataD['dataMatrix']

    min_numON = chooseCountThreshold(dataD)
    if (min_numON < (numCol / 100)):
        min_numON = int(numCol / 100)
    print " minimum count threshold : ", min_numON

    kFeat = 0
    max_numON = 0
    max_fracON = 0.
    for aPathway in pathwayList:

        for aMutType in mutationTypes:

            numON = 0
            newFeatName = "B:GNAB:" + aPathway + "::::" + aMutType

            # first make sure we don't already have a feature with this name
            # ...
            stopNow = 0
            for iRow in range(numRow):
                if (newFeatName == rowLabels[iRow]):
                    stopNow = 1
            if (stopNow):
                continue

            print " tentative new feature #%d ... <%s> " % (kFeat, newFeatName)
            newNameVec[kFeat] = newFeatName
            newDataMat[kFeat] = numpy.zeros(numCol)

            if (0):
                print " "
                print " "
                print aPathway, newFeatName
                print len(pathways[aPathway]), pathways[aPathway]

            for iR in range(numRow):

                # if ( iR%1000 == 0 ): print iR, numRow

                if (1):
                    gnabLabel = rowLabels[iR]
                    if (not gnabLabel.startswith("B:GNAB:")):
                        continue
                    if (gnabLabel.find(aMutType) < 0):
                        continue

                    try:
                        gnabTokens = gnabLabel.split(':')
                        gnabGene = gnabTokens[2].upper()
                    except:
                        print " FAILED to parse GNAB feature name ??? ", gnabLabel
                        continue

                    if (gnabGene in pathways[aPathway]):
                        for iCol in range(numCol):
                            if (dMat[iR][iCol] == 1):
                                if (newDataMat[kFeat][iCol] != 1):
                                    numON += 1
                                print " %d getting mutation bit from gene %s, column %d " % (newDataMat[kFeat][iCol], gnabGene, iCol)
                                newDataMat[kFeat][iCol] = 1

            if (numON > min_numON):
                kFeat += 1
                print " --> keeping this feature ... ", kFeat, newFeatName, numON, min_numON

                if (max_numON <= numON):
                    max_numON = numON
                    max_pathway = newFeatName
                    print "         MOST mutated so far (1) ... ", max_pathway, max_numON, len(pathways[aPathway])

                # note that this is not the fraction of the genes in the pathway that are
                # mutated, but just a count normalized by the # of genes in the
                # pathway
                numGenes = len(pathways[aPathway])
                fracON = float(numON) / float(len(pathways[aPathway]))
                if (numGenes >= 10):
                    if (max_fracON <= fracON):
                        max_fracON = fracON
                        max_pathway2 = newFeatName
                        print "         MOST mutated so far (2) ... ", max_pathway2, max_fracON, len(pathways[aPathway])

            # else:
            # print " --> NOT keeping this feature ... ", newFeatName, numON,
            # min_numON

    numNewFeat = kFeat
    print " "
    print " --> number of new features : ", numNewFeat
    print len(newDataMat), len(newDataMat[0])

    # now we need to append these new features to the input data matrix
    newRowLabels = [0] * (numRow + numNewFeat)
    newMatrix = [0] * (numRow + numNewFeat)
    for iR in range(numRow):
        newRowLabels[iR] = rowLabels[iR]
        newMatrix[iR] = dMat[iR]
    for iR in range(numNewFeat):
        newRowLabels[iR + numRow] = newNameVec[iR]
        newMatrix[iR + numRow] = newDataMat[iR]

    dataD['rowLabels'] = newRowLabels
    dataD['dataMatrix'] = newMatrix

    print " "
    print " --> finished with pathwayGnab ... "
    print " "

    return (dataD)

# -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#


def driverGnab(dataD, driverList):

    print " "
    print " ************************************************************* "
    print " ************************************************************* "
    print " "
    print " in driverGnab ... "

    # check that the input feature matrix looks ok ...
    try:
        numRow = len(dataD['rowLabels'])
        numCol = len(dataD['colLabels'])
        rowLabels = dataD['rowLabels']
        print " %d rows x %d columns " % (numRow, numCol)
        # print rowLabels[:5]
        # print rowLabels[-5:]
    except:
        print " ERROR in driverGnab ??? bad data ??? "
        return (dataD)

    mutationTypes = [":y_n_somatic", ":nonsilent_somatic",
                     ":y_del_somatic", ":y_amp_somatic"]
    numTypes = len(mutationTypes)

    numK = 1
    newNameVec = [0] * (numK * numTypes)
    newDataMat = [0] * (numK * numTypes)

    dMat = dataD['dataMatrix']

    kFeat = 0
    if (1):

        for aMutType in mutationTypes:

            newFeatName = "B:GNAB:driverMut" + "::::" + aMutType

            # first make sure we don't already have a feature with this name
            # ...
            stopNow = 0
            for iRow in range(numRow):
                if (newFeatName == rowLabels[iRow]):
                    stopNow = 1
            if (stopNow):
                continue

            print " tentative new feature #%d ... <%s> " % (kFeat, newFeatName)
            newNameVec[kFeat] = newFeatName
            newDataMat[kFeat] = numpy.zeros(numCol)

            for iR in range(numRow):

                if (iR % 1000 == 0):
                    print iR, numRow

                if (1):
                    gnabLabel = rowLabels[iR]
                    if (not gnabLabel.startswith("B:GNAB:")):
                        continue
                    if (gnabLabel.find(aMutType) < 0):
                        continue

                    try:
                        gnabTokens = gnabLabel.split(':')
                        gnabGene = gnabTokens[2].upper()
                    except:
                        print " FAILED to parse GNAB feature name ??? ", gnabLabel
                        continue

                    print "         considering ", iR, gnabTokens, gnabGene
                    if (gnabGene in driverList):
                        for iCol in range(numCol):
                            if (dMat[iR][iCol] == 1):
                                print "             yes!  setting bit at ", kFeat, iCol
                                newDataMat[kFeat][iCol] = 1

            if (1):
                kFeat += 1
                print " --> keeping this feature ... ", kFeat, newFeatName

    numNewFeat = kFeat
    print " "
    print " --> number of new features : ", numNewFeat
    print len(newDataMat), len(newDataMat[0])

    # now we need to append these new features to the input data matrix
    newRowLabels = [0] * (numRow + numNewFeat)
    newMatrix = [0] * (numRow + numNewFeat)
    for iR in range(numRow):
        newRowLabels[iR] = rowLabels[iR]
        newMatrix[iR] = dMat[iR]
    for iR in range(numNewFeat):
        newRowLabels[iR + numRow] = newNameVec[iR]
        newMatrix[iR + numRow] = newDataMat[iR]

    dataD['rowLabels'] = newRowLabels
    dataD['dataMatrix'] = newMatrix

    print " "
    print " --> finished with driverGnab ... "
    print " "

    return (dataD)

# -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#


def combineGnabCnvr(dataD):

    print " "
    print " ************************************************************* "
    print " ************************************************************* "
    print " "
    print " in combineGnabCnvr ... "

    # check that the input feature matrix looks ok ...
    try:
        numRow = len(dataD['rowLabels'])
        numCol = len(dataD['colLabels'])
        rowLabels = dataD['rowLabels']
        colLabels = dataD['colLabels']
        print " %d rows x %d columns " % (numRow, numCol)
        # print rowLabels[:5]
        # print rowLabels[-5:]
    except:
        print " ERROR in combineGnabCnvr ??? bad data ??? "
        return (dataD)

    # next, we need to find all of the GNAB features and all of the CNVR
    # features
    print " --> assigning gnab / cnvr flags ... "
    isGnab = setFeatBits(rowLabels, "B:GNAB:", ":y_n", "")
    isCnvr = setFeatBits(rowLabels, "N:CNVR:", "", "Gistic")

    print len(isGnab), max(isGnab)
    print len(isCnvr), max(isCnvr)

    if (not max(isGnab) and not max(isCnvr)):
        print " missing either GNAB or CNVR features ... "
        return (dataD)

    # now we need to map each of the GNAB features to one or more CNVR features
    mapVec = [0] * numRow

    for iR in range(numRow):

        if (iR % 1000 == 0):
            print iR, numRow

        if (isGnab[iR]):
            mapVec[iR] = []
            gnabLabel = rowLabels[iR]

            try:
                gnabTokens = gnabLabel.split(':')
                gnabChrName = gnabTokens[3].upper()
                gnabStart = int(gnabTokens[4])
                gnabStop = int(gnabTokens[5])
            except:
                print " FAILED to parse GNAB feature name ??? ", gnabLabel
                continue

            # avoid X and Y chromosome genes ...
            if (gnabChrName.endswith("X")):
                continue
            if (gnabChrName.endswith("Y")):
                continue

            for jR in range(numRow):
                if (isCnvr[jR]):
                    cnvrLabel = rowLabels[jR]
                    cnvrTokens = cnvrLabel.split(':')
                    cnvrChrName = cnvrTokens[3].upper()
                    if (gnabChrName != cnvrChrName):
                        continue
                    # print " comparing ... ", gnabLabel, cnvrLabel
                    cnvrStart = int(cnvrTokens[4])
                    if (gnabStop < cnvrStart):
                        continue
                    cnvrStop = int(cnvrTokens[5])
                    if (gnabStart > cnvrStop):
                        continue
                    mapVec[iR] += [jR]
                    # print " found match! ", gnabLabel, cnvrLabel, iR, jR,
                    # mapVec[iR]

            if (0):
                if (len(mapVec[iR]) > 5):
                    print iR, gnabLabel, len(mapVec[iR])
                    for kR in mapVec[iR]:
                        print "         ", kR, rowLabels[kR]
                # sys.exit(-1)

    # now we need to actually loop over the data ...
    dMat = dataD['dataMatrix']

    # -------------------------------------------------------------------------
    if (0):
        # FIRST we want to check for any "adjacent normal" samples and set those to 0 ...
        # --> ACTUALLY, deciding NOT to do this anymore ( 31 oct 2012 )  NEW CHANGE
        numGNABfeat = 0
        numCNVRfeat = 0
        for iRow in range(numRow):
            curFeature = rowLabels[iRow]
            if (curFeature.startswith("B:GNAB:")):
                numGNABfeat += 1
            elif (curFeature.startswith("N:CNVR:")):
                numCNVRfeat += 1
        print " number of GNAB features : %d " % (numGNABfeat)
        print " number of CNVR features : %d " % (numCNVRfeat)
        print " "

        numGNABset = 0
        numCNVRset = 0
        numGNABfeat = 0
        numCNVRfeat = 0
        numNormalCol = 0
        for iCol in range(numCol):
            curLabel = colLabels[iCol]
            if (curLabel.startswith("TCGA-")):
                if (len(curLabel) >= 15):
                    sampleType = curLabel[13:15]
                    if (sampleType == '11'):
                        numNormalCol += 1
                        # print iCol, curLabel
                        for iRow in range(numRow):
                            curFeature = rowLabels[iRow]
                            if (curFeature.startswith("B:GNAB:")):
                                # print curFeature, dMat[iRow][iCol]
                                if (dMat[iRow][iCol] == "NA" or dMat[iRow][iCol] == NA_VALUE):
                                    dMat[iRow][iCol] = 0
                                    numGNABset += 1
                            elif (curFeature.startswith("N:CNVR:")):
                                if (curFeature.find(":chrX:") > 0):
                                    continue
                                if (curFeature.find(":chrY:") > 0):
                                    continue
                                # print curFeature, dMat[iRow][iCol]
                                if (dMat[iRow][iCol] == "NA" or dMat[iRow][iCol] == NA_VALUE):
                                    dMat[iRow][iCol] = 0.
                                    numCNVRset += 1
    # -------------------------------------------------------------------------

    ## cnvrThreshold = 2.
    cnvrThreshold = 1.

    print " --> now checking for deletions and amplifications ... ", cnvrThreshold
    print "     and creating new y_del and y_amp features "

    numNewFeat = 0
    newNameVec = []
    newDataMat = []

    for iR in range(numRow):

        if (iR % 1000 == 0):
            print iR, numRow

        if (isGnab[iR]):

            print iR, rowLabels[iR], len(mapVec[iR])
            print mapVec[iR]

            # how often is this gene mutated?
            numYes = 0
            numDel = 0
            numAmp = 0
            numYesDel = 0
            numYesAmp = 0

            maxCN = -999.
            minCN = 999.

            for iCol in range(numCol):
                mutFlag = 0
                ampFlag = 0
                delFlag = 0
                for jR in mapVec[iR]:
                    if (dMat[iR][iCol] == 1):
                        mutFlag = 1
                    if (dMat[jR][iCol] == NA_VALUE):
                        continue
                    if (dMat[jR][iCol] > maxCN):
                        maxCN = dMat[jR][iCol]
                    if (dMat[jR][iCol] < minCN):
                        minCN = dMat[jR][iCol]
                    if (dMat[jR][iCol] < -cnvrThreshold):
                        delFlag = 1
                    if (dMat[jR][iCol] > cnvrThreshold):
                        ampFlag = 1
                numYes += mutFlag
                numDel += delFlag
                numAmp += ampFlag
                if (mutFlag or delFlag):
                    numYesDel += 1
                if (mutFlag or ampFlag):
                    numYesAmp += 1

                if (mutFlag and delFlag):
                    print " NOTE: mutation AND deletion ??? ", iCol, dMat[iR][iCol]
                    # for jR in mapVec[iR]:
                    # print dMat[jR][iCol]

            if (numYes + numAmp + numDel > 0):
                print "         --> %3d mutations " % numYes, numYesDel, numYesAmp
                print "             %3d deletions " % numDel, minCN
                print "             %3d amplifications " % numAmp, maxCN
                if (numYesDel > 0):
                    if (float(numYesDel - numYes) / float(numCol) > 0.10):
                        if (float(numYesDel) / float(numCol) > 0.10):
                            print "                 looks very significant !!! "

            if (numDel > 1):
                numNewFeat += 1
                curFeatName = rowLabels[iR]
                newFeatName = makeNewFeatureName(
                    curFeatName, ":y_n", ":y_del")
                print "         newFeatName <%s> " % newFeatName

                # make sure that there is not already a feature by this name!!!
                addFeat = 1
                for aLabel in rowLabels:
                    if (aLabel == newFeatName):
                        addFeat = 0
                        print "             oops ??? <%s> already exists ??? " % aLabel

                if (addFeat):
                    newNameVec += [newFeatName]
                    newDataMat += [numpy.zeros(numCol)]
                    for iCol in range(numCol):

                        # we need to start with NA
                        newDataMat[-1][iCol] = NA_VALUE

                        # if we already have a 'yes' for the mutation, that's
                        # all we need ...
                        if (dMat[iR][iCol] == 1):
                            newDataMat[-1][iCol] = 1
                            continue
                        # if not, then check for deletions ...
                        for jR in mapVec[iR]:
                            if (dMat[jR][iCol] == NA_VALUE):
                                continue
                            if (dMat[jR][iCol] < -cnvrThreshold):
                                newDataMat[-1][iCol] = 1

                        # if we have set this bit we are done ...
                        if (newDataMat[-1][iCol] == 1):
                            continue

                        # and otherwise if we have no mutation, set it to 0
                        if (dMat[iR][iCol] == 0):
                            newDataMat[-1][iCol] = 0

            if (numAmp > 1):
                numNewFeat += 1
                curFeatName = rowLabels[iR]
                newFeatName = makeNewFeatureName(
                    curFeatName, ":y_n", ":y_amp")
                print "         newFeatName <%s> " % newFeatName

                # make sure that there is not already a feature by this name!!!
                addFeat = 1
                for aLabel in rowLabels:
                    if (aLabel == newFeatName):
                        addFeat = 0
                        print "             oops ??? <%s> already exists ??? " % aLabel

                if (addFeat):
                    newNameVec += [newFeatName]
                    newDataMat += [numpy.zeros(numCol)]
                    for iCol in range(numCol):

                        # we need to start with NA
                        newDataMat[-1][iCol] = NA_VALUE

                        # if we already have a 'yes' for the mutation, that's
                        # all we need ...
                        if (dMat[iR][iCol] == 1):
                            newDataMat[-1][iCol] = 1
                            continue
                        # if not, then check for amplifications ...
                        for jR in mapVec[iR]:
                            if (dMat[jR][iCol] == NA_VALUE):
                                continue
                            if (dMat[jR][iCol] > cnvrThreshold):
                                newDataMat[-1][iCol] = 1

                        # if we have set this bit we are done ...
                        if (newDataMat[-1][iCol] == 1):
                            continue

                        # and otherwise if we have no mutation, set it to 0
                        if (dMat[iR][iCol] == 0):
                            newDataMat[-1][iCol] = 0

    # if ( numNewFeat == 0 ):
    # print " --> NO new features "
    # print " --> finished with combineGnabCnvr ... "
    # return ( dataD )

    print " "
    print " --> number of new features : ", numNewFeat
    if (numNewFeat > 0):
        print len(newNameVec)
        print len(newDataMat), len(newDataMat[0])
        for ii in range(numNewFeat):
            if (newNameVec[ii].find("CSMD1") > 0):
                print newNameVec[ii]
                print newDataMat[ii]
        print " "

    # now we need to append these new features to the input data matrix
    newRowLabels = [0] * (numRow + numNewFeat)
    newMatrix = [0] * (numRow + numNewFeat)
    for iR in range(numRow):
        newRowLabels[iR] = rowLabels[iR]
        newMatrix[iR] = dMat[iR]
    for iR in range(numNewFeat):
        newRowLabels[iR + numRow] = newNameVec[iR]
        newMatrix[iR + numRow] = newDataMat[iR]

    dataD['rowLabels'] = newRowLabels
    dataD['dataMatrix'] = newMatrix

    print " "
    print " --> finished with combineGnabCnvr ... "
    print " "

    return (dataD)

# -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
# -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

if __name__ == "__main__":

    if (1):
        if (len(sys.argv) == 3):
            inFile = sys.argv[1]
            outFile = sys.argv[2]
            do_combineGnabCnvr = 1
            do_pathwayGnab = 1
            do_driverGnab = 0
            driverList = ["TP53", "KRAS", "PIK3CA", "PTEN"]
        else:
            print " "
            print " Usage: %s <input TSV file> <output TSV file> "
            print " "
            sys.exit(-1)

    print " "
    print " Running : %s  %s  %s  " % (sys.argv[0], sys.argv[1], sys.argv[2])
    print " "

    # read in the input feature matrix first, just in case there
    # actually isn't one yet available ...
    testD = tsvIO.readTSV(inFile)
    try:
        print len(testD['rowLabels']), len(testD['colLabels'])
    except:
        print " --> invalid / missing input feature matrix "
        sys.exit(-1)

    # we want to come up with a 'merged' mutation OR deletion feature
    if (do_combineGnabCnvr):
        newD = combineGnabCnvr(testD)
        testD = newD

    # and then pathway level mutation features
    if (do_pathwayGnab):
        pwDict = readPathways()
        newD = pathwayGnab(testD, pwDict)
        testD = newD

    # and then a 'driverMut' feature based on the driverList above
    # (which is just 4 hardcoded genes for now)
    if (do_driverGnab):
        newD = driverGnab(testD, driverList)
        testD = newD

    # and finally write it out ...
    tsvIO.writeTSV_dataMatrix(testD, 0, 0, outFile)

# -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#