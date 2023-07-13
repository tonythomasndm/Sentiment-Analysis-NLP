import tweepy
import re
import csv
from tweepy import OAuthHandler
from textblob import TextBlob
class Twitter():
    ##Twitter class for sentiment analysis##

    def __init__(self):
        ##Authorising Twitter API client##
    
        consumer_key = "XXX"    # API key
        consumer_secret = "XXX"   # API secret key  
        access_token = "XXX"
        access_token_secret = "XXX"

        try:
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(access_token, access_token_secret)
            self.api = tweepy.API(self.auth)
        except:
            print("Authentication Failed")

    def preprocess_tweet(self, tweet):
        ##Preprocessing a tweet##

        link_ex = "https?:\/\/[A-Za-z0-9./]+"
        handle_ex = "@[A-Za-z0-9_]+"
        hashtag_ex = "#[A-Za-z0-9_]+"
        spcl_ex = "[^0-9A-Za-z ]"

        tweet = re.sub(link_ex, " ", tweet)         #removing links
        tweet = re.sub(handle_ex, " ", tweet)       #removing twitter handles
        tweet = re.sub(hashtag_ex, " ", tweet)      #removing hashtags
        tweet = re.sub(spcl_ex, " ", tweet)         #removing special characters
        
        tweet = ''.join([i if ord(i) < 128 else ' ' for i in tweet])    #removing non-ascii characters

        return tweet

    def clean_tweet_text(self, tweet_text):
        ##Cleaning tweet to store in the CSV file##
        
        spcl_ex = "[^0-9A-Za-z .@#!?]"
        tweet_text = re.sub(spcl_ex, " ", tweet_text)       #removing special characters
        tweet_text = ''.join([i if ord(i) < 128 else ' ' for i in tweet_text])  #removing non-ascii characters

        return tweet_text

    def get_tweet_sentiment(self, tweet):
        ##Getting sentiment of a tweet##

        tweet_stats = TextBlob(self.preprocess_tweet(tweet))
        if tweet_stats.sentiment.polarity < 0:
            return "negative"
        elif tweet_stats.sentiment.polarity == 0:
            return "neutral"
        else:
            return "positive"

    def get_tweets(self, topic, tweet_count):
        ##GET request to retrieve english tweets on a particular topic##

        tweets = list()
        try:
            matched_tweets = self.api.search(q = topic, lang='en', show_user = False, count = tweet_count)
            for tweet in matched_tweets:
                parsed_tweet = {}
                parsed_tweet['text'] = self.clean_tweet_text(tweet.text)
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

                #Checking if the tweet is already present in our list because of it being retweeted
                if tweet.retweet_count > 0:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
            return tweets
        except tweepy.TweepError as e:
            print("Error: " +str(e))

def main():
    my_api = Twitter()
    topic = "avengers"
    tweets = my_api.get_tweets(topic, tweet_count = 100)

    for tweet in tweets:
      print(tweet['text'] + " --------->> " + tweet['sentiment'] + "\n\n")

    pos_tweets = [t for t in tweets if t['sentiment'] == 'positive']
    neg_tweets = [t for t in tweets if t['sentiment'] == 'negative']
    neut_tweets_num = len(tweets)-len(pos_tweets)-len(neg_tweets)

    pos_percentage = float(100*len(pos_tweets)/len(tweets))
    neg_percentage = float(100*len(neg_tweets)/len(tweets))
    neut_percentage = float(100*neut_tweets_num/len(tweets))

    print("\n\n---Aggregate Analysis for the topic: " + topic + " ---\n")
    print("1. Percentage of POSITIVE tweets -> " + str(pos_percentage) + "%")
    print("2. Percentage of NEGATIVE tweets -> " + str(neg_percentage) + "%")
    print("3. Percentage of NEUTRAL tweets -> " + str(neut_percentage) + "%\n\n")
    
