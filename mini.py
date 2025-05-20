import speech_recognition as sr
from logging.config import listen
from datetime import datetime
from datetime import time
import pyttsx3
import webbrowser
import wikipedia
from datetime import date
import pywhatkit as kit
import pyaudio
import os
import pywhatkit
import calendar
import subprocess
import geocoder
import requests
import random




engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voices',voices[0].id)
activationWord = 'computer'

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))


def speak(text, rate = 120):
    engine.setProperty('rate', rate)
    engine.say(text)
    engine.runAndWait()
 

def parse_command():
    listener = sr.Recognizer()
    print('listening for a command')

    with sr.Microphone() as source:
        listener.pause_threshold = 1.5
        input_speech = listener.listen(source)

    try:
        print('Recognizing speech ......')
        query = listener.recognize(input_speech)
        print(f'the input speech was : {query}')

    except Exception as exception:
        print('i did not quite catch that')
        speak('i did not quite catch that')
        print(exception)
        return 'None'
    return query

def search_wikipedia(query =' '):
    searchResults = wikipedia.search(query)
    if not searchResults:
        print('No wikipedia result')
        return 'No result recived'
    try:
        wikiPage = wikipedia.page(searchResults[0])
    except wikipedia.DisambiguationError as error :
       wikiPage = wikipedia.page(error.options[0])
    print(wikiPage.title)
    wikiSummary = str(wikiPage.summary)
    return wikiSummary

def playsong(query = ' '):
    music_dir = r'C:\Users\HP\Desktop\AI MUSIC'
    songs = os.listdir(music_dir)
    os.startfile(os.path.join(music_dir, songs[0]))



def play_youtube_music(song_name):
    kit.playonyt(song_name)


def show_current_date():
    current_date = date.today().strftime('%Y-%m-%d')
    return f'Current date is: {current_date}'


def show_current_time():
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return f'Current time is: {current_time}'


def show_current_calendar():
    current_month_calendar = calendar.month(datetime.now().year, datetime.now().month)
    return f'Calendar for the current month:\n{current_month_calendar}'


def show_current_weekday():
    current_weekday = datetime.now().strftime('%A')
    return f'Today is {current_weekday}'


def get_current_temperature(city='Dehradun', country='India', api_key='c7fe367ad440dcbbc437fd17c84ccbb4'):
    base_url = r"http://api.openweathermap.org/data/2.5/weather"
    
    params = {
        'q': f'{city},{country}',
        'appid': api_key,
        'units': 'metric',  
    }
    
    response = requests.get(base_url, params=params)
    data = response.json()
    
    if response.status_code == 200:
        temperature = data['main']['temp']
        return f'Current temperature in {city}, {country}: {temperature}°C'
    else:
        return 'Unable to fetch the temperature.'




def get_current_location():
    try:
        location = geocoder.ip('me')
        return location
    except Exception as e:
        print(f"Error getting location: {e}")
        return None



def open_application1(application_name):
    try:
        subprocess.run([application_name], check=True)
        print(f"{application_name} opened successfully!")
    except Exception as e:
        print(f"Error opening {application_name}: {e}")



def get_weather(api_key, city):
    base_url = r"http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric', 
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if response.status_code == 200:
            weather_description = data['weather'][0]['description']
            temperature = data['main']['temp']
            return f"The weather in {city} is {weather_description} with a temperature of {temperature}°C."
        else:
            return "Unable to fetch weather information."

    except Exception as e:
        return f"Error: {e}"




