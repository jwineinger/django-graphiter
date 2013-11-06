from django.db import models


class Chart(models.Model):
	title = models.CharField(max_length=50)
	url = models.CharField(max_length=1024)

	def __unicode__(self):
		return self.title


class Page(models.Model):
	title = models.CharField(max_length=50)
	slug = models.SlugField()
	charts = models.ManyToManyField(Chart)

	time_from = models.CharField(max_length=50, default=u"-24h")
	time_until = models.CharField(max_length=50, default=u"", blank=True)

	image_width = models.PositiveIntegerField(default=1200)
	image_height = models.PositiveIntegerField(default=400)

	def __unicode__(self):
		return self.title
		
	def get_absolute_url(self):
	    return reverse('page_detail', kwargs={'slug': self.slug})
