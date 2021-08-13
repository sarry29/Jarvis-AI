import pyttsx3
import pyaudio
import datetime
import speech_recognition as sr

import wikipedia # opening wikipedia search
import webbrowser #opening browser to open a link
import os
import random
import smtplib # for mail
import pyjokes # for jokes
import pywhatkit # for music in utube

from plyer import notification #notification
import requests #fetching data from api
import json #fetch api in json file
import bs4

import os #changing directory , and executing script
import time # for sleep

# windows api for gathering voices
engine = pyttsx3.init('sapi5')
# lower down jarvis voice
newVoiceRate = 175
engine.setProperty('rate',newVoiceRate)

voices = engine.getProperty('voices')
# 2 voices male or female
# print(voices) 
# 0 for daniel and 1 for zira
engine.setProperty('voice',voices[0].id)
# print(voices[0].id)

def speak(audio):
    # string audio is speak by engine 
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)

    if hour>=6 and hour<12 :
        speak("Good Morning !")

    elif hour>=12 and hour<18:
        speak("Good Afternoon !")
    
    elif hour>=18 and hour<=21:
        speak("Good Evening !")
    
    else:
        speak("Good Night !")
    
    speak("I'm Jarvis Sir. Please tell me how may I help you")



def takeCommand():
    '''
    it takes microphone input from user and return string output
    '''
    # audio recognize 
    r=sr.Recognizer()

    # source microphone
    with sr.Microphone() as source:
        print('Listening...')
        # seconds of non-speaking audio before a phrase is considered complete
        r.pause_threshold = 1
        audio=r.listen(source)

    try:
        # google engine used for recognizing
        print("Recognizing...")
        query=r.recognize_google(audio,language='en-in')
        print(f'User said: {query}\n')
    
    except Exception as e:
        # Exception error occur
        # print(e)
        print('Say that again please...')
        speak('Sir,Please Say that again')
        return 'None'
    return query


def sendEmail(to,content):
    '''
    TO send mail
    '''
    server=smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    # mail,password(sender side)
    server.login('omjain1290@gmail.com','omjain1290')
    # sender , reciever ,content
    server.sendmail('omjain1290@gmail.com',to,content)
    server.close

# request , notification
def getData(url):
    r = requests.get(url)
    return r

def notifyMe(title , message):
    notification.notify(
        title=title , 
        message = message,
        app_icon = 'C:\project\jarvisAI\covid.ico' ,
        timeout = 40
        )

def notifyData(query):
    data = getData('https://api.apify.com/v2/key-value-stores/toDWvRj1JpTXiM8FF/records/LATEST?disableRedirect=true')
    ans=data.json()['regionData']
    # print(ans)

    region1=[]
    acase1 =[]
    newDeceased1=[]
    newRecovered1=[]
    totalInfected1=[]

    for a in ans:
        region1.append(a['region'])
        acase1.append( a['activeCases'])
        newDeceased1.append( a['newDeceased'])
        newRecovered1.append( a['newRecovered'])
        totalInfected1.append( a['totalInfected'])

    data={}
    for a in range(len(region1)):
        data[region1[a]]=[acase1[a],newDeceased1[a],newRecovered1[a],totalInfected1[a]]

    for a in range(len(region1)):
        
        check=region1[a].lower()

        if check in query:
            ntitle='Covid-19 Cases in '+region1[a]
            lis = data.get(region1[a])
            ntext=f"Active Cases : {lis[0]} \n Death : {lis[1]} \n Cured : {lis[2]} \n Total Infected : {lis[3]}"
            notifyMe(ntitle,ntext)
            speak(ntext)

# Quote of day
def quoteDetail():
    r = getData('https://quotes.rest/qod?language=en')
    data = r.json()
    quote = data['contents']['quotes'][0]['quote']
    author = data['contents']['quotes'][0]['author']
    para = quote[0:230]+'\n -'+author
    notifyMe('Quote of the Day' , para)
    speak(quote+' by '+author)

# Weather of any city
def weather(city):
    # enter city name
    # city = "indore"
    temp=""
    str=""
    try:
        # creating url and requests instance
        url = "https://www.google.com/search?q=weather"+city
        data = requests.get(url).text
        
        # getting raw data
        soup = bs4.BeautifulSoup(data, 'html.parser')
        temp = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text
        str = soup.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text
    except Exception :
        speak('Sir ; Say only name of city ;not country or state or continent or anything irreleavant')
        return 

    # formatting data
    d = str.split('\n')
    time = d[0]
    sky = d[1]
    
    atmDescNotification="Temperature : "+temp+" \nTime :"+time+"\n Atmosphere :"+sky
    weatherNotifyMe(city.title()+' Weather',atmDescNotification)

    atmDescSpeak="Sir, "+city+" temperature is "+temp+" ; at "+time+"and ;the atmosphere is "+sky
    speak(atmDescSpeak)
    # print("Temperature is", temp)
    # print("Time: ", time)
    # print("Sky Description: ", sky)


