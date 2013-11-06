from django.conf.urls import patterns, url
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy

from .views import PageListView, PageDetailView


urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url=reverse_lazy('pages_list')), name="home"),
	url(r'^pages/$', PageListView.as_view(), name="pages_list"),
	url(r'^page/(?P<slug>[a-zA-Z0-9\-_]{0,50})/$', PageDetailView.as_view(), name="page_detail"),
)
