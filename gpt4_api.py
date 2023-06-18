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



# general advice
setup_gpt4()
input_from_humm = read_json('emotion.json')['emotions']
a = generate_answer(f"Give user a emotion analysis and advice within 5 sentences using these emotional factors she felt : {input_from_humm}")
print("General advice : ", a)

# Movie recommendation



