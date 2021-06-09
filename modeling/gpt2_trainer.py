import os
from pathlib import Path

import tensorflow as tf
from transformers import GPT2Config, TFGPT2LMHeadModel, GPT2Tokenizer
from transformers import WEIGHTS_NAME, CONFIG_NAME

from tokenization.tokenizator import BPE_token


class GPT2_Trainer:
    def __init__(self, tokenizePath, contentDir, tokenizedContentDir):
        self.tokenizePath = tokenizePath
        self.contentDir = contentDir
        self.tokenizedContentDir = tokenizedContentDir
        self.contentFilePaths = []
        self.initContentPaths()

    def initContentPaths(self):
        dirs = os.listdir(self.contentDir)
        for package in dirs:
            curDir = self.contentDir + '/' + package
            files = os.listdir(curDir)
            for file in files:
                if 'Content_' in file:
                    self.contentFilePaths.append(curDir + '/' + file)

    def createTokenizedFiles(self):
        tokenizer = BPE_token()
        tokenizer.bpe_train(self.contentFilePaths)
        # saving the tokenized data in our specified folder
        tokenizer.save_tokenizer(self.tokenizePath)

    def initModel(self):
        tokenizer = GPT2Tokenizer.from_pretrained(self.tokenizePath)
        tokenizer.add_special_tokens({
            "eos_token": "</s>",
            "bos_token": "<s>",
            "unk_token": "<unk>",
            "pad_token": "<pad>",
            "mask_token": "<mask>"
        })
        # creating the configurations from which the model can be made
        config = GPT2Config(
            vocab_size=tokenizer.vocab_size,
            bos_token_id=tokenizer.bos_token_id,
            eos_token_id=tokenizer.eos_token_id
        )
        # creating the model
        model = TFGPT2LMHeadModel(config)
        tokenizedContentPath = self.tokenizedContentDir + '/all_content.txt'
        encodedFilePath = self.tokenizedContentDir + '/all_content_encoded.txt'
        if not Path(tokenizedContentPath).exists():
            self.tokenizeData(tokenizer, tokenizedContentPath)
        if not Path(encodedFilePath).exists():
            self.createEncodedFile(tokenizer, tokenizedContentPath, encodedFilePath)
        print('Started Preparing')
        # PREPARE DATA
        encodedSymbols = self.getEncodedData(encodedFilePath)
        examples = []
        block_size = 100
        BATCH_SIZE = 12
        BUFFER_SIZE = 1000
        for i in range(0, len(encodedSymbols) - block_size + 1, block_size):
            examples.append(encodedSymbols[i:i + block_size])
        print('Examples passed')
        inputs, labels = [], []
        for ex in examples:
            inputs.append(ex[:-1])
            labels.append(ex[1:])
        print('inputs and labels passed')
        dataset = tf.data.Dataset.from_tensor_slices((inputs, labels))
        print('from_tensor_slices passed')
        dataset = dataset.shuffle(BUFFER_SIZE).batch(BATCH_SIZE, drop_remainder=True)

        print('Started Training')
        # TRAIN
        # defining our optimizer
        optimizer = tf.keras.optimizers.Adam(learning_rate=3e-5, epsilon=1e-08, clipnorm=1.0)
        print('passed optimizer')
        # defining our loss function
        loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
        print('passed loss')
        # defining our metric which we want to observe
        metric = tf.keras.metrics.SparseCategoricalAccuracy('accuracy')
        print('passed metric')
        # compiling the model
        model.compile(optimizer=optimizer, loss=[loss, *[None] * model.config.n_layer], metrics=[metric])
        print('passed model.compile')
        # train model
        num_epoch = 10
        print('training')
        history = model.fit(dataset, epochs=num_epoch)
        try:
            print('History is: ' + history.params)
        except Exception as e:
            print(e)

        print('Test model')
        # TEST MODEL
        text = "Ну что, привет мир! "
        # encoding the input text
        input_ids = tokenizer.encode(text, return_tensors='tf')
        # getting out output
        beam_output = model.generate(
            input_ids,
            max_length=50,
            num_beams=5,
            temperature=0.7,
            no_repeat_ngram_size=2,
            num_return_sequences=5
        )
        res = tokenizer.decode(beam_output[0])
        resultFilePath = 'D:\Programming\Idea_Projects\MasterDegreeData\DataToTransfer\MasterDegree\Dzen\Modeling\AdditionalFiles\model_result.txt'
        try:
            with open(resultFilePath, 'w', encoding='utf-8') as resFile:
                resFile.write(str(res))
        finally:
            print('\n\n\n' + 'Result is: ' + str(res) + '\n\n\n')
        dirForSavedModel = 'D:\Programming\Idea_Projects\MasterDegreeData\DataToTransfer\MasterDegree\Dzen\Modeling\Model'
        print('Save model')
        self.saveModel(model, tokenizer, dirForSavedModel)

    def tokenizeData(self, tokenizer, pathToFile):
        with open(pathToFile, 'x', encoding='utf-8') as contentFile:
            for index, filename in enumerate(self.contentFilePaths):
                print("Index " + str(index) + ' from ' + str(len(self.contentFilePaths)))
                with open(filename, "r", encoding='utf-8') as f:
                    x = f.read()
                contentFile.write(x + tokenizer.eos_token)
                # single_string += x + tokenizer.eos_token

    def createEncodedFile(self, tokenizer, inputFile, outputFile):
        print('Started encoding')
        with open(inputFile, 'r', encoding='utf-8') as contentFile:
            result = tokenizer.encode(contentFile.read())
        print('Passed encoding')
        with open(outputFile, 'x', encoding='utf-8') as encodedFile:
            for item in result:
                encodedFile.write(str(item) + '\n')
        print('Finished encoding')

    def getEncodedData(self, encodedFilePath):
        with open(encodedFilePath, 'r') as file:
            return [int(line.rstrip('\n')) for line in file]

    def saveModel(self, model, tokenizer, output_dir):
        # creating directory if it is not present
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        model_to_save = model.module if hasattr(model, 'module') else model
        output_model_file = os.path.join(output_dir, WEIGHTS_NAME)
        output_config_file = os.path.join(output_dir, CONFIG_NAME)
        # save model and model configs
        model.save_pretrained(output_dir)
        model_to_save.config.to_json_file(output_config_file)
        # save tokenizer
        tokenizer.save_pretrained(output_dir)

    def print(self):
        print("Length is " + str(len(self.contentFilePaths)))
        print("tokenizePath is " + str(self.tokenizePath))
        print("contentDir is " + str(self.contentDir))
        print(tf.config.list_physical_devices())
