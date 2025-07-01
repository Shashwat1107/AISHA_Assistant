import requests
from bs4 import BeautifulSoup
from webbrowser import open as webopen
from AppOpener import open as appopen

useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"

# def OpenApp(app, sess=requests.session()):
#     try:
#         if app.lower() == "youtube":
#             webopen("https://www.youtube.com")
#         else:
#             appopen(app, match_closest=True, output=True, throw_error=True)
#         return True
#     except Exception:
#         def extract_links(html):
#             if html is None:
#                 return []
#             soup = BeautifulSoup(html, 'html.parser')
#             results = soup.find_all('a', class_='result__a')
#             return [link.get('href') for link in results]

#         def search_duckduckgo(query):
#             url = f"https://html.duckduckgo.com/html/?q={query}"
#             headers = {'User-Agent': useragent}
#             response = sess.get(url, headers=headers)
#             if response.status_code == 200:
#                 return response.text
#             else:
#                 print("[red]Error: Unable to fetch search results [/red]")
#             return None

#         html = search_duckduckgo(app)
#         links = extract_links(html)
#         if links:
#             webopen(links[0])
#         else:
#             print("[red]No links found[/red]")

#         return True
# OpenApp("Youtube")


"----------------------"
# def search_bing(query):
#     headers = {'User-Agent': useragent}
#     url = f"https://www.bing.com/search?q={query}"
#     response = requests.get(url, headers=headers)
#     soup = BeautifulSoup(response.text, 'html.parser')
#     results = soup.find_all('li', {'class': 'b_algo'})

#     for r in results:
#         link = r.find('a')
#         if link:
#             print("Opening:", link['href'])
#             webopen(link['href'])
#             break
# search_bing("facebook")
"----------------------------------"
from dotenv import dotenv_values
from groq import Groq
env_vars = dotenv_values('.env')

GroqAPI = env_vars.get('GroqAPIKey')
client = Groq(api_key=GroqAPI)

for m in client.models.list().data:
        print(m.id)
