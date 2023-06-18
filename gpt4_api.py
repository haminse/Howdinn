# make sure to set : pip install openai
import openai
import json
import random

#setup
def setup_gpt4():
    try:
        KEY = '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'
        openai.api_key = KEY
    except Exception as e:
        raise Exception("OPEN_ AI API KEY Error occured!!!", str(e))

#read json file
def read_json(file_name):
    with open(file_name) as file:
        return json.load(file)    

#flatten the emotion json
def flatten_json(data):
    flattened = '\n'.join([f"{item['emotion']}: {item['percentage']}%" for item in data])
    return flattened


#get entry question
def get_entry_question():
    questions = read_json('entry_question.json')
    return random.choice(questions['entry_q'])

#generate answer
def generate_answer(query):
    msg = [
        {"role": "system", "content": "You are a helpful and considerate listner and advisor."},
        {"role": "user", "content": query}
    ]
    response = openai.ChatCompletion.create(
        model='gpt-4', # gpt-3.5-turbo / gpt-4
        messages=msg
    )
    answer = response['choices'][0]['message']['content']
    return answer



# Examples



# general advice example
# setup_gpt4()
# input_from_humm = read_json('chart_data(example).json')
# print(input_from_humm)
# emotion_factors = flatten_json(input_from_humm)
# a = generate_answer(f"Give user a emotion analysis and advice within 5 sentences using these emotional factors that user felt : {emotion_factors}")
# print("General advice : ", a)




