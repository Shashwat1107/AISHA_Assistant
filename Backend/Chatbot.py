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

messages = [] # to store chat messages


System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which also has real-time up-to-date information from the internet.
*** Do not tell time until I ask, be brief and specific to the topic and commands.***
*** Be concise and to the point, do not repeat yourself.***
*** Reply only in English, even if the question is in Hindi, reply in English.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
""" # System message that provides context to the AI Chatbot about its 

SystemChatBot = [
    {"role": "system", "content": System}
]

try:
    with open(r"Data/ChatLog.json", 'r') as file:
        messages = load(file)

except FileNotFoundError:
    with open(r"Data/ChatLog.json", 'w') as file:
        dump([], file)

def RealtimeInformation():
    current_datetime = datetime.datetime.now()
    day = current_datetime.strftime("%A")
    date = current_datetime.strftime("%d")
    month = current_datetime.strftime("%B")
    year = current_datetime.strftime("%Y")
    hour = current_datetime.strftime("%I")
    minute = current_datetime.strftime("%M")
    # second = current_datetime.strftime("%S")

    #Format info str
    data = f"Please use this real-time information if needed, \n"
    data += f"Day: {day}\nDate: {date}\nMonth: {month}\nYear: {year}\n"
    data += f"Time: {hour}{minute} HOURS\n"
    return data

def AnswerModifier(answer):
    lines = answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    return '\n'.join(non_empty_lines) # Modified Answer.

def ChatBot(query):  # sourcery skip: extract-method, use-join
    '''This func sends the user's query to the chatbot and returns the AI's Response.
    This is the View part of the proj.'''

    try:
        #Loading the existing chat messages
        with open(r"Data/ChatLog.json", 'r') as file:
            messages = load(file)
        messages.append({"role": "user", "content": f"{query}"})

        # Make a request to the Groq API for a response
        completion = client.chat.completions.create(
            model = "llama3-70b-8192",
            messages = SystemChatBot + [{"role":"system", "content": RealtimeInformation()}] + messages,
            max_tokens = 1024, # limit the max tokens in the response.
            temperature=0.7, # Response Randomness (higeher means more random)
            top_p=1,
            stream=True, # Stream the response
            stop=None
        )
        Answer = ''
        
        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content # Check if there's content in the current chunk
                # print(chunk.choices[0].delta.content, end='', flush=True)
        Answer = Answer.replace("</s>","") # remove the unwanted

        # Append the AI's response to the chat messages
        messages.append({"role": "assistant", "content": Answer})

        with open(r"Data/ChatLog.json", 'w') as file:
            dump(messages, file, indent=4) # Save the updated chat messages

        return AnswerModifier(Answer) # Return the modified answer
    except Exception as e:
        print(f"Error: {e}")
        with open(r"Data\ChatLog.json", 'w') as file:
            dump([], file, indent=4) # Reset the chat log on error
        return ChatBot(query)
    
if __name__ == "__main__":
    while True:
        user_input = input("Enter your query: ")
        print(ChatBot(user_input))
        print()

