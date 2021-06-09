import os
import subprocess
import time
# ' ' + modelType +
# + ' ' + saveMemoryParam
startToken = '<BOS>'
endToken = '<EOS>'

pythonPath = 'D:/Programming/Python/python.exe'
fileToExecute = 'D:/Programming/Idea_Projects/MasterDegreeData/transformers/examples/legacy/run_language_modeling.py'

modelingDir = 'D:/Programming/Idea_Projects/MasterDegreeData/DataToTransfer/MasterDegree/Dzen/Modeling'
outputModelPathParam = modelingDir + '/Model'
outputDirParam = '--output_dir=' + outputModelPathParam
gpt2 = 'gpt2'
modelType = '--model_type=' + gpt2
modelNameOrPath = '--model_name_or_path=' + gpt2
doTrain = '--do_train'
doEval = '--do_eval'
trainBatchSize = '--per_device_train_batch_size=2'
evalBatchSize = '--per_device_eval_batch_size=2'
lineByLine = '--line_by_line'
evaluationStrategy = '--evaluation_strategy=epoch'
learningRate = '--learning_rate=5e-5'
numEpoch = '--num_train_epochs=5'
trainFileNameParam = '--train_data_file='
validFileNameParam = '--eval_data_file='
saveMemoryParam = '--fp16_full_eval'
_params = outputDirParam + ' ' + modelType + ' ' + modelNameOrPath + ' ' + doTrain + ' ' + doEval + ' '+ trainBatchSize + ' ' + evalBatchSize + ' ' + lineByLine + ' ' + evaluationStrategy + ' ' + learningRate + ' ' + numEpoch



trainPackagePath = modelingDir + '/train'
validPackagePath = modelingDir + '/valid'

trainFiles = os.listdir(trainPackagePath)
validFiles = os.listdir(validPackagePath)

curTrainFile = trainPackagePath + '/' + trainFiles[0]
curValidFile = validPackagePath + '/' + validFiles[0]

# _params += ' ' + trainFileNameParam + curTrainFile + ' ' + validFileNameParam + curValidFile
# command = pythonPath + ' ' + fileToExecute + ' ' + _params
# res = subprocess.call(command, shell=True)
# print("Returned Value: ", res)
