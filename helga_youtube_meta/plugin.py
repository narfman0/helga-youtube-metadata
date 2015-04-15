""" Plugin entry point for helga """
import math
from youtube_scraper.scraper import scrape_url
from helga.plugins import match

TEMPLATE = 'Title: {}, poster: {}, date: {}, views: {}, like ratio: {}'

@match(r'(youtu\.be/\S+|youtube\.com/watch\?v=\S+)')
def youtube_meta(client, channel, nick, message, match):
    """ Return meta information about a video """
    v = scrape_url('http://' + match[0])
    if v.like and v.dislike:
        ratio = math.floor(v.like * 100 / float(v.dislike))
    elif v.like:
        ratio = 'infinite'
    elif v.dislike:
        ratio = '0'
    else:
        ratio = 'unknown'
    return TEMPLATE.format(v.title, v.poster, v.published, v.views, ratio)
