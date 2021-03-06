import time
import twitter
from Tweet import Tweet

#DOWNLOAD_PHOTOS_ENABLED = True
MEDIA_URLS_ENABLED = False
GEOCODES_ENABLED = False

class TwitterSearch(object):    
  def api_rate_limit_sleep(self, api):
    rate_limit_status = api.GetRateLimitStatus()
    reset_time = rate_limit_status['resources']['search']['/search/tweets']['reset']
    sleep_time = (int)(reset_time - time.time())
    print ('\n Twitter rate limit exceeded. Sleeping for {0} seconds..'.format(str(sleep_time)))
    
    try:
      time.sleep(sleep_time)
    except KeyboardInterrupt:
      raise KeyboardInterrupt
    
  def lookup_media_urls(self, status):
    tweet_media = []
    for media in status.media:
      tweet_media.append(media['media_url_https'])
    
    if not tweet_media:
      return None
        
  def lookup_geocode(self, status, geo):
    """Get geocode either from tweet's 'coordinates' field (unlikely) or from tweet's location and Google."""
    if not geo.quota_exceeded:
      try:
        geocode = geo.geocode_tweet(status)
        if geocode[0]:
          #print('geoCODE: %s %s,%s' % geocode)
          return geocode
      except Exception as e:
        if geo.quota_exceeded:
          print('geoCODER QUOTA EXCEEDED: %s' % geo.count_request)
    return None
    
  def get_100_search_results(self, api, query, starting_id=None):
    params = { 'term' : query,
          'count' : 100,
          'lang' : 'en',
          'result_type' : 'recent',
          'include_entities' : True
          }
          
    if starting_id:
      params['max_id'] = starting_id
      
    results = api.GetSearch(**params)
    return results
    
  def update_Tweets_list(self, search_results, tweets):
    try:
      for result in search_results:
        tweet = self.create_Tweet_object(result)
        tweets.append(tweet)      
    except KeyboardInterrupt:
      print "\n Terminated by user (update_Tweets_list)\n"
      raise KeyboardInterrupt
    return tweets  
    
  def create_Tweet_object(self, search_result):
    media_urls = None
    geocode = None
    
    if MEDIA_URLS_ENABLED:
      media_urls = self.lookup_media_urls(search_result)
    if GEOCODES_ENABLED:
      geocode = self.lookup_geocode(search_result, geocoder)
      
    tweet = Tweet(search_result, media_urls, geocode)
    return tweet

class BasicTwitterSearch(TwitterSearch):
  def search(self, api, query):
    tweets = []
    
    # Get 100 (max) most recent results
    results = self.get_first_100_results(api, query, tweets)
      
    #if len(tweets) < 100:
    #FOR DEMO, JUST RETURN
    return tweets

    # Get next 100 results ignoring ones already found, and so on...
    try:
      self.get_next_100_results(api, query, results, tweets)    
      
    except KeyboardInterrupt:
      print('\n Terminated by user (search)\n')
    except MemoryError:
      print('\n Terminated due to memory error\n')
    except Exception as e:
      print('\n Terminated due to error\n')
      print str(e)

    return tweets

  def get_next_100_results(self, api, query, results, tweets):
    while (len(results) == 100):
      lowest_id = results[99].GetId()
      
      try:
        results = super(BasicTwitterSearch, self).get_100_search_results(api, query, lowest_id)
      except twitter.TwitterError as e:
        super(BasicTwitterSearch, self).api_rate_limit_sleep(api)
        continue
      
      super(BasicTwitterSearch, self).update_Tweets_list(results, tweets)
      
      print str(len(tweets)) + " tweets gathered.."
    
    
  def get_first_100_results(self, api, query, tweets):
    results = []
    try:
      results = super(BasicTwitterSearch, self).get_100_search_results(api, query)
      super(BasicTwitterSearch, self).update_Tweets_list(results, tweets)
    except KeyboardInterrupt:
      print ('\n Terminated by user (search)\n')
    except twitter.TwitterError as e:
      
      try:
        super(BasicTwitterSearch, self).api_rate_limit_sleep(api)
      except KeyboardInterrupt:
        return results
      
      return self.get_first_100_results(api, query, tweets)
    return results
    
'''
class SearchLastXDays(object):
  # search
  #...
  
class SearchDateRange(object):
  # search, ...
'''

'''  
=====
Date restricted searches
=====
'''

'''  
def search_date_range(api, query, start_date, end_date):
  # search for tweets in date range
  
def search_streaming(api, query):
  # start streaming for new tweet results
'''

'''
def search_last_x_days(api, query, num_days):
  # search for tweets in the last x number of days
  tweets = []
  date = num_days * 3600 * 24
  
  results = get_first_100_results(api, query, tweets)
  remove_Tweets_older_than_date(tweets, date)
  
  if len(tweets) < 100:
    return tweets
    
  try:
    get_next_100_results(api, query, results, tweets)
    #remove_Tweets_older_than_date(tweets, date)
    
  
  return tweets

def remove_Tweets_older_than_date(tweets, date):      
  for i in range(0 to len(tweets)):
    if date < tweets[i].api_tweet_data.created_at:
      tweets[i:len(tweets)] = []
      break  
'''