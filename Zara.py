import speech_recognition as sr
import pyttsx3
import warnings
import datetime
import calendar
import pyttsx3 as tts
import wikipedia
import enchant
from enchant.checker import SpellChecker
from playsound import playsound
import random
from bs4 import BeautifulSoup
import requests
import webbrowser
import wolframalpha
import subprocess
import json
import warnings
from json import (load as jsonload, dump as jsondump)
from os import path

warnings.filterwarnings('ignore')

engine = pyttsx3.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', 250)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.runAndWait()
now = int(datetime.datetime.now().hour)

def wakeWord(text):
    WAKE_WORDS = ['hello'] 
    text = text.lower()
    for phrase in WAKE_WORDS:
        if phrase in text:
            return True
    return False

def is_in_english(quote):
    d = SpellChecker("en_US")
    d.set_text(quote)
    errors = [err.word for err in d]
    return False if ((len(errors) > 4) or len(quote.split()) < 3) else quote

def is_english_word(word):
    d = enchant.Dict("en_US")
    t=d.check(word)
    if t==True:
        return word
    else:
        return False    

def getdate():
    now = datetime.datetime.now()
    datestime = now.strftime("%m/%d/%Y, %I:%M:%S")
    year = now.strftime("%Y")
    my_date=datetime.datetime.today()
    weekday=calendar.day_name[my_date.weekday()]
    monthnum=now.month
    daynum=now.day
    monthname=['JANUARY','FEBRAURY','MARCH','APRIL','MAY','JUNE','JULY','AUGUST','SEPTEMBER','OCTOBER','NOVEMBER','DECEBER']
    datenum=['1st','2nd','3rd','4th','5th','6th','7th','8th','9th','10th','11th','12th','13th','14th','15th','16th','17th','18th','19th','20th','21st','22nd','23rd','24th','25th','26th','27th','28th','29th','30th','31st']
    return 'TODAY IS '+weekday+' '+monthname[monthnum-1]+' '+datenum[daynum-1]+' '+year+'.......'+datestime+''

def getperson(text):
    wordlist=text.split()
    for i in range(0,len(wordlist)):
        if i+3<=len(wordlist)-1 and wordlist[i].lower=='who' and wordlist[i+1].lower()=='is':
            return wordlist[i+2]+' ' +wordlist[i+3]

def takeCommand():
    required = 0
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        if "pulse" in name:
            required = index
    r=sr.Recognizer()
    with sr.Microphone(device_index=required) as source:
        r.adjust_for_ambient_noise(source)
        audio=r.listen(source,phrase_time_limit=7)
        try:
            statement=r.recognize_google(audio,language='en-US')
            print(f"you said: {statement}\n")
        except Exception as e:
            return "None"
        return statement
    

    
def speak(text):
    engine.say(text)
    engine.runAndWait()


