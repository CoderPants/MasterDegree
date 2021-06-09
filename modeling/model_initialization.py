from modeling.gpt2_trainer import GPT2_Trainer

rootDir = 'D:/Programming/Idea_Projects/MasterDegreeData/DataToTransfer/MasterDegree/Dzen/Top_Extracted/Travel'
save_path = 'D:/Programming/Idea_Projects/MasterDegreeData/DataToTransfer/MasterDegree/Dzen/Modeling/AdditionalFiles'
trainer = GPT2_Trainer(tokenizePath=save_path, contentDir=rootDir, tokenizedContentDir=save_path)
trainer.print()
trainer.initModel()