def get_music_recommendation(api_key):
    base_url = r"http://ws.audioscrobbler.com/2.0/"
    method = "chart.gettoptracks"
    format_type = "json"

    params = {
        'method': method,
        'api_key': api_key,
        'format': format_type,
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if response.status_code == 200 and data.get('tracks') and data['tracks'].get('track'):
            random_track = random.choice(data['tracks']['track'])
            track_name = random_track['name']
            artist_name = random_track['artist']['name']
            return f"I recommend the song: {track_name} by {artist_name}"
        else:
            return "Unable to fetch music recommendation."

    except Exception as e:
        return f"Error: {e}"


def get_movie_recommendation(api_key):
    base_url = r"https://api.themoviedb.org/3"
    discover_url = f"{base_url}/discover/movie"
    random_page = random.randint(1, 100) 

    params = {
        'api_key': api_key,
        'page': random_page,
    }

    try:
        response = requests.get(discover_url, params=params)
        data = response.json()

        if response.status_code == 200 and data.get('results'):
            random_movie = random.choice(data['results'])
            title = random_movie['title']
            overview = random_movie['overview']
            return f"I recommend the movie: {title}\nOverview: {overview}"

        else:
            return "Unable to fetch movie recommendation."

    except Exception as e:
        return f"Error: {e}"

def send_whatsapp_message(number, message, hours, minutes):
    try:
        pywhatkit.sendwhatmsg(f"+{number}", message, hours, minutes)
        print(f"Message sent to {number} on WhatsApp!")
    except Exception as e:
        print(f"Error sending message: {e}")


def open_application(application_name):
    
    applications = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "chrome":"chrome.exe",
        "word" : "WINWORD.EXE",
        "powerpoint" : "POWERPNT.EXE",
        "Excel" : "excel.exe",
        


    }

    
    if application_name.lower() in applications:
        try:

            subprocess.Popen(applications[application_name.lower()], shell=True)
            print(f"Opening {application_name}")
        except Exception as e:
            print(f"Error opening application: {e}")
    else:
        print(f"Application '{application_name}' not found")




if __name__ == '__main__':
    speak('All system nominal...')
    print("hello__I am Jarvish")
    print("How I help you.....???")

    while True:

        query = parse_command().lower().split()

        if query[0] == activationWord:
            query.pop(0)

            if query[0] == 'speak':
                if 'hello' in query:
                    speak('Greeting , All.')
                    print('Greeting,All..')
                else:
                    query.pop(0)
                    speech = ' '.join(query)
                    speak(speech)


            if query[0] == 'go' and query[1] == 'to':
                speak('Opening....')
                query = ' '.join(query[2:])
                webbrowser.get('chrome').open_new(query)
             
            if "search" in query:
                query = ' '.join(query[1:])
                speak('Quering the universal databank')
                print(search_wikipedia(query))
                speak(search_wikipedia(query))
            

            if query[0] == 'play':
                song_name = ' '.join(query[1:])
                print(f'Playing {song_name} from YouTube...')
                play_youtube_music(song_name)

            
            if "date" in query:
                 speak(show_current_date())
                 print(show_current_date())
           
            
            if "time" in query:
                speak(show_current_time())
                print(show_current_time())
           
            
            if  query[0] == 'open' and query[1] == 'calender':
              print(show_current_calendar())
 
            if  "day" in query:
              speak(show_current_weekday())
              print(show_current_weekday())
            
            if "temperature" in query:
              speak(get_current_temperature())
              print(get_current_temperature())


            if  "message" in query:
              number = input("Enter the recipient's phone number (without '+'): ")
              message = input("Enter the message: ")
              hours = int(input("Enter the hours to send the message: "))
              minutes = int(input("Enter the minutes to send the message: "))
              send_whatsapp_message(number, message, hours, minutes)

           

 
            if  "location" in query:
               current_location = get_current_location()
               if current_location:
                 print(f"Your current location is: {current_location}")
                 speak(f"Your current location is: {current_location}")
               else:
                 print("Unable to retrieve current location.")
            
               
            
            if  "weather" in query:
              api_key = 'c7fe367ad440dcbbc437fd17c84ccbb4'
              city = "Dehradun"
              print(get_weather(api_key, city))
              speak(get_weather(api_key, city))
    

            
            if query[0]== "recommend"  and  query[1] == "music":
              api_key = '5b49de27e95020de2ac359df112f77cc'
              speak(get_music_recommendation(api_key))  
              print(get_music_recommendation(api_key))

            if query[0]== "recommend" and query[1] == "movie":
               api_key = 'ce77607f23feefd7b486c18b63bf2875'  
               print(get_movie_recommendation(api_key))
               speak(get_movie_recommendation(api_key))
   

        
            if query[0].lower() == "open":
              application_name = ' '.join(query[1:])
              open_application(application_name)

 

