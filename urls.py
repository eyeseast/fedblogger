from django.conf.urls.defaults import *

from django.views.generic import date_based, list_detail
from fedblogger.models import *
from fedblogger import views

blog_info_dict = {
    'queryset': BlogEntry.objects.filter(blog__status=2),
    'date_field': 'pub_date',
    'allow_empty': True
}

entry_info_dict = {
    'queryset': BlogEntry.objects.all(),
    'paginate_by': 10,
}

urlpatterns = patterns('',
    url(r'^$',
        views.blog_index,
        name="fedblogger_blog_list"
        ),
        
    url(r'^(?P<year>\d{4})/$',
        date_based.archive_year,
        blog_info_dict,
        name="fedblogger_archive_year"
        ),
    
    url(r'^(?P<year>\d{4})/(?P<month>[a-zA-Z]{3})/$',
        date_based.archive_month,
        blog_info_dict,
        name="fedblogger_archive_month"
        ),
        
    url(r'^(?P<year>\d{4})/(?P<month>[a-zA-Z]{3})/(?P<day>\d{1,2})/$',
        date_based.archive_day,
        blog_info_dict,
        name="fedblogger_archive_day"
        ),
    
    url(r'^river/$',
        list_detail.object_list,
        entry_info_dict,
        name="fedblogger_entry_river"
        ),
        
    url(r'^(?P<agency_id>[-\w]+)/$',
        views.agency_detail,
        name="fedblogger_agency_detail"
        ),
        
    url(r'^(?P<agency_id>[-\w]+)/(?P<blog_id>[-\w]+)/$',
        views.blog_detail,
        name="fedblogger_blog_detail"
        ),
)