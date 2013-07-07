######################
#Freecycle ETL Script#
#########by###########
#####Jared Pavan######
######################

##TO DO##
#-Load data to database
#-Scrape poster from message

##START SCRIPT##

import urllib2
import urllib
import cookielib
import pprint

from BeautifulSoup import BeautifulSoup as Soup
from soupselect import select

LoginUrl = "https://login.yahoo.com/config/login?"

MessagesURL = "http://groups.yahoo.com/group/freecycledc/messages"

Message_Data = ['Message ID','Title','Message Body']
column_count = len(Message_Data) #Number of columns in table

StartMessage = 198000 #Message ID from June 9th, 2013

test_bool = 'Y' #Use test variables

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

def Loop_Through_Messages(i): #i = start ID - 1
    MaxMSG = Find_Max_Post_ID()
    
    while i < MaxMSG:
        i += 1
        try:
            soup = Make_Soup("http://groups.yahoo.com/group/freecycledc/message/" + str(i))

            MSG_Title = select(soup, 'title')[0].text

            msgbodyhtml = select(soup, '.msgarea')[0]
            MSG_Body = unicode.join(u' ',map(unicode,msgbodyhtml)).replace('<br />', '~break~')
            
            Message_Data.append(i) #Message ID
            Message_Data.append(MSG_Title) #Message Title
            Message_Data.append(MSG_Body) #Message Body
            print "Post Data:", i, MSG_Title, MSG_Body
            print i, "of", MaxMSG
        except:
            print "ERROR: SCRAPE FAIL ON POSTING ID", i
            Check_Column("Title", MSG_Title)
            Check_Column("Body HTML", msgbodyhtml)
            Check_Column("Body Text", MSG_Body)
            break

#Start ETL

opener = Init_Opener()

Login_To_Yahoo()

#TEST VARIABLES#
if test_bool == 'Y':
    StartMessage = MaxMSG - 10 #pull in 10 postings for testing

Loop_Through_Messages(StartMessage - 1)

table_format = zip(*[iter(Message_Data)]*column_count) #Turn list in to column_count by i table

#INSERT DATA IN TO DATABASE


#OLD CODE#    
#Convert BS object to unicode string and replace all HTML breaks with ~break~
#msgbody = unicode.join(u' ',map(unicode,select(msgbodyhtml, 'div')[0])).replace('<br />', '~break~')
