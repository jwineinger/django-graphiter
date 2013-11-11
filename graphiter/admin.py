from django.contrib import admin
from django import forms

from .models import Chart, Page, PageChart


class ChartForm(forms.ModelForm):
	class Meta:
		model = Chart
		widgets = {
			'url': forms.Textarea(attrs={'cols': '120'}),
			'item_definition': forms.Textarea(attrs={'cols': '120'}),
		}


class PageChartInline(admin.TabularInline):
	model = PageChart


class ChartAdmin(admin.ModelAdmin):
	list_display = ('title',)
	form = ChartForm
admin.site.register(Chart, ChartAdmin)


class PageAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug": ("title",)}
	list_display = ('title',)
	inlines = [PageChartInline]
admin.site.register(Page, PageAdmin)
