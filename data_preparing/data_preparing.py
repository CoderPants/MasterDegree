import os
import subprocess
import time

startToken = '<BOS>'
endToken = '<EOS>'
modelingDir = 'D:/Programming/Idea_Projects/MasterDegreeData/DataToTransfer/MasterDegree/Dzen/Modeling'


def fillFiles(_list, path, mType):
    data = ''
    for index, _file in enumerate(_list):
        print('Type: ' + mType + ' index: ' + str(index) + ' of: ' + str(len(_list)))
        with open(_file, 'r', encoding='utf-8') as dataFile:
            data += startToken + ' ' + dataFile.read() + ' ' + endToken + '\n'
    with open(path, 'x', encoding='utf-8') as mFile:
        mFile.write(data)


rootDir = 'D:/Programming/Idea_Projects/MasterDegreeData/DataToTransfer/MasterDegree/Dzen/Top_Extracted/Travel'
dirs = os.listdir(rootDir)
contentFiles = []
for package in dirs:
    curDir = rootDir + '/' + package
    files = os.listdir(curDir)
    for file in files:
        if 'Content_' in file:
            contentFiles.append(curDir + '/' + file)

size = len(contentFiles)
trainSize = int(size * 0.7)
validSize = int(size * 0.2)
testSize = int(size * 0.1)
trainList = contentFiles[:trainSize]
validList = contentFiles[trainSize:trainSize + validSize]
testList = contentFiles[trainSize + validSize:size]

trainPackagePath = modelingDir + '/train'
validPackagePath = modelingDir + '/valid'
testPackagePath = modelingDir + '/test'

trainBatchSize = 100
batchSizePercent = trainBatchSize / (trainSize / 100)
validBatchSize = int((validSize / 100) * batchSizePercent)
testBatchSize = int((testSize / 100) * batchSizePercent)

currentTrainIndex = 0
currentValidIndex = 0
currentTestIndex = 0

needToBreak = False
while True:
    print('Current train index ' + str(currentTrainIndex) + ' from ' + str(trainSize))
    print('Current valid index ' + str(currentValidIndex) + ' from ' + str(validSize))
    print('Current test index ' + str(currentTestIndex) + ' from ' + str(testSize))
    print('\n')
    curId = round(time.time() * 1000)
    trainFilePath = trainPackagePath + '/' + str(curId) + '.txt'
    validFilePath = validPackagePath + '/' + str(curId) + '.txt'
    testFilePath = testPackagePath + '/' + str(curId) + '.txt'

    if currentTrainIndex + trainBatchSize <= trainSize:
        curTrainList = trainList[currentTrainIndex:currentTrainIndex + trainBatchSize]
        curValidList = validList[currentValidIndex:currentValidIndex + validBatchSize]
        curTestList = testList[currentTestIndex:currentTestIndex + testBatchSize]
    else:
        needToBreak = True
        curTrainList = trainList[currentTrainIndex:trainSize]
        curValidList = validList[currentValidIndex:validSize]
        curTestList = trainList[currentTestIndex:testSize]

    fillFiles(curTrainList, trainFilePath, 'Train')
    fillFiles(curValidList, validFilePath, 'Valid')
    fillFiles(curTestList, testFilePath, 'Test')

    currentTrainIndex += trainBatchSize
    currentValidIndex += validBatchSize
    currentTestIndex += testBatchSize

    if needToBreak:
        break
    time.sleep(1)

# for index in range(len(trainFiles)):
#     curTrainFile = trainPackagePath + '/' + trainFiles[index]
#     curValidFile = validPackagePath + '/' + validFiles[index]
#     curTestFile = testPackagePath + '/' + testFiles[index]

# trainFilePath = modelingDir + '/train.txt'
# validFilePath = modelingDir + '/valid.txt'
# testFilePath = modelingDir + '/test.txt'
#
# fillFiles(trainList, trainFilePath, 'Train')
# fillFiles(validList, validFilePath, 'Valid')
# fillFiles(testList, testFilePath, 'Test')
#
#
#
# pythonPath = '/usr/bin/python3.6'
# fileToExecute = '/home/misha/transformers/examples/legacy/run_language_modeling.py'
# _params = '--output_dir=/home/misha/MasterDegree/Dzen/Modeling/Model --model_type=gpt2 ' \
#           '--model_name_or_path=gpt2 --do_train ' \
#           '--train_data_file=/home/misha/MasterDegree/Dzen/Modeling/test.txt --do_eval ' \
#           '--eval_data_file=/home/misha/MasterDegree/Dzen/Modeling/valid.txt --per_device_train_batch_size=2 ' \
#           '--per_device_eval_batch_size=2 --line_by_line --evaluation_strategy=epoch --learning_rate=5e-5 ' \
#           '--num_train_epochs=5 '
# command = pythonPath + ' ' + fileToExecute + ' ' + _params
# res = subprocess.call(command, shell=True)
# print("Returned Value: ", res)
