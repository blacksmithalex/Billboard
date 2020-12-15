import billboard #импорт библиотеки
import telebot
import socket
import config

chart = billboard.ChartData('hot-100') #топ 100 (считываем)

tg_output = 'Billboard: Chart '+ chart.name +' ; Date = '+chart.date + ' (Top 10)'+'\n\n' #info 
tg_output += '№ в топе/Кол. нед. в топе/Артист - Трек\n\n'

a = ''
for x in chart[:10]:
    a+= str(x.rank)+'/'
    a+= str(x.weeks)+'/ '
    a += x.artist + ' - ' + x.title
    a+='\n'
tg_output+= a

#Анализировали количество появлений исполнителей в топе
Artists = []
for j in range(len(chart)):
    t = chart[j].artist
    if '+' in t:
        t = t.replace('+','&')
    if 'x' in t:
        ind = t.index('x')
        if t[ind-1] == ' ' and t[ind+1] == ' ':
            t = t.replace('x','&')
    if 'X' in t:
        ind = t.index('X')
        if t[ind-1] == ' ' and (ind+1 == len(t) or t[ind+1] == ' '):
            t = t.replace('X','&')
    if '&' in t:
        t = t.split('&')
    else:
        t = [t]
    for i in range(len(t)):
        if 'Featuring' not in t[i]:
            Artists.append(t[i].strip())
        else:
            p = t[i].split('Featuring')
            for x in p:
                Artists.append(x.strip())  
if '' in Artists:
    del(Artists[Artists.index('')])

Performers = dict()
for x in Artists:
    if x not in Performers:
        Performers[x] = 1
    else:
        Performers[x] += 1
        
otvet = 'Исполнители, которые больше всего засветились в топе: \n\n'
for key in Performers:
    if Performers[key] > 5:
        otvet+=key+' - '+ str(Performers[key])+' Треков\n'
    elif Performers[key] > 1:
        otvet+=key+' - '+ str(Performers[key])+' Трека\n'

tg_output += '\n\n'+ otvet

#Бот подключен
telebot_token = #telebot_token
telegram_id = #telegram_id 
bot = telebot.TeleBot(telebot_token)
bot.send_message(telegram_id,tg_output)
pass
