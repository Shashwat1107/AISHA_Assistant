"""
GOogle search the Answer, and  then Compress it using the Groq AI.
the ChatBot just gives a General Answer of query
Here we are searching the realtime data, and giving it to chatbot to summarise
"""

from googlesearch import search
from groq import Groq
from json import dump, load
import datetime
from dotenv import dotenv_values

env_vars = dotenv_values(".env")  # Load environment variables from .env file
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")

# Init the Groq
client = Groq(api_key=GroqAPIKey)

System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which has real-time up-to-date information from the internet.
*** Provide Answers In a Professional Way, make sure to add full stops, commas, question marks, and use proper grammar.***
*** Just answer the question from the provided data in a professional way. ***"""

try:
    with open(r'Data\ChatLog.json', 'r') as file:
        messages = load(file)
except FileNotFoundError:
    with open(r'Data\ChatLog.json', 'w') as file:
        dump([], file)

def GoogleSearch(query):
    results = list(search(query, num_results=5, advanced=True))
    Answer = f"The search results for your query '{query}' are:\n[start]\n"

    for i in results:
        Answer += f"Title {i.title}\nDescription: {i.description}\n\n"

    Answer += "[end]"
    # print(Answer)
    return Answer

def AnswerModifier(answer):
    lines = answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    return '\n'.join(non_empty_lines)  # Modified Answer.

SystemChatBot = [
    {"role": "system", "content": System},
    {'role': 'user', 'content': 'Hi'},
    {"role": "assistant", "content": "Hello, how can I help you?"}
]

def Info():
    data = ""
    current_datetime = datetime.datetime.now()
    day = current_datetime.strftime("%A")
    date = current_datetime.strftime("%d")
    month = current_datetime.strftime("%B")
    year = current_datetime.strftime("%Y")
    hour = current_datetime.strftime("%I")
    minute = current_datetime.strftime("%M")

    data += f"Use this real-time information if needed:\n"
    data += f"Day: {day}\nDate: {date}\nMonth: {month}\nYear: {year}\n"
    data += f"Time: {hour} hours, {minute} minutes\n"
    return data

def RealtimeSearchEngine(prompt):  # sourcery skip: use-join
    global SystemChatBot, messages
    with open(r'Data/ChatLog.json', 'r') as file:
        messages = load(file)
    messages.append({"role": "user", "content": f"{prompt}"})

    SystemChatBot.append({"role": "system", "content": GoogleSearch(prompt)})

    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=SystemChatBot + [{"role" : "system", "content" : Info()}] + messages,
        temperature=0.7,
        max_tokens= 2048,
        top_p=1,
        stream=True,
        stop=None
    )

    Answer = ""
    for chunk in completion:
        if chunk.choices[0].delta.content:
            Answer += chunk.choices[0].delta.content
        
    Answer = Answer.strip().replace("</s>", "")
    messages.append({"role": "assistant" , "content":Answer})

    with open(r"Data/ChatLog.json", 'w') as file:
        dump(messages, file, indent=4)

    SystemChatBot.pop()
    return AnswerModifier(answer=Answer)


if __name__ == "__main__":
    while True:
        prompt = input("\nEnter your Query: ")
        print() 
        print(RealtimeSearchEngine(prompt))
        
            
            