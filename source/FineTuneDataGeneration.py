#%%
from openai import OpenAI
import time
import json
import re

#%%
# Function to generate tags
def TagGeneration(client):
    response = client.chat.completions.create(
    model = "gpt-4",
    messages = [
        {"role": "system", 
        "content": """You are an intelligent assistant tasked with generating a list of sports-related tags. 
        These tags should be diverse and encompass various aspects of sports, such as specific sports, strategies, 
        training, competition, sports culture, and events. The tags should be selected with the intent of later using them 
        to create insightful, engaging, and informative question-and-answer pairs, which will be used for fine-tuning a 
        language learning model in the sports domain. Focus on generating tags that can facilitate a wide range of sports-related 
        queries and discussions, providing a solid foundation for creating a rich and varied Q&A dataset."""}, #context
        
        {"role": "user", 
        "content": """Please generate a list of 100 unique sports-related tags.
        """}  #prompt
    ])

    ResponseStr = response.choices[0].message.content.strip()

    return ResponseStr

# Convert tags into list
def Tag2List(ResponseStr):
    lines = ResponseStr.strip().split('\n')

    SportsList = [line.split('. ', 1)[1] for line in lines if line]

    return SportsList

# Function to generate questions from tag
def QuestionGeneration(client, tag):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", 
             "content": f"""Generate two questions that a user might naturally ask in a casual conversation about {tag}. 
             Each question should be engaging, easy to understand for a broad audience, and distinct from each other.
             Format the two questions as a numbered list starting from 1. 
             Each question should start on a new line and be preceded by its number and a period. 
             Organize it as follows: '1. [First question] 2. [Second question]'"""},
            {"role": "user", "content": "Give me a list of two questions"}
        ]
    )
    return response.choices[0].message.content.strip()

# Function to paraphrase a question
def QuestionParaphrase(client, question):
    ParaQuestions = []
    for _ in range(2):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", 
                 "content": """Paraphrase the following question in a conversational 
                 and user-friendly manner, as if it were being asked in a casual, 
                 real-life scenario: """ + question},
                {"role": "user", "content": ""}
            ]
        )
        ParaQuestions.append(response.choices[0].message.content.strip())
        time.sleep(1)  
    return ParaQuestions

# Function to generate answers for a question
def AnswerGeneration(client, question):
    answers = []

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"""Provide three different answers to the following question, each with a slightly 
                different style. Ensure that each answer is a somehow different from the other or have different information.
                Format the answers as a numbered list starting from 1. Each answer should start on a new line and be preceded by its number and a period. 
                Organize it as follows: '1. [First answer] 2. [Second answer] 3. [Third answer]': {question}"""},
            {"role": "user", "content": "Give me a list of three answers"}
        ]
    )
    answers = response.choices[0].message.content.strip()
    return answers


def Tag2All(client, tags):
    finetune = []

    for index, tag in enumerate(tags):
        print(f"Processing tag {index + 1}/{len(tags)}: {tag}")

        questions = QuestionGeneration(client, tag)
        QuestionList = questions.strip().split('\n')
        QuestionList = [line.split('. ', 1)[1] for line in QuestionList if line]

        for question in QuestionList:
            ParaQuestions = QuestionParaphrase(client, question)
            AllQuestions = [question] + ParaQuestions

            answers = AnswerGeneration(client, question)
            answers = re.split(r'\d+\.\s', answers)
            answers = [answer.strip() for answer in answers if answer.strip()]

            intent = {
                "tag": tag,
                "questions": AllQuestions,
                "responses": answers
            }

            finetune.append(intent)

    JsonData = json.dumps({"finetune": finetune}, indent = 4)

    return JsonData


def JsonStore(dir, JsonData):
    with open(dir, 'w') as file:
        file.write(JsonData)


#%%
if __name__ == '__main__': 
    client = OpenAI(api_key="YourKeyHere")

    TagList = Tag2List(TagGeneration(client))

    JsonData = Tag2All(client, TagList)

    JsonStore('../data/GPTGenerated.json', JsonData)
