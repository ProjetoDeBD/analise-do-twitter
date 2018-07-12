# coding: utf-8
import tweepy
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import sys
from traceback import print_tb, extract_tb, format_list

from controllers.db_controllers import get_location, get_user, add_hashtag
from dao.hashtag_dao import insert_hashtag
from dao.tweet_dao import insert_tweet
from models.hashtag import HashTagObj
from models.location import LocationObj
from models.tweet import TweetObj
from models.user import UserObj
from dao.user_dao import insert_user, search_user
from utils.location_utils import search_location_by_name


def printError():
    error = sys.exc_info()
    type = error[0]#tipo do erro
    print('\n'+'Type: \n'+str(type)+'\n')
    value = error[1] # valor do erro
    print('Value: \n'+str(error[1])+'\n')
    tb=error[2]
    print('Traceback:')
    e_tb=extract_tb(tb)
    f_l=format_list(e_tb)#traceback em forma de lista para futuro usos
    print_tb(tb)


def get_tweets(hashtag):
    arquivo = open('{}.txt'.format(hashtag),'r')
    lista=arquivo.read().split()
    lista1=[]
    for x in range (len(lista)):
        if x%2==0:
            lista1.append(lista[x])


    cwd = os.getcwd()
    auth = tweepy.OAuthHandler('jkwDvQkT5Es6S24JiLq2FLxrb', 'ju5ogpsqo3cQLxtgTurMgq7cmWt8CN2H9lQ0F5wGGrmegcvAMp')
    auth.set_access_token('89299395-PpehItyb3bnxSI3TEbve9Y8uDZKKOgaYiQinCCrvg', 'Rh8FHQk0Vd66LCZJIf20DrFzFZfmBZqqPLaAN3hXCmT3n')
    api = tweepy.API(auth)

    for x in lista1:
        print(x)
        try:
            tweet = api.get_status(x , tweet_mode='extended')
            hashtags = tweet.entities["hashtags"]
            nomeUsuario = tweet.user.screen_name#nick fixo
            location = tweet.user.location
            followersUsuario = tweet.user.followers_count
            totalTweetsUsuario = tweet.user.statuses_count #SERÁ NECESSARIO?
            textoTweet = tweet.full_text
            tweetDate = tweet.created_at
            retweetCount = tweet.retweet_count
            likes = tweet.favorite_count

            location_name = search_location_by_name(location)
            if location_name:
                location_obj = LocationObj(location_name[0])
                location_obj.set_latitude(location_name[1])
                location_obj.set_longitude(location_name[0])
                location_obj = get_location(location_obj)
                location_id = location_obj.get_id()
            else:
                location_id = None

            # hash_list = []
            # for hash in hashtags:
            #     h = HashTagObj(hash)
            #     hash_list.append(add_hashtag(h))
            #
            # hash_id = hash_list[0] if hash_list else None

            user_obj = UserObj(nomeUsuario)
            user_id = get_user(user_obj).get_id()

            tweet_obj = TweetObj(textoTweet)
            tweet_obj.set_number_likes(likes)
            tweet_obj.set_location(location_id)
            tweet_obj.set_user(user_id)
            # tweet_obj.set_hasstag(hash_id)
            tweet_obj.set_number_retweet(retweetCount)

            insert_tweet(tweet_obj)
            print("------------------------------------------------------------")
            print(nomeUsuario)
            print("hash",hashtags)
            print("localizacao",location)
            print("followers",followersUsuario)
            print("totalTweets",totalTweetsUsuario)
            print("texto",textoTweet)
            print("retweet",retweetCount)
            print("likes",likes)
            print("----------------------------------- NEW TWEET -------------------------")

        except:
            printError()
get_tweets("LulaLivre")