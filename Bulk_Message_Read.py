import ast
import csv

file = 'C:\Documents and Settings\D501472\My Documents\Freecycle Stuff\PulledData.txt'
analyzed_msg = 'C:\Documents and Settings\D501472\My Documents\Freecycle Stuff\msganalyzed.csv'


ins = open(file, "r")

messages = []

for line in ins:
    messages.insert(0, ast.literal_eval(line))

ins.close()

#if 'offer' in msg[1].lower(): print msg[0],'offer'

msg_types = []

#Message_Data.insert(0, )

for msg in messages:
    offer = 0
    offer_a = 0
    pending = 0
    ppu = 0
    taken = 0
    wanted = 0
    predict = ''
    
    if 'offer' in msg[1].lower(): offer = 1
    if 'pending' in msg[1].lower(): pending = 1
    if 'ppu' in msg[1].lower(): ppu = 1
    if 'taken' in msg[1].lower() or 'received' in msg[1].lower(): taken = 1
    if 'wanted' in msg[1].lower() or 'want' in msg[1].lower(): wanted = 1

    sum_types = offer + pending + ppu + taken + wanted
    
    if sum_types == 0: offer_a = 1 #if none

    if taken == 1: predict = 'taken'
    elif pending == 1 or ppu == 1: predict = 'pending'
    elif wanted == 1: predict = 'wanted'
    elif offer == 1 or offer_a == 1: predict = 'offer'

    if msg[1] != 'FAIL':
        msg_types.insert(0, (msg[0], offer, offer_a, pending, ppu, taken, wanted, predict))

bad_msgs = []
multi_msgs = []

for tps in msg_types:
    sum_types = tps[1] + tps[2] + tps[3] + tps[4] + tps[5] + tps[6]
    
    if sum_types == 0: bad_msgs.insert(0, tps)
    if sum_types >= 2: multi_msgs.insert(0, tps)

print len(bad_msgs), "bad messages"
print len(multi_msgs), "multi messages"

msg_allgood = []

for msg in messages:
    for chk in msg_types:
        if msg[0] == chk[0]:
            msg_allgood.insert(0,(chk[0], chk[1], chk[2],chk[3],chk[4],chk[5],chk[6],chk[7],msg[1]))

with open(analyzed_msg, 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerows(msg_allgood)
