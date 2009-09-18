from django.core.management.base import NoArgsCommand

import datetime
import feedparser
import time

from django.utils.encoding import smart_unicode

class Command(NoArgsCommand):
    """
    manage.py update_feeds [app...]
    
    Parses stored feeds and loads items into the database.
    
    In theory, it can be used with any aggregator application, but it assumes the Entry model follows a certain pattern:
        title, text, link, pub_date, guid
        
    """
    help = "Updates aggregated feeds for fedblogger"
    
    args = "Takes no arguments, just options"
    
    def handle_noargs(self, **options):
        verbosity = options.get('verbosity', 0)
        #print verbosity

        from fedblogger.models import BlogFeed, BlogEntry
        
        for blog in BlogFeed.objects.filter(status=BlogFeed.APPROVED):
            parsed_feed = feedparser.parse(blog.feed_url)
            #if verbosity > 1:
                #print "Feed parsed for %s: %s" % (blog.name, blog.feed_url)
            
            for entry in parsed_feed.entries:
                # basic metadata
                title = entry.title.encode(parsed_feed.encoding, 'xmlcharrefreplace')
                link = entry.link.encode(parsed_feed.encoding, 'xmlcharrefreplace')
                guid = entry.get('id', link).encode(parsed_feed.encoding, 'xmlcharrefreplace')
                
                if not guid:
                    guid = link
                
                # the meat of it
                if hasattr(entry, 'description'):
                    text = entry.description
                    
                elif hasattr(entry, 'summary'):
                    text = entry.summary
                    
                elif hasattr(entry, 'content'):
                    text = entry.content
                    
                else:
                    text = ''
                    
                text = text.encode(parsed_feed.encoding, 'xmlcharrefreplace')
                
                # needs a date
                try:
                    if entry.has_key('modified_parsed'):
                        pub_date = datetime.datetime.fromtimestamp(time.mktime(entry.modified_parsed))
                        
                    elif entry.has_key('published_parsed'):
                        pub_date = datetime.datetime.fromtimestamp(time.mktime(entry.published_parsed))
                        
                    elif entry.has_key('date_parsed'):
                        pub_date = datetime.datetime.fromtimestamp(time.mktime(entry.date_parsed))
                    
                    elif parsed_feed.has_key('modified'):
                        pub_date = datetime.datetime.fromtimestamp(time.mktime(parsed_feed.modified))
                    
                    else:
                        pub_date = datetime.datetime.now()
                
                except ValueError:
                    pub_date = datetime.datetime.now()
                
                # ok, got everything? Let's load this sucker
                try:
                    BlogEntry.objects.get(guid=guid)
                
                except BlogEntry.DoesNotExist:
                    if title.isupper():
                        title = title.title()
                    BlogEntry.objects.create(title=title,
                                             link=link,
                                             guid=guid,
                                             text=text,
                                             pub_date=pub_date,
                                             blog=blog
                                             )
                    #if verbosity > 1:
                    #    print "New entry on %s: %s" % (blog.name, smart_unicode(title))



