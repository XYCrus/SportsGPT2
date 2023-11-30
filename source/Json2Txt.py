#%%
import json

#%%
def PreprocessJson(JsonFile):
    with open(JsonFile, "r") as f:
        data = json.load(f)
    
    PrepData = []
    
    for load in data["finetune"]:
        for question in load["questions"]:
            PrepData.append(f"User: {question}\n")
            for response in load["responses"]:
                PrepData.append(f"Assistant: {response}\n")
    
    return "".join(PrepData)


def PrepDataStore(PrepData, OutputFile):
    with open(OutputFile, "w") as f:
        f.write(PrepData)

#%%
if __name__ == '__main__': 
    PrepData = PreprocessJson("../data/GPTGenerated.json")
    
    PrepDataStore(PrepData, "../data/FinetuneData.txt")