while True:
    required = 0
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        if "pulse" in name:
            required = index
    r = sr.Recognizer()
    with sr.Microphone(device_index=required) as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source,phrase_time_limit=10)
        
        try:
            task = r.recognize_google(audio,language='en-US')
            print("Listening.....")
            print(f"You Said: {task} \n")
            engine.say(task)
            if(wakeWord(task) == True):
                if now >= 0 and now < 12:
                    engine.say("Good morning sir")
                    engine.runAndWait()
                    print("Good Morning sir")
                    
                elif now >= 12 and now < 16:
                    engine.say("good afternoon sir")
                    engine.runAndWait()
                    print("Good Afternoon sir")
                elif now >= 16 and now < 21:
                    engine.say("Good Evening sir")
                    engine.runAndWait()
                    print("Good Evening sir")
                else:
                    engine.say("Good Night sir")
                    engine.runAndWait()
                    print("Good Night sir")
                    
                print("i am Alin your personal assistant")
                engine.say("i am alin your personal assistant")
                print("What can can i do for you ?")
                engine.say("What can i do for you ?")
                engine.runAndWait()
                
            elif 'wikipedia' in task.lower():
                try:
                    engine.say('Searching Wikipedia...')
                    task =task.replace("wikipedia", "")
                    results = wikipedia.summary(task, sentences=3)
                    print("According to Wikipedia")
                    engine.say("According to Wikipedia")
                    print(results)
                    engine.say(results)
                    engine.say("Do you wanna know more about {}".format(task))
                    engine.runAndWait()
                    r = sr.Recognizer()
                    with sr.Microphone() as source:
                        playsound('D:\double-beep.mp3')
                        audios = r.listen(source)
                        prompt = r.recognize_google(audios)
                        try:
                            if "please" in prompt.lower() or "sure" in prompt.lower() or "yes" in prompt.lower():
                                result = wikipedia.summary("{}".format(task),sentences=3)
                                engine = tts.init()
                                engine.say(result)
                                engine.runAndWait()
                            else:
                                engine = tts.init()
                                engine.say("Okay")
                                engine.runAndWait()
                        except:
                            engine = tts.init()
                            engine.say("Okay")
                            engine.runAndWait()
                except wikipedia.exceptions.DisambiguationError as e:
                    s = random.choice(e.options)
                    print(s)
                    engine.say(s)
                except wikipedia.exceptions.WikipediaException as e:
                    print('Search not include, try again wikipedia and your search')
                else:
                    continue
            
            elif "weather" in task.lower() or "climate" in task.lower():
                print("Whats the city name")
                engine.say("whats the city name")
                city_name= takeCommand()
                api_key="394d4ebf0a7de20604147666d665d2d0"
                base_url="https://api.openweathermap.org/data/2.5/weather?"
                complete_url=base_url+"appid="+api_key+"&q="+city_name
                response = requests.get(complete_url)
                x=response.json()
                if x["cod"]!="404":
                    y=x["main"]
                    w=x["wind"]
                    z = x["weather"] 
                    c=x["coord"]
                    cl=x["clouds"]
                    current_temperature = y["temp"]
                    current_wind=w["speed"]
                    current_lat=c["lat"]
                    current_lon=c["lon"]
                    current_cloud=cl["all"]
                    current_maxtemp=y["temp_max"]
                    current_humidiy = y["humidity"]
                    weather_description = z[0]["description"]
                    celsius= current_temperature - 273.15
                    maxcelsius=current_maxtemp - 273.15
                    
                    print(city_name +
                          " Temperature in kelvin unit = "+ str(current_temperature) +
                          "\n Humidity (in percentage) = " + str(current_humidiy) +
                          "\n Weather Description  " + str(weather_description) 
                          )
                    print("Temperature in celsius:",celsius )
                    print( "Wind speed:",current_wind)
                    print( "Longitude:",current_lon)
                    print("Latitude:",current_lat)
                    print("Clouds:",current_cloud)
                    print("Max Temperature:",current_maxtemp)
                    
                    engine.say(city_name+
                          "Temperature in kelvin unit is"+ str(current_temperature) +
                          "\n Humidity in percentage is " + str(current_humidiy) +
                          "\n Weather Description  " + str(weather_description)
                          )
                    engine.say("Temperature in celsius " +str(celsius)+"celsius")
                    engine.say("Wind speed: "+str(current_wind)+"miles per minute")
                    engine.say( "Longitude:"+str(current_lon)+"degree")
                    engine.say("Latitude:"+str(current_lat)+"degree")
                    engine.say("Clouds:"+str(current_cloud)+"percentage")
                    engine.say("Max Temparature:"+str(maxcelsius)+"celsius")
                    
                    engine.runAndWait()
                else:
                    print(" City Not Found\n")
                    engine.say(" City Not Found ")
                    engine.runAndWait()
                    
            elif "goodbye" in task.lower() or "ok bye" in task.lower() or "stop" in task.lower() or "bye" in task.lower():
                print('Your virtual assistant Alin is shutting down,Good bye')
                engine.say('your virtual assistant Alin is shutting down,Good bye')
                engine.runAndWait()
                break
            
            elif 'open google' in task.lower() or "google" in task.lower():
                webbrowser.open_new_tab("https://www.google.com")
                print("Google chrome is open now")
                engine.say("Google chrome is open now")
                engine.runAndWait()
                
            elif 'time' in task.lower():
                strTime=datetime.datetime.now().strftime("%H:%M:%S %d-%m-%Y")
                print(f"The time and date is {strTime}")
                engine.say(f"the time and date is {strTime}")
                engine.runAndWait()
                
            elif "open facebook" in task.lower() or "facebook" in task.lower():
                webbrowser.open_new_tab("https://www.facebook.com/")
                print("Facebook is open now")
                engine.say("Facebook is open now")
                engine.runAndWait()

            elif 'news' in task.lower() or "tell news" in task.lower():
                news = webbrowser.open_new_tab("https://edition.cnn.com/")
                print('Here are some headlines from the CNN,Happy reading')
                engine.say('Here are some headlines from the CNN,Happy reading')
                url1 = ("https://edition.cnn.com")
                url2 = ("https://timesofindia.indiatimes.com")
                page1 = requests.get(url1)
                page2 = requests.get(url2)
                soup=BeautifulSoup(page1.content,'html.parser')
                soup=BeautifulSoup(page2.content,'html.parser')
                a=soup.find_all("figcaption")
                c=soup.find_all("figcaption")
                b1=(a[0].get_text())
                b2=(a[1].get_text())
                b3=(a[2].get_text())
                b4=(a[3].get_text())
                
                d1=(c[0].get_text())
                d2=(c[1].get_text())
                d3=(c[2].get_text())
                d4=(c[3].get_text())
                
                print("INTERNATIONAL NEWS")
                engine.say("INTERNATIONAL NEWS")
                print(b1)
                print(b2)
                print(b3)
                print(b4)
                engine.say(b1)
                engine.say(b2)
                engine.say(b3)
                engine.say(b4)
                engine.runAndWait()
                print("REGIONAL NEWS")
                engine.say("REGIONAL NEWS")
                print(d1)
                print(d2)
                print(d3)
                print(d4)
                engine.say(d1)
                engine.say(d2)
                engine.say(d3)
                engine.say(d4)
                engine.runAndWait()

            elif 'search'  in task.lower():
                task = task.replace("search", "")
                webbrowser.open_new_tab(task)
                print('Here is your search')
                engine.say('Here is your search')
                engine.say("Do you wanna know more about {}".format(task))
                engine.runAndWait()
                r = sr.Recognizer()
                with sr.Microphone() as source:
                    playsound('D:\double-beep.mp3')
                    audios = r.listen(source)
                    prompt = r.recognize_google(audios)
                    try:
                        if "please" in prompt.lower() or "sure" in prompt.lower() or "yes" in prompt.lower():
                            result = wikipedia.summary("{}".format(task),sentences=3)
                            engine = tts.init()
                            engine.say(result)
                            engine.runAndWait()
                        else:
                            engine = tts.init()
                            engine.say("Okay")
                            engine.runAndWait()
                    except:
                        engine = tts.init()
                        engine.say("Okay")
                        engine.runAndWait()
                    
                
            elif "what" in task.lower() or "where" in task.lower() or "how" in task.lower() or "do " in task.lower() or "why " in task.lower() or "when" in task.lower() or "which" in task.lower():
                webbrowser.open_new_tab(task)
                results = wikipedia.summary(task, sentences=2)
                print('Here is your answer')
                engine.say('Here is your answer')
                print(results)
                engine.say(results)
                engine.runAndWait()
                
            elif 'who is' in task.lower():
                person=getperson(task)
                wiki=wikipedia.summary(person,sentences=3)
                response=response + '' +wiki
                print(response)
                engine.say(response)
                engine.runAndWait()
                
            
                
                
            elif "log off" in task.lower() or "sign out" in task.lower() or "shutdown" in task.lower():
                print("Ok , your pc will log off in 10 sec make sure you exit from all applications")
                engine.say("Ok , your pc will log off in 10 sec make sure you exit from all applications")
                subprocess.call(["shutdown", "/l"])
                engine.runAndWait()
            
            elif 'time' in task.lower() or 'in' in task.lower():
                now=datetime.datetime.now()
                meridiem=''
                if now.hour>=12:
                    meridiem="P.M"
                    hour=now.hour-12
                else:
                    meridiem="A.M"
                    hour=now.hour
                if now.minute<10:
                    min='0'+str(now.minute)
                else:
                    min=str(now.minute)
                response=response + '' + 'IT IS '+hour+' : '+min+'..'+meridiem+'..'
                print(response)
                engine.say(response)
                engine.runAndWait()
                
            elif 'date' in task.lower():
                response=getdate()
                print(response)
                engine.say(response)
                engine.runAndWait()
            
            elif 'map' in task.lower() or 'locate' in task.lower() or 'location' in task.lower():
                api_key = "AIzaSyCZObKumZBOPunJFuCfPvEBbloXNP8N16g"
                
                
            

            else:
                engine.say("Can't do it Sorry")
                engine.runAndWait()
                print("Can't do it, Sorry")
                print("Listening.....")
                
                
        except sr.UnknownValueError:
                    print("ALIN can't understand it")
                    engine.say("ALIN can't understand it")
                    engine.runAndWait()
        except sr.RequestError as e:
                    print("Request can't be accepted;{0}".format(e))