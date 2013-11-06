import urllib, urlparse
from django.views.generic import DetailView, ListView
from .models import Page


class PageListView(ListView):
	model = Page


class PageDetailView(DetailView):

	context_object_name = 'page'
	queryset = Page.objects.all()
	slug_field = 'slug'

	DEFAULT_WIDTH = 1200
	DEFAULT_HEIGHT = 400

	def get_context_data(self, **kwargs):
		context = super(PageDetailView, self).get_context_data(**kwargs)

		obj = context[self.context_object_name]
		obj.charts_cache = []

		for chart in obj.charts.all():
			parsed = urlparse.urlparse(chart.url)
			qs = urlparse.parse_qs(parsed.query)

			qs['from'] = self.request.GET['from'] if 'from' in self.request.GET else (obj.time_from if obj.time_from else qs['from'])
			qs['until'] = self.request.GET['until'] if 'until' in self.request.GET else (obj.time_until if obj.time_until else qs['until'])

			qs['width'] = obj.image_width if obj.image_width else qs.get('width', self.DEFAULT_WIDTH)
			qs['height'] = obj.image_height if obj.image_height else qs.get('height', self.DEFAULT_HEIGHT)

			parts = list(parsed)
			parts[4] = urllib.urlencode(qs, doseq=True)
			chart.mangled_url = urlparse.urlunparse(parts)
			obj.charts_cache.append(chart)

		return context