#   keys = tweets[0].keys()
#   with open("Sentiment_Analysis_TOPIC.csv", "wb") as f:
#       w = csv.DictWriter(f,keys)
#       w.writeheader()
#       w.writerows(tweets)
#   print("\n\n\nCSV file named \"Sentiment_Analysis_TOPIC.csv\" created for individual analysis!\n\n")

if __name__ == "__main__": 
    main()

# Output : 
# RT @missingabhijeet  Get ready to witness World Class Action. Because the action director of Hollywood movies like Mission Impossible  Top  --------->> positive


# ay to they got Portugal. The Man  Paramore  Blink 182  Ashnikko  Avril Lavigne  Beach Boys  MCR  Queen  Cyndi Laupe  https   t.co Y8cBCLKf2W --------->> neutral


# RT @fxala2  BACK TO THE ORIGINS # 27  Colored   amp  final  #Xmen #Avengers #Marvel #ferranxalabarder https   t.co ItqdizLljQ --------->> neutral


# Get ready to witness World Class Action. Because the action director of Hollywood movies like Mission Impossible  T  https   t.co 8V8QBn7FKo --------->> negative


# RT @IronNinja2000  Avengers budget is nonexistent at this point... my god... https   t.co i5mafrQepc --------->> neutral


# RT @kanemoyoshi  the way that treasure s video background for mama performance looks like it got from avengers. i know that it might was hy  --------->> neutral


# @Harshav74123148 No bro. Avengers Endgame grossed  62 678 476 in India which is approximately  437.8cr. --------->> negative


# Remember a Tweet each day about The Avengers keeps those Diabolical Masterminds at Bay. #TheAvengers #PatrickMacnee  https   t.co 4fGplk9buP --------->> neutral


# @kanemoyoshi it looks like a combination of doctor stranger and avengers --------->> neutral


# The sale of  new  Premier Access passes for Avengers Assemble  Flight Force has started. The actual price is  12.  https   t.co uyY9fiC6sX --------->> positive


# the things id do to go back in time and watch avengers infinity war and endgame for the first time --------->> positive


# the way that treasure s video background for mama performance looks like it got from avengers. i know that it might was hyunsuk s idea   --------->> neutral


# Before Tony Stark died that mf was the Brett Favre of the avengers. Like bro just retire already. --------->> negative


# Like X Men and or Fantastic Four or Avengers https   t.co Ce0gGxla55 --------->> positive


# 1993 Cornerstone The Avengers In Color Series 2 Promos Life After Death! #B3 d8k via @eBay #eBay   https   t.co DRHPlAGXC8 --------->> neutral


# 1993 Cornerstone The Avengers In Color Series 2 Promos Life After Death! #B3 d8k via @eBay #eBay   https   t.co KgIhH0nLo4 --------->> neutral


# @UnholyTitaness  The Assassin would put the Avengers hand over there own mouth and kiss her hand where the lips sho  https   t.co QkEqcqmufo --------->> positive


# @hiddenhush The problem some have with being chinstrapless  avengers cap and szn 5 flash  is that the open part goe  https   t.co 7twVmD3ppl --------->> neutral


# @history0fthemcu  Avengers getting washed by Thanos --------->> neutral


# @BishopSteiner BECMI  Not B X because Weapon Mastery  Avengers  Paladins  and Mystics   but colonialism can kick rocks.  --------->> neutral


# Happy December 1st everyone. Here s Mrs Gale  amp  Steed  amp  the Countdown to an Avengers Christmas. #TheAvengers  https   t.co KzmA2sMxVL --------->> positive


# @moviemenfes Avengers end games --------->> neutral


# Tonight s bedtime reading is some new #Avengers comic book goodness https   t.co ry1mSsqrkq --------->> positive


# RT @jungyuz  and they really put wonyoung sakura xiaoting bahiyyih danielle sullyoon in one group SO CRAZY THATS LITERALLY AVENGERS TEAM ht  --------->> negative


# Some folks just need killin . Live vicariously.         AVENGERS OF BLOOD   Book 2 in the Cass Elliot Crime Series  https   t.co g4XDvQEBxT --------->> positive


# @uuuulkenberg it s giving this line from avengers and i hate it https   t.co FS8H2McuOO --------->> negative


