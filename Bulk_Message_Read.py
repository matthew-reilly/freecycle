##############################
#Freecycle Message Processing#
#############by###############
#########Jared Pavan##########
##############################

##TO DO##
#-Find post type
#-Clean title
#-Find location metadata
#-Scrape poster from message

##START SCRIPT##

import ast

file = 'C:\Users\jpavan\Dropbox\Deloitte Stuff\Project_Scripts\Message_Data\Export_TEST.txt'

ins = open(file, "r")

messages = []

for line in ins:
    messages.insert(0, ast.literal_eval(line))

ins.close()
