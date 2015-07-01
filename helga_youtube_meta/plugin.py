""" Plugin entry point for helga """
from datetime import timedelta
from dateutil.parser import parse as parse_date
import requests, re, traceback
from helga.plugins import match
from helga import settings

REQUEST_TEMPLATE = '{}videos?id={}&key={}&part=snippet,statistics,contentDetails'
RESPONSE_TEMPLATE = ("Title: {}, poster: {}, date: {}, views: {}, likes: {}, "
                     "dislikes: {}, duration: {}")
API_ROOT = 'https://www.googleapis.com/youtube/v3/'
API_KEY = getattr(settings, 'YOUTUBE_DATA_API_KEY', 'NO_API_KEY')
DURATION_REGEX = r'P(?P<days>[0-9]+D)?T(?P<hours>[0-9]+H)?(?P<minutes>[0-9]+M)?(?P<seconds>[0-9]+S)?'
NON_DECIMAL = re.compile(r'[^\d]+')

@match(r'(?:youtu\.be/|youtube\.com/watch\?v=)([-\w]+)')
def youtube_meta(client, channel, nick, message, match):
    """ Return meta information about a video """
    identifier = match[0]
    request_url = REQUEST_TEMPLATE.format(API_ROOT, identifier, API_KEY)
    response = requests.get(request_url)
    if response.status_code != 200:
        return 'Error in response, ' + str(response.status_code) + ' for identifier: ' + identifier
    try:
        data = response.json()['items'][0]
    except:
        print 'Exception requesting info for identifier: ' + identifier
        traceback.print_exc()
    title = data['snippet']['title']
    poster = data['snippet']['channelTitle']
    date = str(parse_date(data['snippet']['publishedAt']))
    views = data['statistics']['viewCount']
    likes = data['statistics']['likeCount']
    dislikes = data['statistics']['dislikeCount']
    duration = parse_duration(data['contentDetails']['duration'])
    return RESPONSE_TEMPLATE.format(title, poster, date, views, likes, dislikes, duration)

def parse_duration(duration):
    """ Parse and prettify duration from youtube duration format """
    duration_dict = re.search(DURATION_REGEX, duration).groupdict()
    converted_dict = {}
    # convert all values to ints, remove nones
    for a, x in duration_dict.iteritems():
        if x is not None:
            converted_dict[a] = int(NON_DECIMAL.sub('', x))
    return str(timedelta(**converted_dict))
