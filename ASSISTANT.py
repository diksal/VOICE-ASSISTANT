import mysql.connector as sql
import speech_recognition as sr
import os
import pyttsx3 as p
from datetime import datetime as d
import webbrowser as web
import time
import wolframalpha
from playsound import playsound


appId = "#please enter your wolfram app id"
client = wolframalpha.Client(appId)

def add(query,output):
  con = sql.connect(host='localhost',user='root',passwd='*********',database='voice_search')
  cursor = con.cursor()
  tw = str(d.now().strftime("%Y-%m-%d %H:%M:%S"))
  data = (("insert into searches values('%s','%s','%s')") % (query,tw,output))
  cursor.execute(data)
  con.commit()
  con.close()

def search(text):
  res = client.query(text)
  # Wolfram cannot resolve the question
  if res['@success'] == 'false':
     print('Question cannot be resolved')
  # Wolfram was able to resolve question
  else:
    result = ''
    # pod[0] is the question
    pod0 = res['pod'][0]
    # pod[1] may contains the answer
    pod1 = res['pod'][1]
    # checking if pod1 has primary=true or title=result|definition
    if (('definition' in pod1['@title'].lower()) or ('result' in  pod1['@title'].lower()) or (pod1.get('@primary','false') == 'true')):
      # extracting result from pod1
      result = resolveListOrDict(pod1['subpod'])
      speak(result)
      print(result)
      question = resolveListOrDict(pod0['subpod'])
      question = removeBrackets(question)
      
    else:
      # extracting wolfram question interpretation from pod0
      question = resolveListOrDict(pod0['subpod'])
      # removing unnecessary parenthesis
      question = removeBrackets(question)
def removeBrackets(variable):
  return variable.split('(')[0]

def resolveListOrDict(variable):
  if isinstance(variable, list):
    return variable[0]['plaintext']
  else:
    return variable['plaintext']      


def removeBrackets(variable):
  return variable.split('(')[0]

def resolveListOrDict(variable):
  if isinstance(variable, list):
    return variable[0]['plaintext']
  else:
    return variable['plaintext']

def start():
  h = int(d.now().strftime("%H"))
  if h>-1 and h<12:
      speak('GOOD MORNING, USER')
  elif h>11 and h<17:
      speak('GOOD AFTERNOON, USER')
  else:
      speak('GOOD EVENING, USER')
  print('''YOU CAN
USE GOOGLE ; USE YOUTUBE ; USE CURRENT AFFAIRS ; USE CURRENT TIME ; USE CLOSE ; USE HELLO ; USE SLEEP ASSISTANT ; USE SEARCH ; USE HOW TO USE YOU ; USE WHO CREATED YOU ; ....e.t.c.''')

def helpp():
  print('AS I AM A NEWLY CREATED SOFTWARE WITH SIMPLE CODES YOU REQUIRE TO USE SOME SPECIAL WORDS TO TRIGGER A FUNCTION')
  print('''SOME OF THEM ARE :
1. use google if you want to google a query
2. use you tube in query if you want to open you tube
3. you can directly use current affairs or daily updates to know about daily affairs
4. you must use the word time in the query, to know about the current time
5. must use exit or close in the query, in order to close the assistant
6. also you can say hello to assistant
7. you can use sleep assistant to pause the application for a given period of time.
8. last but not the least.............. you can use the word search in the query to do any computational/analytical-calculations, general thinking questions, and so on....like enquiring weather of a city, capital of a country, etc. THE IMPORTANT THING HERE IS THAT USING THIS COMMAND YOUR QUERY IS RESOLVED WITHOUT REDIRECTING YOU TO A BROWSER''')
  time.sleep(10)

def info():
  speak('I AM  A VIRTUAL ASSISTANT CREATED BY DIKSAL FOR DOING SOME ACTIVITIES LIKE OPENING YOU TUBE, SEARCHING IN THE BROWSER, SPEAKING THE CURRENT TIME AND SO ON . MY SOFTWARE IS BEING UPDATED REGULALRY SO THAT I CAN PERFORM MORE FUNCTIONS.') 

def speak(a):
  engine=p.init()
  voices = engine.getProperty('voices')
  engine.setProperty('voice',voices[1].id)

  rate = engine.getProperty('rate')
  engine.setProperty('rate', 135)
  engine.say(a)
  engine.runAndWait()

def listen():
    try:
      mic = sr.Microphone()
      r = sr.Recognizer()
      with mic as source:
        playsound('C:\\Users\\Lenovo\\Downloads\\start_sound.wav')
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
      t = r.recognize_google(audio,language='en-in')
      return t
    except:
      return 'unable to recognise the audio'


if __name__=='__main__':
    start()
    print('LISTENING .....')
    while True:
        query = listen().lower()
        if query == 'unable to recognise the audio':
          output = 'query not satisfied'
          add(query,output)
        else:
          output = 'query satisfied'
          add(query,output)
        if query == 'hello':
          speak('hello')
          
        elif 'who created you' in query or 'who are you' in query:
          info()
          
        elif 'time' in query:
          speak('THE TIME IS')
          print('\t\tTHE TIME IS',d.now().strftime("%H:%M:%S"))
          speak(d.now().strftime("%H:%M:%S"))
          
        elif 'openyoutube' in query or 'open you tube' in query:
          speak('OPENING YOU TUBE')
          web.open('https://www.youtube.com/')
          
        elif 'google' in query:
          speak('OPENING GOOGLE')
          query = query.replace('google','')
          s = 'https://www.google.co.in/search?q='+query
          web.open(s)

        elif 'open google' in query or 'open chrome' in query:
          appli = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
          os.startfile(appli)
          
        elif 'search' in query:
          search(query)
          
        elif 'daily news' in query or 'current affairs' in query:
          speak('OPENING JAGRAN JOSH FOR DAILY UPDATES')
          web.open('https://m.jagranjosh.com/current-affairs')
          
        elif 'how to use you' in query:
          helpp()

        elif 'open python' in query:
          appli = "C:\\Users\\Lenovo\\AppData\\Local\\Programs\\Python\\Python38"
          os.startfile(appli)
              
        elif 'sleep assistant' in query:
          speak('for how much seconds')
          sl = int(input('for how much seconds'))
          time.sleep(sl)
          
        elif query == 'unable to recognise the audio':
          speak('unable to recognise the audio')
          
        elif 'exit' or 'close' in query:
          speak('bye. have a good day')
          break
time.sleep(5)
