import urlparse
import urllib
from datetime import timedelta

from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse

from .attime import parseTimeOffset
from utils import seconds_to_other


class Chart(models.Model):
	title = models.CharField(max_length=50)
	url = models.CharField(max_length=1024)
	override_chart_title = models.BooleanField(default=True)

	def __unicode__(self):
		return self.title


class Page(models.Model):
	title = models.CharField(max_length=50)
	slug = models.SlugField()
	charts = models.ManyToManyField("graphiter.Chart", through="graphiter.PageChart")

	time_from = models.CharField(
		max_length=50,
		blank=True,
		help_text=u"The default 'from' parameter to use for all charts on this page. Can be overridden via GET param "
		u"when viewing the Page.",
	)
	time_until = models.CharField(
		max_length=50,
		blank=True,
		help_text=u"The default 'until' parameter to use for all charts on this page. Can be overridden via GET param"
		u"when viewing this Page.",
	)

	image_width = models.PositiveIntegerField(default=1200)
	image_height = models.PositiveIntegerField(default=400)

	def __unicode__(self):
		return self.title
		
	def get_absolute_url(self):
		return reverse('page_detail', kwargs={'slug': self.slug})

	def get_from_timerange(self, qs, time_from):
		_seconds = parseTimeOffset(qs['from']) if 'from' in qs else timedelta(seconds=0)

		if time_from:
			extra_delta = parseTimeOffset(time_from)
			_seconds += extra_delta

		qs['from'] = '%dseconds' % _seconds.total_seconds()
		return "{range} ago".format(range=seconds_to_other(-int(_seconds.total_seconds())))

	def get_to_timerange(self, qs, time_until):
		_seconds = parseTimeOffset(qs['until'] if 'until' in qs else timedelta(seconds=0))

		if time_until:
			extra_delta = parseTimeOffset(time_until)
			_seconds += extra_delta

		qs['until'] = '%dseconds' % _seconds.total_seconds()
		title_to = seconds_to_other(-int(_seconds.total_seconds()))

		if int(_seconds.total_seconds()) == 0:
			del qs['until']
			title_to = "now"

		return title_to

	def get_charts_for_display(self, time_from=None, time_until=None):
		_chart_urls = []
		for page_chart in self.pagecharts.all().order_by("position").select_related('chart'):
			chart = page_chart.chart

			parsed = urlparse.urlparse(chart.url)
			qs = urlparse.parse_qs(parsed.query)

			if time_from:
				qs['from'] = time_from
			elif self.time_from:
				qs['from'] = self.time_from

			if time_until:
				qs['until'] = time_until
			elif self.time_until:
				qs['until'] = self.time_until

			if chart.override_chart_title:
				title_from = self.get_from_timerange(qs, page_chart.time_from)
				title_to = self.get_to_timerange(qs, page_chart.time_until)
				qs['title'] = "{title} ({tfrom} to {tto})".format(title=chart.title, tfrom=title_from, tto=title_to)

			qs['width'] = self.image_width if self.image_width else qs.get('width', settings.DEFAULT_CHART_WIDTH)
			qs['height'] = self.image_height if self.image_height else qs.get('height', settings.DEFAULT_CHART_HEIGHT)

			parts = list(parsed)
			parts[4] = urllib.urlencode(qs, doseq=True)
			_chart_urls.append(urlparse.urlunparse(parts))
		return _chart_urls


class PageChart(models.Model):
	chart = models.ForeignKey("graphiter.Chart", related_name="pagecharts")
	page = models.ForeignKey("graphiter.Page", related_name="pagecharts")

	position = models.SmallIntegerField(default=0)

	time_from = models.CharField(
		max_length=50,
		blank=True,
		help_text=u"This value will be added to a 'from' value set on the Page or in the 'from' GET parameter when "
		u"viewing the page."
	)
	time_until = models.CharField(
		max_length=50,
		blank=True,
		help_text=u"This value will be added to a 'until' value set on the Page or in the 'until' GET parameter when "
		u"viewing the page."
	)
