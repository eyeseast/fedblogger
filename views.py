# Create your views here.

from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.views.generic import list_detail
from fedblogger.models import *


def blog_index(request):
    entry_list = BlogEntry.objects.all()[:10]
    blogs = BlogFeed.objects.all()
    return render_to_response('fedblogger/blogentry_list.html',
                              {'object_list': entry_list,
                               'blog_list': blogs},
                               context_instance=RequestContext(request))


def agency_detail(request, agency_id):
    agency = get_object_or_404(Agency, slug__iexact=agency_id)
    blogs = BlogFeed.objects.filter(agency=agency)
    entries = BlogEntry.objects.filter(blog__agency=agency)
    return render_to_response("fedblogger/agency_detail.html", {
                              "agency": agency,
                              "blog_list": blogs,
                              "entry_list": entries[:10]},
                              context_instance=RequestContext(request)
                              )
                              

def blog_detail(request, agency_id, blog_id):
    agency = get_object_or_404(Agency, slug__iexact=agency_id)
    blog = get_object_or_404(BlogFeed, agency=agency, slug__iexact=blog_id)
    entries = blog.entries.all()
    return list_detail.object_list(request,
                                   queryset=entries,
                                   template_name="fedblogger/blog_detail.html",
                                   extra_context={'agency': agency, 'blog': blog},
                                   paginate_by=15
                                   )