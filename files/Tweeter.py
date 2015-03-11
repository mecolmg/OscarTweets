import csv
import plotly.plotly as py
from plotly.graph_objs import *
from collections import defaultdict

#Contains Tweet Data, accesed by (...).value
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
#For use in location() function
with open('states.csv', 'rb') as File:
    File = csv.reader(File, delimiter=',',quotechar='"')
    states = [data for data in File]

####Functions####

#Determines Most Tweeted Nominees
def popularity():
    nominees = ["American Sniper","Birdman","Boyhood",
                "The Grand Budapest Hotel","The Imitation Game",
                "Selma","The Theory of Everything","Whiplash"]
    count = defaultdict(int)
    for tweet in tweets:
        text = tweet.text.lower()
        for nominee in nominees:
            if text.count(nominee.lower().strip('the ')) != 0:
                count[nominee] += 1
    top = sorted(count.items(),key=lambda x:x[1], reverse=True)

    #Prints out results
    count = 1
    print("The Most Tweeted About Best Picture Nominees:")
    for t in top:
        print("\t"+str(count)+": "+t[0])
        count += 1

    #Graphs results
    data = Data([Bar(x=[data[0] for data in top],
                     y=[data[1] for data in top],
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
    
#Determines when Birdman (the winner) was most tweeted about
def winner():
    count = defaultdict(int)
    for tweet in tweets:
        hour = int(tweet.time[11:13])
        minute = int(tweet.time[14:16])
        text = tweet.text.lower()
        if text.count('birdman') != 0:
            count[(hour,minute)] += 1
    times = sorted(count.items(),key=lambda x:x[1], reverse=True)

    #Prints results
    print("Birdman was mentioned most frequently at:")
    print("\t {:02d}:{:02d} GMT".format((times[0][0][0]-1)%12 +1, times[0][0][1]))

    #Graphs results
    x=[data[0][0] for data in times for i in range(data[1])]
    y=[data[0][1] for data in times for i in range(data[1])]
    data = Data([
        Histogram2d(
            x=x,
            y=y,
            autobinx=False,
            xbins=XBins(
                start=0.5,
                end=6.5,
                size=1
            ),
            autobiny=False,
            ybins=YBins(
                start=0.5,
                end=60.5,
                size=1
            ),
            colorscale=[[0, 'rgb(12,51,131)'], [0.25, 'rgb(10,136,186)'], [0.5, 'rgb(242,211,56)'], [0.75, 'rgb(242,143,56)'], [1, 'rgb(217,30,30)']]
        )
    ])
    layout = Layout(
        title='Times where Birdman is Mentioned<br> (GMT)',
        font=Font(
            family='"Open sans", verdana, arial, sans-serif',
            size=17,
            color='#000'
        ),
        yaxis=YAxis(title='Minute'),
        xaxis=XAxis(title='Hour')
    )
    fig = Figure(data=data,layout=layout)
    plot = py.plot(fig)

#Determines the top tweeting states in the US
def location():
    count = defaultdict(int)
    for tweet in tweets:
        loc = tweet.usrloc
        if len(loc) != 0:
            for state in states:
                if loc.count(state[0]) != 0 or loc.count(state[1]) != 0:
                    count[state[0]] += 1
    times = sorted(count.items(),key=lambda x:x[1], reverse=True)    

    #Prints results
    print("The top 10 tweeting US states were:")
    for i in range(10):
        print("\t" + str(i+1)+": "+times[i][0])

    #Graphs results
    x = [state[0] for state in times[:10]]
    y = [state[1] for state in times[:10]]
    text = [state[0] for state in times[:10]]
    data = Data([Bar(x=x,y=y,text=text,marker=Marker(color='#b09953'))])
    layout = Layout(
        title='Top Tweeting States',
        font=Font(
            family='"Open sans", verdana, arial, sans-serif',
            size=17,
            color='#000'
        ),
        yaxis=YAxis(title='Number of Tweets Sent')
    )
    fig = Figure(data=data,layout=layout)
    plot = py.plot(fig, filename='Top Tweeting States')

#### Additional Functions ####

#Returns inforomation on the most retweeted Tweet of the night
def topRT():
    toprt = 0
    topTweet = tweets[0]
    for tweet in tweets:
        trt = int(tweet.rt)
        if trt > toprt:
            toprt = trt
            topTweet = tweet
    print("The top tweet was:")
    print("\n{:s}".format(topTweet.text))
    print("\nWith {:s} retweets".format(topTweet.rt))
    print("URL: http://twitter.com/{:s}/status/{:s}".format(topTweet.usrhandle, topTweet.tweetid))

topRT()
