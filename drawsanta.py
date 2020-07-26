#!/usr/bin/python3
import random
import getpass
import datetime
import smtplib
import configparser
import os.path
import re
from email.message import EmailMessage
from datetime import datetime

def picksantas(santas): 
    username =""
    password =""
    config = configparser.ConfigParser()
    config.read("secretsanta.conf")
    
    mailserver = config["mailserver"]["server"]
    promptForAuth = config["mailserver"]["promptForAuth"]
    requireAuth = config["mailserver"]["requireAuth"]
    

    #Requesting username and password for mailserver
    if promptForAuth == "yes": 
        print("Your need to authenticate with " + mailserver) 
        username = input("Username: ") 
        password = getpass.getpass("Password: ")

    if requireAuth == "yes" and promptForAuth == "no": 
        username = config["mailserver"]["username"]
        password = config["mailserver"]["password"]
    

    #creating a new random list of santas
    santas = random.sample(santas, len(santas))
    

    print("Sending mail...")
    
    i = 0
    #Matching list1 with list2
    failed = False
    while i < len(santas):
        santaComma = santas[i].find(",")
        santaName = santas[i][:santaComma]
        santaEmail = santas[i][santaComma+1:len(santas[i])]
        
        #last santa on list gets first as child
        if i == len(santas)-1:
            childComma = santas[0].find(",")
            childName = santas[0][:childComma]
            childEmail = santas[0][childComma+1:len(santas[0])]
        else:
            childComma = santas[i+1].find(",")
            childName = santas[i+1][:childComma]
            childEmail = santas[i+1][childComma+1:len(santas[i+1])]
        
        print(santaName + " <"+santaEmail + "> --> " + "**********")
        #Logging in case someone someone deletes mail, forgets or whatever
        log(santaName + " <"+santaEmail + "> --> " + childName)
        
        #Sending mail to santas
        if sendmail(santaName, santaEmail, childName, username, password):
            i+=1
        else:
            i=999999
            failed = True
    
    if not failed:
        print("Done!")
        print(str(len(santas)) + " mails sent")    

def sendmail(santaName, santaEmail, childName, username, password):
    #fetching config from config file
    config = configparser.ConfigParser()
    config.read("secretsanta.conf")
    
    #fetching mailserver settings
    mailserver = config["mailserver"]["server"]
    port = config["mailserver"]["port"]
    starttls = config["mailserver"]["starttls"]
    ssl = config["mailserver"]["ssl"]
    requireAuth = config["mailserver"]["requireAuth"]
    
    #fetching email content
    fromName = config["email"]["fromName"]
    fromEmail = config["email"]["fromEmail"]
    subject = config["email"]["subject"]
    emailContent = config["email"]["emailContent"]
    
    #Adding name of santa and child to email message
    emailContent = open(emailContent, 'r').read()
    emailContent = emailContent.replace("%santaName%", santaName)
    emailContent = emailContent.replace("%childName%", childName)

    #Adding email header and content
    message = EmailMessage() 
    message['From'] = fromName + " <" + fromEmail + ">"
    message['To'] = santaEmail
    message['Subject'] = subject
    message.set_content(emailContent)
    
    #connecting to mailserver based on configuration
    try: 
        if starttls == "yes": 
            server = smtplib.SMTP(mailserver, port)
            server.starttls()
        elif ssl =="yes" and starttls !="yes": 
            server = smtplib.SMTP_SSL(mailserver, port) 
        else: 
            server = smtplib.SMTP(mailserver, port) 
        
        if requireAuth == "yes": 
            server.login(username, password)
        
        server.send_message(message)
        server.quit()
        return True
    except:
        print("Unable to connect to " + mailserver + "!")
        print("Please verify that your username and password!")
        return False

#reading a list of names and emails from a file
def readfile(filename):
    if os.path.isfile(filename):
        with open(filename, 'r' ) as f:
            content = f.readlines()   
        
        #Checking that each line has the correct format 
        #regex pathern that checks for random word characters followed by a command and a valid email. 
        pathern = re.compile('^.*,[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        newcontent=[]
        for line in content: 
            #removing spaces in front and back
            cleanline = line.strip()
            #removing space before and after comma
            cleanline = cleanline.replace(" ,", ",")
            cleanline = cleanline.replace(", ", ",")

            #removing empty lines 
            if cleanline:
                #checking that clineline matches the regex pattern
                if pathern.match(cleanline) is not None:
                    newcontent.append(cleanline)
                else: 
                    return False
    
        return newcontent
    else:
        return False


#a function that writes a log to santas.log
def log(line):
    config = configparser.ConfigParser()
    config.read("secretsanta.conf")
    
    createLogFile = config["logging"]["createLogFile"]
    if createLogFile == "yes": 
        timeformat = config["logging"]["logTimeFormat"]
        logfile = config["logging"]["logfile"]
    
        currtime = datetime.now().strftime(timeformat)
        with open(logfile, 'a', newline='') as f:
            f.write(currtime + " - " + line + "\n")

def checkConfig(filename): 
    #checks if configfile exist
    if os.path.isfile(filename):
        return True
    else:
        #creates a config file with default values if it does not exist
        config = configparser.ConfigParser()
        config["general"] = {"santaslist":"santas.txt"}
        config["mailserver"] = {"server":"your.mailserver.com", 
                "ssl":"yes", 
                "starttls":"yes", 
                "port":"587", 
                "requireAuth":"yes", 
                "promptForAuth":"yes", 
                "username":"", 
                "password":""             
                }
        config["email"] = {"fromName":"Santas little helper", 
                "fromEmail":"secretsanta@yourdomain.com", 
                "subject":"Secret Santa", 
                "emailContent":"email.txt" 
                }
        config["logging"] = {"createLogFile":"yes", 
                "logfile":"santas.log", 
                "logTimeFormat":"%%d-%%m-%%Y %%H:%%M:%%S" 
                }
        config.write(open(filename, "w"))
        return False
def main():
    configfile = "secretsanta.conf"
    #runs script only if config file exist
    if checkConfig(configfile):
        #fetching data from config file
        config = configparser.ConfigParser()
        config.read(configfile)
    
        santasfile = config["general"]["santaslist"]
        
        #tries to read file containing santas 
        content = readfile(santasfile)
        if content: 
            picksantas(content)
        else: 
            print("Could not read " + santasfile) 
            print("Please make sure the file exist and that it has the correct format")
            print("Each line must contain name,email") 
    else: 
        print(configfile + " does not exist! The file is needed in order to run!")
        print(configfile + " has been created with default values. Please edit the file before running running the script again!")
        


#calling main function
if __name__ == "__main__": 
    main()

