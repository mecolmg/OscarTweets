import csv
from collections import defaultdict

#Contains Tweet Data
class Tweet:
    def __init__(self, data):
        self.time,self.tweetid,self.text,self.rt,self.geo,self.placetag,self.favs,self.usr,self.usrloc,self.usrid,self.timezone,self.usrfollow,self.usrstats,self.usrfriends,self.usrhandle,self.hashtags,self.mentions = data

#Imports data to the variable 'tweets'
with open('oscar_tweets.csv', 'rb') as theFile:
    theFile = csv.reader(theFile, delimiter=',',quotechar='"')
    tweets = [Tweet(data) for data in theFile][1:]
with open('states.csv', 'rb') as theFile:
    theFile = csv.reader(theFile, delimiter=',',quotechar='"')
    states = [data for data in theFile]

#Determines Most Tweeted Nominees
def popularity():
    nominees = ["American Sniper","Birdman","Boyhood","The Grand Budapest Hotel","The Imitation Game","Selma","The Theory of Everything","Whiplash"]
    count = defaultdict(int)
    for tweet in tweets:
        text = tweet.text.lower()
        for nominee in nominees:
            if text.count(nominee.lower().strip('the ')) != 0:
                count[nominee] += 1
    top = sorted(count.items(),key=lambda x:x[1], reverse=True)
    count = 1
    print("The Most Tweeted About Best Picture Nominees:")
    for t in top:
        print("\t"+str(count)+": "+t[0])
        count += 1

#Determines when Birdman (the winner) was most tweeted about
def winner():
    count = defaultdict(int)
    for tweet in tweets:
        time = tweet.time[11:16]
        text = tweet.text.lower()
        if text.count('birdman') != 0:
            count[time] += 1
    times = sorted(count.items(),key=lambda x:x[1], reverse=True)
    print("Birdman was mentioned most frequently at:")
    print("\t"+times[0][0])

#Determines the top tweeting states in the US
def location():
    count = defaultdict(int)
    for tweet in tweets:
        loc = tweet.usrloc
        for state in states:
            if loc.count(state[0]) != 0 or loc.count(state[1]) != 0:
                count[state[0]] += 1
    times = sorted(count.items(),key=lambda x:x[1], reverse=True)
    print("The top 10 tweeting US states were:")
    for i in range(10):
        print("\t" + str(i+1)+": "+times[i][0])

#Runs through previous functions to print results
popularity()
print
winner()
print
location()
