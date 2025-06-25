from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import dotenv_values
import os
import mtranslate as mt
import speech_recognition as sr


env_vars = dotenv_values(".env")

InputLang = env_vars.get("InputLanguage")

HtmlCode = \
'''
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Speech Recognition</title>
</head>
<body>
    <button id="start" onclick="startRecognition()">Start Recognition</button>
    <button id="end" onclick="stopRecognition()">Stop Recognition</button>
    <p id="output"></p>
    <script>
        const output = document.getElementById('output');
        let recognition;

        function startRecognition() {
            recognition = new webkitSpeechRecognition() || new SpeechRecognition();
            recognition.lang = '';
            recognition.continuous = true;

            recognition.onresult = function(event) {
                const transcript = event.results[event.results.length - 1][0].transcript;
                output.textContent += transcript;
            };

            recognition.onend = function() {
                recognition.start();
            };
            recognition.start();
        }

        function stopRecognition() {
            recognition.stop();
            output.innerHTML = "";
        }
    </script>
</body>
</html>
'''

HtmlCode = str(HtmlCode).replace("recognition.lang = '';", f"recognition.lang = '{InputLang}'")
with open(r"Data/Voice.html", 'w') as file:
    file.write(HtmlCode)

current_dir = os.getcwd()
Link = f"{current_dir}\Data\Voice.html"

chrome_options = Options()
user_agents = "Edg/137.0.3296.83 Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/89.0.142.86"
chrome_options.add_argument(f'user-agent={user_agents}')
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--use-fake-device-for-media-stream")
chrome_options.add_argument("--headless=new")

service = Service(ChromeDriverManager().install())
driver = webdriver.Edge(service=service, options=chrome_options)

TempDirPath = rf"{current_dir}\Frontend\File"

def SetAssistantStatus(Status):
    with open(rf"{TempDirPath}\Status.data", 'w', encoding='utf-8') as file:
        file.write(Status)
def QueryModifier(Query):
    new_query = Query.lower().strip()
    query_words = new_query.split()
    question_words = [
    "what", "when", "where", "who", "whom", "whose", "which", "why","what's","where's","how's", "how",
    "is", "are", "am", "was", "were", "do", "does", "did", "can you", "could",
    "will", "would", "shall", "should", "may", "might", "have", "has", "had"
      ]
    if any(word + " " in new_query for word in question_words):
      if query_words[-1][-1] in ['.', '?', '!']:
                  new_query = new_query[:-1] + "?"
      else:
                  new_query += "?"
    else:
          if query_words[-1][-1] in ['.', '?', '!']:
                new_query = new_query[:-1] + "?"
          else:
                new_query += '.'

    return new_query.capitalize()

def UniversalTranslator(Text):
      english_trans = mt.translate(Text, 'en-IN', 'auto')
      return english_trans.capitalize()

def SpeechRecognition():
      driver.get(f"file:///{Link}")
      driver.find_element(by=By.ID, value="start").click()
      timeout = 30
      import time
      start = time.time()
      while True:
            try:
                  Text = driver.find_element(by=By.ID, value='output').text
                  if Text:
                        driver.find_element(by=By.ID, value="end").click()

                        if( (InputLang.lower() == "en") or ("en" in InputLang.lower())):
                              return QueryModifier(Text)
                        else:
                              SetAssistantStatus("Translating....")
                              return QueryModifier(UniversalTranslator(Text))
                        
                  if(time.time() - start > timeout):
                        print("Speech Recog timed out.")
                        return ""
            except Exception as e:
                  print("{:-^30}".format("Error"))
                  print(e)
                  print("{:-^30}".format("Error"))
      # recognizer = sr.Recognizer()
      # with sr.Microphone() as source:
      #     print("Listening...")
      #     audio = recognizer.listen(source)
      # try:
      #       text = recognizer.recognize_google(audio, language='en-IN')
      #       if( (InputLang.lower() == "en") or ("en" in InputLang.lower())):
                  
      #             return QueryModifier(Text)
      #       else:
      #             SetAssistantStatus("Translating....")
      #             return QueryModifier(UniversalTranslator(Text))

      # except sr.UnknownValueError:
      #     print("Sorry, I could not understand the audio.")
      #     return ""
      # except sr.RequestError as e:
      #     print(f"Could not request results; {e}")
      #     return ""
      

if __name__ == "__main__":
      while True:
            Text = SpeechRecognition()
            print(Text)