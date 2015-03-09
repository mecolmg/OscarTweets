import csv
import plotly.plotly as py
from plotly.graph_objs import *
from collections import defaultdict
import plotly.tools as tls
tls.set_credentials_file(username='mecolmg', api_key='tub4jew75t')

#Contains Tweet Data
class Tweet:
    def __init__(self, data):
        self.time, self.tweetid, self.text, self.rt, \
        self.geo, self.placetag, self.favs, self.usr, \
        self.usrloc, self.usrid, self.timezone, self.usrfollow, \
        self.usrstats, self.usrfriends, self.usrhandle, \
        self.hashtags, self.mentions = data

#Imports data as Tweet objects to the variable 'tweets'
with open('oscar_tweets.csv', 'rb') as File:
    File = csv.reader(File, delimiter=',',quotechar='"')
    tweets = [Tweet(data) for data in File][1:]
    
#Imports a list of states from a CSV file to the variable 'states'
#For use in location() method
with open('states.csv', 'rb') as File:
    File = csv.reader(File, delimiter=',',quotechar='"')
    states = [data for data in File]

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
    data = Data([Bar(x=[data[0] for data in top], y=[data[1] for data in top],
                     marker=Marker(color='#b09953'))])
    layout = Layout(
        title='Tweets about Best Picture Nominees',
        font=Font(
            family='"Open sans", verdana, arial, sans-serif',
            size=17,
            color='#000'
        ),
        yaxis=YAxis(title='Number of Tweets')
        )
    fig = Figure(data=data,layout=layout)
    plot = py.plot(fig)
    count = 1
    print("The Most Tweeted About Best Picture Nominees:")
    for t in top:
        print("\t"+str(count)+": "+t[0])
        count += 1
    return top

#Determines when Birdman (the winner) was most tweeted about
def winner():
    count = defaultdict(int)
    for tweet in tweets:
        if len(tweet.timezone) == 0:
            timezone = 0
        else:
            timezone = int(tweet.timezone)/3600            
        hour = int(tweet.time[11:13])+timezone
        minute = int(tweet.time[14:16])
        text = tweet.text.lower()
        if text.count('birdman') != 0:
            count[(hour,minute)] += 1
    times = sorted(count.items(),key=lambda x:x[1], reverse=True)
    print("Birdman was mentioned most frequently at:")
    print("\t {:02d}:{:02d} GMT".format((times[0][0][0]-1)%12 +1, times[0][0][1]))

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

winner()
