######################
#Freecycle ETL Script#
#########by###########
#####Jared Pavan######
######################

##TO DO##
#-Load data to database
#-Scrape poster from message

##START SCRIPT##

import time
import random
import urllib2
import urllib
import cookielib
import pprint

from BeautifulSoup import BeautifulSoup as Soup
from soupselect import select

#INITIALIZE VARIABLES AND RANDOM NUMBER GENERATOR
LoginUrl = "https://login.yahoo.com/config/login?"
MessagesURL = "http://groups.yahoo.com/group/freecycledc/messages"
Message_Data = []
StartMessage = 200542 #Message ID from July 18th, 2013

random.seed() #Initialize rnd num generator

test_bool = 'N' #Use test variables
#END INITIALIZATION

#DEFINE FUNCTIONS
def Init_Opener():
    #Initiate URL opener
    jar = cookielib.CookieJar()
    return urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))

def Login_To_Yahoo():
    #Sign in to Freecycle Yahoo Group Page
    form_data = {'login' : 'jaredpavan', 'passwd' : 'Fr33cyc1e'}
    form_data = urllib.urlencode(form_data)
    resp = opener.open(LoginUrl, form_data)

def Make_Soup(URL):
    #Read in page HTML
    resp = opener.open(URL)
    soup = Soup(resp.read())
    return soup

def Find_Max_Post_ID():
    soup = Make_Soup(MessagesURL)
    MaxMSG = int(select(soup, '.msgnum')[0].contents[0])
    print "Max Post ID:", MaxMSG
    return MaxMSG

def Check_Column(col, value):
    #On scrape fail, check each variable to find point of failure
    try:
        print "result: Column:", col, "Value:", value, "scrape success"
    except:
        print "result: Scrape fail on column,", col

def Message_Data_to_Table(msg_id, title, body):
    Message_Data.insert(0, (msg_id,title.encode('utf-8'),body.encode('utf-8')))

def Humanize(s):
    sleepTime = random.random() * s
    print "sleep for duration: " + str(sleepTime)
    time.sleep(sleepTime)

def Loop_Through_Messages(i): #i = start ID - 1
    
    while i < MaxMSG:
        i += 1
        
        Humanize(2) #Humanize the program by sleeping 0-2 seconds
        
        try:
            soup = Make_Soup("http://groups.yahoo.com/group/freecycledc/message/" + str(i))

            MSG_Title = select(soup, 'title')[0].text.replace('\n', '~n-break~')

            msgbodyhtml = select(soup, '.msgarea')[0]
            MSG_Body = unicode.join(u' ',map(unicode,msgbodyhtml)).replace('<br />', '~break~').replace('\n', '~n-break~')
            
            if MSG_Title == '': MSG_Title = '(none)'
            if MSG_Body == '': MSG_Body = '(none)'
            
            Message_Data_to_Table(i, MSG_Title, MSG_Body)
            
            print i, "of", MaxMSG
        except:
            print "ERROR: SCRAPE FAIL ON POSTING ID", i
            
            Check_Column("Title", MSG_Title)
            Check_Column("Body HTML", msgbodyhtml)
            Check_Column("Body Text", MSG_Body)
            
            if MSG_Title == 'freecycledc':
                Message_Data_to_Table(i, 'Message does not exist', 'NOTHING TO SEE HERE, FOLKS')
            else:
                Message_Data_to_Table(i, 'FAIL', 'FAIL')
                
#Start ETL

opener = Init_Opener()

Login_To_Yahoo()

MaxMSG = Find_Max_Post_ID()

#TEST VARIABLES#
if test_bool == 'Y':
    MaxMSG = 198020
    StartMessage = MaxMSG - 10 #pull in 10 postings for testing

Loop_Through_Messages(StartMessage - 1)

#INSERT DATA IN TO DATABASE

#Temp data grab, export data to text file
Export_File = 'C:\Users\jpavan\Dropbox\Deloitte Stuff\Project_Scripts\Message_Data\Export_TEST.txt'

with open(Export_File,'w') as file:
    for msg in Message_Data:
        print>>file, msg
          