def weatherNotifyMe(title , message):
    notification.notify(
        title=title , 
        message = message,
        app_icon = 'C:\project\jarvisAI\weather.ico' ,
        timeout = 40
        )

# lyrics singer
def lyrics(title,singer):
    import lyricsgenius

    genius = lyricsgenius.Genius("DM5yB550KcmG111dJsHXpdOBJ4jgxrw-R4odcVfS3F8mnR5BKc08UpvDYzxrBKrq") #API Key

    try:
        song = genius.search_song(title,singer)
        speak("Title of song is; "+song.title)
        speak("Lyrics of song goes like this ; ;"+song.lyrics)
    except Exception:
        speak('Unable to find any result')
        


if __name__ == '__main__':    
    
    wishMe()

    while True:
        query=takeCommand().lower()
        # always  say jarvis before giving commands
        if True:
            # logic for executing task based on query     
            if 'wikipedia' in query or 'tell me something about' in query:
                speak('Searching Wikipedia...')
                
                try:
                    # replace wikipedia with ''
                    query = query.replace('wikipedia','')
                    query = query.replace('tell me something about','')

                    # 2 sentences about query
                    results = wikipedia.summary(query, sentences=2)
                    speak('According to Wikipedia')
                    print(results)
                    speak(results)
                    
                except Exception as e:
                    speak('Sorry sir unable to fetch details')

            # opening websites 
            elif 'open youtube' in query:
                webbrowser.open('youtube.com')
            
            elif 'open google' in query:
                webbrowser.open('google.com')

            elif 'open instagram' in query:
                webbrowser.open('instagram.com')
            
            elif 'open facebook' in query:
                webbrowser.open('facebook.com')
    
            elif 'open stack overflow' in query:
                webbrowser.open('stackoverflow.com')
        
            elif 'open whatsapp' in query:
                webbrowser.open('whatsapp.com')
       
            #play random music/movies    
            elif 'play random music' in query or 'random music' in query:
                music_dir='C:\\Users\\sarry\\Music\\Playlists\\music'
                # double slash (\\) is using to escape from character
                songs=os.listdir(music_dir)
                # print(songs)
                b=[]
                for i in range(len(songs)):
                    b.append(i)
                    
                no=random.choice(b)
                str=songs[no].replace('.mp3','')

                speak(f'Playing song {str}!')
                os.startfile(os.path.join(music_dir, songs[no]))
                # open file open path join and add music_dir and play songs[index]

            elif 'play random movie' in query or 'random movie' in query:
                movie_dir='C:\\Film'
                # double slash (\\) is using to escape from character
                movies=os.listdir(movie_dir)
                # print(songs)
        
                b=[]
                for i in range(len(movies)):
                    b.append(i)

                no=random.choice(b)
                speak(f'Playing movie {movies[no]}!')
                os.startfile(os.path.join(movie_dir, movies[no]))
                # open file open path join and add movie_dir and play movies[index]


            # time
            elif 'time' in query:
                strTime = datetime.datetime.now().strftime('%H:%M:%S')
                speak(f'Sir, The time is {strTime}')

            # open programs
            elif 'open code' in query:
                codepath = "C:\\Users\\sarry\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
                os.startfile(codepath)
            
            elif 'open arduino'  in query or 'open audino' in query:
                arpath = "C:\\Program Files (x86)\\Arduino\\arduino.exe"
                os.startfile(arpath)

            elif 'open chrome' in query:
                chromepath = "C:\\Program Files\\Google\\Chrome\\Application\\Chrome.exe"
                os.startfile(chromepath)
                
            elif 'open firefox' in query:
                firepath = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"
                os.startfile(firepath)

            # search in youtube
            elif 'on youtube' in query:
                query = query.replace('on youtube','')
                query = query.replace('play','')
                pywhatkit.playonyt(query)

            # func email              
            elif 'email' in query:
                email_address=dict(sarry='sarrysingh1290@gmil.com'
                                    ,rabdeep='rabdeepsinghkharbanda29@gmail.com'
                                    ,om='omjain1290@gmail.com'
                                    ,prerana='tprerana6@gmail.com'
                                    ,deepak = 'deepakramchandani8349@gmail.com')
                try:
                    speak('What should I say?')
                    content = takeCommand()
                    to = 'deepakramchandani8349@gmail.com'
                    sendEmail(to, content)
                    speak('Email has been sent successfully!')
                
                except Exception as e:
                    print(e)
                    speak('Sorry unable to sent message at the moment')
            
            # for joke
            elif 'joke' in query:
                speak(pyjokes.get_joke())

            #cases of covid state india 
            elif 'covid cases' in query or 'case' in query or 'cases' in query or '19 case' in query:
                notifyData(query)

            #Secure Vision
            elif 'secure vision' in query or 'security vision' in query:
                speak('Activating Secure Vision System')
                os.chdir(r"C:\project\Secure Vision")
                os.system('python secureVision.py')
            
            #Custom Browser
            elif 'custom browser' in query:
                speak('Opening Custom Browser')
                os.chdir(r"C:\project\CustomBrowser")
                os.system('python cusBrowser.py')

            # Face detection module
            elif 'face recognization' in query or 'face detection' in query or 'phase' in query: 
                speak('Opening Face Detection System')
                os.chdir(r"C:\project\face detector")
                os.system('python facedetector1.py')

            # covid 19 portal 
            elif 'covid portal' in query or 'portal' in query: 
                speak('Opening ;COVID19 PORTAL')

                url = 'http://127.0.0.1:5000/'
                chrome = "C://Program Files//Google//Chrome//Application//chrome.exe %s"
                webbrowser.get(chrome).open(url)
                
                os.chdir(r"C:\project\coronavirus")
                os.system('python CovidDetectorSystem.py')

            # Quotes of the day
            elif 'quote of the day' in query:
                quoteDetail() 
                

            # Some basic Question
            elif 'hello jarvis' in query or 'hello' in query:
                speak('Hello Sir, How are you')
            
            elif 'how are you' in query or 'how is you' in query:
                speak('Sir, I am fine thanks for asking')
            
            elif 'how do you do' in query:
                speak('Fine Sir, Thank You! ,Sir, How\'s you day going')
            
            elif 'day is good' in query or 'i am fine' in query :
                speak('Happy to hear that Sir')

            elif 'who are you' in query or 'are you' in query:
                speak('Sir, I am jarvis ;your personal assistant')
            
            elif 'what can you do' in query or 'what you can do' in query or 'you can do' in query or 'can you do' in query :
                
                speak('Sir, I keep track of the things you care about and , help filter out what you don\'t ;so you can focus on what matters.')
                speak('for example say play random music or movies ;search anything video on youtube ;open programs ;say quote of the day; tells covid cases in india state ;open system or module made by developer ; tells weathers ;  find lyrics of any music; crack a joke')

            
            elif 'who is rabdeep' in query or 'rab deep' in query or 'rab dip' in query or 'sarry'in query or 'sari' in query or 'dip' in query or 'ravdeep' in query or 'steep' in query:
                speak('Rabdeep is my creater and; I help him to do his daily task')

            # weather
            elif 'weather' in query or 'temperature in' in query or 'weather in' in query:
                lis=query.split();
                weather(lis[-1])

            # lyrics
            elif 'lyrics' in query or  'lyrics' in query or 'find lyrics' in query or 'find lyric' in query or 'speak lyrics' in query or 'say lyrics' in query:
                speak('Please say singer and title of the song')
                songQry=takeCommand().lower()
                songQry=songQry.split('by')
                lyrics(songQry[0],songQry[1])

            #wait for a minute
            elif 'seconds' in query or 'second' in query:
                a=query.split()
                if 'a second' in query or 'a seconds' in query:
                    speak('Ok sir!')
                    time.sleep(30)

                elif 'couple of second' in query or 'couple of seconds' in query:   
                    speak('Ok sir!')
                    time.sleep(40)                  
                else:  
                    speak('Ok sir!')
                    time.sleep(int(a[-2]))    
            
            elif 'minute' in query or 'minutes' in query:
                a=query.split()
                if 'a minute' in query or 'a minutes' in query:
                    speak('Ok sir!')
                    time.sleep(60)    
                
                elif 'couple of minute' in query or 'couple of minutes' in query:
                    speak('Ok sir!')
                    time.sleep(60*2)
                
                else:
                    speak('Ok sir!')
                    time.sleep(60*int(a[-2]))    
            
            elif 'hour' in query or 'hours' in query:
                a=query.split()
                if 'an hour' in query or 'an hours' in query:
                    speak('Ok sir!')
                    time.sleep(60*60)    
                
                elif 'couple of hour' in query or 'couple of hours' in query:
                    speak('Ok sir!')
                    time.sleep(60*60*2)
                
                else:
                    speak('Ok sir!')
                    time.sleep(60*60*int(a[-2]))

            # system functionality
            elif 'shutdown' in query:
                speak('Shutting Down the System')
                os.system("shutdown /s /t 1")

            # exit  
            elif 'exit' in query or 'close' in query:
                speak('Thank You! Sir, Have a nice day')
                break

            else:
                if query!='none':
                    speak('Sir , I cannot understand')

# news
