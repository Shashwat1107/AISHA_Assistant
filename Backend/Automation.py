from AppOpener import close,open as appopen
from webbrowser import open as webopen
from pywhatkit import search, playonyt
from dotenv import dotenv_values
from bs4 import BeautifulSoup
from rich import print
from groq import Groq
import webbrowser
import requests
import subprocess
import keyboard
from volume_control import VolumeController
import asyncio
import os

env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey", "")

#Define CSS Classes for parsing specific elements in HTML contnent
classes = [ "zCubwf", "hgKElc", "LTKOO sY7ric", "Z0LcW", "gsrt vk_bk FzvWSb YwPhnf", "pclqee", "tw-Data-text tw-text-small tw-ta", "IZ6rdc", "O5uR6d LTKOO",
           "vlzY6d", "webanswer-webanswers_table__webanswer-table", "dDoNo ikb4Bb gsrt", "sXLaOe",
           "LWkfKe", "VQF4g", "qv3Wpe", "kno-rdesc", "SPZz6b"]

useragent = "Edg/137.0.3296.83 Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/89.0.142.86"

client = Groq(api_key=GroqAPIKey)

professional_responses = [
    "Your satisfaction is our priority. If you have any further questions or need additional assistance, just ask",
    "I am in your hands, please let me know how I can assist you further",
]

messages = []

SystemChatBot = [{"role": "system", "content": f"Hello, I am {os.environ['Username']}, You are a content writer. You have to write content like letters, paragraphs, reports, essays, etc."}]

def GoogleSearch(Topic):
    search(Topic)
    return True

def Content(Topic):
    def OpenNotepad(File):
        default_text_editor = 'notepad.exe'
        subprocess.Popen([default_text_editor, File])
    
    def ContentWriterAI(prompt):
        messages.append({"role": "user", "content": f"{prompt}"})

        completion = client.chat.completions.create(
            model='mixtral-8x7b-32768',
            messages=messages,
            max_tokens=2048,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None
        )
        Answer = ""

        for chunck in completion:
            if chunck.choices[0].delta.content:
                Answer += chunck.choices[0].delta.content
        
        Answer = Answer.replace("</s>", "")
    
    Topic = Topic.replace("Content ", "")
    ContentByAI = ContentWriterAI(Topic)

    with open(rf"Data\{Topic.lower().replace(' ', '_')}.txt", "w", encoding="utf-8") as file:
        file.write(ContentByAI)
    
    OpenNotepad(rf"Data\{Topic.lower().replace(' ', '_')}.txt")
    return True

def YoutubeSearch(Topic):
    Url4srch = f"https://www.youtube.com/results?search_query={Topic}"
    webbrowser.open(Url4srch)
    return True

def PlayOnYoutube(Topic):
    try:
        if Topic.__contains__("Hanuman Chalisa"):
            webbrowser.open("https://www.youtube.com/watch?v=1Uh03H6R23g&list=RD1Uh03H6R23g&start_radio=1")
        elif Topic.__contains__("Bajrang Baan"):
            webbrowser.open("https://youtu.be/dXl2NdlmeIE?si=nL8STeQ4RcDwy1vZ")
        else:
            playonyt(Topic)
        return True
    except Exception as e:
        print(f"[red]Error playing on YouTube: {e}[/red]")
        return False # Example usage, can be removed later
def OpenApp(app):
    try:
        if app.lower() == "youtube":
            webopen("https://www.youtube.com", new=0)
        else:
            appopen(app, match_closest=True, output=True, throw_error=True)
        return True
    except Exception:
        headers = {'User-Agent': useragent}
        url = f"https://www.bing.com/search?q={app}"
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.find_all('li', {'class': 'b_algo'})

        for r in results:
            link = r.find('a')
            if link:
                print("Opening:", link['href'])
                webopen(link['href'], new=0)
                break
def CloseApp(app):

    if 'edge' in app.lower() or 'MS Edge' in app.lower():
        pass # Don't close the Browser.
    else:
        try:
            close(app, match_closest=True, output=True, throw_error=True)
            return True
        except:
            return False

def System(command):
    command = command.lower()
    volume = VolumeController()
    
    if command == 'mute':
        volume.mute()
    elif command == 'unmute':
        volume.unmute()
    elif command in ('volume up', 'increase volume'):
        volume.volume_up()
    elif command in ('volume down', 'decrease volume'):
        volume.volume_down()
    elif command == 'increase volume a bit':
        volume.volume_up_a_bit()
    elif command == 'decrease volume a bit':
        volume.volume_down_a_bit()
    elif command == 'full volume':
        volume.volume_to(1.0)
    if command == 'shut down computer':
        os.system("shutdown /s /t 1")
    elif command == 'minimize all':
        keyboard.send('win + d')
async def TranslateAndExecute(commands: list[str]):
    """
    "exit", "general", "realtime", "open", "close", "play", "pause",
    "next", "previous", "volume up", "increase volume", "decrease volume","volume down",
    "generate image", "system", "content", "google search", "search", "youtube search",
    "reminder",

    "close window", "close tab", "minimize all", "shut down computer"
    """
    funcs = []
    for command in commands:
        if command.startswith("open"):
            if "open it" in command:
                pass
            if "open file" == command:
                pass
            else:
                fun = asyncio.to_thread(OpenApp, command.removeprefix("open "))
                funcs.append(fun)
        elif command.startswith("general"):
            pass
        elif command.startswith("realtime"):
            pass
        elif command.startswith("close "):
            fun = asyncio.to_thread(CloseApp, command.removeprefix("close "))
            funcs.append(fun)

        elif command.startswith("content "):
            fun = asyncio.to_thread(Content, command.removeprefix("content "))
            funcs.append(fun)
        elif command.startswith("google ") or command.startswith("google search "):
            fun = asyncio.to_thread(GoogleSearch, command.removeprefix("google ").removeprefix("search "))
            funcs.append(fun)
        elif command.startswith("youtube search "):
            fun = asyncio.to_thread(YoutubeSearch, command.removeprefix("youtube search "))
            funcs.append(fun)
        
        elif command.startswith("system "):
            fun = asyncio.to_thread(System, command.removeprefix("system "))
            funcs.append(fun)
        else:
            print(f"NO function found for command: {command}")
    
    results = await asyncio.gather(*funcs)

    for result in results:
        if isinstance(result, str):
            yield result
        else:
            yield str(result)
    
async def Automation(commands: list[str]):
    async for result in TranslateAndExecute(commands):
        pass
    return True