# @BLADESNYSSA I love the blade intro  but the Avengers infinity war intro tops it. Thanos  thrashing of hulk is epic. --------->> positive


# Thirty cats! . violets you you? Superman Star World The .   Day!   Private Down Iron Twilight chamber Avengers Pira  https   t.co C6u8yUiqrx --------->> negative


# RT @delightfulcomic  Out of 10  what score would you  give Marvel s The Avengers  2012 ?! #Avengers #Marvel #Movies https   t.co DtQMLYJqHP --------->> neutral


# it would be like avengers endgame where there s 30 seconds of peak fiction when you see everyone together and the e  https   t.co BWJxEOkxZU --------->> neutral


# RT @MCUPerfectGifs  The first Trailer for  Avengers  Infinity War  was released 5 years ago.  The rest is history  https   t.co xB76apsyo0 --------->> positive


# RT @Shybaka289  @RevolverJerm Chris Brown  Kid Ink  Tyga  Ty Dolla Sign  Omarion  YG  etc..  Dj Mustard had the Avengers during that time. --------->> neutral


# RT @mijjanggu  To everyone who has Netflix Account  Gentlemen s League Episode 60 where Dujun and Gikwang appeared as part of Park Jisung s  --------->> neutral


# @poteido  Same he is my fave too huhu. So sadge when I also saw what happened on avengers 4. --------->> neutral


# 180 Faith Charged Games for Children s Ministry  Grades K   5 AMBRCWS  https   t.co k6iFJYgp9U  #avengers #services  https   t.co ljmATvIL2H --------->> neutral


# RT @eurogamer  Marvel s Midnight Suns is brilliant fun https   t.co MyqXCkwF0K --------->> positive


# @Itatchiuchihaa  No shit hes my fav marvel hero. I havent watched marvel movies since avengers 4 im still mourning --------->> positive


# Thor Stormbreaker Marvel Avengers Wallet Marvel Avengers Accessory EDFQ2WV  https   t.co rBWmqZJavH https   t.co ZrerJoX3Uk --------->> neutral


# RT @DaveOshry  Who would win in a fight  all the Avengers or Cocaine Bear? https   t.co YDMVWEWnOe --------->> positive


# RT @50shadesoftayyy  Congrats to my friend @JScottCampbell on the new  Avengers release! We had to pick up 2 copies because they re so gorg  --------->> positive


# .Dirty real tired   an cat? Batman Star Jurassic Of Alien   Day!   Private Down Man Twilight Potter Avengers Pirate  https   t.co ujNyI3dr5z --------->> negative


# RT @Natboanyurrear  @Rexnoct @blurayangel Marriage Story  Jojo Rabitt  Lost In Translation  Match Point  Lucy  Under the Skin...  Dude  Sca  --------->> neutral


# RT @hist0ry0fthemcu  Avengers  Infinity War  2018  https   t.co bRHaC5gndv --------->> neutral


# RT @lokiedlanna  Can we talk about this lil bitch i found in an avengers Shakespeare book at the globe?? https   t.co s5O4Jt3WRK --------->> neutral


# RT @history0fthemcu  thanos takes on the avengers while wanda destroys the mind stone https   t.co Rhl5dLxbJy --------->> neutral


# RT @YearOneComics  Avengers #202 cover dated December 1980. https   t.co LxKJofs0Yg --------->> neutral


# RT @babyboyav   Hey Avengers   thank you so much for your patience and love  am super hyped and geeked to announce my first official body o  --------->> positive


# RT @MCU Direct  Chris Hemsworth says Robert Downey Jr. praised his performance in #AvengersEndgame s Aether breakdown scene    He goes...    --------->> neutral


#   #IronMan #Avengers #marvel   Source  https   t.co tf0BbRmJwM https   t.co emvWz2CYkD --------->> neutral


# esposito inking perez in this issue is a fucking travesty Avengers #202 https   t.co AtfoKteZrm --------->> negative


