from Frontend.GUI import (GraphicalUserInerface, SetAssistantStatus,
                          ShowTextToScreen, TempDirectoryPath, 
                          SetMicrophoneStatus, AnswerModifier,
                          QueryModifier, GetAssistantStatus, GetMicrophoneStatus)

from Backend.Model import FirstLayerDMM
from Backend.RealtimeSearchEngine import RealtimeSearchEngine
from Backend.Automation import Automation
from Backend.SpeechToText_edge import SpeechRecognition
from Backend.Chatbot import ChatBot
from Backend.TextToSpeech import TextToSpeech
from Backend.Model import keywords
#----------------------------------------------------------------------------------

# Other Requirements
from dotenv import dotenv_values
from asyncio import run
from time import sleep
import subprocess
import threading
import json
import os

env_vars = dotenv_values('.env')
Username = env_vars.get('Username')
Assistantname = env_vars.get('Assistantname')
DefaultMessage = f'''
{Username} : Hello {Assistantname}, How are You.
{Assistantname} : Hi {Username}, I am doing Good, So what's your first command?'''

subprocesses = list()
functions = ['open', 'close', 'play', 'system', 'content', 'google search', 'youtube search']#keywords.copy()

def ShowDefaultChat(): # This is Helpful when the ChatLog.json is Empty and New Chat is started.
    file = open(r'Data\ChatLog.json', 'r', encoding='utf-8')
    if len(file.read())<5:
        with open(TempDirectoryPath('Database.data'), 'w', encoding='utf-8') as file:
            file.write("")
        with open(TempDirectoryPath('Database.data'), 'w', encoding='utf-8') as file:
            file.write(DefaultMessage)
    file.close()
def ReadChatLogJson():
    with open(r'Data\ChatLog.json', 'r', encoding='utf-8') as file:
        chat_data = json.load(file)
    return chat_data

def ChatLogIntegration():
    json_data = ReadChatLogJson()
    formatted_chatlog = ""
    for entry in json_data:
        if entry['role'] == 'user':
            formatted_chatlog += f"User: {entry['content']}\n"
        elif entry['role'] == 'assistant':
            formatted_chatlog += f"Assistant: {entry['content']}\n"
    
    formatted_chatlog = formatted_chatlog.replace("User", Username+" ")
    formatted_chatlog = formatted_chatlog.replace("Assistant", Assistantname+" ")

    with open(TempDirectoryPath("Database.data"), 'w', encoding='utf-8') as file:
        file.write(AnswerModifier(formatted_chatlog))

def ShowChatsOnGUI():
    file = open(TempDirectoryPath("Database.data"), 'r', encoding='utf-8')
    data = file.read()
    if len(str(data)) > 0:
        lines = data.split('\n')
        result = '\n'.join(lines)
        file.close()
        file = open(TempDirectoryPath('Responses.data'), 'w', encoding='utf-8')
        file.write(result); file.close()

def InitialExecution():
    SetMicrophoneStatus('False')
    ShowTextToScreen("")
    ShowDefaultChat()
    ChatLogIntegration()
    ShowChatsOnGUI()


InitialExecution()

def MainExecution():
    TaskExecution = False
    SetAssistantStatus("Ready to Perform...")

    Query = SpeechRecognition()
    ShowTextToScreen(f"{Username} : {Query}")
    SetAssistantStatus("Thinking...")
    Decision = FirstLayerDMM(Query)

    print("")
    print(f"Decision : {Decision}")
    print("")

    G = any([i for i in Decision if i.startswith("general")])
    R = any([i for i in Decision if i.startswith("realtime")])

    mearged_query = " and ".join(
        [" ".join(i.split()[1:]) for i in Decision if i.startswith('general') or i.startswith('realtime')]
    )

    for queries in Decision:
        if TaskExecution == False:
            if any(queries.startswith(func) for func in functions):
                run(Automation(list(Decision)))
                TaskExecution = True
        
    if G and R or R:
        SetAssistantStatus("Searching...")
        Answer = RealtimeSearchEngine(QueryModifier(mearged_query))
        ShowTextToScreen(f"{Assistantname} : {Answer}")
        SetAssistantStatus("...Answering...")
        TextToSpeech(Answer)
        return True

    else:
        for Queries in Decision:
            if 'general' in Queries:
                SetAssistantStatus("Thinking...")
                QueryFinal = Queries.replace("general ", "")
                Answer = ChatBot(QueryModifier(QueryFinal))
                ShowTextToScreen(f'{Assistantname} : {Answer}')
                SetAssistantStatus("Answering...")
                TextToSpeech(Answer)
                return True
            
            elif 'realtime' in Queries:
                SetAssistantStatus("Searching...")
                QueryFinal = Queries.replace("realtime ", "")
                Answer = ChatBot(QueryModifier(QueryFinal))
                ShowTextToScreen(f'{Assistantname} : {Answer}')
                SetAssistantStatus("Answering...")
                TextToSpeech(Answer)
                return True
            
            elif ('terminate' in Queries) or ('exit' in Queries):
                QueryFinal = "Okay, GoodBye!!"
                Answer = ChatBot(QueryModifier(QueryFinal))
                ShowTextToScreen(f"{Assistantname} : {Answer}")
                SetAssistantStatus("Executing...")
                TextToSpeech(Answer)
                os._exit(1)
            
def FirstThread():
    while True:
        CurrentStatus = GetMicrophoneStatus()
        if CurrentStatus == "True":
            MainExecution()
        
        else:
            AIStatus = GetAssistantStatus()
            if "Available..." in AIStatus:
                sleep(0.1)

            else:
                SetAssistantStatus("Available...")

def SecondThread():
    GraphicalUserInerface()

if __name__ == "__main__":
    thread2 = threading.Thread(target=FirstThread, daemon=True)
    thread2.start()
    SecondThread()

