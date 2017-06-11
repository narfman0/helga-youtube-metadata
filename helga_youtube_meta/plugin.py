""" Plugin entry point for helga """
import re
import traceback
from datetime import timedelta
from dateutil.parser import parse as parse_date

import requests

from helga.plugins import match
from helga import settings


API_KEY = getattr(settings, 'YOUTUBE_DATA_API_KEY', False)
API_ROOT = 'https://www.googleapis.com/youtube/v3/videos'
DURATION_REGEX = r'P(?P<days>[0-9]+D)?T(?P<hours>[0-9]+H)?(?P<minutes>[0-9]+M)?(?P<seconds>[0-9]+S)?'
NON_DECIMAL = re.compile(r'[^\d]+')
MATCH_DEFAULT = r'(?:youtu\.be/|youtube\.com/watch\?(?:(?:\S+)&)?v=)([-\w]+)'
MATCH_REGEX = getattr(settings, 'YOUTUBE_META_MATCH_REGEX', MATCH_DEFAULT)
RESPONSE_TEMPLATE = getattr(settings, 'YOUTUBE_META_RESPONSE',
                            ("Title: {title}, poster: {poster}, date: {date},"
                             "views: {views}, likes: {likes}, dislikes: {dislikes},"
                             "duration: {duration}"))


@match(MATCH_REGEX)
def youtube_meta(client, channel, nick, message, match):
    """ Return meta information about a video """
    if not API_KEY:
        return 'You must set YOUTUBE_DATA_API_KEY in settings!'
    identifier = match[0]
    params = {
        'id': identifier,
        'key': API_KEY,
        'part': 'snippet,statistics,contentDetails',
    }
    response = requests.get(API_ROOT, params=params)

    if response.status_code != 200:
        return 'Error in response, ' + str(response.status_code) + ' for identifier: ' + identifier
    try:
        data = response.json()['items'][0]
    except:
        print('Exception requesting info for identifier: ' + identifier)
        traceback.print_exc()

    response_dict = {
        'title': data['snippet']['title'],
        'poster': data['snippet']['channelTitle'],
        'date': str(parse_date(data['snippet']['publishedAt'])),
        'views': data['statistics']['viewCount'],
        'likes': data['statistics']['likeCount'],
        'dislikes': data['statistics']['dislikeCount'],
        'duration': parse_duration(data['contentDetails']['duration']),
    }

    return RESPONSE_TEMPLATE.format(**response_dict).encode('utf-8').strip()


def parse_duration(duration):
    """ Parse and prettify duration from youtube duration format """
    duration_dict = re.search(DURATION_REGEX, duration).groupdict()
    converted_dict = {}
    # convert all values to ints, remove nones
    for a, x in duration_dict.iteritems():
        if x is not None:
            converted_dict[a] = int(NON_DECIMAL.sub('', x))
    return str(timedelta(**converted_dict))