# Potter gt  gt Arteta Give Potter the same trust Arteta got  amp  he ll deliver something better Also Arteta didn t have the f  https   t.co 9tQqltc46h --------->> positive


# RT @DoktaStrange  Wus the plan?!?        Stackin ?   Or Slackin ?    Avengers Annual #10 FA   Rouge   #VeVe X #Marvel https   t.co IwQQGWps  --------->> neutral


# RT @MKatungi  Meeting the Presidents and officials of Motorsport clubs of Uganda in Joint cooperation under MK Avengers support for Sports  --------->> neutral


# Thanks Alan Silvestri for spending 99 minutes with me in 2022. I couldn t stop listening to The Avengers.  https   t.co 9C1dsJAAi5 --------->> positive


# @RachelNotley This is MCU type rhetoric Rachel! Better bring in the avengers! --------->> positive


# I was always amused when Avengers End Game made Sebastian Stan  the actor canon in the MCU by mentioning Hot Tub Ti  https   t.co kDKIXlPSuk --------->> negative


# Avengers tho! https   t.co YrSwa7U2Tk --------->> neutral


# @humko nhi pta @The Chobbar nahi bhullar  he is a part of Avengers and belongs to mcu --------->> neutral


# RT @jing cing king  @midnightsuns Now will reveal secret  skin code Midnight suns is over bloated with avengers cast --------->> negative


# Roses real red! pansies alien cat? Superman Wars Jurassic Rings .   Day! Armagedon Ryan Hawk Man Twilight of  Avengers Of Titanic Revnant Of --------->> negative


# Salad Fingers vs Don t Hug Me I m Scared has the same energy as X Men vs Avengers --------->> neutral


#   ULTIMATE AVENGERS Curt Geda  Steven E. Gordon  Bob Richardson  2006 https   t.co zMfNMgiHxG https   t.co BUVPnMcyDg --------->> neutral


# New on Brain Drain  LEGO Marvel Avengers https   t.co AE1VhxCBPQ --------->> positive


# I d give anything to watch avengers endgame for the first time in cinema again   --------->> positive


# You ll do vastly more good for the city as part of my personal Avengers... the Superior Avengers! --------->> positive


# @XRP Avengers I hold xrp since 2 years. I panic sold in the past and i FOMO bought . But im still here --------->> negative


# @thesilveryvenom So so so excited und kinda sad to leave avengers campus but also too excited to try on my Nat cosplay tonight! --------->> positive


# Yall the avengers lost the infinity war!!   --------->> neutral


# RT @YearOneComics  Savage Avengers #4 from August 2019. https   t.co cvvOXF0ApF --------->> neutral


# @XRP Avengers Can t sell cuz no exchanges have it for sale. --------->> neutral


# RT @uhhslimbo  Avengers  recycling the final boss of their campaign after two years of service  Gotham knights  yeah our game s been out fo  --------->> negative


# MAKE MINE MARVEL     Lots of classic Marvel back issue comics from 1980 s through to present day! View the entire c  https   t.co Ma9tF9wZUK --------->> positive


# .Dirty cats! red! tulips are you? Superman Star Jurassic Of Alien Terminator Day! Armagedon Ryan Down Man Twilight  https   t.co FmitYQOtr8 --------->> negative


# RT @miguel4real   Catch the Starstruck kids first Prince @MiguelTanfelix   with the starstruck kids avengers play on @FamilyFeudPH  later 5  --------->> positive


# RT @NostalgiaVortex  Star Virgin  1988   Director   Ichiro Omomo  I can see why the Avengers haven t Recruited  Star Virgin.  #StarVirgin #  --------->> neutral


# RT @Urstruly AK45  AVENGERS PEAKED HERE   END OF AN ERA   https   t.co ccDbuxfB6c --------->> neutral




# ---Aggregate Analysis for the topic: avengers ---

# 1. Percentage of POSITIVE tweets -> 31.57894736842105%
# 2. Percentage of NEGATIVE tweets -> 18.42105263157895%
# 3. Percentage of NEUTRAL tweets -> 50.0%
