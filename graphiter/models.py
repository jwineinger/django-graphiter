import urlparse
import urllib
import requests
from datetime import timedelta

from django.db import models
from django.core.urlresolvers import reverse

from .attime import parseTimeOffset
from utils import seconds_to_other


class Chart(models.Model):
	title = models.CharField(max_length=50)
	url = models.CharField(max_length=1024)
	override_chart_title = models.BooleanField(default=True)
	item_definition = models.CharField(
		max_length=1024,
		help_text=u"A graphite URL that selects a list of metrics. This Chart will render one image for each "
		u"item in the list. Use {item} in the `url` field as a placeholder for this substitution.",
		blank=True,
	)

	def __unicode__(self):
		return self.title

	def get_items(self):
		# make sure we're using the raw format
		parsed = urlparse.urlparse(self.item_definition)
		qs = urlparse.parse_qs(parsed.query)
		qs['format'] = 'raw'
		parts = list(parsed)
		parts[4] = urllib.urlencode(qs, doseq=True)
		url = urlparse.urlunparse(parts)

		resp = requests.get(url)
		return sorted([line.split(',')[0] for line in resp.text.splitlines()])

	def get_from_timerange(self, qs, time_from):
		_seconds = parseTimeOffset(qs['from']) if 'from' in qs else timedelta(hours=-24)

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

	def render(self, **kwargs):
		if self.item_definition:
			for item in self.get_items():
				url = self.url.format(item=item)
				yield self._render(url=url, item=item, **kwargs)

				# if the formatted url is no different, then assume the item replacement wasn't used
				# and only yield once
				if url == self.url:
					break
		else:
			yield self._render(**kwargs)

	def _render(self, **kwargs):
		parsed = urlparse.urlparse(kwargs.get('url') or self.url)
		qs = urlparse.parse_qs(parsed.query)

		if kwargs['time_from']:
			qs['from'] = kwargs['time_from']

		if kwargs['time_until']:
			qs['until'] = kwargs['time_until']

		title_from = self.get_from_timerange(qs, kwargs['add_time_from'])
		title_to = self.get_to_timerange(qs, kwargs['add_time_until'])

		if self.override_chart_title:
			title = self.title
			if self.item_definition:
				title = self.title.format(item=kwargs.get('item'))
			qs['title'] = "{title} ({tfrom} to {tto})".format(title=title, tfrom=title_from, tto=title_to)

		qs['width'] = kwargs['image_width']
		qs['height'] = kwargs['image_height']

		parts = list(parsed)
		parts[4] = urllib.urlencode(qs, doseq=True)

		return {
			'url': urlparse.urlunparse(parts),
			'time_range': "{tfrom}{tto}".format(tfrom=title_from, tto=title_to).replace(" ", ""),
		}


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

	def get_charts_for_display(self, time_from=None, time_until=None):
		time_from = time_from or self.time_from or None
		time_until = time_until or self.time_until or None
		_charts = []
		for page_chart in self.pagecharts.all().order_by("position").select_related('chart'):
			kwargs = {
				"time_from": time_from,
				"time_until": time_until,
				"add_time_from": page_chart.time_from or None,
				"add_time_until": page_chart.time_until or None,
				"image_width": self.image_width,
				"image_height": self.image_height,
			}
			_charts.extend([_chart for _chart in page_chart.chart.render(**kwargs)])

		return _charts


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
