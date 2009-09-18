from django.conf.urls.defaults import *

from django.views.generic import list_detail
from fedblogger.models import *
from fedblogger import views

blog_info_dict = {
    'queryset': BlogFeed.objects.filter(status=BlogFeed.APPROVED),
    'extra_context': {'latest': BlogEntry.objects.all()[:5]}
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