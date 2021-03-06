from zipfile import ZipFile
import csv
import os
import shutil


def processDownloads():
    #Paths, change as necessary
    #ZIP = "zippedFiles"
    TEMPDIR = "allFiles"
    DESTDIR = "processedFiles"
    FAULTDIR = "faultyFiles"
    LOGFILE = "log.txt"

    if not os.path.isdir(DESTDIR):
        os.makedirs(DESTDIR)
    if not os.path.isdir(FAULTDIR):
        os.makedirs(FAULTDIR)
    #for zippedFile in os.listdir(ZIP):
    #    with ZipFile(zippedFile, 'r') as zip:
    #        zip.extractall(TEMPDIR) #Fill this with a path to a temp directory to store all files - TEMPDIR

    #Keep track of error types for log
    errorTypes = ["none",
    "file not csv",
    "file contains duplicate batches",
    "a batch does not contain ten readings",
    "a batch contains reading outside range",
    "a batch contains invalid reading"]
    #For each file in directory
    for filen in os.listdir(TEMPDIR): #Fill this with path - TEMPDIR
        faultyFile = (False, 0)
        if not filen.endswith(".csv"): #If not csv, it's a fault
            #Log the error, filename, move on
            faultyFile=(True, 1)
            logError(filen, faultyFile[1]) # log the error
            shutil.copy(TEMPDIR+"\\"+filen, FAULTDIR)
            pass
        else: #Open it and check for internal faults
            with open(TEMPDIR + "\\" + filen) as csv_f:
                data = csv.reader(csv_f, delimiter=',')
                lineCount=0
                batches = [] #Keep track of batch names so that duplicates can be detected
                for batch in data:
                    if lineCount != 0: #First line contains titles etc
                        if len(batch) != 12: #If length is wrong (id, timestamp, 10 readings) flag error and break loop
                            faultyFile = (True, 3)
                            break
                        for entry in range(len(batch)):
                            if entry == 0:
                                batches.append(batch[entry]) #add batch id to checker
                            elif entry >= 2:
                                if float(batch[entry]) > 9.9 or float(batch[entry]) < 0:
                                    faultyFile = (True, 4)
                                    break
                                elif len(batch[entry].split('.')[1]) > 3: #If there are more than 3dp
                                    faultyFile = (True, 5)
                                    break
                    lineCount += 1
                if not faultyFile[0]: #If that data is fine, check for duplicate batch IDs
                    if batches[0] in batches[1:] or batches[len(batches)-1] in batches[:len(batches)-1]:
                        faultyFile = (True, 2)
                    else:
                        for i in range(1,len(batches)-1):
                            if batches[i] in batches[:i] or batches[i] in batches[i+1:]:
                                faultyFile = (True, 2)
                                break
            if not faultyFile[0]: #If the data is fine, copy it to the correct place - DESTDIR
                shutil.copy(TEMPDIR+"\\"+filen, DESTDIR)
            else:
                logError(filen, faultyFile[1]) # log the error
                shutil.copy(TEMPDIR+"\\"+filen, FAULTDIR)


def logError(filename, errortype): #Log files
    errorTypes = ["none",
"file not csv",
"file contains duplicate batches",
"a batch does not contain ten readings",
"a batch contains reading outside range",
"a batch contains invalid reading"]
    LOGFILE = "log.txt"
    log = open(LOGFILE, "a")
    stri = "ERROR: " + filename + " : " + errorTypes[errortype] + "\n"
    log.write(stri)
    log.close()
