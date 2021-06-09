from transformers import GPT2Tokenizer, TFGPT2LMHeadModel

outputDir = 'D:\Programming\Idea_Projects\MasterDegreeData\DataToTransfer\MasterDegree\Dzen\Modeling\Model'
tokenizer = GPT2Tokenizer.from_pretrained(outputDir)
model = TFGPT2LMHeadModel.from_pretrained(outputDir)

text = "Тестирование модели начинается. "
input_ids = tokenizer.encode(text, return_tensors='tf')
beam_output = model.generate(
    input_ids,
    max_length=200,
    num_beams=5,
    temperature=0.7,
    no_repeat_ngram_size=2,
    num_return_sequences=5
)
res = tokenizer.decode(beam_output[0])

print('\n\n\n' + 'Result is: ' + str(res) + '\n\n\n')
