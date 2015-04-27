""" Plugin entry point for helga """
import math
from youtube_scraper.scraper import scrape_url
from helga.plugins import match

TEMPLATE = 'Title: {}, poster: {}, date: {}, views: {}, likes: {}, dislikes: {}'

@match(r'(youtu\.be/|youtube\.com/watch\?v=)\w+')
def youtube_meta(client, channel, nick, message, match):
    """ Return meta information about a video """
    v = scrape_url('http://' + match[0])
    return TEMPLATE.format(v.title, v.poster, v.published, v.views, v.likes,
                           v.dislikes)
