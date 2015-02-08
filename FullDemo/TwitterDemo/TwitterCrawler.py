import twitter
import TwitterSearch

class TwitterCrawler(object):

  # Login to api
  def login(self):
    self.api = twitter.Api(consumer_key='684nljJUHfn6SCaYSCG0yAhbW',
            consumer_secret='mIRCyxLdIC5cQc7HukUtb7KhKqIvSYOB6LjBZb3CQOQ2n4ents',
            access_token_key='2805813624-2V4XKmbtM18s8osRDpSsr4H2An7JTpMdBE5N2la',
            access_token_secret='szChpRZhXg9F7n5gmlQhG2gEXe5C5g1vgYLGfqmeViPj8'
            )
    return self.api
  
  # Search
  def BasicSearch(self, query):
    self.query = query
    search = TwitterSearch.BasicTwitterSearch()
    tweets = search.search(self.api, query)
    
    #FOR DEMO
    for tweet in tweets:
      print "[",tweet.api_tweet_data.user.screen_name.encode('utf-8'),"]:"
      print "\t",tweet.api_tweet_data.text.encode('utf-8')

    return tweets
  
  # SearchLastXDays
  # SearchDateRange
  # Output to DB
  
  # Output to file
  def output_tweets(self, tweets):
    output = open("tweets.txt", "wb")
    output.write("SEARCH QUERY: " + self.query + "\n")

    for tweet in tweets:
      output.write("\n\n[" + tweet.api_tweet_data.user.screen_name.encode('utf-8') + "] ")
      output.write("[" + tweet.api_tweet_data.created_at + "] ")
      output.write(tweet.api_tweet_data.text.encode('utf-8'))
      
    output.close()