# -*- coding: utf-8 -*-

#este script trata de analizar n tweets que resultan de un query dado y determina su relevancia 
# para ver si es importante o no y  también  filtra los tweets que tienen muy poca respuesta
# para que sea inmediatamente canalizado.

# ejemplo:
# 1) "ayuda estoy en morelos"
# 2) "ayuda necesitamos remover escombros estamos en en jojutla calle .. , ocupamos palas, y camiones "
# este script determinara que el tweet numero 2 tiene muchar mayor relavancia
# puesto que es mas específico y se entiende que piden ayuda debido al sismo,
# a diferencia del primer tweet que es mas ambiguo.

# proximas tareas
# 1 mejorar querys, mas inteligeentes y  mejor estructurados.
# 2 cuidar limite de peticiones https://developer.twitter.com/en/docs/basics/rate-limiting
# 3 si los twitts encontrados es menor a 100 continuar explorando.
# buscar cuentas influyentes que ayuden con rt y respuestas.

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import tweepy
import csv
import re
import json
from time import sleep

from keywords import *
from classes.tuit import Tuit

from random import randint

# Create variables for each key, secret, token
consumer_key = 'cCS3DVcF2L7pB0GpndJwqpnUQ'
consumer_secret = 'bQ03sHJAzODlVIMA9g8SD9ynXXXjGO9mDBGMYqIljTHe2jm6Ed'
access_token = '1470808525-Um9ZGtU5KrjpMZhEvQzmJwIGi7MAp94cJr6vbKz'
access_token_secret = 'mvXu6dGy5VFYzSGgaDuq5syuiBhJIA5T28H39wS0vTmN7'

# Set up OAuth and integrate with API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

api = tweepy.API(auth)

#data = api.search(q='escombro ayuda',
        #result_type="recent")
        
def isReply(t):
    if hasattr(t, 'retweeted_status') and  hasattr(t,'in_reply_to_status_id') and hasattr(t,'in_reply_to_status_id_str') and  hasattr(t,'in_reply_to_user_id') and hasattr(t,'in_reply_to_user_id_str') and hasattr(t,'in_reply_to_screen_name'):
        if t.retweeted_status or t.in_reply_to_status_id or tweet.in_reply_to_status_id_str or t.in_reply_to_status_id_str or t.in_reply_to_user_id or t.in_reply_to_user_id_str or t.in_reply_to_screen_name:  
            return True
            
def isRT(t):
    if hasattr(t, 'retweeted_status'):
     if t.retweeted_status :
        return True

print("!!!!TODA DATA!!!!")
#print(data[1])
#print "datos    "
print("!!!TODA DATA!!")
tuits = []

counter = 0
#formacion de query con palabras aletorias
searchQuery = acciones[randint(0,len(acciones)-1)]+" "+lugares[randint(0,len(lugares)-1)]
searchQuery="revisa grieta"
print searchQuery
maxTweets = 1000
tweetsPerQry = 100  
max_id = -1L
sinceId = None


while counter < maxTweets:
    print "conteo: "+str(counter)+"/"+str(maxTweets)
    try:
        if max_id <= 0:
            if not sinceId:
                new_tweets = api.search(q=searchQuery, count=tweetsPerQry)
            else:
                new_tweets = api.search(q=searchQuery, count=tweetsPerQry,since_id=sinceId)
        else:
            if not sinceId :
                new_tweets = api.search(q=searchQuery, count=tweetsPerQry,max_id=str(max_id - 1))
            else:
                new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                        max_id=str(max_id - 1),
                                        since_id=sinceId)
        
        if not new_tweets:
            print "No se econtraron mas tweets"
            counter=maxTweets
        else:
            for d in new_tweets:
                if not isRT(d):   
                    tuits.append(Tuit(d.author.screen_name, d.text, d.id_str,d.retweet_count,0,d.created_at))
            counter += len(new_tweets)
            max_id = new_tweets[-1].id           
    except tweepy.TweepError as e:            
        print("error en : " + str(e))
        break            

    counter += 1

retweets=[]
for t in tuits:
    print t.getText()
    print t.getNumRT()
    banaccion=0
    banlugar=0
    banobjeto=0
    if t.getNumRT()<=30:
        print t.getText().encode('utf-8','ignore').lower()
        print t.getAuthor().encode('utf-8','ignore')        
        palabras=t.getText().encode('utf-8','ignore').lower().split(" ")
        peso=0
        for accion in acciones:
            if re.search(accion,t.getText().encode('utf-8','ignore').lower()):              
                peso+=1 
                banaccion=1
        for lugar in lugares:
            if re.search(lugar,t.getText().encode('utf-8','ignore').lower()):              
                peso+=1 
                banlugar=1
        for objeto in objetos:
            if re.search(objeto,t.getText().encode('utf-8','ignore').lower()):              
                peso+=1 
                banobjeto=2
        pesoban=banaccion+banlugar+banobjeto
        peso=peso*pesoban
    
        print "peso:"+str(peso) 
        if peso>4:
            #api.retweet(t.getIdt())
            row=[t.getIdt(),t.getText().encode('utf-8','ignore').lower(),t.getAuthor().encode('utf-8','ignore'),t.getNumRT(),peso,t.getDateCreated()]
            retweets.append(row)
            with open("output.csv", "a") as fp:
                wr = csv.writer(fp, dialect='excel')
                wr.writerow(row)
            

for rt in retweets:
    api.retweet(rt[0])

