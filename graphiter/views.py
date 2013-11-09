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
		obj.charts_cache = obj.get_charts_for_display(
			time_from=self.request.GET.get('from'),
			time_until=self.request.GET.get('until'),
		)

		return context
