import os
import shutil
import numpy as np

commonFolder = './desktop/AllImages/'
AllTags = ['Up','Stop','Left','Right']
trainFold = './desktop/signals/'
valFold = './desktop/signals_val/'

trainExists = os.path.exists(trainFold)
valExists = os.path.exists(valFold)

if(trainExists):
    shutil.rmtree (trainFold)

if(valExists):
    shutil.rmtree (valFold)


valPerc = 0.15
trainPerc = 1-valPerc

for tag in AllTags:
    tagFiles = []
    tagFolderDir = commonFolder + tag + "/"
    newfolderDir = trainFold + tag + "/"
    newFolderValDir = valFold + tag + "/"
    if(not os.path.exists(newfolderDir)):
        os.makedirs(newfolderDir)
    if(not os.path.exists(newFolderValDir)):
        os.makedirs(newFolderValDir)
    
    for (dirpath, dirnames, filenames) in os.walk(tagFolderDir):
        tagFiles.extend(filenames)
    
    npfiles = np.array(tagFiles)
    permutation = np.random.permutation(npfiles)
    valFilesN = np.int(len(tagFiles)*valPerc)
    valFiles = permutation[:valFilesN]
    trainFiles = permutation[valFilesN:]
    for valFile in valFiles:
        fileFromFullName = tagFolderDir + valFile
        fileToFullName = newFolderValDir + valFile
        shutil.copyfile(fileFromFullName,fileToFullName)
    for trainFile in trainFiles:
        fileFromFullName = tagFolderDir + trainFile
        fileToFullName = newfolderDir + trainFile
        shutil.copyfile(fileFromFullName,fileToFullName)






