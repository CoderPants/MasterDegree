import os
from pathlib import Path

# the folder 'text' contains all the files
from tokenization.tokenizator import BPE_token
from transformers import GPT2Config, TFGPT2LMHeadModel, GPT2Tokenizer


rootDir = 'D:/Programming/Idea_Projects/MasterDegreeData/DataToTransfer/MasterDegree/Dzen/Top_Extracted/Travel'
dirs = os.listdir(rootDir)
contentFiles = []
for package in dirs:
    curDir = rootDir + '/' + package
    files = os.listdir(curDir)
    for file in files:
        if 'Content_' in file:
            contentFiles.append(curDir + '/' + file)

tokenizer = BPE_token()
# train the tokenizer model
tokenizer.bpe_train(contentFiles)
# saving the tokenized data in our specified folder
save_path = 'D:/Programming/Idea_Projects/MasterDegreeData/DataToTransfer/MasterDegree/Dzen/Modeling/AdditionalFiles'
tokenizer.save_tokenizer(save_path)
