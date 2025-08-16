import datetime
import os
import os.path
import webbrowser
import pyjokes
import pyttsx3
import speech_recognition as sr
import wikipedia
import winshell
import mysql.connector as ms
import csv



def virtualAssistant():

    def credAccess():
        with open("userCred.txt", 'r') as fin:
            creds = fin.readlines()
            username = creds[1]
            USERNAME = username[0:len(username) - 1]
            email_id = creds[3]
            USER_EMAIL_ID = email_id[0:len(email_id) - 1]
            password = creds[5]
            USER_EMAIL_PASS = password[0:len(password) - 1]
            sql = creds[7]
            global USER_SQL_PASS
            USER_SQL_PASS = sql[0:len(sql) - 1]
            return USERNAME, USER_EMAIL_ID, USER_EMAIL_PASS, USER_SQL_PASS

    def speak(text):
        engine = pyttsx3.init("sapi5")
        """ RATE"""
        rate = engine.getProperty('rate')
        engine.setProperty('rate', 200)

        """VOLUME"""
        volume = engine.getProperty('volume')
        engine.setProperty('volume', 2.0)

        """VOICE"""
        voices = engine.getProperty('voices')

        engine.setProperty('voice', voices[1].id)

        engine.say(text)
        engine.runAndWait()


    recognitionMode = int(input('''By which mode would you like to give commands : 
        1 - Voice Mode 
        2 - text Mode\n'''))

    def take_command():
        global query, endTime
        if recognitionMode == 1:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                speak("Listening")
                r.pause_threshold = 1
                audio = r.listen(source)
            try:
                print("Recognizing...")
                query = r.recognize_google(audio, language='en-in')
                print(f"User said: {query}\n")
            except Exception as e:
                print("Say that again please...")
                return "None"

        elif recognitionMode == 2:
            try:
                query = input('Enter Command : ')
            except Exception as e:
                print(e)
        return query.lower()


    def get_date(text):
        text = text.lower()
        today = datetime.date.today()

        if text.count("today") > 0:
            return today

    def note(text):
        date = datetime.datetime.now()
        file_name = str(date).replace(":", "-") + "-note.txt"
        with open(file_name, "w") as f:
            f.write(text)
        speak("I've made a note of that.")
        osCommandString = f"notepad.exe {file_name}"
        os.system(osCommandString)

    def history(text):
        date_time = datetime.datetime.now().strftime("%d-%m-%Y, %H:%M:%S")
        f = open("Command history.txt", "a")
        f.write(f"{date_time} : {text}\n")

    def contactBook():
        global emailID
        mydb = ms.connect(host="localhost", user="root",password="%s",database="contact_book")%(USER_SQL_PASS)
        mycursor = mydb.cursor()
        name1 = str(input("Enter the name : "))
        mycursor.execute("SELECT * FROM contact_table")
        myresult = mycursor.fetchall()
        for x in myresult:
            if name1 == x[0]:
                emailID = x[1]
                break
        else:
            print("Record not found")
            insertChoice = input("Would you like to add contact ? ")
            if insertChoice.lower().startswith("y"):
                mydb1 = ms.connect(host="localhost", user="root",password="%s",database="contact_book")%(USER_SQL_PASS)
                mycursor1 = mydb1.cursor()
                mail = str(input("Enter the e-mail ID of the new contact : "))
                sql = "INSERT INTO contact_table(name, email_id) VALUES(%s,%s)"
                val = (name1, mail)
                mycursor1.execute(sql, val)
                mydb1.commit()
                print(mycursor1.rowcount, "record inserted.")

            mydb1 = ms.connect(host="localhost", user="root", password="%s", database="contact_book")%(USER_SQL_PASS)
            mycursor = mydb1.cursor()
            mycursor.execute("SELECT * FROM contact_table")
            myresult = mycursor.fetchall()
            for x in myresult:
                if name1 == x[0]:
                    emailID = x[1]
                    break
        return emailID

    def wishMe(name):
        hour = int(datetime.datetime.now().hour)
        if hour >= 0 and hour < 12:
            speak("Good Morning!" + str(name))
        elif hour >= 12 and hour < 16:
            speak("Good Afternoon!" + str(name))
        else:
            speak("Good Evening!" + str(name))

    if __name__ == "__main__":
        USERNAME, USER_EMAIL_ID, USER_EMAIL_PASS, USER_SQL_PASS = credAccess()
        wishMe(USERNAME)
        initTime = datetime.datetime.now()
        WAKE = "computer"
        print("Listening")

        while True:
            text = take_command()

            if text.count(WAKE) == 0:

                text = text.replace(WAKE, "")

                NOTE_STRS = ["make a note", "write this down", "remember this"]
                for phrase in NOTE_STRS:
                    if phrase in text:
                        speak("What would you like me to write down?")
                        note_text = take_command()
                        note(note_text)

                if "wikipedia" in text:
                    try:
                        speak('Searching Wikipedia...')
                        text = text.replace("wikipedia", "")
                        results = wikipedia.summary(text, sentences=2)
                        speak("According to Wikipedia")
                        print(results)
                        speak(results)
                    except Exception as e:
                        print(e)

                elif text in 'open youtube':
                    speak("Here you go to Youtube")
                    webbrowser.open("https://www.youtube.com")

                elif 'search' in text:
                    speak("Searching")
                    search = text.replace("search", "")
                    link = f"https://www.google.com.tr/search?q={search}"
                    webbrowser.open(link)

                elif 'open stackoverflow' in text:
                    speak("Here you go to Stack Over flow. Happy coding!")
                    webbrowser.open("https://www.stackoverflow.com")

                elif 'play' in text:
                    music = text.replace("play", "")
                    link = f"https://music.youtube.com/search?q={music}"
                    webbrowser.open(link)

                elif 'time' in text:
                    strTime = datetime.datetime.now().strftime("%H:%M:%S")
                    print(strTime)
                    speak(f"the time is {strTime}")

                elif 'narrate' in text:
                    speak('What shall I narrate?')
                    string = input("What shall I narrate : ")
                    speak(string)


                elif 'how are you' in text:
                    speak("I am fine. Thanks for asking")
                    speak(f"How are you?")
                    text = take_command()
                    if 'fine' in text or "good" in text:
                        speak("It's good to know that your fine")

                elif "change name" in text:
                    speak("What would you like to call me")
                    WAKE = take_command()
                    speak("Thanks for giving me special name")


                elif 'joke' in text:
                    joke = pyjokes.get_joke()
                    print(joke)
                    speak(joke)

                elif "why you came to world" in text:  # 4
                    speak("To help you out, further thanks to gowtham and sai"
                          "")
                elif "today" in text:
                    speak("today's date is")
                    x=get_date(text)
                    speak(x)
                    print(x)
                elif "who are you" in text:  # 1
                    speak("I am  your personal assistant")

                elif 'tell me something about you' in text:
                    speak("")

                elif "empty recycle bin" in text:
                    winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=True)
                    speak("Recycle Bin Recycled")

                elif "history" in text:
                    osCommandString = f"notepad.exe Command history.txt"
                    os.system(osCommandString)
                    speak("Would you like me to clear your command history ?")
                    confirmation = take_command()
                    if confirmation.lower().startswith("y"):
                        open("Command history.txt", 'w').close()

                elif 'exit' in text or 'good bye' in text:
                    endTime = datetime.datetime.now()
                    print(f"Time duration of Usage : {endTime - initTime}")
                    speak("Thanks for giving me your time")
                    exit()


                history(text)


if __name__ == "__main__":
    try:
        virtualAssistant()
    except Exception as e:
        print(e)


